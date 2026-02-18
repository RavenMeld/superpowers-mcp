---
name: debugging-checklist
description: Provide a systematic debugging checklist. Use when a junior developer is stuck and needs a structured approach.
---

# Debugging Checklist

## When to use
- A bug is reported but root cause is unclear.
- “It doesn’t work” without a crisp repro.

## Inputs to request
- Exact repro steps and expected vs actual behavior
- Frequency (always / intermittent) and scope (one machine / everyone)
- Environment (OS, versions, env vars, recent changes)
- Logs/stack traces (first failure + context), plus any artifacts produced

## Workflow
1. Reproduce and minimize.
- Reduce to the smallest input/command that still fails.
2. Bound the blast radius.
- Identify which component is failing (ingress, router, executor, storage).
3. Add the smallest useful probe.
- Structured logs around state transitions and IO boundaries.
- Avoid logging payloads/prompts that can contain secrets.
4. Confirm hypotheses with a targeted test.
- Add a unit/integration test that fails before the fix and passes after.
5. Fix, then re-run the exact repro.
- Verify no regression with the smallest relevant suite.

## Outputs
- A checklist of likely causes ordered by probability
- 1-3 concrete next probes or tests to run/add
- Clear “stop conditions” (what evidence would falsify the current hypothesis)

## Stack Notes (agent_playground)
Prefer safe modes before “real calls”:
- TaskFork: `node ./bin/taskfork.js smoke` (probe-only)
- Spinnybot: `--preflight-only --no-write`
- Model-Jump: use `dry_run: true` for routing checks when possible

