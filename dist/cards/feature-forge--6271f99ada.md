# feature-forge

Use when defining new features, gathering requirements, or writing specifications. Invoke for feature definition, requirements gathering, user stories, EARS format specs.

## Quick Facts
- id: `feature-forge--6271f99ada`
- worth_using_score: `55/100`
- tags: `security, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/claude-skills/skills/feature-forge/SKILL.md`

## Use When
- Defining new features from scratch
- Gathering comprehensive requirements
- Writing specifications in EARS format
- Creating acceptance criteria
- Planning implementation TODO lists

## Workflow / Steps
- **Discover** - Use `AskUserQuestions` to understand the feature goal, target users, and user value. Present structured choices where possible (e.g., user types, priority level).
- **Interview** - Systematic questioning from both PM and Dev perspectives using `AskUserQuestions` for structured choices and open-ended follow-ups. Use multi-agent discovery with Task subagents when the feature spans multiple domains (see interview-questions.md for guidance).
- **Document** - Write EARS-format requirements
- **Validate** - Use `AskUserQuestions` to review acceptance criteria with stakeholder, presenting key trade-offs as structured choices
- **Plan** - Create implementation checklist

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
