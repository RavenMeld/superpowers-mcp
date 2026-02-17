# spreadsheet

Use when tasks involve creating, editing, analyzing, or formatting spreadsheets (`.xlsx`, `.csv`, `.tsv`) using Python (`openpyxl`, `pandas`), especially when formulas, references, and formatting need to be preserved and verified.

## Quick Facts
- id: `spreadsheet--cb653911c9`
- worth_using_score: `55/100`
- tags: `python, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/spreadsheet/SKILL.md`

## Use When
- Build new workbooks with formulas, formatting, and structured layouts.
- Read or analyze tabular data (filter, aggregate, pivot, compute metrics).
- Modify existing workbooks without breaking formulas or references.
- Visualize data with charts/tables and sensible formatting.

## Workflow / Steps
- Confirm the file type and goals (create, edit, analyze, visualize).
- Use `openpyxl` for `.xlsx` edits and `pandas` for analysis and CSV/TSV workflows.
- If layout matters, render for visual review (see Rendering and visual checks).
- Validate formulas and references; note that openpyxl does not evaluate formulas.
- Save outputs and clean up intermediate files.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
