---
name: ci-failure-triage
description: Diagnose CI failures and stabilize pipelines. Use when a mid-level developer needs to resolve flaky or failing builds.
---

# CI Failure Triage

## When to use
- A CI run is red and you need the actual root cause (not the cascade of follow-on failures).
- Tests are flaky and need stabilization without hiding real failures.

## Inputs to request
- Link to the failing run + job name(s) + failing step(s)
- The *first* failing error/stack trace and ~50-200 lines of surrounding logs
- Commit SHA(s) / PR link and what changed (deps, lockfiles, timeouts, parsing, platform assumptions)
- Runner environment (OS, Node/Python versions, container image)

## Workflow
1. Identify the first failure.
- Ignore later failures caused by missing outputs or early aborts.
2. Classify the failure.
- Deterministic vs flaky.
- Unit vs integration vs E2E.
- Infra (network/rate limits) vs code (logic/parsing) vs environment (toolchain versions).
3. Reproduce locally with the narrowest command.
- Prefer a single test file or a single script invocation.
- If reproduction requires external services, add a stubbed test first.
4. Isolate the change that introduced it.
- Diff recent changes; pay attention to dependency updates and time-based logic.
5. Fix + add guardrails.
- Make the fix deterministic.
- Add/adjust tests so the failure can’t silently regress.
- Improve logs, but never leak secrets (tokens, keys, auth headers).

## Outputs
- Short RCA: what failed, why it failed, and what change triggered it
- Minimal repro command(s)
- Proposed fix + tests to add/update
- Risk assessment: what else might break and how to validate quickly

## Stack Notes (agent_playground)
- The workspace root is not a git repo; validate/push per sub-repo.
- Useful smoke/triage loops:
  - TaskFork: `npm test` then `node ./bin/taskfork.js smoke`
  - Model-Jump: `npm test` then `node scripts/smoke-mcp.js`
  - CAO: `.venv/bin/python -m pytest -q`
  - Spinnybot: `python orchestrator.py --goal "Preflight" --preflight-only --no-write`

