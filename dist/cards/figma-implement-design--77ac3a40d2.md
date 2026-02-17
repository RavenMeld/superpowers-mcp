# figma-implement-design

Translate Figma nodes into production-ready code with 1:1 visual fidelity using the Figma MCP workflow (design context, screenshots, assets, and project-convention translation). Trigger when the user provides Figma URLs or node IDs, or asks to implement designs or components that must match Figma specs. Requires a working Figma MCP server connection.

## Quick Facts
- id: `figma-implement-design--77ac3a40d2`
- worth_using_score: `33/100`
- tags: `mcp, typescript, node, ci, docs, figma`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/figma-implement-design/SKILL.md`

## Workflow / Steps
- *Follow these steps in order. Do not skip steps.**
- Add the Figma MCP:
- `codex mcp add figma --url https://mcp.figma.com/mcp`
- Enable remote MCP client:
- Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
- Log in with OAuth:
- `codex mcp login figma`
- *URL format:** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`
- *Extract:**
- **File key:** `:fileKey` (the segment after `/design/`)

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `2`
- has_scripts: `False`
- has_references: `False`
- has_assets: `True`
