---
name: wsl-windows-path-debugger
description: |
  Diagnose and fix WSL/Windows path translation, newline, and permission mismatches that break toolchains.
---

# WSL Windows Path Debugger

## Use When

- Commands work in PowerShell but fail in WSL (or vice versa).
- Tools cannot find files due to `/mnt/c/...` versus `C:\...` confusion.
- Scripts break on CRLF/LF or executable permission differences.

## Workflow

1. Confirm the execution shell and absolute path assumptions.
2. Normalize path conversion at the boundary (`wslpath` / explicit mapping).
3. Check newline format and shebang compatibility.
4. Validate file permissions + executable bits in WSL.
5. Re-test from both shells with the same target file.

## Copy/Paste Examples

```bash
wslpath 'C:\Users\LIZ\Downloads'
```

```bash
file scripts/run.sh && sed -n '1,3p' scripts/run.sh
```

```bash
dos2unix scripts/run.sh && chmod +x scripts/run.sh
```

## Common Fixes

- Convert Windows paths before passing into Linux tools.
- Keep scripts in LF if executed under bash.
- Avoid relative paths when crossing shell boundaries.

## Safety Notes

- Do not run destructive path rewrites without backups.
- Treat mixed-shell automation as explicit interop, not implicit behavior.
