# pr-reviewer

Review a pull request for correctness, regressions, and missing tests. Use when a mid-level developer needs structured review guidance.

## Quick Facts
- id: `pr-reviewer--163c01f10a`
- worth_using_score: `45/100`
- tags: `mcp, go, ci, docs, rag`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/frameworks/Spinnybot/skills-selected/pr-reviewer/SKILL.md`

## Use When
- You need a correctness-first review: behavior changes, regressions, missing tests, unsafe defaults.
- The change touches agent harness boundaries (MCP tools, edit protocols, IO boundaries).

## Workflow / Steps
- Identify behavior changes and risk surfaces.
- API contracts, tool schemas, default settings, auth/network exposure.
- Check error handling and failure modes.
- Timeouts, retries, partial failures, and user-facing errors.
- Check tests and validate commands.
- Ensure there’s coverage for the new behavior (and regression for the old bug).
- Review logging and secrets handling.
- No prompt/secret leakage; logs should be actionable.
- Review docs.
- README/usage changes match implementation.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
