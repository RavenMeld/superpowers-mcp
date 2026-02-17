# feishu-doc

Feishu document read/write operations. Activate when user mentions Feishu docs, cloud docs, or docx links.

## Quick Facts
- id: `feishu-doc--f7157e71fa`
- worth_using_score: `60/100`
- tags: `docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/feishu-doc/SKILL.md`

## Workflow / Steps
- Start with `action: "read"` - get plain text + statistics
- Check `block_types` in response for Table, Image, Code, etc.
- If structured content exists, use `action: "list_blocks"` for full data

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `10`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
