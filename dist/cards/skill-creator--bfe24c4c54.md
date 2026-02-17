# skill-creator

Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

## Quick Facts
- id: `skill-creator--bfe24c4c54`
- worth_using_score: `45/100`
- tags: `python, testing, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/compound-engineering-plugin/plugins/compound-engineering/skills/skill-creator/SKILL.md`

## Workflow / Steps
- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"
- Considering how to execute on the example from scratch
- Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly
- Rotating a PDF requires re-writing the same code each time
- A `scripts/rotate_pdf.py` script would be helpful to store in the skill
- Writing a frontend webapp requires the same boilerplate HTML/React each time
- An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `4`
- has_scripts: `True`
- has_references: `False`
- has_assets: `False`
