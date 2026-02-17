#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

OUT_DIR="${OUT_DIR:-.smoke_dist}"

python -m py_compile awesome_skills/*.py

python -m awesome_skills build \
  --root /home/wolvend/codex/agent_playground \
  --root /home/wolvend/.codex/skills \
  --out "$OUT_DIR" >/dev/null

python -m awesome_skills search "mcp server" --db "$OUT_DIR/awesome_skills.sqlite" --limit 5 >/dev/null
python -m awesome_skills search "mcp-builder" --db "$OUT_DIR/awesome_skills.sqlite" --limit 5 >/dev/null
python -m awesome_skills top --db "$OUT_DIR/awesome_skills.sqlite" --limit 5 >/dev/null

echo "smoke ok"
