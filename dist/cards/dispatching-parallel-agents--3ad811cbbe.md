# dispatching-parallel-agents

Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies

## Quick Facts
- id: `dispatching-parallel-agents--3ad811cbbe`
- worth_using_score: `55/100`
- tags: `typescript, testing, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/dispatching-parallel-agents/SKILL.md`

## Use When
- *Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations
- *Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `False`
- code_examples: `4`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
