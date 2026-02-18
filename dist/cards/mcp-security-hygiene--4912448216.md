# mcp-security-hygiene

Treat MCP servers as executable code: least privilege, safe defaults, review checklist, and common failure modes.

## Quick Facts
- id: `mcp-security-hygiene--4912448216`
- worth_using_score: `50/100`
- tags: `mcp, github, security, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/mcp-security-hygiene/SKILL.md`

## Use When
- You’re adding a new MCP server (especially from GitHub/marketplaces).
- You’re exposing filesystem, shell, browser automation, or network tools.
- You need a quick “is this safe enough?” review before enabling.

## Workflow / Steps
- Identify what the server can access (filesystem roots, env vars, network).
- Reduce privileges (allowlists, localhost binds, minimal env).
- Pin versions after it works.
- Log carefully (redact tokens), and keep outputs bounded.
- Prefer “manual start + inspect” before letting a client auto-launch it.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
