# prepare-pr

Prepare a GitHub PR for merge by rebasing onto main, fixing review findings, running gates, committing fixes, and pushing to the PR head branch. Use after /review-pr. Never merge or push to main.

## Quick Facts
- id: `prepare-pr--fb100e1295`
- worth_using_score: `55/100`
- tags: `github, node, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/openclaw/.agents/archive/prepare-pr-v1/SKILL.md`

## Workflow / Steps
- Identify PR meta with one API call
- Fetch PR head and rebase on latest `origin/main`
- Resolve each conflicted file.
- Run `git add <resolved_file>` for each file.
- Run `git rebase --continue`.
- Fix issues from `.local/review.md`
- Fix all BLOCKER and IMPORTANT items.
- NITs are optional.
- Keep scope tight.
- List which review items you fixed.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `16`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
