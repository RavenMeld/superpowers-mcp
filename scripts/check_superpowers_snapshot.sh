#!/usr/bin/env bash
set -euo pipefail

# Compare vendored superpowers snapshot commit with a target GitHub repo ref.
# Exit codes:
#   0: in sync
#   2: unable to determine remote commit (e.g., private repo / network issue)
#   3: drift detected (snapshot commit != target commit)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

UPSTREAM_FILE="${UPSTREAM_FILE:-${REPO_ROOT}/skillpacks/superpowers/UPSTREAM.txt}"
TARGET_REPO="${TARGET_REPO:-erophames/superpowers-mcp}"
TARGET_REF="${TARGET_REF:-main}"

if [[ ! -f "${UPSTREAM_FILE}" ]]; then
  echo "{\"ok\":false,\"code\":\"UPSTREAM_METADATA_MISSING\",\"upstream_file\":\"${UPSTREAM_FILE}\"}"
  exit 2
fi

LOCAL_COMMIT="$(sed -n 's/^source_commit:[[:space:]]*//p' "${UPSTREAM_FILE}" | head -n1 | tr -d '[:space:]')"
LOCAL_SOURCE_REPO="$(sed -n 's/^source_repo:[[:space:]]*//p' "${UPSTREAM_FILE}" | head -n1)"

if [[ -z "${LOCAL_COMMIT}" ]]; then
  echo "{\"ok\":false,\"code\":\"LOCAL_COMMIT_MISSING\",\"upstream_file\":\"${UPSTREAM_FILE}\"}"
  exit 2
fi

API_URL="https://api.github.com/repos/${TARGET_REPO}/commits/${TARGET_REF}"
ATOM_URL="https://github.com/${TARGET_REPO}/commits/${TARGET_REF}.atom"
API_BODY="$(curl -fsSL "${API_URL}" 2>/dev/null || true)"

REMOTE_COMMIT="$(
  python - "${API_BODY}" <<'PY'
import json
import re
import sys

raw = sys.argv[1]
try:
    data = json.loads(raw)
except json.JSONDecodeError:
    print("")
    raise SystemExit(0)

sha = data.get("sha")
if isinstance(sha, str) and re.fullmatch(r"[0-9a-fA-F]{40}", sha):
    print(sha.lower())
else:
    print("")
PY
)"

if [[ -z "${REMOTE_COMMIT}" ]]; then
  ATOM_BODY="$(curl -fsSL "${ATOM_URL}" 2>/dev/null || true)"
  REMOTE_COMMIT="$(
    python - "${ATOM_BODY}" <<'PY'
import re
import sys

raw = sys.argv[1]
match = re.search(r"Grit::Commit/([0-9a-fA-F]{40})", raw)
if match:
    print(match.group(1).lower())
else:
    print("")
PY
  )"
fi

if [[ -z "${REMOTE_COMMIT}" ]]; then
  safe_api_url="$(printf "%s" "${API_URL}" | sed 's/"/\\"/g')"
  safe_atom_url="$(printf "%s" "${ATOM_URL}" | sed 's/"/\\"/g')"
  safe_local_commit="$(printf "%s" "${LOCAL_COMMIT}" | sed 's/"/\\"/g')"
  safe_local_repo="$(printf "%s" "${LOCAL_SOURCE_REPO}" | sed 's/"/\\"/g')"
  echo "{\"ok\":false,\"code\":\"REMOTE_COMMIT_UNAVAILABLE\",\"target_repo\":\"${TARGET_REPO}\",\"target_ref\":\"${TARGET_REF}\",\"api_url\":\"${safe_api_url}\",\"atom_url\":\"${safe_atom_url}\",\"local_commit\":\"${safe_local_commit}\",\"local_source_repo\":\"${safe_local_repo}\"}"
  exit 2
fi

safe_local_commit="$(printf "%s" "${LOCAL_COMMIT}" | sed 's/"/\\"/g')"
safe_remote_commit="$(printf "%s" "${REMOTE_COMMIT}" | sed 's/"/\\"/g')"
safe_local_repo="$(printf "%s" "${LOCAL_SOURCE_REPO}" | sed 's/"/\\"/g')"

if [[ "${LOCAL_COMMIT}" == "${REMOTE_COMMIT}" ]]; then
  echo "{\"ok\":true,\"in_sync\":true,\"target_repo\":\"${TARGET_REPO}\",\"target_ref\":\"${TARGET_REF}\",\"local_commit\":\"${safe_local_commit}\",\"remote_commit\":\"${safe_remote_commit}\",\"local_source_repo\":\"${safe_local_repo}\"}"
  exit 0
fi

echo "{\"ok\":true,\"in_sync\":false,\"target_repo\":\"${TARGET_REPO}\",\"target_ref\":\"${TARGET_REF}\",\"local_commit\":\"${safe_local_commit}\",\"remote_commit\":\"${safe_remote_commit}\",\"local_source_repo\":\"${safe_local_repo}\"}"
exit 3
