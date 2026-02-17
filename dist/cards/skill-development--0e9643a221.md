# Skill Development

This skill should be used when the user wants to "create a skill", "add a skill to plugin", "write a new skill", "improve skill description", "organize skill content", or needs guidance on skill structure, progressive disclosure, or skill development best practices for Claude Code plugins.

## Quick Facts
- id: `skill-development--0e9643a221`
- worth_using_score: `55/100`
- tags: `mcp, python, testing, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/skill-development/SKILL.md`

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
- code_examples: `26`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
