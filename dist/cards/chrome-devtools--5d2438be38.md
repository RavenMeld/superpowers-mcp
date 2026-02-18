# chrome-devtools

Uses Chrome DevTools via MCP for efficient debugging, troubleshooting and browser automation. Use when debugging web pages, automating browser interactions, analyzing performance, or inspecting network requests.

## Quick Facts
- id: `chrome-devtools--5d2438be38`
- worth_using_score: `35/100`
- tags: `mcp, github, git, browser, chrome, ci, docs, eval`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/chromedevtools-chrome-devtools/SKILL.md`

## Workflow / Steps
- Navigate: `navigate_page` or `new_page`
- Wait: `wait_for` to ensure content is loaded if you know what you look for.
- Snapshot: `take_snapshot` to understand page structure
- Interact: Use element `uid`s from snapshot for `click`, `fill`, etc.
- Use `filePath` parameter for large outputs (screenshots, snapshots, traces)
- Use pagination (`pageIdx`, `pageSize`) and filtering (`types`) to minimize data
- Set `includeSnapshot: false` on input actions unless you need updated page state
- **Automation/interaction**: `take_snapshot` (text-based, faster, better for automation)
- **Visual inspection**: `take_screenshot` (when user needs to see visual state)
- **Additional details**: `evaluate_script` for data not in accessibility tree

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
