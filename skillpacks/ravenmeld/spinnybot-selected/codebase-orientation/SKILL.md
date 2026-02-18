---
name: codebase-orientation
description: Guide quick orientation of an unfamiliar codebase with module mapping, entry points, and local run steps. Use when a junior developer needs to get situated fast.
---

# Codebase Orientation

## When to use
- You need a fast, accurate map of a repo: entrypoints, key modules, and how to run/test it.
- You’re onboarding to a new codebase and want to avoid “random walking” the tree.

## Inputs to request
- Repo path (or URL) and what the user is trying to do (bugfix/feature/integration)
- Runtime + package manager expectations (Node/Python/Go, npm/uv/pip)
- Any failing command, log snippet, or target subsystem

## Workflow
1. Identify the primary entrypoints.
- CLI binaries, server mains, MCP servers, and scripts.
2. Map the “spine” of the system.
- Core modules/services + config loading + IO boundaries (HTTP/MCP/filesystem).
3. Find how to run and test locally.
- Look for `package.json`, `pyproject.toml`, `Makefile`, CI config.
4. Document the minimum set of commands.
- Install, run, test, smoke.
5. Suggest one safe starter change.
- Small, reversible, and easy to validate.

## Outputs
- Module map with concrete file paths
- Copy/paste local run/test commands (with prerequisites)
- Top 3 “where to look first” pointers for the target task

## Stack Notes (agent_playground)
Common entrypoints in the stack:
- Spinnybot: `orchestrator.py`
- TaskFork: `bin/taskfork.js` and MCP `bin/taskfork-mcp.js`
- Model-Jump: `src/index.js` (MCP stdio server)
- CAO: `cao-server` (FastAPI + MCP, tmux-backed)

Useful navigation commands:
```bash
rg -n "main\\(|__main__|bin/|src/index\\.js|mcp" .
ls -la
```

