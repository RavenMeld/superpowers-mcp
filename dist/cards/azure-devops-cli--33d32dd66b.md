# azure-devops-cli

Manage Azure DevOps resources via CLI including projects, repos, pipelines, builds, pull requests, work items, artifacts, and service endpoints. Use when working with Azure DevOps, az commands, devops automation, CI/CD, or when user mentions Azure DevOps CLI.

## Quick Facts
- id: `azure-devops-cli--33d32dd66b`
- worth_using_score: `50/100`
- tags: `github, git, ssh, browser, go, docker, azure, security, ci, linux, devops, eval`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/azure-devops-cli/SKILL.md`

## Workflow / Steps
- -source-branch $CURRENT_BRANCH \
- -target-branch main \
- -title "Feature: $(git log -1 --pretty=%B)" \
- -open
- -title "Build $BUILD_BUILDNUMBER failed" \
- -type bug \
- -org $SYSTEM_TEAMFOUNDATIONCOLLECTIONURI \
- -project $SYSTEM_TEAMPROJECT
- -artifact-name 'webapp' \
- -path ./output \

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `187`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
