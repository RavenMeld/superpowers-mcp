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
  --root /home/wolvend/.codex/skills
```

Search:

```bash
python -m awesome_skills search "mcp server"
python -m awesome_skills search "write a professional email"
python -m awesome_skills search "playwright e2e test"
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
