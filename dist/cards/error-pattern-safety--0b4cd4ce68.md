# error-pattern-safety

Error Pattern Safety Guidelines for Agentic Engines

## Quick Facts
- id: `error-pattern-safety--0b4cd4ce68`
- worth_using_score: `55/100`
- tags: `testing, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/automation/devtools/gh-aw/skills/error-pattern-safety/SKILL.md`

## Workflow / Steps
- ```go
- // Test that pattern doesn't match empty string
- func TestPatternSafety(t *testing.T) {
- pattern := "your-pattern"
- regex := regexp.MustCompile(pattern)
- if regex.MatchString("") {

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `9`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
