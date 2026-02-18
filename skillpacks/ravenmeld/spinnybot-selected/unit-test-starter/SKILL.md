---
name: unit-test-starter
description: Generate starter unit tests for a small function or module. Use when a junior developer needs test scaffolding and edge cases.
---

# Unit Test Starter

## When to use
- A function/module changed and needs tests.
- A bug needs a regression test.

## Inputs to request
- Function signature + expected behavior (inputs/outputs)
- Test framework + language (Node `node --test`, `pytest`, etc.)
- Edge cases and error conditions to cover

## Workflow
1. Define the contract.
- Inputs, outputs, invariants, and failure modes.
2. Pick test granularity.
- Unit test preferred; add integration test only when IO boundaries matter.
3. Build a table of cases.
- Happy path, boundary, invalid input, and one “weird” case.
4. Add a regression test for the bug (if applicable).
- Fails before fix, passes after.
5. Document how to run tests.
- Exact command(s) and expected output.

## Outputs
- Case table (inputs -> expected outputs)
- Starter test code snippet that matches the repo’s conventions
- Notes on what to mock/stub for determinism

