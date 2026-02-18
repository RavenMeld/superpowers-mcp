# python-project-bootstrap

Bootstrap a clean Python project with reproducible environments, lint/type/test gates, and a fast debug loop.
Focuses on uv/venv + ruff + pyright + pytest patterns.

## Quick Facts
- id: `python-project-bootstrap--1be93be29e`
- worth_using_score: `60/100`
- tags: `python, go, ci, wsl, windows, linux`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/python-project-bootstrap/SKILL.md`

## Use When
- You’re starting a new Python repo and want good defaults.
- You need fast setup on Linux/WSL/Windows with minimal yak shave.
- You want a repeatable “format + lint + typecheck + tests” loop.

## Workflow / Steps
- Create an isolated environment (uv or venv).
- Add quality gates (ruff, pyright, pytest).
- Add a single command that runs the full gate.
- Add a minimal smoke test and iterate.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `4`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
