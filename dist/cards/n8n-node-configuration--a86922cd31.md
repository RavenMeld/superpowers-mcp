# n8n-node-configuration

Operation-aware node configuration guidance. Use when configuring nodes, understanding property dependencies, determining required fields, choosing between get_node detail levels, or learning common configuration patterns by node type.

## Quick Facts
- id: `n8n-node-configuration--a86922cd31`
- worth_using_score: `55/100`
- tags: `mcp, node, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/n8n-node-configuration/SKILL.md`

## Workflow / Steps
- Identify node type and operation
- Use get_node (standard detail is default)
- Configure required fields
- Validate configuration
- If field unclear → get_node({mode: "search_properties"})
- Add optional fields as needed
- Validate again
- Deploy
- *Step 1**: Identify what you need
- *Step 2**: Get node info

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `42`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
