# comfy-edit

Use when editing ComfyUI workflow JSON, adding nodes, wiring connections, modifying workflows, adding ControlNet/LoRA/upscaling to a workflow, or submitting workflows to ComfyUI.

## Quick Facts
- id: `comfy-edit--b2b01b2266`
- worth_using_score: `40/100`
- tags: `github, comfyui, python, node`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/comfy-edit/SKILL.md`

## Workflow / Steps
- *Repo**: https://github.com/peteromallet/VibeComfy
- *Tip**: Use `trace` first to find slot numbers, then `wire` to connect.
- **Find the node**: `comfy_search("controlnet")` (use comfy-registry skill)
- **Get the spec**: `comfy_spec("ControlNetLoader")` - see inputs/outputs
- **Understand the flow**: `python we_vibin.py trace workflow.json <ksampler_id>`
- **Create and wire**:

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
