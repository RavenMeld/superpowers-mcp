---
name: python-project-bootstrap
description: |
  Bootstrap a clean Python project with reproducible environments, lint/type/test gates, and a fast debug loop.
  Focuses on uv/venv + ruff + pyright + pytest patterns.
---

# Python Project Bootstrap

## Use When

- You’re starting a new Python repo and want good defaults.
- You need fast setup on Linux/WSL/Windows with minimal yak shave.
- You want a repeatable “format + lint + typecheck + tests” loop.

## Workflow

1. Create an isolated environment (uv or venv).
2. Add quality gates (ruff, pyright, pytest).
3. Add a single command that runs the full gate.
4. Add a minimal smoke test and iterate.

## Example: uv (Recommended)

Create project + venv:

```bash
uv init
uv venv
```

Add tools:

```bash
uv pip install -U ruff pyright pytest
```

Run gates:

```bash
ruff format .
ruff check .
pyright
pytest -q
```

## Example: venv (Fallback)

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip ruff pyright pytest
```

## Common Files

Minimal `pyproject.toml` tool config is usually enough (ruff + project metadata).
Keep CI commands identical to local commands.

## Safety Notes

- Pin Python versions when reproducibility matters (use `.python-version` or toolchain pinning).
- Avoid mixing system Python packages with your project env.

