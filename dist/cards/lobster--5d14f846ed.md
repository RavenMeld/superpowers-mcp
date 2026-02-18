# lobster

Guidance for building multi-step workflows with explicit approval checkpoints for safe automation.

## Quick Facts
- id: `lobster--5d14f846ed`
- worth_using_score: `55/100`
- tags: `go, ci, llm`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/lobster/SKILL.md`

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
