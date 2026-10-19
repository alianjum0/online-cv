"""Check a real exported PDF for the blank opening page regression.

Requires Poppler's pdftoppm on PATH. Pass PDFs exported with the site's PDF
button, both at the top of the page and after scrolling down at least 1200px.
"""

import subprocess
import sys


def check(pdf):
    raster = subprocess.check_output(
        ["pdftoppm", "-f", "1", "-singlefile", "-r", "36", pdf]
    )
    magic, dimensions, maximum, pixels = raster.split(b"\n", 3)
    assert magic == b"P6" and maximum == b"255", "Expected an RGB PPM raster"
    width, height = map(int, dimensions.split())
    # Content must appear in the upper quarter, allowing normal page margins.
    top = pixels[: width * (height // 4) * 3]
    visible = sum(min(top[i : i + 3]) < 230 for i in range(0, len(top), 3))
    assert visible > 100, f"{pdf}: opening quarter is blank ({visible} content pixels)"
    print(f"PASS {pdf}: content appears near the top ({visible} pixels)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 scripts/check-pdf-top.py PDF [PDF ...]")
    for path in sys.argv[1:]:
        check(path)
