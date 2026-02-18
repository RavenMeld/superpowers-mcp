---
name: hyimporter-hytale-terrain-pipeline
description: |
  Use HyImporter to convert wow.export map packages into seam-safe OBJ tiles and async-pastable `.schematic` tiles for Hytale.
  Includes WSL/Windows path conventions and validation steps.
---

# HyImporter: WoW Export -> Hytale Terrain Pipeline

## Use When

- You exported a WoW zone via `wow.export` on Windows and want to import terrain into Hytale.
- You want seam-safe tiled terrain with a strict Y budget (0..319).
- Hytale’s OBJ import freezes on large tiles and you need async schematic paste.

## Workflow

1. Prepare the shared folder layout (`C:\\hyimporter\\input` + `C:\\hyimporter\\out`).
2. Place the wow.export package under `<input_root>/<map_name>/`.
3. Create `config.yaml` and set `project.map_name`, `paths.input_root`, `paths.output_root`.
4. Run the build (WSL bash or Windows PowerShell wrapper).
5. Use the generated runbook (`runbook/hytale_import_runbook.md`) to paste into Hytale.

## Directory Layout (Recommended)

Windows:

```text
C:\hyimporter\input\<map_name>\
C:\hyimporter\out\<map_name>\
```

WSL view of the same folders:

```text
/mnt/c/hyimporter/input/<map_name>/
/mnt/c/hyimporter/out/<map_name>/
```

## Build (WSL/Linux/macOS)

From the HyImporter repo root:

```bash
cp config/config.example.yaml config.yaml
# edit config.yaml
bash scripts/build_world.sh config.yaml
```

Key flags you’ll actually use:

```bash
# Force synchronous tile export (debugging)
bash scripts/build_world.sh config.yaml --sync-tiles

# Pin tile workers for reproducibility
bash scripts/build_world.sh config.yaml --tile-workers 8
```

## Async Import into Hytale (Recommended)

HyImporter can output `.schematic` tiles for async paste using `cc.invic_SchematicLoader`.

1. Ensure schematics are enabled in config:
   - `outputs.export_schematic: true`
   - Prefer: `outputs.schematic_full_volume: false` (surface-only)
2. Sync tiles into your Hytale save:

```bash
# WSL -> Windows Hytale save folder
bash scripts/sync_to_hytale_schematicloader.sh <map_name> /mnt/c/hyimporter/out <WorldName>
```

3. Restart the world/server, then in game:
   - `/schem list`
   - `/schem load <tile_0_0.schematic>`
   - `/schem paste` (at the correct origin from `runbook/tile_manifest.csv`)

## Validation / Confidence

Quick deterministic validation:

```bash
bash scripts/self_test.sh quick
```

Full suite:

```bash
bash scripts/self_test.sh full
```

## Where the Docs Live (Local)

In this workspace:

```text
source/agents/tooling/hyimporter/README.md
source/agents/tooling/hyimporter/docs/hytale_import_runbook.md
```

## Safety Notes

- Avoid importing full-volume tiles unless you really need it; it can explode size.
- Treat the pipeline as deterministic: change one knob at a time and re-check seams + height budget.

