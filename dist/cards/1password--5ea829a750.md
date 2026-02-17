# 1password

Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op.

## Quick Facts
- id: `1password--5ea829a750`
- worth_using_score: `50/100`
- tags: `ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/1password/SKILL.md`

## Workflow / Steps
- Check OS + shell.
- Verify CLI present: `op --version`.
- Confirm desktop app integration is enabled (per get-started) and the app is unlocked.
- REQUIRED: create a fresh tmux session for all `op` commands (no direct `op` calls outside tmux).
- Sign in / authorize inside tmux: `op signin` (expect app prompt).
- Verify access inside tmux: `op whoami` (must succeed before any secret read).
- If multiple accounts: use `--account` or `OP_ACCOUNT`.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `1`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
