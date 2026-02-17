# notion-research-documentation

Research across Notion and synthesize into structured documentation; use when gathering info from multiple Notion sources to produce briefs, comparisons, or reports with citations.

## Quick Facts
- id: `notion-research-documentation--52df606065`
- worth_using_score: `35/100`
- tags: `mcp, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/notion-research-documentation/SKILL.md`

## Workflow / Steps
- Add the Notion MCP:
- `codex mcp add notion --url https://mcp.notion.com/mcp`
- Enable remote MCP client:
- Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
- Log in with OAuth:
- `codex mcp login notion`
- Search first (`Notion:notion-search`); refine queries, and ask the user to confirm if multiple results appear.
- Fetch relevant pages (`Notion:notion-fetch`), skim for facts, metrics, claims, constraints, and dates.
- Track each source URL/ID for later citation; prefer direct quotes for critical facts.
- Quick readout → quick brief.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
