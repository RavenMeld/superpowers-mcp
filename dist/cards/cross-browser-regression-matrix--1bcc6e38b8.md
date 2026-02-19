# cross-browser-regression-matrix

Run and compare regression results across Chromium, Firefox, and WebKit with a repeatable browser matrix.

## Quick Facts
- id: `cross-browser-regression-matrix--1bcc6e38b8`
- worth_using_score: `60/100`
- tags: `playwright, browser, chrome, firefox, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/cross-browser-regression-matrix/SKILL.md`

## Use When
- A change must be validated on Chrome/Firefox/WebKit before release.
- A bug reproduces only on one browser engine.
- You need a reproducible browser compatibility gate in CI.

## Workflow / Steps
- Define the browser project matrix in Playwright config.
- Run a focused smoke subset on all browsers for quick feedback.
- Run full regression matrix for release candidates.
- Diff failures by browser to isolate engine-specific issues.
- Add browser-targeted assertions only when behavior genuinely differs.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
