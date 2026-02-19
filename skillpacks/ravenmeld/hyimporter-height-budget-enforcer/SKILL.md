---
name: hyimporter-height-budget-enforcer
description: |
  Enforce strict world-height budgets in HyImporter outputs to avoid invalid imports and in-game clipping.
---

# HyImporter Height Budget Enforcer

## Use When

- Terrain exceeds target world Y limits.
- Imports succeed but gameplay shows clipping or missing regions.
- You need hard guarantees for min/max elevation bounds.

## Workflow

1. Define allowed min/max Y envelope for target world.
2. Scan generated tiles for out-of-range samples.
3. Apply offset/clamp policy and re-export affected tiles.
4. Re-validate bounds and generate compliance report.
5. Block import when any tile violates budget.

## Copy/Paste Examples

```bash
bash scripts/build_world.sh config.yaml --tile-workers 8
```

```bash
rg -n "height|elevation|min|max" output/**/*.json runbook/* 2>/dev/null
```

```bash
python -m awesome_skills search "height budget"
```

## Budget Rules

- Use one canonical height envelope per project.
- Prefer explicit offset mapping over ad-hoc manual edits.
- Keep per-tile budget reports versioned with builds.

## Safety Notes

- Never ignore out-of-range warnings for production imports.
- Preserve pre-clamp outputs for debugging root cause.
