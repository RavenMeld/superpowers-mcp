# imagegen

Use when the user asks to generate or edit images via the OpenAI Image API (for example: generate image, edit/inpaint/mask, background removal or replacement, transparent background, product shots, concept art, covers, or batch variants); run the bundled CLI (`scripts/image_gen.py`) and require `OPENAI_API_KEY` for live calls.

## Quick Facts
- id: `imagegen--fd300907ba`
- worth_using_score: `65/100`
- tags: `python, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/imagegen/SKILL.md`

## Use When
- Generate a new image (concept art, product shot, cover, website hero)
- Edit an existing image (inpainting, masked edits, lighting or weather transformations, background replacement, object removal, compositing, transparent background)
- Batch runs (many prompts, or many variants across prompts)

## Workflow / Steps
- Decide intent: generate vs edit vs batch (see decision tree above).
- Collect inputs up front: prompt(s), exact text (verbatim), constraints/avoid list, and any input image(s)/mask(s). For multi-image edits, label each input by index and role; for edits, list invariants explicitly.
- If batch: write a temporary JSONL under tmp/ (one job per line), run once, then delete the JSONL.
- Augment prompt into a short labeled spec (structure + constraints) without inventing new creative requirements.
- Run the bundled CLI (`scripts/image_gen.py`) with sensible defaults (see references/cli.md).
- For complex edits/generations, inspect outputs (open/view images) and validate: subject, style, composition, text accuracy, and invariants/avoid items.
- Iterate: make a single targeted change (prompt or mask), re-run, re-check.
- Save/return final outputs and note the final prompt + flags used.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `True`
- has_references: `True`
- has_assets: `False`
