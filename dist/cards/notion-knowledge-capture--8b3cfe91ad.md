# notion-knowledge-capture

Capture conversations and decisions into structured Notion pages; use when turning chats/notes into wiki entries, how-tos, decisions, or FAQs with proper linking.

## Quick Facts
- id: `notion-knowledge-capture--8b3cfe91ad`
- worth_using_score: `20/100`
- tags: `mcp, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/notion-knowledge-capture/SKILL.md`

## Workflow / Steps
- Add the Notion MCP:
- `codex mcp add notion --url https://mcp.notion.com/mcp`
- Enable remote MCP client:
- Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
- Log in with OAuth:
- `codex mcp login notion`
- Ask purpose, audience, freshness, and whether this is new or an update.
- Determine content type: decision, how-to, FAQ, concept/wiki entry, learning/note, documentation page.
- Pick the correct database using `reference/*-database.md` guides; confirm required properties (title, tags, owner, status, date, relations).
- If multiple candidate databases, ask the user which to use; otherwise, create in the primary wiki/documentation DB.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
