---
name: tool-selection-rubric
description: |
  A practical rubric for deciding whether a library/repo/tool is worth adopting: maintenance, docs, security, compatibility, and escape hatches.
---

# Tool Selection Rubric

## Use When

- You found a promising GitHub repo/library and need to decide quickly.
- You’re choosing between multiple options (same category).
- You want to avoid supply-chain traps and abandoned projects.

## Workflow

1. Fit: does it solve your exact use case with minimal glue?
2. Health: is it maintained and used by real people?
3. Safety: what permissions does it need, and can you sandbox it?
4. Integration: does it fit your stack (Python/Node/CI/OS)?
5. Exit: can you swap it out later without rewriting everything?

## Quick Checks (Copy/Paste)

Repo maintenance signals:

```bash
# last 20 commits; look for recent activity and regular cadence
git log -20 --oneline
```

License sanity:

```bash
rg -n \"^license\" -S README.md || true
ls -la LICENSE* 2>/dev/null || true
```

Dependency risk:

```bash
rg -n \"postinstall|preinstall|curl\\s+https?://|wget\\s+https?://\" package.json **/package.json 2>/dev/null || true
```

## Red Flags

- Requires broad filesystem access without an allowlist.
- Runs shell commands as part of install without clear docs.
- No releases/tags and unclear compatibility promises.
- Unbounded output (tools that can dump huge files into context).

## Green Flags

- Clear docs + examples + troubleshooting section.
- Pinned releases, changelog, and stable upgrade path.
- Minimal permissions + clear configuration boundaries.
- Tests and CI present.

