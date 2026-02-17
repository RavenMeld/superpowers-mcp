# merge-pr

Script-first deterministic squash merge with strict required-check gating, head-SHA pinning, and reliable attribution/commenting.

## Quick Facts
- id: `merge-pr--f57b516d71`
- worth_using_score: `40/100`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/openclaw/.agents/skills/merge-pr/SKILL.md`

## Workflow / Steps
- Validate artifacts
- Validate checks and branch status
- Merge deterministically (wrapper-managed)
- deterministic squash merge pinned to `PREP_HEAD_SHA`
- reviewer merge author email selection with fallback candidates
- one retry only when merge fails due to author-email validation
- co-author trailers for PR author and reviewer
- post-merge verification of both co-author trailers on commit message
- PR comment retry (3 attempts), then comment URL extraction
- cleanup after confirmed `MERGED`

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `7`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
