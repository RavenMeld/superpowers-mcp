---
name: hytale-asset-pipeline
description: |
  Build a repeatable Hytale asset pipeline from modeling tools to validated, pack-ready game assets.
---

# Hytale Asset Pipeline

## Use When

- You are producing custom Hytale models/textures/animations.
- You need consistent export and validation standards.
- Assets work locally but fail in packaged builds.

## Workflow

1. Model with naming and scale conventions.
2. Export with deterministic format settings.
3. Validate geometry/material/animation compatibility.
4. Assemble assets into a pack with manifest metadata.
5. Test pack load and runtime behavior in a minimal scene.

## Copy/Paste Examples

```bash
ls -R assets/models assets/textures
```

```bash
rg -n "TODO|FIXME|placeholder" assets
```

```bash
sha256sum assets/**/*.png 2>/dev/null | head
```

## Asset Standards

- Enforce consistent pivot/origin conventions.
- Keep texture naming and resolution policy explicit.
- Track source file -> exported file lineage.

## Safety Notes

- Do not overwrite source assets during export.
- Keep immutable snapshots before large re-exports.
