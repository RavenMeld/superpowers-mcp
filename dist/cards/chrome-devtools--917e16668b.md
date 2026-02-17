# chrome-devtools

Uses Chrome DevTools via MCP for efficient debugging, troubleshooting and browser automation. Use when debugging web pages, automating browser interactions, analyzing performance, or inspecting network requests.

## Quick Facts
- id: `chrome-devtools--917e16668b`
- worth_using_score: `20/100`
- tags: `mcp, github, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/chrome-devtools-mcp/skills/chrome-devtools/SKILL.md`

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
