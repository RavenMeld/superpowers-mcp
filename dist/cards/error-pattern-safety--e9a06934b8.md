# error-pattern-safety

Error Pattern Safety Guidelines for Agentic Engines

## Quick Facts
- id: `error-pattern-safety--e9a06934b8`
- worth_using_score: `55/100`
- tags: `go, java, testing, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/error-pattern-safety/SKILL.md`

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
