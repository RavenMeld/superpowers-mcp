# ssh-multi-account-guardian

Prevent account/key mixups when using multiple SSH identities (for example default GitHub + RavenMeld) across WSL and Windows.

## Quick Facts
- id: `ssh-multi-account-guardian--39c31e9c77`
- worth_using_score: `60/100`
- tags: `github, git, ssh, ci, wsl, windows`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/ssh-multi-account-guardian/SKILL.md`

## Use When
- You use multiple GitHub accounts and separate SSH keys.
- Push/pull operations hit the wrong account or permission scope.
- You need deterministic host alias routing across WSL and Windows.

## Workflow / Steps
- Generate one keypair per account/use-case.
- Define explicit `Host` aliases in `~/.ssh/config`.
- Pin each git remote to the intended alias.
- Verify auth identity before push.
- Keep key names and repo remotes clearly labeled.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
