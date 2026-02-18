---
name: mcp-security-hygiene
description: |
  Treat MCP servers as executable code: least privilege, safe defaults, review checklist, and common failure modes.
---

# MCP Security Hygiene

## Use When

- You’re adding a new MCP server (especially from GitHub/marketplaces).
- You’re exposing filesystem, shell, browser automation, or network tools.
- You need a quick “is this safe enough?” review before enabling.

## Workflow

1. Identify what the server can access (filesystem roots, env vars, network).
2. Reduce privileges (allowlists, localhost binds, minimal env).
3. Pin versions after it works.
4. Log carefully (redact tokens), and keep outputs bounded.
5. Prefer “manual start + inspect” before letting a client auto-launch it.

## Checklist

- Source trust:
  - Prefer official orgs / well-maintained repos.
  - Read README + quick scan entrypoint code before running.
- Runtime containment:
  - Run on `127.0.0.1` when possible.
  - Use a dedicated OS user or container if the server needs broad access.
- Auth:
  - Pass secrets via env vars or OS keychain, not hardcoded JSON checked into git.
  - Rotate tokens if you accidentally paste them into logs.
- Filesystem:
  - Use explicit allowlists (avoid “/” or your whole home dir).
  - Separate read-only vs read-write where supported.
- Reproducibility:
  - Pin versions (avoid implicit `latest`).
  - Keep a working config snippet in a doc for rollback.

## Red Flags

- Requires full-disk access for “convenience”.
- Installs arbitrary postinstall scripts without review.
- Unbounded tool outputs (can dump huge files into the model context).
- Runs a remote endpoint without auth/TLS.

