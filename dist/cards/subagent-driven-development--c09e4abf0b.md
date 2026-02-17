# subagent-driven-development

Use when executing implementation plans with independent tasks in the current session

## Quick Facts
- id: `subagent-driven-development--c09e4abf0b`
- worth_using_score: `65/100`
- tags: `ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/automation/devtools/superpowers/skills/subagent-driven-development/SKILL.md`

## Use When
- *vs. Executing Plans (parallel session):**
- Same session (no context switch)
- Fresh subagent per task (no context pollution)
- Two-stage review after each task: spec compliance first, then code quality
- Faster iteration (no human-in-loop between tasks)

## Workflow / Steps
- ```dot
- digraph process {
- rankdir=TB;
- subgraph cluster_per_task {
- label="Per Task";
- "Dispatch implementer subagent (./implementer-prompt.md)" [shape=box];

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
