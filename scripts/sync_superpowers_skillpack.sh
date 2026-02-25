#!/usr/bin/env bash
set -euo pipefail

# Sync superpowers skills into this repo's skillpacks/ as a deterministic snapshot.
# Local mode: uses git object data from source HEAD to avoid depending on source working-tree state.
# Remote mode: downloads a GitHub archive for TARGET_REPO/TARGET_REF.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

DEFAULT_SOURCE_REPO=""
for candidate in \
  "${REPO_ROOT}/source/automation/devtools/superpowers" \
  "${REPO_ROOT}/../source/automation/devtools/superpowers" \
  "${REPO_ROOT}/../../source/automation/devtools/superpowers"; do
  if [[ -d "${candidate}/.git" ]]; then
    DEFAULT_SOURCE_REPO="${candidate}"
    break
  fi
done

SOURCE_REPO="${SOURCE_REPO:-${DEFAULT_SOURCE_REPO}}"
DEST_DIR="${DEST_DIR:-${REPO_ROOT}/skillpacks/superpowers}"
SYNC_MODE="${SYNC_MODE:-auto}"           # auto|local|remote
TARGET_REPO="${TARGET_REPO:-erophames/superpowers-mcp}"
TARGET_REF="${TARGET_REF:-main}"

if [[ "${SYNC_MODE}" != "auto" && "${SYNC_MODE}" != "local" && "${SYNC_MODE}" != "remote" ]]; then
  echo "[ERROR] invalid SYNC_MODE='${SYNC_MODE}'. Expected one of: auto, local, remote." >&2
  exit 2
fi

resolve_remote_commit() {
  local repo="$1"
  local ref="$2"
  local api_url="https://api.github.com/repos/${repo}/commits/${ref}"
  local atom_url="https://github.com/${repo}/commits/${ref}.atom"
  local body sha

  body="$(curl -fsSL "${api_url}" 2>/dev/null || true)"
  sha="$(
    python - "${body}" <<'PY'
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
  if [[ -n "${sha}" ]]; then
    printf "%s" "${sha}"
    return 0
  fi

  body="$(curl -fsSL "${atom_url}" 2>/dev/null || true)"
  sha="$(
    python - "${body}" <<'PY'
import re
import sys
raw = sys.argv[1]
m = re.search(r"Grit::Commit/([0-9a-fA-F]{40})", raw)
print(m.group(1).lower() if m else "")
PY
  )"
  printf "%s" "${sha}"
}

mode=""
if [[ "${SYNC_MODE}" == "local" ]]; then
  mode="local"
elif [[ "${SYNC_MODE}" == "remote" ]]; then
  mode="remote"
else
  if [[ -n "${SOURCE_REPO:-}" && -d "${SOURCE_REPO}/.git" ]]; then
    mode="local"
  else
    mode="remote"
  fi
fi

SOURCE_COMMIT=""
SOURCE_URL=""

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

if [[ "${mode}" == "local" ]]; then
  if [[ ! -d "${SOURCE_REPO}/.git" ]]; then
    echo "[ERROR] SOURCE_REPO is not a git repository: ${SOURCE_REPO:-<unset>}" >&2
    echo "        Set SOURCE_REPO=/path/to/superpowers/repo, or use SYNC_MODE=remote." >&2
    exit 2
  fi
  SOURCE_COMMIT="$(git -C "${SOURCE_REPO}" rev-parse HEAD)"
  SOURCE_URL="$(git -C "${SOURCE_REPO}" remote get-url upstream 2>/dev/null || git -C "${SOURCE_REPO}" remote get-url origin)"
  git -C "${SOURCE_REPO}" archive --format=tar "${SOURCE_COMMIT}" skills | tar -xf - -C "${TMP_DIR}"
else
  SOURCE_URL="https://github.com/${TARGET_REPO}.git"
  SOURCE_COMMIT="$(resolve_remote_commit "${TARGET_REPO}" "${TARGET_REF}")"
  ARCHIVE_URL="https://codeload.github.com/${TARGET_REPO}/tar.gz/refs/heads/${TARGET_REF}"
  ARCHIVE_PATH="${TMP_DIR}/source.tar.gz"
  if ! curl -fsSL "${ARCHIVE_URL}" -o "${ARCHIVE_PATH}" 2>/dev/null; then
    echo "[ERROR] failed to download remote archive: ${ARCHIVE_URL}" >&2
    exit 2
  fi
  tar -xzf "${ARCHIVE_PATH}" -C "${TMP_DIR}"

  skills_dir="$(find "${TMP_DIR}" -maxdepth 3 -type d -name skills | head -n1 || true)"
  if [[ -z "${skills_dir}" ]]; then
    echo "[ERROR] skills/ not found in downloaded archive for ${TARGET_REPO}@${TARGET_REF}" >&2
    exit 2
  fi
  mkdir -p "${TMP_DIR}/skills"
  cp -a "${skills_dir}/." "${TMP_DIR}/skills/"
fi

if [[ ! -d "${TMP_DIR}/skills" ]]; then
  echo "[ERROR] skills/ not found in source snapshot ${SOURCE_COMMIT:-<unknown>}" >&2
  exit 2
fi

STAGING_DIR="${TMP_DIR}/superpowers-staging"
mkdir -p "${STAGING_DIR}"
cp -a "${TMP_DIR}/skills/." "${STAGING_DIR}/"

cat > "${STAGING_DIR}/UPSTREAM.txt" <<META
source_repo: ${SOURCE_URL}
source_commit: ${SOURCE_COMMIT:-unknown}
source_ref: ${TARGET_REF}
synced_at_utc: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
sync_tool: scripts/sync_superpowers_skillpack.sh
sync_mode: ${mode}
META

mkdir -p "$(dirname "${DEST_DIR}")"
NEW_DEST="${DEST_DIR}.new.$$"
rm -rf "${NEW_DEST}"
mv "${STAGING_DIR}" "${NEW_DEST}"

if [[ -d "${DEST_DIR}" ]]; then
  OLD_DEST="${DEST_DIR}.old.$$"
  mv "${DEST_DIR}" "${OLD_DEST}"
  mv "${NEW_DEST}" "${DEST_DIR}"
  rm -rf "${OLD_DEST}"
else
  mv "${NEW_DEST}" "${DEST_DIR}"
fi

echo "[OK] Synced superpowers skillpack"
if [[ "${mode}" == "local" ]]; then
  echo "      source: ${SOURCE_REPO}"
else
  echo "      source: ${TARGET_REPO}@${TARGET_REF}"
fi
echo "      mode:   ${mode}"
echo "      commit: ${SOURCE_COMMIT:-unknown}"
echo "      dest:   ${DEST_DIR}"
