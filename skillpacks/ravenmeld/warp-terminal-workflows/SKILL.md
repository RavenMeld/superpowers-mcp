---
name: warp-terminal-workflows
description: |
  Use Warp Terminal effectively for dev workflows: projects, saved commands/workflows, SSH sessions, and safe team sharing.
---

# Warp Terminal Workflows

## Use When

- You use Warp as your daily terminal and want faster repeatable command runs.
- You want a clean workflow for SSH sessions, project entrypoints, and env setup.
- You want to share runbooks with teammates without leaking secrets.

## Workflow

1. Define your “project entry” commands (cd + env + dev server).
2. Save common commands/workflows so they stay discoverable.
3. Create SSH session shortcuts (hostnames + identities).
4. Keep secrets out of shared workflows; inject via env or a secret manager.

## Practical Patterns

### Project Entry (Repeatable)

Example (bash):

```bash
cd /path/to/repo
source .venv/bin/activate
make dev
```

### SSH Session Shortcut

Prefer SSH config aliases so your terminal command stays stable:

```bash
ssh git@github-ravenmeld
```

### Shareable Runbooks (No Secrets)

Write workflows that reference env vars:

```bash
export API_TOKEN="${API_TOKEN:?missing API_TOKEN}"
curl -H "Authorization: Bearer $API_TOKEN" https://example.com/health
```

## Safety Notes

- Never bake tokens/keys into saved workflows if they sync to the cloud.
- Prefer least-privilege SSH identities and host aliases per account.

