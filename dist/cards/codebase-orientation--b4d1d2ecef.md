# codebase-orientation

Guide quick orientation of an unfamiliar codebase with module mapping, entry points, and local run steps. Use when a junior developer needs to get situated fast.

## Quick Facts
- id: `codebase-orientation--b4d1d2ecef`
- worth_using_score: `60/100`
- tags: `mcp, python, node, go, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/spinnybot-selected/codebase-orientation/SKILL.md`

## Use When
- You need a fast, accurate map of a repo: entrypoints, key modules, and how to run/test it.
- You’re onboarding to a new codebase and want to avoid “random walking” the tree.

## Workflow / Steps
- Identify the primary entrypoints.
- CLI binaries, server mains, MCP servers, and scripts.
- Map the “spine” of the system.
- Core modules/services + config loading + IO boundaries (HTTP/MCP/filesystem).
- Find how to run and test locally.
- Look for `package.json`, `pyproject.toml`, `Makefile`, CI config.
- Document the minimum set of commands.
- Install, run, test, smoke.
- Suggest one safe starter change.
- Small, reversible, and easy to validate.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `1`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
