# refactor

Surgical code refactoring to improve maintainability without changing behavior. Covers extracting functions, renaming variables, breaking down god functions, improving type safety, eliminating code smells, and applying design patterns. Less drastic than repo-rebuilder; use for gradual improvements.

## Quick Facts
- id: `refactor--4f640e2f77`
- worth_using_score: `65/100`
- tags: `git, ssh, go, testing, ci, rag, eval`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/refactor/SKILL.md`

## Use When
- Code is hard to understand or maintain
- Functions/classes are too large
- Code smells need addressing
- Adding features is difficult due to code structure
- User asks "clean up this code", "refactor this", "improve this"
- --

## Workflow / Steps
- PREPARE
- Ensure tests exist (write them if missing)
- Commit current state
- Create feature branch
- IDENTIFY
- Find the code smell to address
- Understand what the code does
- Plan the refactoring
- REFACTOR (small steps)
- Make one small change

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `16`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
