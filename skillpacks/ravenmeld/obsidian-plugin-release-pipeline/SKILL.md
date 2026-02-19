---
name: obsidian-plugin-release-pipeline
description: |
  Release Obsidian plugins safely with versioning, changelog generation, packaging checks, and reproducible publish steps.
---

# Obsidian Plugin Release Pipeline

## Use When

- You are preparing an Obsidian plugin release.
- You need a repeatable version/changelog/package workflow.
- A release failed and needs deterministic rerun steps.

## Workflow

1. Verify working tree cleanliness and test status.
2. Bump version in manifest and package metadata.
3. Generate release notes from merged changes.
4. Build distributable artifacts and verify checksums.
5. Publish only after post-build smoke checks pass.

## Copy/Paste Examples

```bash
git status -sb
```

```bash
npm ci && npm run build && npm test
```

```bash
git tag vX.Y.Z && git push origin vX.Y.Z
```

## Release Guardrails

- Keep plugin manifest and package version in sync.
- Include migration notes for breaking changes.
- Attach reproducible build artifacts to each release.

## Safety Notes

- Do not release from a dirty tree.
- Do not skip smoke checks on “hotfix” releases.
