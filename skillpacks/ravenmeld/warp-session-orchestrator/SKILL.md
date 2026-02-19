---
name: warp-session-orchestrator
description: |
  Build repeatable Warp terminal session layouts for coding, testing, deployment, and incident response workflows.
---

# Warp Session Orchestrator

## Use When

- You want one-command setup of your daily terminal workflow.
- You switch between dev/test/release contexts often.
- You need shareable but secret-safe terminal runbooks.

## Workflow

1. Define session goals (dev loop, test triage, release ops).
2. Create command blocks for each pane/tab responsibility.
3. Use environment guards so missing secrets fail fast.
4. Keep one cleanup/reset command per workflow.
5. Version session docs with your repository runbooks.

## Copy/Paste Examples

```bash
cd /path/to/repo && source .venv/bin/activate && make dev
```

```bash
cd /path/to/repo && npm test -- --watch
```

```bash
export OPENAI_API_KEY="${OPENAI_API_KEY:?missing OPENAI_API_KEY}" && make smoke
```

## Orchestration Notes

- Separate long-running services from one-shot commands.
- Prefer explicit `cd` and env setup in every block.
- Keep session templates minimal and composable.

## Safety Notes

- Do not store plaintext secrets in shared Warp workflows.
- Confirm destructive commands before adding them to reusable sessions.
