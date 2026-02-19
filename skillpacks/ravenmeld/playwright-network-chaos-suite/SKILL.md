---
name: playwright-network-chaos-suite
description: |
  Stress Playwright E2E flows with network latency, failures, and offline scenarios to harden client behavior.
---

# Playwright Network Chaos Suite

## Use When

- UI behavior breaks under slow/unstable network.
- Retries and fallback UX are untested.
- You need resilience gates before release.

## Workflow

1. Identify critical user journeys for resilience testing.
2. Inject latency, timeout, and intermittent failure scenarios.
3. Validate fallback UI states and retry controls.
4. Verify telemetry/error reporting under degraded conditions.
5. Promote fixes into standard regression suite.

## Copy/Paste Examples

```bash
npx playwright test tests/e2e/resilience.spec.ts
```

```bash
npx playwright test --project=chromium --repeat-each=5
```

```bash
npx playwright show-report
```

## Chaos Patterns

- Simulate 500/429/timeout responses on key endpoints.
- Validate offline mode and reconnect transitions.
- Assert user-visible recovery messaging.

## Safety Notes

- Keep chaos mocks test-scoped; never leak to production endpoints.
- Do not mask real backend regressions with broad retries.
