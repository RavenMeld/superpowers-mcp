# file-todos

This skill should be used when managing the file-based todo tracking system in the todos/ directory. It provides workflows for creating todos, managing status and dependencies, conducting triage, and integrating with slash commands and code review processes.

## Quick Facts
- id: `file-todos--054156fe07`
- worth_using_score: `58/100`
- tags: `ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/compound-engineering-plugin/plugins/compound-engineering/skills/file-todos/SKILL.md`

## Workflow / Steps
- *To create a new todo from findings or feedback:**
- Determine next issue ID: `ls todos/ | grep -o '^[0-9]\+' | sort -n | tail -1`
- Copy template: `cp assets/todo-template.md todos/{NEXT_ID}-pending-{priority}-{description}.md`
- Edit and fill required sections:
- Problem Statement
- Findings (if from investigation)
- Proposed Solutions (multiple options)
- Acceptance Criteria
- Add initial Work Log entry
- Determine status: `pending` (needs triage) or `ready` (pre-approved)

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `11`
- has_scripts: `False`
- has_references: `False`
- has_assets: `True`
