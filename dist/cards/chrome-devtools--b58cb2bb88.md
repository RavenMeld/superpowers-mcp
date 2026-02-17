# chrome-devtools

Expert-level browser automation, debugging, and performance analysis using Chrome DevTools MCP. Use for interacting with web pages, capturing screenshots, analyzing network traffic, and profiling performance.

## Quick Facts
- id: `chrome-devtools--b58cb2bb88`
- worth_using_score: `65/100`
- tags: `mcp, ci`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/github-chrome-devtools/SKILL.md`

## Use When
- **Browser Automation**: Navigating pages, clicking elements, filling forms, and handling dialogs.
- **Visual Inspection**: Taking screenshots or text snapshots of web pages.
- **Debugging**: Inspecting console messages, evaluating JavaScript in the page context, and analyzing network requests.
- **Performance Analysis**: Recording and analyzing performance traces to identify bottlenecks and Core Web Vital issues.
- **Emulation**: Resizing the viewport or emulating network/CPU conditions.

## Workflow / Steps
- `take_snapshot` to get the current page structure.
- Find the `uid` of the target element.
- Use `click(uid=...)` or `fill(uid=..., value=...)`.
- `list_console_messages` to check for JavaScript errors.
- `list_network_requests` to identify failed (4xx/5xx) resources.
- `evaluate_script` to check the value of specific DOM elements or global variables.
- `performance_start_trace(reload=true, autoStop=true)`
- Wait for the page to load/trace to finish.
- `performance_analyze_insight` to find LCP issues or layout shifts.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
