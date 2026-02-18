# bootstrap

Bootstrap Warp terminal configuration for Rails projects. Creates launch configurations with colored tabs for dev server, Claude, shell, and more. This skill should be used when setting up Warp for a Rails project. Triggers on "setup warp", "configure warp", "warp rails", "warp bootstrap", "terminal setup for rails", "warp-rails".

## Quick Facts
- id: `bootstrap--dfdb2e61e3`
- worth_using_score: `55/100`
- tags: `warp, terminal, go, docs, windows`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/aviflombaum-bootstrap/SKILL.md`

## Workflow / Steps
- Execute these steps IN ORDER. Do not skip steps.
- ### Step 1: Verify Rails Project
- Run this command:
- ```bash
- test -f config/application.rb && echo "RAILS PROJECT" || echo "NOT RAILS"
- ```

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `4`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
