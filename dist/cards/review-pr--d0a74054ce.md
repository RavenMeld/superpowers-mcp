# review-pr

Script-first review-only GitHub pull request analysis. Use for deterministic PR review with structured findings handoff to /prepare-pr.

## Quick Facts
- id: `review-pr--d0a74054ce`
- worth_using_score: `55/100`
- tags: `github, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/openclaw/.agents/skills/review-pr/SKILL.md`

## Workflow / Steps
- Setup and metadata
- Existing implementation check on main
- Claim PR
- Read PR description and diff
- Optional local tests
- Initialize review artifact templates
- Produce review outputs
- Fill `.local/review.md` sections A through J.
- Fill `.local/review.json`.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `11`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
