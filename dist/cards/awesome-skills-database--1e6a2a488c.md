# awesome-skills-database

Use the local Awesome SKILLS database to quickly find and rank `SKILL.md` files.
Trigger when:
- the user asks "which skill should we use?"
- you need to search for the right `SKILL.md` across multiple roots
- you want a deterministic "worth using" ranking (not just text match)

## Quick Facts
- id: `awesome-skills-database--1e6a2a488c`
- worth_using_score: `60/100`
- tags: `mcp, python, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/.agents/skills/awesome-skills-database/SKILL.md`

## Use When
- You need the right `SKILL.md` fast (across multiple roots).
- You want a deterministic ranking that’s better than grep.
- You want to browse condensed cards before opening the full skill.

## Workflow / Steps
- Build (or refresh) the DB from one or more roots.
- Search with a short query.
- Open the top matching card and follow the referenced `SKILL.md`.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
