# sora

Use when the user asks to generate, remix, poll, list, download, or delete Sora videos via OpenAI’s video API using the bundled CLI (`scripts/sora.py`), including requests like “generate AI video,” “Sora,” “video remix,” “download video/thumbnail/spritesheet,” and batch video generation; requires `OPENAI_API_KEY` and Sora API access.

## Quick Facts
- id: `sora--3b582ffd83`
- worth_using_score: `80/100`
- tags: `python, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/sora/SKILL.md`

## Use When
- Generate a new video clip from a prompt
- Remix an existing video by ID
- Poll status, list jobs, or download assets (video/thumbnail/spritesheet)
- Batch runs (many prompts or variants)

## Workflow / Steps
- Decide intent: create vs remix vs status/download vs batch.
- Collect inputs: prompt, model, size, seconds, and any input reference image.
- If batch: write a temporary JSONL under tmp/ (one job per line), run once, then delete the JSONL.
- Prefer CLI augmentation flags (`--use-case`, `--scene`, `--camera`, etc.) instead of pre-writing a structured prompt. If you already produced a structured prompt file, pass `--no-augment` to avoid double-wrapping.
- Run the bundled CLI (`scripts/sora.py`) with sensible defaults (see references/cli.md). For long prompts, prefer `--prompt-file` to avoid shell-escaping issues; pair with `--no-augment` if the prompt is already structured.
- For async jobs, poll until complete (or use create-and-poll).
- Download assets (video/thumbnail/spritesheet) and save locally.
- Remove intermediate files created during invocation (for example `prompt.txt`, `remix_job.json`, temp JSONL). If the sandbox blocks `rm`, skip cleanup or truncate the files without surfacing an error.
- Iterate with a single targeted change per prompt.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `True`
- has_references: `True`
- has_assets: `False`
