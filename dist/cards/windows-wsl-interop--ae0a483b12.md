# windows-wsl-interop

Practical WSL <-> Windows interop cheatsheet: paths, clipboard, opening files, and moving data safely.

## Quick Facts
- id: `windows-wsl-interop--ae0a483b12`
- worth_using_score: `65/100`
- tags: `github, git, ssh, node, go, ci, wsl, windows`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/windows-wsl-interop/SKILL.md`

## Use When
- You bounce between Windows apps and WSL tooling.
- You need reliable path conversion and clipboard transfer.
- You want quick “open this folder/file in Windows” from WSL.

## Workflow / Steps
- Convert paths with `wslpath`.
- Use `explorer.exe` to open folders/files.
- Use `clip.exe` to copy text to Windows clipboard.
- Prefer working inside the WSL filesystem for performance (especially git/node).

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `6`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
