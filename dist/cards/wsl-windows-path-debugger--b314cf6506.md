# wsl-windows-path-debugger

Diagnose and fix WSL/Windows path translation, newline, and permission mismatches that break toolchains.

## Quick Facts
- id: `wsl-windows-path-debugger--b314cf6506`
- worth_using_score: `60/100`
- tags: `powershell, ci, wsl, windows, linux`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/wsl-windows-path-debugger/SKILL.md`

## Use When
- Commands work in PowerShell but fail in WSL (or vice versa).
- Tools cannot find files due to `/mnt/c/...` versus `C:\...` confusion.
- Scripts break on CRLF/LF or executable permission differences.

## Workflow / Steps
- Confirm the execution shell and absolute path assumptions.
- Normalize path conversion at the boundary (`wslpath` / explicit mapping).
- Check newline format and shebang compatibility.
- Validate file permissions + executable bits in WSL.
- Re-test from both shells with the same target file.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
