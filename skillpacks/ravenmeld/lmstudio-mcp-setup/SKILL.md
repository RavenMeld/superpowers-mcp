---
name: lmstudio-mcp-setup
description: |
  Configure MCP servers in LM Studio (MCP host support), including where to edit mcp.json and common gotchas.
---

# LM Studio MCP Setup

## Use When

- You want LM Studio to act as an MCP Host (local or remote MCP servers).
- You need to manually edit `mcp.json`.
- Tools aren’t appearing and you need a deterministic check list.

## Workflow

1. In LM Studio, open the MCP config editor (Program tab -> Install -> Edit `mcp.json`).
2. Add/merge servers under `"mcpServers"`.
3. Save and restart LM Studio (or re-open the app).
4. Ask the model to list available tools to confirm.

## Example: Remote MCP (URL + Auth Header)

```json
{
  "mcpServers": {
    "hf-mcp-server": {
      "url": "https://huggingface.co/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_HF_TOKEN>"
      }
    }
  }
}
```

## Gotchas

- Treat MCP servers as code: only add servers you trust.
- Some MCPs are designed for frontier models and can be token-heavy; watch context limits.
- When merging config manually, ensure you keep a single top-level `"mcpServers"` object.

