# agent-browser

Automates browser interactions for web testing, form filling, screenshots, and data extraction. Use when the user needs to navigate websites, interact with web pages, fill forms, take screenshots, test web applications, or extract information from web pages.

## Quick Facts
- id: `agent-browser--3ce6e63398`
- worth_using_score: `55/100`
- tags: `github, git, playwright, browser, chrome, go, java, testing, ci, windows, vercel, rag, eval`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/code-yeongyu-agent-browser/SKILL.md`

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
