---
name: cursor-mcp-setup
description: |
  Configure MCP servers in Cursor using mcp.json (global or per-project), plus validation and common failure modes.
---

# Cursor MCP Setup

## Use When

- You want Cursor to call tools via MCP (stdio, SSE, or streamable HTTP).
- You need to add a custom server not available in “one-click installs”.
- Your MCP servers aren’t showing up and you need a deterministic debug flow.

## Workflow

1. Decide scope: project (`.cursor/mcp.json`) vs global (`~/.cursor/mcp.json`).
2. Add/merge a server entry under `"mcpServers"`.
3. Restart Cursor (or reload window) so it re-reads config.
4. Verify the server is reachable / starts successfully.
5. Troubleshoot JSON validity, paths, and auth env vars.

## Config Locations

Project:

```text
.cursor/mcp.json
```

Global:

```text
~/.cursor/mcp.json
```

## Example: stdio Server (Cursor Manages the Process)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allow"],
      "env": {}
    }
  }
}
```

Notes:
- Prefer pinning versions once a server is working (replace `@latest` style installs).
- Keep `env` minimal; do not paste secrets into logs.

## Example: Remote HTTP / Streamable HTTP

```json
{
  "mcpServers": {
    "docs": {
      "url": "https://example.com/mcp",
      "headers": {
        "Authorization": "Bearer <TOKEN>"
      }
    }
  }
}
```

## Troubleshooting Checklist

- Validate JSON (missing commas/trailing commas break loading).
- Confirm the file is in the correct location (`.cursor/mcp.json` vs `~/.cursor/mcp.json`).
- Confirm you restarted Cursor after editing.
- If using `stdio`: confirm `command` exists on PATH and works in a normal terminal.
- If using `url`: confirm the server is reachable and responds at the expected endpoint.
- If tools appear in the IDE but not the CLI, treat them as separate products (config discovery may differ).

## Safety Notes

MCP servers can execute code and access local resources:
- Only install from trusted sources.
- Prefer localhost binds (`127.0.0.1`) for local servers.
- Use least-privilege filesystem allowlists where supported.

