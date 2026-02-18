# llm-evaluation-harness

Build a lightweight, repeatable evaluation harness for LLM/agent behavior: test cases, golden outputs, scoring rubrics, and regression gates.

## Quick Facts
- id: `llm-evaluation-harness--6086851fcb`
- worth_using_score: `65/100`
- tags: `github, git, ssh, python, go, ci, wsl, llm, eval`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/llm-evaluation-harness/SKILL.md`

## Use When
- You’re changing prompts/tools/agents and want to prevent regressions.
- You need a “good enough” eval loop before investing in heavy infra.
- You want measurable progress (not vibes).

## Workflow / Steps
- Define a small test set (10-50 tasks) that represent real usage.
- Add a rubric per task (what “good” means).
- Run the suite on every change (CI or local).
- Save artifacts (inputs, outputs, scores, model/version metadata).
- When something regresses: isolate, fix, and add a new test.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
