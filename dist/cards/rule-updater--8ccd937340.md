# rule-updater

Skill for programmatically reading, updating, and creating Cursor rules based on patterns and lessons learned

## Quick Facts
- id: `rule-updater--8ccd937340`
- worth_using_score: `70/100`
- tags: `cursor, python, go, testing, ci, docs, rag`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/basedhardware-rule-updater/SKILL.md`

## Use When
- Updating existing rules with new examples or patterns
- Creating new rules for emerging patterns
- Identifying when rules need updating
- Testing rule effectiveness
- Organizing and maintaining rules

## Workflow / Steps
- *Updating a rule with new pattern**:
- **Identify pattern**: "Multiple PRs show missing context issue"
- **Read rule**: Read `.cursor/rules/context-communication.mdc`
- **Find section**: Find "PR Description Requirements" section
- **Add example**: Add example from recent PR
- **Enhance guidance**: Expand "What to Include" subsection
- **Update references**: Add link to new PR if relevant
- **Write rule**: Save updated rule file
- **Verify**: Check syntax and links
- *Creating new rule**:

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `7`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
