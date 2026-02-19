# llm-prompt-regression-suite

Run prompt regression tests with golden cases, drift thresholds, and failure triage to keep LLM behavior stable.

## Quick Facts
- id: `llm-prompt-regression-suite--ae79af38a2`
- worth_using_score: `60/100`
- tags: `python, go, llm, eval, benchmark`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/llm-prompt-regression-suite/SKILL.md`

## Use When
- Prompt updates cause inconsistent output quality.
- You need before/after evidence for prompt changes.
- Model upgrades require behavior drift checks.

## Workflow / Steps
- Curate representative golden prompts and expected traits.
- Score outputs with deterministic rubric checks.
- Compare new runs against baseline thresholds.
- Classify failures by prompt design, model drift, or data shift.
- Gate prompt releases on regression score floors.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
