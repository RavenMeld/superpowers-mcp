# comfyui-core

Rules and guardrails for safe ComfyUI repo edits and operations (workflows, embedded workflow media, custom_nodes, models layout, dependencies, ComfyUI-Manager/comfy-cli usage, and server exposure). Use when working in a repo that contains ComfyUI workflows, custom nodes, ComfyUI-Manager config, comfy-cli usage, or ComfyUI model folders. Use only when the user explicitly mentions ComfyUI, Comfy...

## Quick Facts
- id: `comfyui-core--09746d6d8d`
- worth_using_score: `20/100`
- tags: `comfyui, python, node, security, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/comfyui-core/SKILL.md`

## Workflow / Steps
- `.json` exports, and/or
- `.png` / `.webp` / other media that embeds workflow metadata.
- `workflows/json/` for `.json`
- `workflows/embedded/` for `.png` / `.webp` (embedded workflows)
- Preserve node IDs, links, widget keys, and parameter names.
- If asked to connect nodes, change only link structure; do not reposition nodes unless explicitly requested.
- Do not mass-format, reorder keys, or rewrite large sections of workflow JSON without a clear request.
- Assume embedded workflow metadata may contain prompts, model names, paths, and other sensitive information.
- Do not publish or share embedded workflow media unless explicitly asked and the user understands it contains workflow metadata.
- If asked to remove or avoid embedded metadata, follow project conventions and documented options/tooling in that repo.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
