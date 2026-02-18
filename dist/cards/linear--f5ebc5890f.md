# linear

Manage issues, projects & team workflows in Linear. Use when the user wants to read, create or updates tickets in Linear.

## Quick Facts
- id: `linear--f5ebc5890f`
- worth_using_score: `48/100`
- tags: `mcp, browser, go, ci, docs, wsl, windows, rag`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/linear/SKILL.md`

## Workflow / Steps
- *Follow these steps in order. Do not skip steps.**
- Add the Linear MCP:
- `codex mcp add linear --url https://mcp.linear.app/mcp`
- Enable remote MCP client:
- Set `[features] rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
- Log in with OAuth:
- `codex mcp login linear`
- *Windows/WSL note:** If you see connection errors on Windows, try configuring the Linear MCP to run via WSL:
- Read first (list/get/search) to build context.
- Create or update next (issues, projects, labels, comments) with all required fields.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `1`
- has_scripts: `False`
- has_references: `False`
- has_assets: `True`
