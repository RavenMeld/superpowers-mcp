---
name: playwright-browser-automation
description: |
  Practical Playwright workflows for web automation and smoke testing: running tests, headed debugging, traces, screenshots, and CI-safe defaults.
---

# Playwright Browser Automation

## Use When

- You need a reliable smoke test for a web app (Chromium/Firefox/WebKit).
- You need screenshots, console logs, or traces for debugging.
- You want deterministic, CI-friendly browser automation.

## Workflow

1. Install Playwright + browsers.
2. Start the app (or target a URL).
3. Run a minimal smoke test (fast, deterministic assertions).
4. If failing, re-run headed with traces and screenshots enabled.
5. Capture evidence (trace + console + screenshot) and fix the root cause.

## Install

Node project:

```bash
npm i -D @playwright/test
npx playwright install --with-deps
```

## Run Tests

```bash
npx playwright test
```

Headed mode (debug visually):

```bash
npx playwright test --headed
```

Run a single test file:

```bash
npx playwright test tests/smoke.spec.ts
```

## Traces + Screenshots

Record traces for failures:

```bash
npx playwright test --trace on
```

Open the trace viewer:

```bash
npx playwright show-trace test-results/**/trace.zip
```

## Stability Tips (Worth Doing)

- Avoid time-based waits; wait for specific UI conditions instead.
- Use `data-testid` (or stable roles/names) rather than brittle CSS selectors.
- Keep smoke tests short:
  - one page load
  - one core action
  - one core assertion

## CI Safety

- Prefer headless in CI.
- Ensure the test runner writes artifacts to a known folder.
- Keep logs bounded (avoid dumping large HTML blobs into CI logs).

