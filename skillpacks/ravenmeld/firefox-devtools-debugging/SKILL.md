---
name: firefox-devtools-debugging
description: |
  Debug web apps using Firefox DevTools: console/network inspection, storage/cookies, accessibility checks, and cross-browser diffs.
---

# Firefox DevTools Debugging

## Use When

- You need cross-browser debugging (Chrome vs Firefox differences).
- You need to inspect storage/cookies and request/response behavior.
- You need to validate accessibility issues with built-in tooling.

## Workflow

1. Reproduce the issue in Firefox with DevTools open.
2. Compare Console errors and Network timings vs Chrome.
3. Inspect Storage (cookies/localStorage) for auth/session mismatch.
4. Use Accessibility panel to find obvious violations.
5. Fix and verify in both browsers.

## Panels You’ll Use

Open DevTools:
- Windows/Linux: `Ctrl+Shift+I`
- macOS: `Cmd+Option+I`

Console:
- Look for CSP errors, blocked requests, and uncaught exceptions.

Network:
- Compare request headers, redirects, caching, and response codes.

Storage:
- Cookies and localStorage are common sources of “works in one browser only”.

Accessibility:
- Run the built-in a11y checks for obvious issues.

## Cross-Browser Diff Checklist

- Feature flags or polyfills missing.
- Different default security policies (CSP, mixed content).
- Subtle layout differences (CSS flex/grid quirks).
- Third-party cookies blocked.

## Safety Notes

- Avoid logging full response bodies if they may contain PII or tokens.

