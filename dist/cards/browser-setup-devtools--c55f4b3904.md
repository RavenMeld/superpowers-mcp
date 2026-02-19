# browser-setup-devtools

Guide users through browser automation setup using Chrome DevTools MCP as the primary path and the OpenCode browser extension as a fallback. Use when the user asks to set up browser automation, Chrome DevTools MCP, browser MCP, browser extension, or runs the browser-setup command.

## Quick Facts
- id: `browser-setup-devtools--c55f4b3904`
- worth_using_score: `35/100`
- tags: `mcp, browser, chrome, go, ci, windows, linux`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/different-ai-browser-setup-devtools/SKILL.md`

## Workflow / Steps
- Ask: "Do you have Chrome installed on this computer?"
- If no or unsure:
- Offer to open the download page yourself and do it if possible.
- Provide a clickable link: https://www.google.com/chrome/
- Continue after installation is confirmed.
- Check DevTools MCP availability:
- Call `chrome-devtools_list_pages`.
- If pages exist, select one with `chrome-devtools_select_page`.
- If no pages, create one with `chrome-devtools_new_page` (use https://example.com) and then select it.
- If DevTools MCP calls fail:

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
