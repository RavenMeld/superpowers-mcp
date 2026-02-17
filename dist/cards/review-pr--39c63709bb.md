# review-pr

Review-only GitHub pull request analysis with the gh CLI. Use when asked to review a PR, provide structured feedback, or assess readiness to land. Do not merge, push, or make code changes you intend to keep.

## Quick Facts
- id: `review-pr--39c63709bb`
- worth_using_score: `40/100`
- tags: `github, node, security, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/openclaw/.agents/archive/review-pr-v1/SKILL.md`

## Workflow / Steps
- Identify PR meta and context
- Check if this already exists in main before looking at the PR branch
- Identify the core feature or fix from the PR title and description.
- Search for existing implementations using keywords from the PR title, changed file paths, and function or component names from the diff.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `9`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
