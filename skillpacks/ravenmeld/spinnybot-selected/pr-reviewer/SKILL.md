---
name: pr-reviewer
description: Review a pull request for correctness, regressions, and missing tests. Use when a mid-level developer needs structured review guidance.
---

# PR Reviewer

## When to use
- You need a correctness-first review: behavior changes, regressions, missing tests, unsafe defaults.
- The change touches agent harness boundaries (MCP tools, edit protocols, IO boundaries).

## Inputs to request
- PR diff + context (goal/requirements)
- How to validate locally (tests/smoke)
- Any related incidents/issues

## Workflow
1. Identify behavior changes and risk surfaces.
- API contracts, tool schemas, default settings, auth/network exposure.
2. Check error handling and failure modes.
- Timeouts, retries, partial failures, and user-facing errors.
3. Check tests and validate commands.
- Ensure there’s coverage for the new behavior (and regression for the old bug).
4. Review logging and secrets handling.
- No prompt/secret leakage; logs should be actionable.
5. Review docs.
- README/usage changes match implementation.

## Outputs
- Findings ordered by severity with concrete file references
- Suggested fixes (specific, testable)
- Validation checklist (exact commands)

