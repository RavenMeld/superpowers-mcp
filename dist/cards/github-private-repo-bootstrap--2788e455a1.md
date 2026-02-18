# github-private-repo-bootstrap

Bootstrap a private GitHub repo safely: SSH remote, branch setup, first push, and verification (including multi-account SSH aliases).

## Quick Facts
- id: `github-private-repo-bootstrap--2788e455a1`
- worth_using_score: `70/100`
- tags: `github, git, ssh, wsl, linux`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/github-private-repo-bootstrap/SKILL.md`

## Use When
- You created a new private repo and need to push code from WSL/Linux.
- You have multiple GitHub accounts and need deterministic SSH identity selection.
- You want a clean `main` branch setup with minimal footguns.

## Workflow / Steps
- Create the repo in GitHub (private).
- Initialize git locally (or enter an existing repo).
- Add the SSH remote using the right host alias.
- Push `main` and verify by fetching.
- Lock in the remote URL and branch upstream.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `6`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
