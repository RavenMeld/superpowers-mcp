# Smithery Seed Installs (Optional)

This repo’s `build`/`search` workflow is intentionally **no-network**.

If you want to expand your *local* skills corpus, you can install extra skills from Smithery into
`~/.agents/skills`, then rebuild the database.

## Batch Install (Codex Agent)

```bash
set -euo pipefail
export NPM_CONFIG_CACHE=/tmp/npm-cache
export NPM_CONFIG_LOGS_DIR=/tmp/npm-logs
mkdir -p "$NPM_CONFIG_CACHE" "$NPM_CONFIG_LOGS_DIR"

skills=(
  # Playwright / browser testing
  comet-ml/playwright-e2e
  prairielearn/playwright-testing
  open-metadata/writing-playwright-tests
  gentleman-programming/playwright
  voicevox/write-playwright-e2e-code
  the-answerai/playwright-debugging

  # Chrome / Firefox / browser automation
  github/chrome-devtools
  chromedevtools/chrome-devtools
  davila7/browser-extension-builder
  zenobi-us/firefox-debug
  mic92/browser-cli
  different-ai/browser-automation
  FradSer/agent-browser
  openclaw/browsh
  modu-ai/moai-platform-chrome-extension

  # Windows / WSL / cross-platform
  evolv3-ai/admin-wsl
  evolv3-ai/admin-windows
  jackspace/windows-expert
  jackspace/network-diagnostics
  janjaszczak/cross-platform-safety

  # PowerShell
  windmill-labs/write-script-powershell
  davila7/powershell-windows
  404kidwiz/powershell-7-expert
  JosiahSiegel/powershell-master
  JosiahSiegel/powershell-security

  # Hytale
  fred-drake/hytale-modding
  neversight/hytale-commands
  neversight/blockbench-hytale
  neversight/hytale-custom-entities
  neversight/hytale-custom-assets
  neversight/hytale-events-api

  # Obsidian
  openclaw/obsidian
  kepano/obsidian-markdown
  heyitsnoah/obsidian-bases
  jeremylongshore/obsidian-hello-world
  jeremylongshore/obsidian-performance-tuning
  neversight/obsidian-developer
)

for s in "${skills[@]}"; do
  echo "==> $s"
  smithery skills install -a codex -g "$s" || echo "!! failed: $s" >&2
done
```

Then rebuild:

```bash
cd projects/awesome-skills-database
python -m awesome_skills build --out dist
```

## Notes

- Some Smithery listings are **not** installable via `smithery skills install` because they don’t
  expose `/.well-known/skills/index.json` (example: `microsoft/playwright-mcp-dev`).
- Always inspect installed skills before use; they can include scripts that run with agent permissions.

