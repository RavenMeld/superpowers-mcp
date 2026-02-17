# pdf

Use when tasks involve reading, creating, or reviewing PDF files where rendering and layout matter; prefer visual checks by rendering pages (Poppler) and use Python tools such as `reportlab`, `pdfplumber`, and `pypdf` for generation and extraction.

## Quick Facts
- id: `pdf--b17d45eba8`
- worth_using_score: `50/100`
- tags: `python, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/pdf/SKILL.md`

## Use When
- Read or review PDF content where layout and visuals matter.
- Create PDFs programmatically with reliable formatting.
- Validate final rendering before delivery.

## Workflow / Steps
- Prefer visual review: render PDF pages to PNGs and inspect them.
- Use `pdftoppm` if available.
- If unavailable, install Poppler or ask the user to review the output locally.
- Use `reportlab` to generate PDFs when creating new documents.
- Use `pdfplumber` (or `pypdf`) for text extraction and quick checks; do not rely on it for layout fidelity.
- After each meaningful update, re-render pages and verify alignment, spacing, and legibility.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `4`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
