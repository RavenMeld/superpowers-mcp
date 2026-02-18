# merge-pr

Merge a GitHub PR via squash after /prepare-pr. Use when asked to merge a ready PR. Do not push to main or modify code. Ensure the PR ends in MERGED state and clean up worktrees after success.

## Quick Facts
- id: `merge-pr--9a00cd4592`
- worth_using_score: `55/100`
- tags: `github, git, go, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/merge-pr-v1/SKILL.md`

## Workflow / Steps
- Identify PR meta and verify prepared SHA still matches
- Run sanity checks
- PR is a draft.
- Required checks are failing.
- Branch is behind main.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `8`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
