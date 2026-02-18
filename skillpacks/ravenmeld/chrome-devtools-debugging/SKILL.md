---
name: chrome-devtools-debugging
description: |
  Debug and profile web apps using Chrome DevTools: console, network, performance traces, memory, and lighthouse-style checks.
---

# Chrome DevTools Debugging

## Use When

- A web page is broken and you need root-cause evidence fast.
- You need to inspect network requests, headers, cookies, and caching behavior.
- You need performance profiling (slow page, jank, long tasks).

## Workflow

1. Reproduce the issue with DevTools open.
2. Capture console errors + stack traces.
3. Capture a Network HAR-like view (requests + responses + timings).
4. Profile performance and identify the bottleneck (CPU, layout, JS, network).
5. Apply the smallest fix and re-check in an incognito profile.

## Fast Evidence Capture

Open DevTools:
- Windows/Linux: `Ctrl+Shift+I`
- macOS: `Cmd+Option+I`

Console: copy errors (include stack traces).

Network:
1. Enable “Preserve log”.
2. Reload the page.
3. Filter by `fetch`/`xhr` and inspect failing requests.

## Performance Profiling

1. DevTools -> Performance -> Record.
2. Reproduce the slow interaction.
3. Stop recording and look for:
   - long tasks
   - layout thrash
   - heavy scripting
   - render blocking resources

## Common Fixes

- Too many requests:
  - batch API calls
  - cache results
  - enable compression
- UI jank:
  - avoid forced synchronous layout
  - memoize expensive renders
  - move heavy work off the main thread when possible

## Safety Notes

- Don’t paste sensitive cookies/tokens into logs or tickets.
- Use a fresh profile/incognito to rule out extensions and cached state.

