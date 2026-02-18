# github-ssh-multi-account-wsl

Create and use multiple GitHub SSH identities from WSL without breaking your existing GitHub SSH setup.
Uses per-host aliases so each repo can target the right key deterministically.

## Quick Facts
- id: `github-ssh-multi-account-wsl--3d479c57e2`
- worth_using_score: `70/100`
- tags: `github, git, ssh, wsl, windows`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/github-ssh-multi-account-wsl/SKILL.md`

## Use When
- You need a **second GitHub account** (or org) on the same WSL machine.
- You want to keep existing `git@github.com:...` remotes working unchanged.
- You want predictable key usage (no agent guessing).

## Workflow / Steps
- Generate a new keypair (one key per account).
- Add a dedicated `Host` alias in `~/.ssh/config` that points at that key.
- Add the **public** key to the target GitHub account.
- Use the alias in your git remotes (clone or `remote set-url`).
- Verify with `ssh -T`.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `8`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
