# github-issues

Create, update, and manage GitHub issues using MCP tools. Use this skill when users want to create bug reports, feature requests, or task issues, update existing issues, add labels/assignees/milestones, or manage issue workflows. Triggers on requests like "create an issue", "file a bug", "request a feature", "update issue X", or any GitHub issue management task.

## Quick Facts
- id: `github-issues--3dcbcfee8e`
- worth_using_score: `55/100`
- tags: `mcp, github, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/github-issues/SKILL.md`

## Workflow / Steps
- **Determine action**: Create, update, or query?
- **Gather context**: Get repo info, existing labels, milestones if needed
- **Structure content**: Use appropriate template from [references/templates.md](references/templates.md)
- **Execute**: Call the appropriate MCP tool
- **Confirm**: Report the issue URL to user

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
