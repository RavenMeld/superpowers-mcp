---
name: playwright-flake-hunter
description: |
  Stabilize flaky Playwright tests using retries, trace triage, selector hardening, and deterministic wait patterns.
---

# Playwright Flake Hunter

## Use When

- A Playwright test passes locally but fails in CI intermittently.
- Retries hide failures and you need root-cause triage.
- You need deterministic selectors and waits before release.

## Workflow

1. Reproduce with retries and isolate flaky specs.
2. Collect trace/video/console for failing retries only.
3. Replace timing-based waits with event/state-based waits.
4. Harden selectors to role, label, and test-id conventions.
5. Re-run in headed/headless + Chromium/Firefox before merge.

## Copy/Paste Examples

```bash
npx playwright test --retries=3 --repeat-each=10
```

```bash
npx playwright test tests/e2e/flaky.spec.ts --trace=retain-on-failure --video=retain-on-failure
```

```bash
npx playwright show-trace test-results/**/trace.zip
```

## Stabilization Rules

- Prefer `getByRole` and `getByTestId` over brittle CSS chains.
- Prefer `await expect(locator).toBeVisible()` over `waitForTimeout`.
- Gate async UI on network/DOM completion signals, not fixed sleeps.

## Safety Notes

- Keep retries low while debugging or flakes are masked.
- Do not disable assertions to "fix" a flaky test.
