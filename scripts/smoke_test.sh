#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

OUT_DIR="${OUT_DIR:-.smoke_dist}"

python -m py_compile awesome_skills/*.py

python -m awesome_skills build \
  --root /home/wolvend/codex/agent_playground \
  --root /home/wolvend/.codex/skills \
  --root /home/wolvend/.agents/skills \
  --out "$OUT_DIR" >/dev/null

python - <<PY
import json
from pathlib import Path

p = Path("$OUT_DIR") / "skills.json"
data = json.loads(p.read_text(encoding="utf-8"))
skills = data.get("skills", [])
assert isinstance(skills, list) and skills, "skills.json missing skills[]"

# Ensure block-scalar frontmatter gets parsed (description: | ...).
python_skill = None
for s in skills:
    if s.get("source_path") == "/home/wolvend/.codex/skills/python/SKILL.md":
        python_skill = s
        break
assert python_skill is not None, "expected python SKILL.md to be indexed"
assert python_skill.get("description") not in (None, "", "|"), f"bad description: {python_skill.get('description')!r}"
assert int(python_skill.get("features", {}).get("word_count", 0)) > 0, "word_count should be > 0"

# Ensure word_count isn't broken across the corpus.
nonzero = sum(1 for s in skills if int(s.get("features", {}).get("word_count", 0)) > 0)
assert nonzero >= 100, f"expected many skills to have word_count > 0, got {nonzero}"
PY

python -m awesome_skills search "mcp server" --db "$OUT_DIR/awesome_skills.sqlite" --limit 5 >/dev/null
python -m awesome_skills search "mcp-builder" --db "$OUT_DIR/awesome_skills.sqlite" --limit 5 >/dev/null
python -m awesome_skills top --db "$OUT_DIR/awesome_skills.sqlite" --limit 5 >/dev/null

echo "smoke ok"
