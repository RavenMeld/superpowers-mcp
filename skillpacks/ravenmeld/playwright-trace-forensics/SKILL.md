---
name: playwright-trace-forensics
description: |
  Perform deep Playwright failure forensics from trace artifacts, network logs, and console/runtime errors.
---

# Playwright Trace Forensics

## Use When

- A CI failure needs precise proof of what happened in browser state.
- You have trace artifacts but no clear diagnosis yet.
- A regression only reproduces under CI timing/network conditions.

## Workflow

1. Open the failing trace and map each action to assertion failure.
2. Inspect network waterfall for blocked/failed requests.
3. Correlate console/runtime errors with the failing step timestamp.
4. Classify failure type: selector drift, race, auth/session, backend error.
5. Produce minimal code fix plus a regression assertion.

## Copy/Paste Examples

```bash
npx playwright test --trace=retain-on-failure --reporter=line
```

```bash
npx playwright show-trace test-results/**/trace.zip
```

```bash
npx playwright test tests/e2e/login.spec.ts -g "should sign in" --project=chromium
```

## Forensic Checklist

- Last successful action before failure.
- Exact selector target at failure time.
- Request/response status for critical API calls.
- Console error stack and source map line.
- Screenshot delta versus expected state.

## Safety Notes

- Preserve original trace artifacts; do not overwrite them during triage.
- Avoid speculative fixes without trace-backed evidence.
