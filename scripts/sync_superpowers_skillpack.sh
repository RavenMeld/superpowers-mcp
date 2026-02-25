#!/usr/bin/env bash
set -euo pipefail

# Sync superpowers skills into this repo's skillpacks/ as a deterministic snapshot.
# Uses git object data from source HEAD to avoid depending on source working-tree state.

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

if [[ ! -d "${SOURCE_REPO}/.git" ]]; then
  echo "[ERROR] SOURCE_REPO is not a git repository: ${SOURCE_REPO:-<unset>}" >&2
  echo "        Set SOURCE_REPO=/path/to/superpowers/repo and retry." >&2
  exit 2
fi

SOURCE_COMMIT="$(git -C "${SOURCE_REPO}" rev-parse HEAD)"
SOURCE_URL="$(git -C "${SOURCE_REPO}" remote get-url upstream 2>/dev/null || git -C "${SOURCE_REPO}" remote get-url origin)"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "${TMP_DIR}"' EXIT

git -C "${SOURCE_REPO}" archive --format=tar "${SOURCE_COMMIT}" skills | tar -xf - -C "${TMP_DIR}"

if [[ ! -d "${TMP_DIR}/skills" ]]; then
  echo "[ERROR] skills/ not found in source commit ${SOURCE_COMMIT}" >&2
  exit 2
fi

STAGING_DIR="${TMP_DIR}/superpowers-staging"
mkdir -p "${STAGING_DIR}"
cp -a "${TMP_DIR}/skills/." "${STAGING_DIR}/"

cat > "${STAGING_DIR}/UPSTREAM.txt" <<META
source_repo: ${SOURCE_URL}
source_commit: ${SOURCE_COMMIT}
synced_at_utc: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
sync_tool: scripts/sync_superpowers_skillpack.sh
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
echo "      source: ${SOURCE_REPO}"
echo "      commit: ${SOURCE_COMMIT}"
echo "      dest:   ${DEST_DIR}"
