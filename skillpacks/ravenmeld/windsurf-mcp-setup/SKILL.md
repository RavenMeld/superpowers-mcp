---
name: windsurf-mcp-setup
description: |
  Configure MCP servers in Windsurf (Codeium Cascade), including config file location and restart/refresh workflow.
---

# Windsurf MCP Setup

## Use When

- You use Windsurf’s Cascade and want to add MCP servers.
- You need to edit raw MCP config (beyond templates/marketplace).
- Your MCP server doesn’t show up and you need a consistent debug loop.

## Workflow

1. Open MCP settings in Windsurf UI, or edit the raw config file.
2. Add a server under `"mcpServers"`.
3. Refresh/restart Windsurf so it reloads.
4. Verify server start and tool availability.

## Config File Location

```text
~/.codeium/windsurf/mcp_config.json
```

## Example: stdio Server

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

## Troubleshooting

- Ensure config is valid JSON (Windsurf can fail silently).
- Fully relaunch if “refresh” doesn’t apply changes.
- Prefer stdio servers first (simpler to debug than remote auth).

## Safety Notes

- Don’t install untrusted MCP servers.
- Use least-privilege allowlists for filesystem-like servers.

