# transcribe

Transcribe audio files to text with optional diarization and known-speaker hints. Use when a user asks to transcribe speech from audio/video, extract text from recordings, or label speakers in interviews or meetings.

## Quick Facts
- id: `transcribe--2a1c42dc48`
- worth_using_score: `58/100`
- tags: `python, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/transcribe/SKILL.md`

## Workflow / Steps
- Collect inputs: audio file path(s), desired response format (text/json/diarized_json), optional language hint, and any known speaker references.
- Verify `OPENAI_API_KEY` is set. If missing, ask the user to set it locally (do not ask them to paste the key).
- Run the bundled `transcribe_diarize.py` CLI with sensible defaults (fast text transcription).
- Validate the output: transcription quality, speaker labels, and segment boundaries; iterate with a single targeted change if needed.
- Save outputs under `output/transcribe/` when working in this repo.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `6`
- has_scripts: `True`
- has_references: `True`
- has_assets: `True`
