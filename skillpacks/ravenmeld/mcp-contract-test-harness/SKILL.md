---
name: mcp-contract-test-harness
description: |
  Validate MCP tools against contract expectations: schema compliance, deterministic error codes, and retry behavior.
---

# MCP Contract Test Harness

## Use When

- You maintain MCP servers/tools with multiple clients.
- Tool calls fail due to schema drift or error-shape mismatch.
- You need regression tests for tool interface contracts.

## Workflow

1. Define contract cases for success and known failures.
2. Validate argument schema and output shape per tool.
3. Verify stable error codes/messages for common failures.
4. Check retry/idempotency behavior for transient faults.
5. Run harness in CI on contract-sensitive changes.

## Copy/Paste Examples

```bash
codex mcp list
```

```bash
python -m awesome_skills search "mcp contract"
```

```bash
rg -n "ANCHOR_MISMATCH|DB_MISSING|POLICY_BLOCKED" -S .
```

## Contract Rules

- Prefer machine-readable error codes over free-text only.
- Keep backward-compatible fields stable across versions.
- Add test vectors for every newly introduced tool.

## Safety Notes

- Never include secrets in contract fixtures.
- Treat contract breaks as release-blocking for shared tools.
