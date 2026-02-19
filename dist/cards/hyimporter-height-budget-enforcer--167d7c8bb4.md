# hyimporter-height-budget-enforcer

Enforce strict world-height budgets in HyImporter outputs to avoid invalid imports and in-game clipping.

## Quick Facts
- id: `hyimporter-height-budget-enforcer--167d7c8bb4`
- worth_using_score: `60/100`
- tags: `hyimporter, python, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/hyimporter-height-budget-enforcer/SKILL.md`

## Use When
- Terrain exceeds target world Y limits.
- Imports succeed but gameplay shows clipping or missing regions.
- You need hard guarantees for min/max elevation bounds.

## Workflow / Steps
- Define allowed min/max Y envelope for target world.
- Scan generated tiles for out-of-range samples.
- Apply offset/clamp policy and re-export affected tiles.
- Re-validate bounds and generate compliance report.
- Block import when any tile violates budget.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
