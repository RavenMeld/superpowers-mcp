# create-skill

Create new skills for Claude Code. Use when users ask to create a skill, add a skill, make a new command, build a skill, add a slash command, create a plugin skill, or define a new automation. Trigger phrases include "create a skill", "new skill", "add a skill", "make a command", "build a skill", "I want a skill that", "add slash command", "create automation".

## Quick Facts
- id: `create-skill--3da64e538b`
- worth_using_score: `30/100`
- tags: `ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/claudeclaw/skills/create-skill/SKILL.md`

## Workflow / Steps
- Ask the user conversationally what the skill should do, what scope (project or global), and what name they want. Suggest ideas based on context.
- Based on their answers, generate the `SKILL.md` content:
- Write a clear, descriptive `name` in kebab-case
- Write a `description` with plenty of trigger phrases so Claude knows when to activate it
- Write detailed body instructions for what Claude should do
- Create the skill:
- **Project level**: Write to `skills/<skill-name>/SKILL.md` relative to project root
- **Global level**: Write to `~/.claude/skills/<skill-name>/SKILL.md`
- Confirm creation and show the user:
- The skill name and path

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `1`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
