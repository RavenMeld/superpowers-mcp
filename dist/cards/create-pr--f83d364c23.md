# create-pr

Creates GitHub pull requests with properly formatted titles that pass the check-pr-title CI validation. Use when creating PRs, submitting changes for review, or when the user says /pr or asks to create a pull request.

## Quick Facts
- id: `create-pr--f83d364c23`
- worth_using_score: `55/100`
- tags: `github, node, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/create-pr/SKILL.md`

## Workflow / Steps
- **Check current state**:
- **Analyze changes** to determine:
- Type: What kind of change is this?
- Scope: Which package/area is affected?
- Summary: What does the change do?
- **Push branch if needed**:
- **Create PR** using gh CLI with the template from `.github/pull_request_template.md`:

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `8`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
