# ExecPlan: MCP Context Search Integration

## Objective
Expose context-aware search through the MCP server so downstream agents can consume phase/tool/source-priority ranking, not only plain FTS search.

## Scope
- Add MCP tool spec + handler for `awesome_skills_context_search`.
- Keep existing `awesome_skills_search` behavior unchanged.
- Add optional `strategy=auto|classic|context` routing to `awesome_skills_search`.
- Extend self-test with context-search assertions.
- Update verification checks and README MCP tool documentation.

## Decisions
- Additive integration only: no breaking changes to existing MCP tool names.
- Default alias map for context tool points to `sources/compat_aliases.json` when present.
- Keep structured error behavior identical to existing tool handlers.

## Progress
- [x] Inspect current MCP tool registry and handlers.
- [x] Add tool spec and server dispatch.
- [x] Implement `_tool_context_search`.
- [x] Add `strategy=auto|classic|context` routing to existing `awesome_skills_search`.
- [x] Update self-test for new tool.
- [x] Update verify policy expectations.
- [x] Update README MCP tool section with examples.
- [x] Run validation and record results.

## Validation Commands
1. `python -m py_compile awesome_skills/*.py`
2. `python -m awesome_skills.mcp_server --skills-json dist/skills.json --db dist/awesome_skills.sqlite --self-test`
3. `bash scripts/smoke_test.sh`
4. `bash scripts/mcp_context_search_smoke.sh`

## Validation Results
- `python -m py_compile awesome_skills/*.py scripts/bench_context_search.py` ✅
- `python -m awesome_skills.mcp_server --skills-json /tmp/as_ctx_main/skills.json --db /tmp/as_ctx_main/awesome_skills.sqlite --self-test` ✅
  - output: `self_test ok`
- `bash scripts/smoke_test.sh` ✅
  - output: `smoke ok`
- `bash scripts/mcp_context_search_smoke.sh` ✅
  - output: `mcp context search smoke assertions passed`
  - output: `mcp context search smoke ok`
  - covers `strategy=classic`, `strategy=auto`, and `strategy=context`
- `python scripts/bench_context_search.py --db /tmp/as_ctx_main/awesome_skills.sqlite --queries sources/context_benchmark_queries.json --alias-json sources/compat_aliases.json --max-p95-ms 120 --min-hit-at-1 0.5 --min-hit-at-3 0.8` ✅
  - `hit@1: 1.0000`
  - `hit@3: 1.0000`
  - `latency_ms: p50=19.383 p95=30.095 max=30.095`
- `bash scripts/sync_superpowers_skillpack.sh` ✅
  - source commit: `e16d611eee14ac4c3253b4bf4c55a98d905c2e64`
- `python -m awesome_skills build --root . --out /tmp/as_ctx_main2` ✅
  - output: `Indexed 1073 skills into /tmp/as_ctx_main2`
- `python -m awesome_skills.mcp_server --skills-json /tmp/as_ctx_main2/skills.json --db /tmp/as_ctx_main2/awesome_skills.sqlite --self-test` ✅
- `python -m awesome_skills verify --skills-json /tmp/as_ctx_main2/skills.json --cards-dir /tmp/as_ctx_main2/cards --readme README.md --mcp-server awesome_skills/mcp_server.py --json` ✅
  - `ok=True`, `errors=0` (warnings remain non-critical and pre-existing category checks)
- behavioral check:
  - query: `triage CI failure`
  - `strategy=auto` top1: `ci-failure-triage`
  - `strategy=classic` top1: `linux-journald-triage-playbook`
