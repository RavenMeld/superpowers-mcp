# comfyui-performance

Performance and memory tuning for ComfyUI (VRAM modes, workload knobs, and safe optimization steps). Use when diagnosing slow runs, VRAM/RAM OOM, or advising on configuration and workflow changes to improve speed or stability. Use only when the user explicitly mentions ComfyUI, ComfyUI workflows, custom_nodes, models/, ComfyUI-Manager, comfy-cli, or paths under this repo.

## Quick Facts
- id: `comfyui-performance--6d8e160b0a`
- worth_using_score: `35/100`
- tags: `comfyui, node, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/comfyui-performance/SKILL.md`

## Workflow / Steps
- 1) Resolution (width/height)
- 2) Batch size
- 3) Steps / sampler settings
- 4) Number of heavy branches (ControlNet, multiple upscalers, etc.)
- 5) Use partial execution for debugging or targeted changes

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
