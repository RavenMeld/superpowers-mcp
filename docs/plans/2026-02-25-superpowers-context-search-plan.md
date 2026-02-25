# Superpowers Compatibility + Context Search Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Make `superpowers` and `awesome_skills` interoperable with a fast, context-aware skill search pipeline that returns execution-ready ranked skills.

**Architecture:** Extend ingestion with compatibility metadata, add a query-context parser, and implement two-stage retrieval/reranking in SQLite+Python. Expose results via a new CLI command (`context-search`) designed for superpowers command hooks.

**Tech Stack:** Python 3.11+, stdlib (`argparse`, `sqlite3`, `json`, `re`), existing `awesome_skills` modules, SQLite FTS5.

---

## Scope and Non-Goals

### In Scope
- Deterministic superpowers skillpack ingestion compatibility.
- Context extraction from user query (phase/domain/tool/risk hints).
- Fast search/rerank path with stable JSON output for agent tooling.
- Local benchmark and acceptance thresholds.

### Out of Scope (Phase 1)
- Online embedding services or external vector DB.
- Full agent runtime changes inside `superpowers` repo.
- Network dependency for indexing/search.

---

## Current Baseline

- `awesome_skills` has:
  - discovery: `awesome_skills/discover.py`
  - record extraction: `awesome_skills/condense.py`
  - scoring: `awesome_skills/scoring.py`
  - search DB: `awesome_skills/db.py`
  - CLI: `awesome_skills/cli.py`
- superpowers snapshot sync exists:
  - `scripts/sync_superpowers_skillpack.sh`
  - `skillpacks/superpowers/`

Gap: Search currently uses plain FTS + worth score only. No context parsing, no phase/tool/domain-aware ranking, no source-priority compatibility policy.

---

## Success Criteria

### Functional
- `python -m awesome_skills context-search "<query>" --json` returns:
  - parsed context
  - ranked results with `why_selected`, `confidence`, `alternatives`
- Queries like "debug flaky playwright test" prioritize debugging + playwright skills over generic matches.
- Queries like "plan a feature" prioritize process skills (`brainstorming`, `writing-plans`) by phase.

### Performance
- Local p95 latency <= 120 ms for `context-search` on repo-contained corpus (`--root .`).
- Candidate retrieval path remains offline/local and deterministic.

### Quality
- Deterministic ordering for equal scores.
- No regressions for existing `search`, `top`, and `show` commands.

---

## Data Model Changes

Add metadata fields to `SkillRecord` (`awesome_skills/condense.py`):
- `source_kind: str` (`core|superpowers|local|external`)
- `canonical_name: str`
- `alias_of: str` (empty if canonical)
- `phases: list[str]` (`brainstorm|plan|implement|debug|review|ship|meta`)
- `tools: list[str]` (detected from text)
- `domains: list[str]` (language/platform domains)
- `risk_level: str` (`low|medium|high`)
- `quality_score: int` (separate from worth)

DB schema bump (`awesome_skills/db.py`):
- increment `SCHEMA_VERSION` to `2`
- add columns for above metadata (JSON text where list)
- maintain backward-compatible `search_db` behavior

---

## Ranking Strategy (Context-Aware)

## Stage 1: Candidate Retrieval
- FTS5 query from normalized tokens.
- hard filters (optional):
  - phase filter when explicit (`debug`, `plan`, etc.)
  - tool filter when explicit (`playwright`, `mcp`, `docker`, etc.)

## Stage 2: Rerank
Composite score:
- `fts_score` (existing)
- `worth_score`
- `quality_score`
- `phase_match_bonus`
- `tool_match_bonus`
- `domain_match_bonus`
- `source_priority_bonus` (prefer `superpowers` for process skills)
- `exact_name/prefix bonus`

Return each result with:
- `score_breakdown`
- `why_selected` (short deterministic reason string)
- `confidence` (0-1 bounded heuristic)

---

## Compatibility Policy

Define precedence policy in new module `awesome_skills/compat.py`:
- Process-skill names (`brainstorming`, `writing-plans`, etc.):
  - prefer `source_kind=superpowers` when present
- Domain/local skills:
  - prefer `source_kind=local`
- External candidates:
  - never outrank direct local/superpowers exact matches

Provide alias-canonicalization map in deterministic local file:
- `sources/compat_aliases.json`

---

## CLI/API Surface

Add command to `awesome_skills/cli.py`:
- `context-search`

Example:
```bash
python -m awesome_skills context-search "debug flaky playwright test" --db dist/awesome_skills.sqlite --limit 5 --json
```

JSON shape:
- `query`
- `context`
- `results[]` with `id,name,score,confidence,why_selected,score_breakdown`
- `alternatives[]`

---

## Implementation Tasks

### Task 1: Add Context Parser

**Files:**
- Create: `awesome_skills/context.py`
- Modify: `awesome_skills/util.py`
- Test: `scripts/context_search_smoke.sh`

**Step 1: Write failing test harness (smoke)**
- Add shell assertions for parsing representative queries.

**Step 2: Implement parser**
- Extract phase/tool/domain/risk hints using deterministic rules.

**Step 3: Verify parser outputs**
Run:
```bash
python - <<'PY'
from awesome_skills.context import parse_query_context
print(parse_query_context('debug flaky playwright test'))
PY
```
Expected: phase includes `debug`; tools includes `playwright`.

**Step 4: Commit**
```bash
git add awesome_skills/context.py awesome_skills/util.py scripts/context_search_smoke.sh
git commit -m "feat: add deterministic query context parser"
```

### Task 2: Extend SkillRecord Metadata

**Files:**
- Modify: `awesome_skills/condense.py`
- Modify: `awesome_skills/scoring.py`
- Test: `scripts/context_search_smoke.sh`

**Step 1: Add new record fields + heuristics**
- populate `source_kind/phases/tools/domains/risk_level/quality_score`.

**Step 2: Build and inspect record output**
Run:
```bash
python -m awesome_skills build --root . --out /tmp/as_ctx
python - <<'PY'
import json
p='/tmp/as_ctx/skills.json'
d=json.load(open(p))
print(d['skills'][0].keys())
PY
```
Expected: new metadata fields present.

**Step 3: Commit**
```bash
git add awesome_skills/condense.py awesome_skills/scoring.py
git commit -m "feat: add compatibility metadata to skill records"
```

### Task 3: DB Schema V2 + Context Search Engine

**Files:**
- Modify: `awesome_skills/db.py`
- Create: `awesome_skills/compat.py`
- Test: `scripts/context_search_smoke.sh`

**Step 1: Add schema v2 columns + serialization**
- store metadata fields in `skills` table.

**Step 2: Implement `context_search_db(...)`**
- stage-1 FTS candidates, stage-2 rerank with score breakdown.

**Step 3: Verify deterministic ordering**
Run same query twice and compare ordered IDs.

**Step 4: Commit**
```bash
git add awesome_skills/db.py awesome_skills/compat.py
git commit -m "feat: add schema v2 and context-aware search ranking"
```

### Task 4: CLI Command and JSON Contract

**Files:**
- Modify: `awesome_skills/cli.py`
- Modify: `README.md`
- Test: `scripts/context_search_smoke.sh`

**Step 1: add `context-search` subcommand**
- support `--db`, `--limit`, `--json`.

**Step 2: document command with examples**
- include process and debugging examples.

**Step 3: verify CLI behavior**
Run:
```bash
python -m awesome_skills context-search "plan a new feature" --db /tmp/as_ctx/awesome_skills.sqlite --json
python -m awesome_skills context-search "debug flaky playwright test" --db /tmp/as_ctx/awesome_skills.sqlite --json
```
Expected: process/debug specific top results.

**Step 4: Commit**
```bash
git add awesome_skills/cli.py README.md scripts/context_search_smoke.sh
git commit -m "feat: expose context-search CLI with stable json output"
```

### Task 5: Compatibility Alias Policy

**Files:**
- Create: `sources/compat_aliases.json`
- Modify: `awesome_skills/compat.py`
- Modify: `README.md`

**Step 1: seed alias map for core process skills**
- canonicalize known superpowers process skill names.

**Step 2: apply source-priority logic**
- process -> superpowers preferred; others balanced.

**Step 3: verify behavior**
Run:
```bash
python -m awesome_skills context-search "write implementation plan" --db /tmp/as_ctx/awesome_skills.sqlite --json
```
Expected: `writing-plans` from superpowers snapshot appears first.

**Step 4: Commit**
```bash
git add sources/compat_aliases.json awesome_skills/compat.py README.md
git commit -m "feat: add compatibility alias map and source priority policy"
```

### Task 6: Benchmarks, Quality Gates, and Rollout

**Files:**
- Create: `scripts/bench_context_search.py`
- Create: `sources/context_benchmark_queries.json`
- Modify: `scripts/smoke_test.sh`
- Modify: `README.md`

**Step 1: benchmark harness**
- measure p50/p95 latency and top-k relevance heuristics.

**Step 2: add gate thresholds**
- fail if p95 > 120ms or relevance drops below baseline.

**Step 3: run full local validation**
Run:
```bash
python -m py_compile awesome_skills/*.py
python -m awesome_skills build --root . --out /tmp/as_ctx
bash scripts/context_search_smoke.sh
python scripts/bench_context_search.py --db /tmp/as_ctx/awesome_skills.sqlite --queries sources/context_benchmark_queries.json
```
Expected: all pass; benchmark prints machine-readable JSON + concise summary.

**Step 4: Commit**
```bash
git add scripts/bench_context_search.py sources/context_benchmark_queries.json scripts/smoke_test.sh README.md
git commit -m "test: add context search benchmarks and quality gates"
```

---

## Rollout Plan

1. Land metadata + parser + context-search behind a flag (`--context-ranking-v2` optional flag in first release).
2. Compare old `search` vs `context-search` on benchmark set.
3. Make `context-search` default for superpowers integration once thresholds are stable.
4. Keep legacy `search` command untouched for backward compatibility.

---

## Risks and Mitigations

- Risk: false-positive phase/tool extraction.
  - Mitigation: keep parser deterministic and conservative; expose parsed context in output.
- Risk: score instability.
  - Mitigation: deterministic tie-break by `(score desc, name asc, id asc)`.
- Risk: schema migration breakage.
  - Mitigation: DB rebuild is already standard; bump schema and regenerate in build step.
- Risk: long card filename edge case in full workspace smoke.
  - Mitigation: track separately; consider stable shortened filename policy in follow-up.

---

## Handoff

Plan complete and saved to `docs/plans/2026-02-25-superpowers-context-search-plan.md`.

Execution options:

1. Subagent-Driven (this session): implement tasks sequentially with review checkpoints.
2. Parallel Session: open new execution session focused only on this plan.
