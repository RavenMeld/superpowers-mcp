# lmstudio-mcp-setup

Configure MCP servers in LM Studio (MCP host support), including where to edit mcp.json and common gotchas.

## Quick Facts
- id: `lmstudio-mcp-setup--6f9f732344`
- worth_using_score: `55/100`
- tags: `mcp, rust, go`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/lmstudio-mcp-setup/SKILL.md`

## Use When
- You want LM Studio to act as an MCP Host (local or remote MCP servers).
- You need to manually edit `mcp.json`.
- Tools aren’t appearing and you need a deterministic check list.

## Workflow / Steps
- In LM Studio, open the MCP config editor (Program tab -> Install -> Edit `mcp.json`).
- Add/merge servers under `"mcpServers"`.
- Save and restart LM Studio (or re-open the app).
- Ask the model to list available tools to confirm.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `1`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
