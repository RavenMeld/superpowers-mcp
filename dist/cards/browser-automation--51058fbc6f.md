# browser-automation

Reliable, composable browser automation using minimal OpenCode Browser primitives.

## Quick Facts
- id: `browser-automation--51058fbc6f`
- worth_using_score: `35/100`
- tags: `browser`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/different-ai-browser-automation/SKILL.md`

## Workflow / Steps
- Inspect tabs with `browser_get_tabs`
- Open new tabs with `browser_open_tab` when needed
- Navigate with `browser_navigate` if needed
- Wait for UI using `browser_query` with `timeoutMs`
- Discover candidates using `browser_query` with `mode=list`
- Click, type, or select using `index`
- Confirm using `browser_query` or `browser_snapshot`

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
