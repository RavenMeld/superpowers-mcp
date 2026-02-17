# Lobster

Lobster executes multi-step workflows with approval checkpoints. Use it when:

## Quick Facts
- id: `lobster--052c9c4ffd`
- worth_using_score: `55/100`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/openclaw/extensions/lobster/SKILL.md`

## Workflow / Steps
- ### Email triage
- ```
- gog.gmail.search --query 'newer_than:1d' --max 20 | email.triage
- ```
- Fetches recent emails, classifies into buckets (needs_reply, needs_action, fyi).
- ### Email triage with approval gate

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `6`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
