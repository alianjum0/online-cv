# Local Preview, Upstream Sync, and PDF Spacing Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Integrate the latest fork-base changes, run the personalized CV locally, and remove unintended whitespace above the PDF content.

**Architecture:** Keep the existing Jekyll/Liquid/Sass site and personalized content. Integrate upstream before diagnosing the final print layout, then make the smallest evidence-backed correction in the print styles or layout. Validate the actual generated PDF, alongside the normal website.

**Tech Stack:** Ruby, Bundler, Jekyll, GitHub Pages, Liquid, Sass, browser PDF export; Docker Compose is an existing alternative runtime.

**Spec:** The user's request in this chat: create an agent execution plan to run locally, obtain the latest from https://github.com/sharu725/online-cv, and fix whitespace at the top of the PDF.

## Global Constraints

- Repository: `/Users/alianjum/work/projects/online-cv`; prefix shell commands with `rtk`, using `rtk proxy` where needed.
- Read applicable AGENTS.md and `/Users/alianjum/.codex/RTK.md` before execution.
- Preserve CV data, recommendations, contact links, branding, and unrelated files.
- Initial checkout is `gh-pages` at `c2e3ec5`; verify current state rather than assuming it remains unchanged.
- Preserve the existing deleted `assets/Anjum_CV.pdf` and untracked `.DS_Store` and `assets/.DS_Store`.
- User update, 2026-10-19: remove the unused standalone portfolio drafts and retain the main Jekyll site and CV data. Both `new-website/` and `website/` were moved out of the project to `/private/tmp/online-cv-unused-websites-20261019/`; do not reintroduce them. The temporary backup is recoverable but is not permanent storage.
- Create a task branch with the `codex/` prefix before implementation. Never commit directly to a publishing/default branch; do not force-push or bypass guards.
- No production deployment or merge as part of this plan. Submit a draft PR, following repository policy.
- Do not introduce a new application stack, hosted PDF service, or broad dependency upgrade.

## Inspection Evidence and Limits

- `origin` points to `alianjum0/online-cv`; `upstream` already points to `sharu725/online-cv`.
- The public upstream page currently identifies `master` as its default branch. Its live commit SHA has not been verified; cached `upstream/master` is `ef0186356192160b3ba0895400f8e421921efd23` and is not proof of latest.
- The local history already contains an earlier upstream merge. Preserve fork history and personalization when integrating subsequent changes.
- `Gemfile.lock` requests Bundler 2.0.2; the active Ruby is 2.6.10 and Bundler activation fails because that version is missing. No local build or browser reproduction has passed yet.
- A remote probe failed with `Could not resolve hostname github.com`; retry with the permitted network path before claiming a successful sync.
- Update, 2026-10-19: an approved network probe verified upstream `master` at `72cdf5f3a116b67b13331e3192dc3825576689fb`. Fetch and verify it again during integration.
- Execution, 2026-10-19: fetched and merged that commit on `codex/online-cv-upstream-pdf`, merge commit `cd77f18`. The merge had no conflicts and did not change `_data/data.yml` or `_config.yml`. Upstream adds `assets/js/pdf-generator.js` using html2pdf.js; investigate the PDF button as well as browser printing. The earlier note about no dedicated PDF generation script describes the pre-merge checkout.
- `_config.yml` currently has an empty `baseurl` and port 4000. README's `/online-cv/` URL does not match that current configuration.
- `_sass/_base.scss` uses a grid wrapper, 30px body padding, and 60px main-content padding. `_sass/_print.scss` adds float/width rules and A4 size without explicit page margins. `_layouts/print.html` overrides body padding. These are investigation targets, not a confirmed root cause.
- No dedicated PDF generation script or application test runner was found in the inspected root files. The deleted binary is not available as a local comparison artifact.

## Review Focus

- First-page spacing: distinguish page margin, body spacing, intentional content padding, and content pushed to a later page.
- Long CV: preserve content across page breaks without blank opening pages, clipping, or overlap.
- Sidebar layout: preserve readable columns and expected ordering in the printed result.
- Screen styles: preserve desktop/mobile presentation after print-specific corrections.
- Export settings: record the route, browser, paper size, scale, margins, headers/footers, and background setting so results are reproducible.

---

### Task 1 — Integration Agent: Sync Upstream and Establish Local Preview

**Files:** Inspect `README.md`, `Gemfile`, `Gemfile.lock`, `_config.yml`, `docker-compose.yml`; merge upstream-tracked files as required. Modify setup documentation only when needed to describe a verified command.

**Interfaces:** Consumes the existing fork and local-change inventory. Produces a task branch containing the verified upstream SHA, a working local URL, exact startup commands, runtime versions, and a list of conflict resolutions.

- [ ] Record `rtk git status --short`, branch, remotes, and current SHA. Create `codex/online-cv-upstream-pdf` if available. Use an isolated checkout if integration could collide with existing work; do not carry unrelated files into it.
- [ ] Fetch origin and upstream through permitted network access. Verify the live default branch and identify the fork's current integration target/publishing configuration. If network access fails, document the blocker and do not substitute cached refs for latest.
- [ ] Compare fork changes against the merge base, especially `_data/data.yml`, `_config.yml`, assets, includes, and recommendations. Merge the verified upstream default-branch commit into the task branch; resolve conflicts by preserving personal content while incorporating upstream fixes. Do not reset the fork to upstream.
- [ ] Identify a compatible available Ruby/Bundler runtime from the lockfile requirements. Install dependencies in an isolated location or use the existing Docker route. Preserve the lockfile unless an actual compatibility issue requires a narrowly explained change; avoid system Ruby changes and blanket `bundle update`.
- [ ] Run `rtk bundle exec jekyll build` and `rtk bundle exec jekyll serve --host 127.0.0.1 --port 4000` with the selected runtime. If using Docker, record the exact equivalent commands and resolve any port collision without stopping unrelated services.
- [ ] Confirm `http://127.0.0.1:4000/`, `/print`, CSS, and avatar assets render successfully; derive the URL again if merged configuration changes the base path. Check personalized content and recommendations, desktop/mobile rendering, and browser console errors.
- [ ] Record the upstream SHA included in branch ancestry, build result, and local server command. Commit only intended integration/setup changes using a Conventional Commit where applicable.

**Gate:** Upstream commit is verified and integrated; local pages and assets load. A blocked fetch or build must be reported before downstream agents treat the baseline as ready.

### Task 2 — PDF Agent: Reproduce and Fix the Top Gap

**Files:** Inspect `assets/js/pdf-generator.js`, `_includes/head.html`, `_sass/_print.scss`, `_sass/_base.scss`, `_sass/_responsive.scss`, `_sass/_default.scss`, `_layouts/print.html`, `print.html`, and `_includes/sidebar.html`. Modify the generator or print styles only when reproduction demonstrates they own the cause. Create a small repeatable regression script under `scripts/` only if existing tooling cannot provide a reproducible check.

**Interfaces:** Consumes Task 1's running site, integrated branch, and runtime commands. Produces a demonstrated root cause, a minimal patch, a repeatable regression check, and before/after PDF artifacts outside tracked source assets.

- [ ] Reproduce the homepage PDF button, export from `/print`, and printing `/`. For browser printing use A4 portrait, 100% scale, headers/footers disabled, backgrounds enabled; record actual margins and browser/version. For the PDF button record the generator's html2canvas/jsPDF settings. Wait for fonts and images before capture. Preserve before PDFs and page-one renders in a temporary evidence directory.
- [ ] Measure the first visible content position and inspect print-media computed styles/bounding boxes for `html`, `body`, `.wrapper`, `.sidebar-wrapper`, and `.main-wrapper`. Inspect all pages to distinguish a top gap from pagination pushing a column or section onto another page.
- [ ] Test one hypothesis at a time using temporary browser overrides: browser/page margins, body/content padding, responsive breakpoints under print, or grid/float fragmentation. Remove each failed experiment before testing another. Do not prescribe zero margins or replace grid until evidence isolates the cause.
- [ ] Before modifying source, save a failing regression check against the reproduced condition. Record the intended top position after isolating the cause, with a small rendering tolerance and exact export settings; verify the original exceeds it. Include a check that the opening CV section appears on page one. A DOM-only assertion is insufficient when the defect appears only in PDF pagination.
- [ ] Apply the smallest correction to the owning print rule/layout. Keep intended document margins and internal spacing explicit. Avoid changing CV copy or global screen styles to conceal the issue.
- [ ] Rebuild and rerun the same export/check. Render and inspect every PDF page: no unintended top gap or blank opening page, no missing text, clipped sidebar, overlapping sections, or unnecessary blank trailing page. Compare extracted text with the original to catch lost content.
- [ ] Compare desktop and mobile screenshots against Task 1's baseline. Exercise a temporary longer-content fixture without changing the user's data; verify page breaks remain readable. Check both direct `/print` export and normal-page printing, documenting any deliberate difference.
- [ ] Document the exact local export procedure and save the successful regression command. Do not regenerate or restore `assets/Anjum_CV.pdf` unless separately authorized; its pre-existing deletion belongs to the user. Commit only the fix and its necessary regression/documentation files with `fix: remove unintended PDF top spacing`.

**Gate:** The regression fails before the patch and passes afterward using identical settings, actual PDFs demonstrate the correction, and screen rendering/content remain intact.

### Task 3 — Review Agent: Verify and Prepare Draft PR

**Files:** Review the complete branch diff and the evidence from Tasks 1–2. No unrelated edits.

**Interfaces:** Consumes the task branch and evidence bundle. Produces review findings, final verification results, commit SHA(s), and a draft PR URL.

- [ ] Independently inspect the upstream merge/conflict resolutions and PDF patch. Verify current upstream ancestry and personalized content; reject unexplained dependency changes or unrelated modifications.
- [ ] Rerun the Jekyll build and focused PDF regression on the final commit. Inspect final PDF renders plus representative desktop/mobile views. Resolve actionable findings and repeat affected checks after changes.
- [ ] Run `rtk git diff --check`, inspect the complete branch diff, and ensure only intended files are committed. Confirm the original deleted PDF and untracked folders remain untouched in the user's original checkout.
- [ ] Push the task branch and open a draft PR against the verified fork integration branch. Describe the observed PDF cause, upstream SHA, local commands, before/after evidence, and verification limits. Attach the created PR to this chat using the app's artifact tool.
- [ ] Inspect available CI/review results and resolve failures attributable to the change. Report absent CI as absent; keep draft status and do not merge or publish.
- [ ] Handoff: local URL and startup command, upstream SHA, root cause and changed files, test/build results, evidence paths, commit SHA(s), draft PR link, remaining risks, and merge status.

**Execution order:** Task 1 → Task 2 → Task 3. These tasks share integration state and should run sequentially; a new agent can take ownership at each gate.

## Execution record — 2026-10-19

- Removed both unused standalone drafts from the checkout via the temporary backup documented above; main Jekyll CV data remains unchanged.
- Task 1: upstream `72cdf5f` integrated at `cd77f18`; Docker container `online-cv-local-20261019` serves `http://127.0.0.1:4000/` and `/print`. Jekyll build passed. The latest fork base also contains `f9d0938` (`Delete CNAME`); preserve that commit when preparing the PR.
- Task 2: reproduced a blank opening PDF page by scrolling 1200px before clicking PDF. A real raster check failed with zero visible pixels in the opening quarter. Setting html2canvas `scrollX: 0` and `scrollY: 0` fixes capture origin without altering CV layout or data. Actual exports from desktop top/middle/bottom and mobile after scrolling pass `scripts/check-pdf-top.py`.
- Tests: `scripts/export-pdf-regression.js` drives actual browser downloads; `scripts/check-pdf-top.py` checks generated PDF pixels using Poppler. Exact commands are in README. The original failing and successful comparison artifacts are in `/private/tmp/online-cv-pdf-evidence-20261019/`; repeated scenario outputs are in `/private/tmp/online-cv-pdf-check/`.
- Task 3: independent review found no actionable findings. Jekyll builds pass; desktop/mobile screenshots captured, mobile has no horizontal overflow, and browser console has no errors. All pages of the desktop/mobile PDF exports were rendered for visual inspection. Existing raster PDF export still splits content at page boundaries and uses the responsive mobile layout; pagination redesign is outside this fix.
- The deleted tracked `assets/Anjum_CV.pdf` remains untouched. No production publish or merge is authorized by this plan; submit the task branch as a draft PR.
