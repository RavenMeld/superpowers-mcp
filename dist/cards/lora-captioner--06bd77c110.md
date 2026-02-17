# lora-captioner

Plan-first workflow for creating detailed image captions for AI/LoRA training datasets, including per-image .txt files, trigger-word inclusion, and batch processing of local image folders.

## Quick Facts
- id: `lora-captioner--06bd77c110`
- worth_using_score: `35/100`
- tags: `ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/lora-captioner-skill/SKILL.md`

## Workflow / Steps
- **Plan first**
- State a brief plan before writing any files.
- Confirm the target folder and image extensions.
- **Collect required inputs**
- Ask for the **trigger word** (do not assume or hardcode it).
- Ask for **overwrite policy**: overwrite existing .txt, skip if exists, or write .new.txt.
- Ask for **caption style** if not provided: high-detail comma tags (default).
- **Enumerate images**
- List image files in the target folder (`.png`, `.jpg`, `.jpeg`, `.webp`, `.bmp`).
- Sort by filename for deterministic order.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
