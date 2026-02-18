# readme-polish

Improve a README for clarity and completeness. Use when a junior developer needs guidance on documenting setup and usage.

## Quick Facts
- id: `readme-polish--f0801e5600`
- worth_using_score: `45/100`
- tags: `git, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/spinnybot-selected/readme-polish/SKILL.md`

## Use When
- README is missing “how do I run this” or “how do I test this”.
- Setup is tribal knowledge and needs to be made reproducible.

## Workflow / Steps
- Add a “Quick Start” that works.
- Install, run, smoke in the smallest number of steps.
- Document configuration.
- Required env vars, optional tuning vars, defaults, and examples.
- Add validation commands.
- `npm test`, `pytest`, smoke scripts, and expected outputs.
- Add troubleshooting.
- 3-5 top failure modes and how to diagnose them.
- Keep it honest.
- If something is optional or flaky, say so and explain why.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
