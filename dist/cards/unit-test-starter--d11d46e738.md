# unit-test-starter

Generate starter unit tests for a small function or module. Use when a junior developer needs test scaffolding and edge cases.

## Quick Facts
- id: `unit-test-starter--d11d46e738`
- worth_using_score: `45/100`
- tags: `node`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/frameworks/Spinnybot/skills-selected/unit-test-starter/SKILL.md`

## Use When
- A function/module changed and needs tests.
- A bug needs a regression test.

## Workflow / Steps
- Define the contract.
- Inputs, outputs, invariants, and failure modes.
- Pick test granularity.
- Unit test preferred; add integration test only when IO boundaries matter.
- Build a table of cases.
- Happy path, boundary, invalid input, and one “weird” case.
- Add a regression test for the bug (if applicable).
- Fails before fix, passes after.
- Document how to run tests.
- Exact command(s) and expected output.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
