# hyimporter-hytale-terrain-pipeline

Use HyImporter to convert wow.export map packages into seam-safe OBJ tiles and async-pastable `.schematic` tiles for Hytale.
Includes WSL/Windows path conventions and validation steps.

## Quick Facts
- id: `hyimporter-hytale-terrain-pipeline--291774c4e1`
- worth_using_score: `70/100`
- tags: `ci, docs, wsl, windows, linux`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/hyimporter-hytale-terrain-pipeline/SKILL.md`

## Use When
- You exported a WoW zone via `wow.export` on Windows and want to import terrain into Hytale.
- You want seam-safe tiled terrain with a strict Y budget (0..319).
- Hytale’s OBJ import freezes on large tiles and you need async schematic paste.

## Workflow / Steps
- Prepare the shared folder layout (`C:\\hyimporter\\input` + `C:\\hyimporter\\out`).
- Place the wow.export package under `<input_root>/<map_name>/`.
- Create `config.yaml` and set `project.map_name`, `paths.input_root`, `paths.output_root`.
- Run the build (WSL bash or Windows PowerShell wrapper).
- Use the generated runbook (`runbook/hytale_import_runbook.md`) to paste into Hytale.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `8`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
