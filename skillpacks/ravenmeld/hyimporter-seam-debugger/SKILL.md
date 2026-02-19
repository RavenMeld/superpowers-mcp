---
name: hyimporter-seam-debugger
description: |
  Diagnose and fix HyImporter tile seam mismatches in terrain outputs before Hytale import.
---

# HyImporter Seam Debugger

## Use When

- Adjacent terrain tiles show visible seam gaps/steps.
- Tile borders disagree after build parameter changes.
- You need deterministic seam verification before import.

## Workflow

1. Identify problematic tile coordinates and neighbor set.
2. Compare border vertex/height values across tile edges.
3. Re-check build parameters that affect interpolation/sampling.
4. Rebuild only affected tiles with fixed settings.
5. Validate seam continuity before bulk export.

## Copy/Paste Examples

```bash
bash scripts/build_world.sh config.yaml --sync-tiles
```

```bash
rg -n "tile|seam|border" runbook/*.md output/**/*.json 2>/dev/null
```

```bash
python -m awesome_skills search "hyimporter seam"
```

## Seam Checks

- Compare east-west and north-south border pairs explicitly.
- Keep voxel scale and padding stable across reruns.
- Log tile-level diffs for reproducible bug reports.

## Safety Notes

- Do not patch seam issues by global smoothing without evidence.
- Keep original tile exports for side-by-side comparison.
