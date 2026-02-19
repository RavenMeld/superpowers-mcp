# hytale-mod-ci

Add CI checks for Hytale mods: lint, build, package validation, and release gates.

## Quick Facts
- id: `hytale-mod-ci--8289e6f049`
- worth_using_score: `60/100`
- tags: `git, hytale, rust, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/hytale-mod-ci/SKILL.md`

## Use When
- You want automated quality gates for Hytale mods.
- Manual mod packaging is error-prone and inconsistent.
- You need confidence before publishing mod updates.

## Workflow / Steps
- Run lint and static checks on every pull request.
- Build mod package in a clean CI environment.
- Validate produced artifact structure and metadata.
- Execute smoke integration checks on sample content.
- Gate release tags on successful CI + changelog presence.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
