# doc

Use when the task involves reading, creating, or editing `.docx` documents, especially when formatting or layout fidelity matters; prefer `python-docx` plus the bundled `scripts/render_docx.py` for visual checks.

## Quick Facts
- id: `doc--bbcd83bf3f`
- worth_using_score: `65/100`
- tags: `python, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/doc/SKILL.md`

## Use When
- Read or review DOCX content where layout matters (tables, diagrams, pagination).
- Create or edit DOCX files with professional formatting.
- Validate visual layout before delivery.

## Workflow / Steps
- Prefer visual review (layout, tables, diagrams).
- If `soffice` and `pdftoppm` are available, convert DOCX -> PDF -> PNGs.
- Or use `scripts/render_docx.py` (requires `pdf2image` and Poppler).
- If these tools are missing, install them or ask the user to review rendered pages locally.
- Use `python-docx` for edits and structured creation (headings, styles, tables, lists).
- After each meaningful change, re-render and inspect the pages.
- If visual review is not possible, extract text with `python-docx` as a fallback and call out layout risk.
- Keep intermediate outputs organized and clean up after final approval.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `6`
- has_scripts: `True`
- has_references: `False`
- has_assets: `False`
