# writing-plans

Use when you have a spec or requirements for a multi-step task, before touching code

## Quick Facts
- id: `writing-plans--b940a8d8d9`
- worth_using_score: `50/100`
- tags: `python, testing, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/automation/devtools/superpowers/skills/writing-plans/SKILL.md`

## Workflow / Steps
- *Announce at start:** "I'm using the writing-plans skill to create the implementation plan."
- *Context:** This should be run in a dedicated worktree (created by brainstorming skill).
- *Save plans to:** `docs/plans/YYYY-MM-DD-<feature-name>.md`
- *Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step
- *Every plan MUST start with this header:**

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
