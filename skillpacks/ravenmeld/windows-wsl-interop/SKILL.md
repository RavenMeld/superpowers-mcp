---
name: windows-wsl-interop
description: |
  Practical WSL <-> Windows interop cheatsheet: paths, clipboard, opening files, and moving data safely.
---

# Windows <-> WSL Interop

## Use When

- You bounce between Windows apps and WSL tooling.
- You need reliable path conversion and clipboard transfer.
- You want quick “open this folder/file in Windows” from WSL.

## Workflow

1. Convert paths with `wslpath`.
2. Use `explorer.exe` to open folders/files.
3. Use `clip.exe` to copy text to Windows clipboard.
4. Prefer working inside the WSL filesystem for performance (especially git/node).

## Copy to Clipboard (Windows)

Copy a file’s content (example: SSH public key):

```bash
cat ~/.ssh/github-ravenmeld.pub | clip.exe
```

Copy arbitrary text:

```bash
printf '%s' 'hello from wsl' | clip.exe
```

## Path Conversion

WSL -> Windows:

```bash
wslpath -w /home/wolvend/codex/agent_playground
```

Windows -> WSL:

```bash
wslpath -u 'C:\\Users\\LIZ\\Downloads'
```

## Open in Explorer

Open the current directory:

```bash
explorer.exe .
```

Open a specific file (Windows will pick the default app):

```bash
explorer.exe "$(wslpath -w ./README.md)"
```

## Common Gotchas

- Avoid running huge `node_modules/` trees on `/mnt/c/...` if you can; it’s slower.
- If a Windows app can’t find a WSL path, convert it with `wslpath -w`.

