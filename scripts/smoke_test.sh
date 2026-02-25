#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd -P)"
cd "$REPO_ROOT"

OUT_DIR="${OUT_DIR:-.smoke_dist}"

build_roots=("$REPO_ROOT")
for candidate in \
  "/home/wolvend/codex/agent_playground" \
  "/home/wolvend/.codex/skills" \
  "/home/wolvend/.agents/skills"; do
  if [[ -d "$candidate" ]]; then
    already=0
    for existing in "${build_roots[@]}"; do
      if [[ "$existing" == "$candidate" ]]; then
        already=1
        break
      fi
    done
    if [[ "$already" -eq 0 ]]; then
      build_roots+=("$candidate")
    fi
  fi
done

python -m py_compile awesome_skills/*.py

build_args=()
for root in "${build_roots[@]}"; do
  build_args+=(--root "$root")
done

python -m awesome_skills build \
  "${build_args[@]}" \
  --out "$OUT_DIR" >/dev/null

python - <<PY
import json
from pathlib import Path

p = Path("$OUT_DIR") / "skills.json"
data = json.loads(p.read_text(encoding="utf-8"))
skills = data.get("skills", [])
assert isinstance(skills, list) and skills, "skills.json missing skills[]"

# Ensure critical scoring fields exist and are in range.
for s in skills:
    q = int(s.get("quality_score", -1))
    w = int(s.get("worth_score", -1))
    assert 0 <= q <= 100, f"quality_score out of range for {s.get('id')}: {q}"
    assert 0 <= w <= 100, f"worth_score out of range for {s.get('id')}: {w}"

# Ensure word_count isn't broken across the corpus.
nonzero = sum(1 for s in skills if int(s.get("features", {}).get("word_count", 0)) > 0)
assert nonzero >= 20, f"expected many skills to have word_count > 0, got {nonzero}"
PY

python -m awesome_skills search "mcp server" --db "$OUT_DIR/awesome_skills.sqlite" --limit 5 --alias-json "$OUT_DIR/name_aliases.json" >/dev/null
python -m awesome_skills search "mcp-builder" --db "$OUT_DIR/awesome_skills.sqlite" --limit 5 --alias-json "$OUT_DIR/name_aliases.json" >/dev/null
python -m awesome_skills context-search \
  "debug flaky playwright test" \
  --db "$OUT_DIR/awesome_skills.sqlite" \
  --alias-json sources/compat_aliases.json \
  --limit 5 >/dev/null
python -m awesome_skills top --db "$OUT_DIR/awesome_skills.sqlite" --limit 5 >/dev/null
python -m awesome_skills invent --skills-json "$OUT_DIR/skills.json" --limit 5 >/dev/null
python -m awesome_skills invent --skills-json "$OUT_DIR/skills.json" --limit 2 --write --out-dir "$OUT_DIR/novel" >/dev/null
python -m awesome_skills curate \
  --skills-json "$OUT_DIR/skills.json" \
  --cards-dir "$OUT_DIR/cards" \
  --aliases-json "$OUT_DIR/name_aliases.json" \
  --fix-level aggressive \
  --write >/dev/null
set +e
python -m awesome_skills verify \
  --skills-json "$OUT_DIR/skills.json" \
  --cards-dir "$OUT_DIR/cards" \
  --alias-json "$OUT_DIR/name_aliases.json" \
  --readme README.md \
  --mcp-server awesome_skills/mcp_server.py \
  --strict >/dev/null
strict_rc=$?
set -e
if [[ "$strict_rc" -gt 1 ]]; then
  echo "verify --strict failed with unexpected exit code: $strict_rc" >&2
  exit "$strict_rc"
fi

python -m awesome_skills bench \
  --db "$OUT_DIR/awesome_skills.sqlite" \
  --skills-json "$OUT_DIR/skills.json" \
  --benchmark sources/benchmark_queries.json \
  --alias-json "$OUT_DIR/name_aliases.json" \
  --min-hit-rate 0.50 \
  --min-mrr 0.45 \
  --min-ndcg 0.50 >/dev/null

python -m awesome_skills.mcp_server --skills-json "$OUT_DIR/skills.json" --db "$OUT_DIR/awesome_skills.sqlite" --self-test >/dev/null
bash scripts/mcp_context_search_smoke.sh >/dev/null

echo "smoke ok"
