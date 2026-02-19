---
name: playwright-auth-state-manager
description: |
  Manage Playwright authentication state safely and deterministically across local runs and CI.
---

# Playwright Auth State Manager

## Use When

- Tests require authenticated sessions.
- Login steps are flaky or too slow in every test.
- CI failures stem from expired or polluted auth state.

## Workflow

1. Create dedicated auth setup project/spec.
2. Persist storage state into scoped, non-secret artifacts.
3. Reuse auth state only for matching test domains/roles.
4. Refresh auth state on expiration signals.
5. Keep logout/cleanup checks in teardown paths.

## Copy/Paste Examples

```bash
npx playwright test tests/auth.setup.ts --project=chromium
```

```bash
npx playwright test --config=playwright.config.ts
```

```bash
ls -lh .auth && rg -n "storageState" playwright.config.ts tests -S
```

## Auth Rules

- Separate admin/user auth states.
- Never share personal session state in CI.
- Regenerate auth state when auth schema changes.

## Safety Notes

- Do not commit `.auth` secrets or cookies.
- Treat auth artifacts as sensitive and short-lived.
