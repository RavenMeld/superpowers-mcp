# playwright-flake-hunter

Stabilize flaky Playwright tests using retries, trace triage, selector hardening, and deterministic wait patterns.

## Quick Facts
- id: `playwright-flake-hunter--c724b6213b`
- worth_using_score: `60/100`
- tags: `playwright, firefox, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/playwright-flake-hunter/SKILL.md`

## Use When
- A Playwright test passes locally but fails in CI intermittently.
- Retries hide failures and you need root-cause triage.
- You need deterministic selectors and waits before release.

## Workflow / Steps
- Reproduce with retries and isolate flaky specs.
- Collect trace/video/console for failing retries only.
- Replace timing-based waits with event/state-based waits.
- Harden selectors to role, label, and test-id conventions.
- Re-run in headed/headless + Chromium/Firefox before merge.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
