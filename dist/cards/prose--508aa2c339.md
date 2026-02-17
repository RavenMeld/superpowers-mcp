# prose

OpenProse VM skill pack. Activate on any `prose` command, .prose files, or OpenProse mentions; orchestrates multi-agent workflows.

## Quick Facts
- id: `prose--508aa2c339`
- worth_using_score: `35/100`
- tags: `github, docker, security, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/openclaw/extensions/open-prose/skills/prose/SKILL.md`

## Workflow / Steps
- **Check for `.prose/state.json`**
- If exists, read the JSON content
- Convert to `.env` format:
- Write to `.prose/.env`
- Delete `.prose/state.json`
- **Check for `.prose/execution/`**
- If exists, rename to `.prose/runs/`
- The internal structure of run directories may also have changed; migration of individual run state is best-effort
- **Create `.prose/agents/` if missing**
- This is a new directory for project-scoped persistent agents

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
