# browser

This skill should be used for browser automation tasks using Chrome DevTools Protocol (CDP). Triggers when users need to launch Chrome with remote debugging, navigate pages, execute JavaScript in browser context, capture screenshots, or interactively select DOM elements. No MCP server required.

## Quick Facts
- id: `browser--ed92b6f327`
- worth_using_score: `65/100`
- tags: `mcp, browser, java, ci, eval`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/cexll-browser/SKILL.md`

## Workflow / Steps
- Launch Chrome: `scripts/start.js --profile` for authenticated sessions
- Navigate: `scripts/nav.js <url>`
- Inspect: `scripts/eval.js 'document.querySelector(...)'`
- Capture: `scripts/screenshot.js` or `scripts/pick.js`
- Return gathered data

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `6`
- has_scripts: `True`
- has_references: `False`
- has_assets: `False`
