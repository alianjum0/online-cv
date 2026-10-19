// Pass this function to playwright-cli run-code with Jekyll running on port 4000.
// Create /tmp/online-cv-pdf-check first; then check the PDFs with check-pdf-top.py.
async (page) => {
  await page.goto("http://127.0.0.1:4000/");
  await page.emulateMedia({ media: "screen" });
  for (const [name, width, scroll] of [
    ["desktop-top", 1440, 0],
    ["desktop-scrolled", 1440, 1200],
    ["desktop-bottom", 1440, "bottom"],
    ["mobile-scrolled", 390, 1200],
  ]) {
    await page.setViewportSize({ width, height: 900 });
    await page.evaluate((position) => {
      window.scrollTo(0, position === "bottom" ? document.body.scrollHeight : position);
    }, scroll);
    const before = await page.evaluate(() => window.scrollY);
    if (scroll !== 0 && before === 0) throw new Error("CV did not scroll");
    const pending = page.waitForEvent("download", { timeout: 60000 });
    await page.locator("#pdfButton").click();
    const download = await pending;
    await download.saveAs(`/tmp/online-cv-pdf-check/${name}.pdf`);
  }
}
