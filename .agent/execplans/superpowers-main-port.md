# ExecPlan: Port Superpowers Compatibility to Main Workspace

## Objective
Port the validated superpowers compatibility + context-aware search work from the isolated worktree into `projects/awesome-skills-database` without regressing existing main-workspace features (`verify`, `curate`, `bench`, alias-collapse search).

## Scope
- Add `context-search` support to the existing CLI and DB code paths.
- Add deterministic bounded skill IDs to prevent long filename failures.
- Integrate context-aware retrieval into MCP server path with safe fallback.
- Add/update supporting files:
  - `sources/compat_aliases.json`
  - `sources/context_benchmark_queries.json`
  - `scripts/context_search_smoke.sh`
  - `scripts/bench_context_search.py`
  - `scripts/sync_superpowers_skillpack.sh`
  - `skillpacks/superpowers/*`
- Update docs with compatibility workflow.

## Decisions
- Preserve schema version and quality-score-based ranking in the existing `search` path.
- Keep alias-collapse behavior for `search`; use separate phrase aliases for `context-search`.
- Integrate context-aware ranking as an additive path (`context-search`) rather than replacing existing search behavior.
- Add backward compatibility for older SQLite DBs that do not have `skills.quality_score` by falling back to `worth_score` in query projections.
- Cache parsed compatibility alias rules by file path + stat metadata to reduce per-query overhead in context parsing.

## Progress
- [x] Diffed worktree and main files; identified divergence risks.
- [x] Added `awesome_skills/context.py`.
- [x] Added `context_search_db` and helper logic in `awesome_skills/db.py` while preserving existing alias-collapse search.
- [x] Added `context-search` CLI command in `awesome_skills/cli.py`.
- [x] Added bounded stable IDs in `awesome_skills/util.py`, and wired usage in `condense.py` + `external.py`.
- [x] Added compatibility artifacts, scripts, and vendored superpowers pack.
- [x] Updated README and `skillpacks/README.md`.
- [x] Integrated MCP context-search tool + `strategy=auto|classic|context` in MCP search tool.
- [x] Added schema-compat fallback in `awesome_skills/db.py` so search works with legacy DB files.
- [x] Added alias-rule cache in `awesome_skills/context.py` to speed repeated context queries.
- [x] Run validation commands.
- [x] Record final verification results.

## Validation Commands
1. `python -m py_compile awesome_skills/*.py scripts/bench_context_search.py`
2. `bash scripts/context_search_smoke.sh`
3. `bash scripts/smoke_test.sh`
4. `python -m awesome_skills build --root . --out /tmp/as_ctx_main`
5. `python scripts/bench_context_search.py --db /tmp/as_ctx_main/awesome_skills.sqlite --queries sources/context_benchmark_queries.json --alias-json sources/compat_aliases.json --max-p95-ms 120 --min-hit-at-1 0.5 --min-hit-at-3 0.8`
6. `python -m awesome_skills.mcp_server --skills-json dist/skills.json --db dist/awesome_skills.sqlite --self-test`

## Validation Results
- `python -m py_compile awesome_skills/*.py scripts/bench_context_search.py` ✅
- `bash scripts/context_search_smoke.sh` ✅
  - `context search smoke assertions passed`
  - `context search smoke ok`
- `bash scripts/smoke_test.sh` ✅
  - `smoke ok`
- `python -m awesome_skills build --root . --out /tmp/as_ctx_main` ✅
  - `Indexed 1061 skills into /tmp/as_ctx_main`
- `python scripts/bench_context_search.py ... --max-p95-ms 120 --min-hit-at-1 0.5 --min-hit-at-3 0.8` ✅
  - `hit@1: 0.7000` (dirty local corpus snapshot)
  - `hit@3: 1.0000`
  - `latency_ms: p50=21.170 p95=33.028 max=33.028`
  - `thresholds: PASS`
- `python -m awesome_skills.mcp_server --skills-json dist/skills.json --db dist/awesome_skills.sqlite --self-test` ✅
  - `self_test ok` (confirms legacy-schema fallback path works on this local DB)
- `python -m ruff check awesome_skills scripts/bench_context_search.py` ⚠️
  - unavailable in this environment (`No module named ruff`)
- MCP checks:
  - `python -m awesome_skills.mcp_server --skills-json /tmp/as_ctx_main2/skills.json --db /tmp/as_ctx_main2/awesome_skills.sqlite --self-test` ✅
  - `bash scripts/mcp_context_search_smoke.sh` ✅
  - `python -m awesome_skills verify --skills-json /tmp/as_ctx_main2/skills.json --cards-dir /tmp/as_ctx_main2/cards --readme README.md --mcp-server awesome_skills/mcp_server.py --json` ✅ (`ok=True`, `errors=0`)

## Repro
From repo root:

```bash
python -m py_compile awesome_skills/*.py scripts/bench_context_search.py
bash scripts/context_search_smoke.sh
bash scripts/smoke_test.sh
python -m awesome_skills build --root . --out /tmp/as_ctx_main
python scripts/bench_context_search.py --db /tmp/as_ctx_main/awesome_skills.sqlite --queries sources/context_benchmark_queries.json --alias-json sources/compat_aliases.json --max-p95-ms 120 --min-hit-at-1 0.5 --min-hit-at-3 0.8
```
