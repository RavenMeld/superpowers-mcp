# agent-browser

Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, or extract information from web pages.

## Quick Facts
- id: `agent-browser--bba0d8f306`
- worth_using_score: `40/100`
- tags: `github, playwright, testing, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/automation/devtools/oh-my-opencode/src/features/builtin-skills/agent-browser/SKILL.md`

## Workflow / Steps
- Navigate: `agent-browser open <url>`
- Snapshot: `agent-browser snapshot -i` (returns elements with refs like `@e1`, `@e2`)
- Interact using refs from the snapshot
- Re-snapshot after navigation or significant DOM changes

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `28`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
