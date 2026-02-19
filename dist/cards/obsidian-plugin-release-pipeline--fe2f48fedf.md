# obsidian-plugin-release-pipeline

Release Obsidian plugins safely with versioning, changelog generation, packaging checks, and reproducible publish steps.

## Quick Facts
- id: `obsidian-plugin-release-pipeline--fe2f48fedf`
- worth_using_score: `60/100`
- tags: `git, ci, obsidian`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/obsidian-plugin-release-pipeline/SKILL.md`

## Use When
- You are preparing an Obsidian plugin release.
- You need a repeatable version/changelog/package workflow.
- A release failed and needs deterministic rerun steps.

## Workflow / Steps
- Verify working tree cleanliness and test status.
- Bump version in manifest and package metadata.
- Generate release notes from merged changes.
- Build distributable artifacts and verify checksums.
- Publish only after post-build smoke checks pass.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
