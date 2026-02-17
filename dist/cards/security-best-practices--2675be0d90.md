# security-best-practices

Perform language and framework specific security best-practice reviews and suggest improvements. Trigger only when the user explicitly requests security best practices guidance, a security review/report, or secure-by-default coding help. Trigger only for supported languages (python, javascript/typescript, go). Do not trigger for general code review, debugging, or non-security tasks.

## Quick Facts
- id: `security-best-practices--2675be0d90`
- worth_using_score: `40/100`
- tags: `python, typescript, security, testing, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/security-best-practices/SKILL.md`

## Workflow / Steps
- The primary mode is to just use the information to write secure by default code from this point forward. This is useful for starting a new project or when writing new code.
- The secondary mode is to passively detect vulnerabilities while working in the project and writing code for the user. Critical or very important vulnerabilities or major issues going against security guidance can be flagged and the user can be told about them. This passive mode should focus on the largest impact vulnerabilities and secure defaults.
- The user can ask for a security report or to improve the security of the codebase. In this case a full report should be produced describe anyways the project fails to follow security best practices guidance. The report should be prioritized and have clear sections of severity and urgency. Then offer to start working on fixes for these issues. See #fixes below.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
