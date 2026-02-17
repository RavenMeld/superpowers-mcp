# speech

Use when the user asks for text-to-speech narration or voiceover, accessibility reads, audio prompts, or batch speech generation via the OpenAI Audio API; run the bundled CLI (`scripts/text_to_speech.py`) with built-in voices and require `OPENAI_API_KEY` for live calls. Custom voice creation is out of scope.

## Quick Facts
- id: `speech--8f24bf6cc3`
- worth_using_score: `65/100`
- tags: `python, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/speech/SKILL.md`

## Use When
- Generate a single spoken clip from text
- Generate a batch of prompts (many lines, many files)

## Workflow / Steps
- Decide intent: single vs batch (see decision tree above).
- Collect inputs up front: exact text (verbatim), desired voice, delivery style, format, and any constraints.
- If batch: write a temporary JSONL under tmp/ (one job per line), run once, then delete the JSONL.
- Augment instructions into a short labeled spec without rewriting the input text.
- Run the bundled CLI (`scripts/text_to_speech.py`) with sensible defaults (see references/cli.md).
- For important clips, validate: intelligibility, pacing, pronunciation, and adherence to constraints.
- Iterate with a single targeted change (voice, speed, or instructions), then re-check.
- Save/return final outputs and note the final text + instructions + flags used.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `True`
- has_references: `True`
- has_assets: `False`
