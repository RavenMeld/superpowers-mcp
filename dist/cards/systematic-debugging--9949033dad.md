# systematic-debugging

Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes

## Quick Facts
- id: `systematic-debugging--9949033dad`
- worth_using_score: `60/100`
- tags: `security, testing, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/systematic-debugging/SKILL.md`

## Use When
- Test failures
- Bugs in production
- Unexpected behavior
- Performance problems
- Build failures
- Integration issues
- *Use this ESPECIALLY when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- You've already tried multiple fixes

## Workflow / Steps
- echo "=== Secrets available in workflow: ==="
- echo "IDENTITY: ${IDENTITY:+SET}${IDENTITY:-UNSET}"

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `1`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
