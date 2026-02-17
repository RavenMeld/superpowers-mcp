# feishu-wiki

Feishu knowledge base navigation. Activate when user mentions knowledge base, wiki, or wiki links.

## Quick Facts
- id: `feishu-wiki--14a771da52`
- worth_using_score: `55/100`
- tags: `node`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/openclaw/extensions/feishu/skills/feishu-wiki/SKILL.md`

## Workflow / Steps
- Get node: `{ "action": "get", "token": "wiki_token" }` → returns `obj_token`
- Read doc: `feishu_doc { "action": "read", "doc_token": "obj_token" }`
- Write doc: `feishu_doc { "action": "write", "doc_token": "obj_token", "content": "..." }`

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `10`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
