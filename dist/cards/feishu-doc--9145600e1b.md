# feishu-doc

|

## Quick Facts
- id: `feishu-doc--9145600e1b`
- worth_using_score: `45/100`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/openclaw/extensions/feishu/skills/feishu-doc/SKILL.md`

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
