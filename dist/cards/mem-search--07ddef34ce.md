# mem-search

Search claude-mem's persistent cross-session memory database. Use when user asks "did we already solve this?", "how did we do X last time?", or needs work from previous sessions.

## Quick Facts
- id: `mem-search--07ddef34ce`
- worth_using_score: `70/100`
- tags: `mcp, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/mem-search/SKILL.md`

## Use When
- "Did we already fix this?"
- "How did we solve X last time?"
- "What happened last week?"

## Workflow / Steps
- *NEVER fetch full details without filtering first. 10x token savings.**
- *Returns:** Table with IDs, timestamps, types, titles (~50-100 tokens/result)
- *Parameters:**
- `query` (string) - Search term
- `limit` (number) - Max results, default 20, max 100
- `project` (string) - Project name filter
- `type` (string, optional) - "observations", "sessions", or "prompts"
- `obs_type` (string, optional) - Comma-separated: bugfix, feature, decision, discovery, change
- `dateStart` (string, optional) - YYYY-MM-DD or epoch ms
- `dateEnd` (string, optional) - YYYY-MM-DD or epoch ms

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `10`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
