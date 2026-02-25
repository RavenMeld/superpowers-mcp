# ExecPlan: Superpowers Compatibility + Context Search

## Objective
Implement an interoperable, fast, context-aware skill search path so superpowers workflows can consume ranked skills from awesome_skills with deterministic local behavior.

## Progress
- [x] Requirements reviewed.
- [x] Baseline architecture and task decomposition drafted.
- [x] Implementation plan written to docs/plans.
- [x] Execution started.
- [x] Added context parser and compatibility helpers (`awesome_skills/context.py`).
- [x] Added context-aware search + source-priority policy (`awesome_skills/db.py`).
- [x] Added CLI command (`awesome_skills context-search`) (`awesome_skills/cli.py`).
- [x] Added alias map (`sources/compat_aliases.json`).
- [x] Added targeted smoke check (`scripts/context_search_smoke.sh`).
- [x] Added benchmark harness + starter query corpus (`scripts/bench_context_search.py`, `sources/context_benchmark_queries.json`).
- [x] Added bounded deterministic skill id generation to avoid long card filename failures.

## Decisions
- Keep search local-first (SQLite FTS + deterministic Python rerank).
- Preserve backward compatibility by adding `context-search` instead of replacing `search` initially.
- Encode compatibility policy in code (source priority + aliases), not ad-hoc docs only.

## Validation Plan
- Unit/smoke checks for context parser.
- Context-search relevance checks for representative process/debug queries.
- Latency benchmark with p95 gate.

## Validation Results
- `python -m py_compile awesome_skills/*.py` ✅
- `scripts/context_search_smoke.sh` ✅
- `python -m awesome_skills context-search "debug flaky playwright test" ...` ✅
- `python -m awesome_skills context-search "write implementation plan for feature" ...` ✅
- `scripts/smoke_test.sh` ✅
- `python scripts/bench_context_search.py --db /tmp/awesome-skills-context-smoke/awesome_skills.sqlite --queries sources/context_benchmark_queries.json --alias-json sources/compat_aliases.json --max-p95-ms 120 --min-hit-at-1 0.5 --min-hit-at-3 0.8` ✅
  - summary: hit@1=1.0, hit@3=1.0, p50≈4.1ms, p95≈8.1ms
- `python -m ruff check ...` ⚠️ not runnable in current env (`No module named ruff`)

## Artifacts
- Plan document: `docs/plans/2026-02-25-superpowers-context-search-plan.md`
