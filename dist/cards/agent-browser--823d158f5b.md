# agent-browser

Browser automation CLI for AI agents. Use when the user needs to interact with websites, including navigating pages, filling forms, clicking buttons, taking screenshots, extracting data, testing web apps, or automating any browser task. Triggers include requests to "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data from a page", "test this web app", "login...

## Quick Facts
- id: `agent-browser--823d158f5b`
- worth_using_score: `60/100`
- tags: `cursor, playwright, browser, chrome, go, java, testing, ci, render, rag, eval`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/vercel-labs-agent-browser/SKILL.md`

## Workflow / Steps
- **Navigate**: `agent-browser open <url>`
- **Snapshot**: `agent-browser snapshot -i` (get element refs like `@e1`, `@e2`)
- **Interact**: Use refs to click, fill, select
- **Re-snapshot**: After navigation or DOM changes, get fresh refs

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `21`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
