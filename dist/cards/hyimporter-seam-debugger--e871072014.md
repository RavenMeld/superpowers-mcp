# hyimporter-seam-debugger

Diagnose and fix HyImporter tile seam mismatches in terrain outputs before Hytale import.

## Quick Facts
- id: `hyimporter-seam-debugger--e871072014`
- worth_using_score: `60/100`
- tags: `hytale, hyimporter, python, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/hyimporter-seam-debugger/SKILL.md`

## Use When
- Adjacent terrain tiles show visible seam gaps/steps.
- Tile borders disagree after build parameter changes.
- You need deterministic seam verification before import.

## Workflow / Steps
- Identify problematic tile coordinates and neighbor set.
- Compare border vertex/height values across tile edges.
- Re-check build parameters that affect interpolation/sampling.
- Rebuild only affected tiles with fixed settings.
- Validate seam continuity before bulk export.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
