# agent-browser

Browser automation command reference and usage patterns for web testing, form filling, screenshots, and data extraction.

## Quick Facts
- id: `agent-browser--f24e57e8bd`
- worth_using_score: `60/100`
- tags: `browser, chrome, go, java, testing, ci, windows, rag, eval`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/fradser-agent-browser/SKILL.md`

## Workflow / Steps
- Navigate: `agent-browser open <url>`
- Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
- Interact using refs from the snapshot
- Re-snapshot after navigation or significant DOM changes

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `27`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
