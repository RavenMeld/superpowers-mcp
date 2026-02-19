---
name: chrome-firefox-profile-manager
description: |
  Manage Chrome and Firefox automation profiles safely for repeatable browser tests and debugging sessions.
---

# Chrome Firefox Profile Manager

## Use When

- You need stable browser state between automation runs.
- Tests fail due to stale cookies/storage/profile drift.
- You want clean profile isolation for Chrome and Firefox debugging.

## Workflow

1. Create dedicated test profiles per browser and environment.
2. Start tests against isolated user-data/profile directories.
3. Reset profile state before critical regression runs.
4. Keep session fixtures explicit (cookies, localStorage, auth seeds).
5. Archive known-good profiles for reproducible bug repro.

## Copy/Paste Examples

```bash
npx playwright test --project=chromium --headed
```

```bash
google-chrome --user-data-dir=/tmp/chrome-profile-debug --remote-debugging-port=9222
```

```bash
firefox -profile /tmp/firefox-profile-debug
```

## Profile Hygiene

- Never mix personal and test profiles.
- Version profile fixtures with test data assumptions.
- Prefer API/session seeding over manual browser login for CI.

## Safety Notes

- Do not store real credentials in profile directories.
- Wipe temporary debug profiles after use.
