# security-ownership-map

Analyze git repositories to build a security ownership topology (people-to-file), compute bus factor and sensitive-code ownership, and export CSV/JSON for graph databases and visualization. Trigger only when the user explicitly wants a security-oriented ownership or bus-factor analysis grounded in git history (for example: orphaned sensitive code, security maintainers, CODEOWNERS reality checks...

## Quick Facts
- id: `security-ownership-map--e8f1fa167d`
- worth_using_score: `55/100`
- tags: `github, python, node, security, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/security-ownership-map/SKILL.md`

## Workflow / Steps
- Scope the repo and time window (optional `--since/--until`).
- Decide sensitivity rules (use defaults or provide a CSV config).
- Build the ownership map with `scripts/run_ownership_map.py` (co-change graph is on by default; use `--cochange-max-files` to ignore supernode commits).
- Communities are computed by default; graphml output is optional (`--graphml`).
- Query the outputs with `scripts/query_ownership.py` for bounded JSON slices.
- Persist and visualize (see `references/neo4j-import.md`).
- -repo /path/to/linux \
- -out ownership-map-out \
- -cochange-exclude "**/Kbuild"

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `9`
- has_scripts: `True`
- has_references: `True`
- has_assets: `False`
