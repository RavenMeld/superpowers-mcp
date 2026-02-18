# cursor-mcp-setup

Configure MCP servers in Cursor using mcp.json (global or per-project), plus validation and common failure modes.

## Quick Facts
- id: `cursor-mcp-setup--e8482ae8f2`
- worth_using_score: `65/100`
- tags: `mcp, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/cursor-mcp-setup/SKILL.md`

## Use When
- You want Cursor to call tools via MCP (stdio, SSE, or streamable HTTP).
- You need to add a custom server not available in “one-click installs”.
- Your MCP servers aren’t showing up and you need a deterministic debug flow.

## Workflow / Steps
- Decide scope: project (`.cursor/mcp.json`) vs global (`~/.cursor/mcp.json`).
- Add/merge a server entry under `"mcpServers"`.
- Restart Cursor (or reload window) so it re-reads config.
- Verify the server is reachable / starts successfully.
- Troubleshoot JSON validity, paths, and auth env vars.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `4`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
