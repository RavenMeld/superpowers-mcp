#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

OUT_DIR="${OUT_DIR:-/tmp/awesome-skills-context-smoke}"
rm -rf "$OUT_DIR"

python -m awesome_skills build --root . --out "$OUT_DIR" >/dev/null

Q1_JSON="$OUT_DIR/q1.json"
Q2_JSON="$OUT_DIR/q2.json"

python -m awesome_skills context-search \
  "debug flaky playwright test" \
  --db "$OUT_DIR/awesome_skills.sqlite" \
  --alias-json sources/compat_aliases.json \
  --limit 5 \
  --json > "$Q1_JSON"

python -m awesome_skills context-search \
  "write implementation plan for feature" \
  --db "$OUT_DIR/awesome_skills.sqlite" \
  --alias-json sources/compat_aliases.json \
  --limit 5 \
  --json > "$Q2_JSON"

python - <<'PY'
import json
import os
from pathlib import Path

out_dir = Path(os.environ.get("OUT_DIR", "/tmp/awesome-skills-context-smoke"))
q1 = json.loads((out_dir / "q1.json").read_text(encoding="utf-8"))
q2 = json.loads((out_dir / "q2.json").read_text(encoding="utf-8"))

assert q1["context"]["phase"] == "debug", q1["context"]
assert q2["context"]["phase"] == "plan", q2["context"]

top1 = [r["name"] for r in q1["results"][:3]]
top2 = [r["name"] for r in q2["results"][:3]]

assert "systematic-debugging" in top1, top1
assert "writing-plans" in top2, top2

print("context search smoke assertions passed")
PY

echo "context search smoke ok"
