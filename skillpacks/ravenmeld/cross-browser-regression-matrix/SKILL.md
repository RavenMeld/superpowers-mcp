---
name: cross-browser-regression-matrix
description: |
  Run and compare regression results across Chromium, Firefox, and WebKit with a repeatable browser matrix.
---

# Cross Browser Regression Matrix

## Use When

- A change must be validated on Chrome/Firefox/WebKit before release.
- A bug reproduces only on one browser engine.
- You need a reproducible browser compatibility gate in CI.

## Workflow

1. Define the browser project matrix in Playwright config.
2. Run a focused smoke subset on all browsers for quick feedback.
3. Run full regression matrix for release candidates.
4. Diff failures by browser to isolate engine-specific issues.
5. Add browser-targeted assertions only when behavior genuinely differs.

## Copy/Paste Examples

```bash
npx playwright test --project=chromium --project=firefox --project=webkit
```

```bash
npx playwright test tests/e2e/smoke --project=chromium --project=firefox
```

```bash
npx playwright test --reporter=html && npx playwright show-report
```

## Matrix Design Notes

- Keep one baseline smoke path that must pass on all engines.
- Track browser-only failures separately from app logic regressions.
- Prefer feature detection over user-agent branching.

## Safety Notes

- Do not skip failing engines by default in CI.
- Re-verify accessibility checks across at least Chromium + Firefox.
