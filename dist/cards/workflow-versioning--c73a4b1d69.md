# workflow-versioning

Versioning and review discipline for ComfyUI workflows (JSON + embedded workflow media). Use only when the user mentions ComfyUI workflows, workflow JSON/PNG, or ComfyUI repo paths.

## Quick Facts
- id: `workflow-versioning--c73a4b1d69`
- worth_using_score: `35/100`
- tags: `comfyui, node, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/workflow-versioning/SKILL.md`

## Workflow / Steps
- Treat JSON exports as the canonical, diff-friendly artifact.
- Keep changes minimal and intentional.
- Store JSON workflows as the source of truth.
- Store embedded-workflow media separately (for sharing), not as the primary source.
- Avoid pretty-printing or key reordering; preserve minimal diffs.
- Use descriptive, stable filenames (e.g., `sdxl_portrait_v3.json`).
- Include purpose and version in the filename or a short changelog nearby.
- Prefer `workflows/json/` and `workflows/embedded/` if the repo uses those folders.
- One logical change per commit (e.g., change sampler OR add node pack, not both).
- Preserve node IDs and input names unless a breaking change is intended.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
