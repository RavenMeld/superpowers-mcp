# notion-spec-to-implementation

Turn Notion specs into implementation plans, tasks, and progress tracking; use when implementing PRDs/feature specs and creating Notion plans + tasks from them.

## Quick Facts
- id: `notion-spec-to-implementation--fe923421bd`
- worth_using_score: `35/100`
- tags: `mcp, go, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/notion-spec-to-implementation/SKILL.md`

## Workflow / Steps
- Add the Notion MCP:
- `codex mcp add notion --url https://mcp.notion.com/mcp`
- Enable remote MCP client:
- Set `[features].rmcp_client = true` in `config.toml` **or** run `codex --enable rmcp_client`
- Log in with OAuth:
- `codex mcp login notion`
- Search first (`Notion:notion-search`); if multiple hits, ask the user which to use.
- Fetch the page (`Notion:notion-fetch`) and scan for requirements, acceptance criteria, constraints, and priorities. See `reference/spec-parsing.md` for extraction patterns.
- Capture gaps/assumptions in a clarifications block before proceeding.
- Simple change → use `reference/quick-implementation-plan.md`.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
