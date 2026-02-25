# Awesome SKILLS Database

A deterministic, local-first database of `SKILL.md` files.

It:
- discovers skills across one or more roots
- generates condensed “cards” per skill
- builds a SQLite FTS index for fast search
- ranks results with blended `worth_score` + `quality_score` (not just text match)
- collapses alias-equivalent duplicate names to canonical skills (optional)

## Quickstart (this machine)

Build from the two common roots in this workspace:

```bash
cd projects/awesome-skills-database
python -m awesome_skills build \
  --root /home/wolvend/codex/agent_playground \
  --root /home/wolvend/.codex/skills \
  --root /home/wolvend/.agents/skills
```

## Repo-Contained Skill Packs (Shareable)

This repo also ships `skillpacks/` (additional `SKILL.md` folders intended to be checked in and shared).

To sync a vendored superpowers snapshot into this repo:

```bash
bash scripts/sync_superpowers_skillpack.sh
```

To build a database from *only* this repo (portable, no absolute `~/.codex/...` paths):

```bash
cd projects/awesome-skills-database
python -m awesome_skills build --root .
```

Search:

```bash
python -m awesome_skills search "mcp server"
python -m awesome_skills search "write a professional email"
python -m awesome_skills search "playwright e2e test"
python -m awesome_skills search "playwright e2e test" --alias-json dist/name_aliases.json
python -m awesome_skills search "playwright e2e test" --no-alias-collapse
python -m awesome_skills context-search "debug flaky playwright test"
python -m awesome_skills context-search "write implementation plan for feature" --json
```

`context-search` adds context-aware ranking with:
- phase fast-lane filtering for strong intents (`debug`, `plan`, `review`)
- phrase aliases from `sources/compat_aliases.json`
- source-priority policy:
  - process/workflow skills prefer `skillpacks/superpowers`
  - domain skills prefer local skillpacks

Stats (corpus summary):

```bash
python -m awesome_skills stats
python -m awesome_skills stats --json
```

Verify generated artifacts and MCP safety/docs policy:

```bash
python -m awesome_skills verify
python -m awesome_skills verify --strict
python -m awesome_skills verify --json
```

Curate artifacts (fills missing MCP guidance, patches card score markers, emits alias metadata):

```bash
python -m awesome_skills curate --skills-json dist/skills.json --cards-dir dist/cards --aliases-json dist/name_aliases.json
python -m awesome_skills curate --skills-json dist/skills.json --cards-dir dist/cards --aliases-json dist/name_aliases.json --write
python -m awesome_skills curate --skills-json dist/skills.json --cards-dir dist/cards --aliases-json dist/name_aliases.json --fix-level aggressive --write
```

Benchmark retrieval quality:

```bash
python -m awesome_skills bench --db dist/awesome_skills.sqlite --skills-json dist/skills.json --benchmark sources/benchmark_queries.json --alias-json dist/name_aliases.json
python -m awesome_skills bench --db dist/awesome_skills.sqlite --skills-json dist/skills.json --benchmark sources/benchmark_queries.json --alias-json dist/name_aliases.json --min-hit-rate 0.50 --min-mrr 0.45 --min-ndcg 0.50
python scripts/bench_context_search.py --db dist/awesome_skills.sqlite --queries sources/context_benchmark_queries.json --alias-json sources/compat_aliases.json
```

MCP context-routing smoke:

```bash
bash scripts/mcp_context_search_smoke.sh
```

Recommended quality gate sequence:

```bash
python -m awesome_skills curate --skills-json dist/skills.json --cards-dir dist/cards --aliases-json dist/name_aliases.json --fix-level aggressive --write
python -m awesome_skills bench --db dist/awesome_skills.sqlite --skills-json dist/skills.json --benchmark sources/benchmark_queries.json --alias-json dist/name_aliases.json --min-hit-rate 0.50 --min-mrr 0.45 --min-ndcg 0.50
python -m awesome_skills verify --skills-json dist/skills.json --cards-dir dist/cards --alias-json dist/name_aliases.json --strict
```

Invent novel skills from corpus gaps:

```bash
python -m awesome_skills invent --skills-json dist/skills.json --limit 20
python -m awesome_skills invent --skills-json dist/skills.json --exclude-domain hytale --limit 20
python -m awesome_skills invent --skills-json dist/skills.json --limit 10 --write --out-dir skillpacks/novel-synthesized
```

How `invent` works (deterministic, local):
- reverse-engineers domain/action coverage from existing `skills.json` records
- identifies under-covered domain-action combinations
- identifies cross-domain bridge opportunities with low current co-occurrence
- ranks proposals by novelty + practical coverage gap
- optionally writes ready-to-edit `SKILL.md` stubs

## MCP Server (Smart Invent + Search)

Run an MCP stdio server for `awesome_skills`:

```bash
cd projects/awesome-skills-database
python -m awesome_skills.mcp_server --skills-json dist/skills.json --db dist/awesome_skills.sqlite
```

Enable write tools safely (allowlist + explicit confirm token):

```bash
python -m awesome_skills.mcp_server \
  --skills-json dist/skills.json \
  --db dist/awesome_skills.sqlite \
  --allow-write-tools \
  --write-root "$(pwd)/skillpacks" \
  --write-root /tmp
```

Alternative launcher:

```bash
python scripts/awesome_skills_mcp_server.py --skills-json dist/skills.json --db dist/awesome_skills.sqlite
```

Self-test:

```bash
python -m awesome_skills.mcp_server --skills-json dist/skills.json --db dist/awesome_skills.sqlite --self-test
```

Write policy summary:
- `awesome_skills_invent_write` is blocked unless `--allow-write-tools` is set.
- write paths are restricted to `--write-root` values (defaults: current directory + `/tmp`).
- write calls require `confirm: "ALLOW_WRITE"` unless `--disable-write-confirm-token` is set.

### MCP Tool Schemas + Copy/Paste Examples

Tool: `awesome_skills_invent`
- Input: `{ skills_json?: string, limit?: integer, exclude_domains?: string[] }`

Example 1:
```json
{"limit": 12}
```

Example 2:
```json
{"skills_json":"dist/skills.json","limit":20,"exclude_domains":["hytale"]}
```

Example 3:
```json
{"skills_json":"/home/wolvend/codex/agent_playground/projects/awesome-skills-database/dist/skills.json","limit":8,"exclude_domains":["hytale","comfyui"]}
```

Tool: `awesome_skills_invent_write`
- Input: `{ out_dir: string, confirm?: string, skills_json?: string, limit?: integer, exclude_domains?: string[] }`

Example 1:
```json
{"out_dir":"skillpacks/novel-synthesized","confirm":"ALLOW_WRITE","limit":10}
```

Example 2:
```json
{"skills_json":"dist/skills.json","out_dir":"skillpacks/novel-synthesized","confirm":"ALLOW_WRITE","limit":12,"exclude_domains":["hytale"]}
```

Example 3:
```json
{"skills_json":"dist/skills.json","out_dir":"/tmp/novel-pack","confirm":"ALLOW_WRITE","limit":5,"exclude_domains":["hytale","browser"]}
```

Tool: `awesome_skills_search`
- Input: `{ query: string, limit?: integer, db_path?: string, alias_json?: string, collapse_aliases?: boolean, strategy?: "auto"|"classic"|"context" }`

Example 1:
```json
{"query":"playwright visual regression","limit":8}
```

Example 2:
```json
{"query":"wsl dns hardening","db_path":"dist/awesome_skills.sqlite","limit":10}
```

Example 3:
```json
{"query":"mcp contract fuzzing","db_path":"/home/wolvend/codex/agent_playground/projects/awesome-skills-database/dist/awesome_skills.sqlite","limit":6}
```

Example 4:
```json
{"query":"debug flaky playwright test","strategy":"auto","limit":5}
```

Tool: `awesome_skills_context_search`
- Input: `{ query: string, limit?: integer, db_path?: string, alias_json?: string }`

Example 1:
```json
{"query":"debug flaky playwright test","limit":5}
```

Example 2:
```json
{"query":"write implementation plan for feature","db_path":"dist/awesome_skills.sqlite","alias_json":"sources/compat_aliases.json","limit":5}
```

Example 3:
```json
{"query":"review this pr","db_path":"/home/wolvend/codex/agent_playground/projects/awesome-skills-database/dist/awesome_skills.sqlite","alias_json":"/home/wolvend/codex/agent_playground/projects/awesome-skills-database/sources/compat_aliases.json","limit":8}
```

Tool: `awesome_skills verify`
- Quality checks are alias-aware when `dist/name_aliases.json` exists.
- You can force alias path with `--alias-json`.

Tool: `awesome_skills curate`
- Output: machine-readable curation report + optional persisted updates with `--write`.
- Supports `--fix-level safe|aggressive`.
- Writes/updates:
  - `skills.json` curation metadata
  - `cards/*.md` score markers where missing
  - `name_aliases.json` duplicate-name canonicalization manifest

Python (common queries):

```bash
python -m awesome_skills search "ruff"
python -m awesome_skills search "pyright"
python -m awesome_skills search "uv package manager"
python -m awesome_skills search "pytest advanced"
python -m awesome_skills search "polars"
python -m awesome_skills search "duckdb parquet"
```

Windows/WSL + Tools (common queries):

```bash
python -m awesome_skills search "wsl ssh"
python -m awesome_skills search "powershell"
python -m awesome_skills search "cursor rules"
python -m awesome_skills search "warp terminal"
python -m awesome_skills search "chrome devtools"
python -m awesome_skills search "firefox automation"
python -m awesome_skills search "hytale modding"
```

Show a specific skill card:

```bash
python -m awesome_skills show mcp-builder--<hash>
```

## Outputs

Generated outputs land in `dist/`:
- `dist/skills.json` (metadata + scoring)
- `dist/cards/*.md` (condensed cards)
- `dist/awesome_skills.sqlite` (SQLite + FTS index)
- `dist/AWESOME_SKILLS.md` (browse by tag + top “worth using”)

Convenience:
- `AWESOME_SKILLS.md` (links into `dist/cards/*`)

## Notes

- No network calls.
- Condensation is extractive and heuristic (reproducible), not LLM-generated.
- `worth_score` and `quality_score` are heuristics. Treat them as ranking hints, not truth.
- `verify --strict` exits `1` when warnings exist (expected behavior).
- CI runs strict verify in warning-tolerant mode for now (`exit 1` from warnings is surfaced as a notice).

## External Discovery (GitHub + Reddit)

We keep external leads in a committed, human-reviewed list:

- `sources/external_candidates.md`

This keeps the build/search workflow deterministic (no network required), while still enabling deep discovery.

## Optional: Add More Skills (Smithery)

If you want to expand the local corpus, you can install additional skills from Smithery into this workspace, then rebuild.

See `sources/smithery_seed_installs.md` for a curated batch that matches common RavenMeld workflows (WSL/Windows, browsers, Playwright, Obsidian, Hytale, PowerShell).

Example:

```bash
cd /home/wolvend/codex/agent_playground
smithery skills search "mcp" --limit 10
smithery skills install -a codex mrgoonie/mcp-management
# Or install "globally" (lands in ~/.agents/skills, which is indexed by default).
smithery skills install -a codex -g mrgoonie/mcp-management

cd projects/awesome-skills-database
python -m awesome_skills build \
  --root /home/wolvend/codex/agent_playground \
  --root /home/wolvend/.codex/skills \
  --root /home/wolvend/.agents/skills
```

Security note: always inspect installed skills before use; they can include scripts that run with agent permissions.

## Mega Essentials Pack (Local, No Network)

To quickly expand the database with a broad, practical baseline, this repo includes a generated pack:

- `skillpacks/ravenmeld/mega-essentials/`

Generation is reproducible via:

```bash
cd projects/awesome-skills-database
python scripts/generate_mega_essentials.py
```

Then rebuild:

```bash
python -m awesome_skills build \
  --root /home/wolvend/codex/agent_playground \
  --root /home/wolvend/.codex/skills \
  --root /home/wolvend/.agents/skills
```

Current coverage focus includes Python, TypeScript, infra/devops, security, MCP/LLM engineering, Obsidian, browser QA/devtools, and Hytale/content pipelines.

## Quality Expert Pack (Curated, Local)

For higher-signal, domain-specific playbooks, this repo also includes:

- `skillpacks/ravenmeld/quality-expert/`

Generate/update it with:

```bash
cd projects/awesome-skills-database
python scripts/generate_quality_expert_pack.py
```

This pack emphasizes practical quality over volume: Python niches, data/ML engineering, Linux/Windows/WSL operations, Playwright/browser forensics, Obsidian/Cursor/Warp workflows, Hytale/Hyimporter/Blockbench pipelines, security hardening, and CI/CD reliability.

## Targeted Non-Hytale Pack

For exact-name, high-priority skills requested for agent/platform operations (excluding Hytale-specific entries), use:

- `skillpacks/ravenmeld/targeted-non-hytale/`

Generate/update with:

```bash
cd projects/awesome-skills-database
python scripts/generate_targeted_non_hytale_pack.py
```
