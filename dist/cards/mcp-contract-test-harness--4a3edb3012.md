# mcp-contract-test-harness

Validate MCP tools against contract expectations: schema compliance, deterministic error codes, and retry behavior.

## Quick Facts
- id: `mcp-contract-test-harness--4a3edb3012`
- worth_using_score: `60/100`
- tags: `mcp, python, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/mcp-contract-test-harness/SKILL.md`

## Use When
- You maintain MCP servers/tools with multiple clients.
- Tool calls fail due to schema drift or error-shape mismatch.
- You need regression tests for tool interface contracts.

## Workflow / Steps
- Define contract cases for success and known failures.
- Validate argument schema and output shape per tool.
- Verify stable error codes/messages for common failures.
- Check retry/idempotency behavior for transient faults.
- Run harness in CI on contract-sensitive changes.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
