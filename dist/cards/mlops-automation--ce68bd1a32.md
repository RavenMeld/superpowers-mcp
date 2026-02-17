# MLOps Automation

Guide to refine MLOps projects with task automation, containerization, CI/CD pipelines, and robust experiment tracking.

## Quick Facts
- id: `mlops-automation--ce68bd1a32`
- worth_using_score: `35/100`
- tags: `github, python, docker, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/.agents/skills/fmind-mlops-automation/SKILL.md`

## Workflow / Steps
- **Platform**: ask for the company CI/CD platform, or use `github-actions` for GitHub.
- **Workflows**:
- `check.yml`: On PRs (Run `just check`).
- `publish.yml`: On Release (Build docker image, publish docs/package).
- **Optimization**: Use `concurrency` to cancel redundant runs.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
