# Awesome SKILLS Database

A deterministic, local-first database of `SKILL.md` files.

It:
- discovers skills across one or more roots
- generates condensed “cards” per skill
- builds a SQLite FTS index for fast search
- ranks results with a “worth using” heuristic (not just text match)

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
```

Python (common queries):

```bash
python -m awesome_skills search "ruff"
python -m awesome_skills search "pyright"
python -m awesome_skills search "uv package manager"
python -m awesome_skills search "pytest advanced"
python -m awesome_skills search "polars"
python -m awesome_skills search "duckdb parquet"
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
- The “worth using” score is a heuristic. Treat it as a ranking hint, not truth.

## External Discovery (GitHub + Reddit)

We keep external leads in a committed, human-reviewed list:

- `sources/external_candidates.md`

This keeps the build/search workflow deterministic (no network required), while still enabling deep discovery.

## Optional: Add More Skills (Smithery)

If you want to expand the local corpus, you can install additional skills from Smithery into this workspace, then rebuild.

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
