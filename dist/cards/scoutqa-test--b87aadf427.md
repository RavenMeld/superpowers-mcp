# scoutqa-test

|

## Quick Facts
- id: `scoutqa-test--b87aadf427`
- worth_using_score: `55/100`
- tags: `security, testing, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/scoutqa-test/SKILL.md`

## Use When
- **User requests testing** - When the user explicitly asks to test a website or verify functionality
- **Proactive verification** - After implementing web features, automatically run tests to verify the implementation works correctly
- *Example proactive usage:**
- After implementing a login form → Test the authentication flow
- After adding form validation → Verify validation rules and error handling
- After building a checkout flow → Test the end-to-end purchase process
- After fixing a bug → Verify the fix works and didn't break other features
- *Best practice**: When you finish implementing a web feature, proactively start a ScoutQA test in the background to verify it works while you continue with other tasks.

## Workflow / Steps
- [ ] Write specific test prompt with clear expectations
- [ ] Run scoutqa command in background
- [ ] Inform user of execution ID and browser URL
- [ ] Extract and analyze results
- *Step 1: Write specific test prompt**
- *Step 2: Run scoutqa command**
- *IMPORTANT**: Use the Bash tool's timeout parameter (5000ms = 5 seconds) to capture execution details:
- This is the Bash tool's built-in timeout parameter in Claude Code (NOT the Unix `timeout` command)
- After 5 seconds, the Bash tool returns control with a task ID and the process continues running in the background
- This is different from Unix `timeout` which kills the process - here the process keeps running

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `15`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
