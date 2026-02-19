# git-signing-ops

Configure and verify Git commit signing (SSH or GPG) across Linux/WSL/Windows with reliable verification checks.

## Quick Facts
- id: `git-signing-ops--be4cd2e2c1`
- worth_using_score: `60/100`
- tags: `github, git, ssh, rust, wsl, windows, linux`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/git-signing-ops/SKILL.md`

## Use When
- You need verified commits for protected branches or org policy.
- Signing works in one shell but fails in another (WSL vs Windows).
- You are standardizing commit signing for multiple repos.

## Workflow / Steps
- Choose signing mode (SSH signing preferred for simple GitHub workflows).
- Configure git signing keys and enable `commit.gpgsign`.
- Test a signed commit locally.
- Verify signature status in `git log --show-signature`.
- Repeat verification in each shell environment you use.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
