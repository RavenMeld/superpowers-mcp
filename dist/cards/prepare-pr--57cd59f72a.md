# prepare-pr

Script-first PR preparation with structured findings resolution, deterministic push safety, and explicit gate execution.

## Quick Facts
- id: `prepare-pr--57cd59f72a`
- worth_using_score: `55/100`
- tags: `ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/openclaw/.agents/skills/prepare-pr/SKILL.md`

## Workflow / Steps
- Setup and artifacts
- Resolve required findings
- Update changelog/docs (changelog is mandatory in this workflow)
- Commit scoped changes
- Run gates
- Push safely to PR head
- robust fork remote resolution from owner/name,
- pre-push remote SHA verification,
- one automatic rebase + gate rerun + retry if lease push fails,
- post-push PR-head propagation retry,

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `9`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
