# windsurf-mcp-setup

Configure MCP servers in Windsurf (Codeium Cascade), including config file location and restart/refresh workflow.

## Quick Facts
- id: `windsurf-mcp-setup--fb4da1e68f`
- worth_using_score: `55/100`
- tags: `mcp, rust`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/windsurf-mcp-setup/SKILL.md`

## Use When
- You use Windsurf’s Cascade and want to add MCP servers.
- You need to edit raw MCP config (beyond templates/marketplace).
- Your MCP server doesn’t show up and you need a consistent debug loop.

## Workflow / Steps
- Open MCP settings in Windsurf UI, or edit the raw config file.
- Add a server under `"mcpServers"`.
- Refresh/restart Windsurf so it reloads.
- Verify server start and tool availability.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `2`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
