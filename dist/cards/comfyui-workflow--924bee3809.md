# comfyui-workflow

How to load, edit, validate, share, and reuse ComfyUI workflows (JSON + embedded workflow media) without breaking graphs or leaking metadata. Use when creating or refactoring workflow graphs, importing/exporting JSON or embedded media, sharing workflows safely, or validating workflows via the server/API queue. Use only when the user explicitly mentions ComfyUI, ComfyUI workflows, custom_nodes,...

## Quick Facts
- id: `comfyui-workflow--924bee3809`
- worth_using_score: `30/100`
- tags: `comfyui, node, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/comfyui-workflow/SKILL.md`

## Workflow / Steps
- ComfyUI stores workflows in metadata of generated images; workflows can also be stored as JSON text files suitable for versioning and sharing.
- Exported media can carry metadata so others can drag-and-drop to rebuild the full workflow.
- JSON workflows are typically obtained via an export or download action in the UI and then re-imported.
- Treat JSON as the canonical, versionable artifact.
- Drag-and-drop an output image back into the ComfyUI canvas to load the embedded workflow.
- For editing embedded workflow metadata in place (before sharing), use the embedded workflow editor tooling if present in the repo/tooling.
- Prefer sharing `workflows/*.json` for collaboration and version control (small, text, diffable).
- Embedded-media sharing is convenient for end users, but it can leak prompts, paths, and full graph logic. Treat it as sensitive.
- Assume embedded workflow metadata can expose private prompts and paths.
- If the user wants to share an image without workflow metadata, use a launch option such as `--disable-metadata` when supported by the local build.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `True`
- has_references: `False`
- has_assets: `False`
