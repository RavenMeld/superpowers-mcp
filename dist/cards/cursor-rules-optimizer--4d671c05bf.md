# cursor-rules-optimizer

Improve Cursor rules using observed failure patterns, repeated review comments, and workflow friction points.

## Quick Facts
- id: `cursor-rules-optimizer--4d671c05bf`
- worth_using_score: `60/100`
- tags: `git, cursor, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/cursor-rules-optimizer/SKILL.md`

## Use When
- Cursor suggestions repeatedly violate local standards.
- PR reviews show recurring mistakes that rules should prevent.
- You want a measurable loop for improving `.cursor/rules` quality.

## Workflow / Steps
- Collect recurring failure patterns from recent diffs/reviews.
- Convert each pattern into a concrete rule with an example.
- Keep rules short, testable, and scoped to repository conventions.
- Validate rule impact on a small batch of representative tasks.
- Keep a changelog for rule additions/removals and observed impact.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
