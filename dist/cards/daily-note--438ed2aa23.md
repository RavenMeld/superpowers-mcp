# daily-note

Work with Obsidian daily notes. Create today's note if missing, append content to existing note, or read current daily note. Uses Obsidian's periodic notes conventions. Requires Obsidian MCP server.

## Quick Facts
- id: `daily-note--438ed2aa23`
- worth_using_score: `45/100`
- tags: `mcp, typescript, obsidian`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/robabby-daily-note/SKILL.md`

## Workflow / Steps
- Use `obsidian_get_periodic_note({ period: "daily" })`
- Display content or note if missing
- Check if daily note exists
- Determine path from periodic notes config or CLAUDE.md
- Create with appropriate template/frontmatter
- Common path patterns:
- `Planner/YYYY/MM-Month/YYYY-MM-DD.md`
- `Daily/YYYY-MM-DD.md`
- `Journal/YYYY/YYYY-MM-DD.md`
- Get existing note content

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `2`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
