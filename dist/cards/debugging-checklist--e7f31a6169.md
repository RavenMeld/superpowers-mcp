# debugging-checklist

Provide a systematic debugging checklist. Use when a junior developer is stuck and needs a structured approach.

## Quick Facts
- id: `debugging-checklist--e7f31a6169`
- worth_using_score: `50/100`
- tags: `node, rag`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/frameworks/Spinnybot/skills-selected/debugging-checklist/SKILL.md`

## Use When
- A bug is reported but root cause is unclear.
- “It doesn’t work” without a crisp repro.

## Workflow / Steps
- Reproduce and minimize.
- Reduce to the smallest input/command that still fails.
- Bound the blast radius.
- Identify which component is failing (ingress, router, executor, storage).
- Add the smallest useful probe.
- Structured logs around state transitions and IO boundaries.
- Avoid logging payloads/prompts that can contain secrets.
- Confirm hypotheses with a targeted test.
- Add a unit/integration test that fails before the fix and passes after.
- Fix, then re-run the exact repro.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
