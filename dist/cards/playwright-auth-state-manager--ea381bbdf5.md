# playwright-auth-state-manager

Manage Playwright authentication state safely and deterministically across local runs and CI.

## Quick Facts
- id: `playwright-auth-state-manager--ea381bbdf5`
- worth_using_score: `60/100`
- tags: `playwright, go, ci, rag`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/playwright-auth-state-manager/SKILL.md`

## Use When
- Tests require authenticated sessions.
- Login steps are flaky or too slow in every test.
- CI failures stem from expired or polluted auth state.

## Workflow / Steps
- Create dedicated auth setup project/spec.
- Persist storage state into scoped, non-secret artifacts.
- Reuse auth state only for matching test domains/roles.
- Refresh auth state on expiration signals.
- Keep logout/cleanup checks in teardown paths.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
