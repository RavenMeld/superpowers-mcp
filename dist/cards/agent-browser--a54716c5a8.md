# agent-browser

Browser automation using Vercel's agent-browser CLI. Use when you need to interact with web pages, fill forms, take screenshots, or scrape data. Alternative to Playwright MCP - uses Bash commands with ref-based element selection. Triggers on "browse website", "fill form", "click button", "take screenshot", "scrape page", "web automation".

## Quick Facts
- id: `agent-browser--a54716c5a8`
- worth_using_score: `55/100`
- tags: `mcp, playwright`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/agent-browser/SKILL.md`

## Workflow / Steps
- *The snapshot + ref pattern is optimal for LLMs:**
- **Navigate** to URL
- **Snapshot** to get interactive elements with refs
- **Interact** using refs (@e1, @e2, etc.)
- **Re-snapshot** after navigation or DOM changes

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `17`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
