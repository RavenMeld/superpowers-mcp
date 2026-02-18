# cross-platform-safety

Ensure commands and paths are safe across Windows + WSL + Docker (PowerShell vs bash, path translation, permissions). Use when instructions touch shell, filesystem, Docker, or OS-specific behavior.

## Quick Facts
- id: `cross-platform-safety--84d876fc7e`
- worth_using_score: `30/100`
- tags: `powershell, docker, ci, wsl, windows`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/janjaszczak-cross-platform-safety/SKILL.md`

## Workflow / Steps
- Determine execution context:
- Where the command will run (Windows host? WSL? container?).
- Provide OS-specific variants ONLY if needed:
- Prefer a single canonical path + “Windows note” if small delta.
- Guardrails:
- Avoid reserved PowerShell variables and quoting pitfalls.
- Avoid whitespace path breakage; use explicit quoting.
- Validate critical commands with “dry read” steps (e.g., `pwd`, `whoami`, `ls`).

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
