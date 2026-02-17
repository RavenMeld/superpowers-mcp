# exploring-data

Exploratory data analysis using ydata-profiling. Use when users upload .csv/.xlsx/.json/.parquet files or request "explore data", "analyze dataset", "EDA", "profile data". Generates interactive HTML or JSON reports with statistics, visualizations, correlations, and quality alerts.

## Quick Facts
- id: `exploring-data--97dc227dc0`
- worth_using_score: `65/100`
- tags: `python`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/exploring-data/SKILL.md`

## Workflow / Steps
- *Defaults:** minimal + html (also generates JSON)
- *Output:**
- `eda_report.html` - Interactive report for user
- `eda_report.json` - Machine-readable for Claude analysis
- *Reads:** `eda_report.json` (comprehensive ydata output)
- *Writes:** `eda_insights_summary.md` (condensed for Claude)
- *Outputs to stdout:** Formatted markdown summary

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `True`
- has_references: `True`
- has_assets: `False`
