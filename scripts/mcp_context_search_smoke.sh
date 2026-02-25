#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

OUT_DIR="${OUT_DIR:-/tmp/awesome-skills-mcp-context-smoke}"
rm -rf "$OUT_DIR"

python -m awesome_skills build --root . --out "$OUT_DIR" >/dev/null

python - <<'PY'
from pathlib import Path

from awesome_skills.mcp_server import AwesomeSkillsMCPServer

out_dir = Path("/tmp/awesome-skills-mcp-context-smoke")
server = AwesomeSkillsMCPServer(
    skills_json=out_dir / "skills.json",
    db_path=out_dir / "awesome_skills.sqlite",
)

classic = server._tool_search(
    {
        "query": "playwright",
        "limit": 3,
        "strategy": "classic",
        "db_path": str(out_dir / "awesome_skills.sqlite"),
    }
)
assert classic["mode_used"] == "classic", classic
assert classic["count"] > 0, classic

auto = server._tool_search(
    {
        "query": "debug flaky playwright test",
        "limit": 3,
        "strategy": "auto",
        "db_path": str(out_dir / "awesome_skills.sqlite"),
    }
)
assert auto["mode_used"] == "context", auto
assert auto["context"]["phase"] == "debug", auto["context"]
assert auto["count"] > 0, auto

forced = server._tool_search(
    {
        "query": "review this pr",
        "limit": 3,
        "strategy": "context",
        "db_path": str(out_dir / "awesome_skills.sqlite"),
    }
)
assert forced["mode_used"] == "context", forced
assert forced["count"] > 0, forced

direct = server._tool_context_search(
    {
        "query": "write implementation plan for feature",
        "limit": 3,
        "db_path": str(out_dir / "awesome_skills.sqlite"),
        "alias_json": str(Path("sources/compat_aliases.json").resolve()),
    }
)
assert direct["context"]["phase"] == "plan", direct["context"]
assert direct["count"] > 0, direct
assert "score" in direct["results"][0], direct["results"][0]

print("mcp context search smoke assertions passed")
PY

echo "mcp context search smoke ok"
