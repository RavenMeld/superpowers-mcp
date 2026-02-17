# comfyui-troubleshooting

Diagnose and recover ComfyUI failures (startup crashes, import failed custom nodes, missing models/nodes, workflow JSON issues, dependency conflicts, VRAM/OOM). Use when the user reports ComfyUI startup issues, red nodes/IMPORT FAILED, workflow validation errors, dependency conflicts, OOM, or API automation failures. Use only when the user explicitly mentions ComfyUI, ComfyUI workflows, custom_...

## Quick Facts
- id: `comfyui-troubleshooting--14efb6df39`
- worth_using_score: `20/100`
- tags: `comfyui, python, node, security, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/comfyui-troubleshooting/SKILL.md`

## Workflow / Steps
- If error references a node id or missing property:
- treat as workflow JSON issue (do not fix by updating everything)
- locate the referenced node id in the JSON and verify it includes required fields (e.g., `class_type`)

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
