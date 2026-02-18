---
name: obsidian-vault-ops
description: |
  Automate and maintain an Obsidian vault safely: search, read, patch, frontmatter updates, tags, and batch hygiene.
  Designed for tool-driven workflows (MCP) and reproducible edits.
---

# Obsidian Vault Ops

## Use When

- You want deterministic vault edits (no manual clicking).
- You need to find and patch notes at scale (tags/frontmatter/links).
- You’re building an “engineering knowledge base” and want structure to stick.

## Workflow

1. Find target notes (search by content or properties/frontmatter).
2. Read the note(s) before editing.
3. Prefer small, anchored edits (patch) over whole-file rewrites.
4. Update frontmatter separately when possible.
5. Re-read after edits to verify the expected change landed.

## Common Operations (Tool-Oriented)

Search notes by content:

```text
operation: search_notes
query: "playwright trace"
limit: 10
```

Read a note:

```text
operation: read_note
path: "Engineering/Playwright/Debugging.md"
```

Patch a note (replace an exact string):

```text
operation: patch_note
path: "Engineering/Playwright/Debugging.md"
oldString: "TODO: add trace steps"
newString: "Trace workflow: run headed, record trace, inspect in viewer."
```

Update frontmatter only:

```text
operation: update_frontmatter
path: "Engineering/Playwright/Debugging.md"
frontmatter:
  tags: ["playwright", "testing"]
  status: "active"
```

## Hygiene Patterns

- Create a stable folder taxonomy:
  - `Engineering/`, `Projects/`, `Runbooks/`, `Decision Records/`, `Snippets/`
- Prefer short “how-to” notes with:
  - prerequisites
  - exact commands
  - known failure modes
  - rollback steps
- Keep sensitive tokens out of notes; store secrets in a password manager.

## Safety Notes

- Patch edits require exact `oldString` matches; if it doesn’t match, re-read first.
- For bulk operations, run in small batches and verify every batch.

