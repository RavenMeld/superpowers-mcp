---
name: hytale-mod-ci
description: |
  Add CI checks for Hytale mods: lint, build, package validation, and release gates.
---

# Hytale Mod CI

## Use When

- You want automated quality gates for Hytale mods.
- Manual mod packaging is error-prone and inconsistent.
- You need confidence before publishing mod updates.

## Workflow

1. Run lint and static checks on every pull request.
2. Build mod package in a clean CI environment.
3. Validate produced artifact structure and metadata.
4. Execute smoke integration checks on sample content.
5. Gate release tags on successful CI + changelog presence.

## Copy/Paste Examples

```bash
git diff --name-only origin/main...HEAD
```

```bash
npm ci && npm run lint && npm run build
```

```bash
test -f dist/mod-package.zip && ls -lh dist/mod-package.zip
```

## CI Rules

- Fail fast on manifest/schema mismatches.
- Keep CI cache scoped to lockfile hashes.
- Promote only artifacts created in CI, not local builds.

## Safety Notes

- Do not publish artifacts from untrusted forks.
- Require signed tags for release workflows.
