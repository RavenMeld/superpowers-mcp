# semgrep

Run Semgrep static analysis scan on a codebase using parallel subagents. Automatically

## Quick Facts
- id: `semgrep--681c2de3e4`
- worth_using_score: `80/100`
- tags: `github, git, python, sql, typescript, node, rust, go, java, docker, kubernetes, security, ci, docs, terraform, eval`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/trailofbits-semgrep/SKILL.md`

## Use When
- Security audit of a codebase
- Finding vulnerabilities before code review
- Scanning for known bug patterns
- First-pass static analysis

## Workflow / Steps
- *Step 3 is a HARD GATE**: Mark as `completed` ONLY after user says "yes", "proceed", "approved", or equivalent.
- Create all 6 tasks with dependencies
- TaskUpdate Step 1 → in_progress, execute detection
- TaskUpdate Step 1 → completed
- TaskUpdate Step 2 → in_progress, select rulesets
- TaskUpdate Step 2 → completed
- TaskUpdate Step 3 → in_progress, present plan with rulesets
- STOP: Wait for user response (may modify rulesets)
- User approves → TaskUpdate Step 3 → completed
- TaskUpdate Step 4 → in_progress (now unblocked)

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `12`
- has_scripts: `True`
- has_references: `True`
- has_assets: `False`
