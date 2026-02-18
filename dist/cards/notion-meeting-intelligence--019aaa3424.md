# notion-meeting-intelligence

Prepare meeting materials with Notion context and Codex research; use when gathering context, drafting agendas/pre-reads, and tailoring materials to attendees.

## Quick Facts
- id: `notion-meeting-intelligence--019aaa3424`
- worth_using_score: `35/100`
- tags: `mcp, go, ci, docs, benchmark`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/notion-meeting-intelligence/SKILL.md`

## Workflow / Steps
- Add the Notion MCP:
- `codex mcp add notion --url https://mcp.notion.com/mcp`
- Enable remote MCP client:
- Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
- Log in with OAuth:
- `codex mcp login notion`
- Ask for objective, desired outcomes/decisions, attendees, duration, date/time, and prior materials.
- Search Notion for relevant docs, past notes, specs, and action items (`Notion:notion-search`), then fetch key pages (`Notion:notion-fetch`).
- Capture blockers/risks and open questions up front.
- Status/update → status template.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
