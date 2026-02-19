# chrome-firefox-profile-manager

Manage Chrome and Firefox automation profiles safely for repeatable browser tests and debugging sessions.

## Quick Facts
- id: `chrome-firefox-profile-manager--cb35f16c42`
- worth_using_score: `60/100`
- tags: `playwright, browser, chrome, firefox, go, ci, rag`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/chrome-firefox-profile-manager/SKILL.md`

## Use When
- You need stable browser state between automation runs.
- Tests fail due to stale cookies/storage/profile drift.
- You want clean profile isolation for Chrome and Firefox debugging.

## Workflow / Steps
- Create dedicated test profiles per browser and environment.
- Start tests against isolated user-data/profile directories.
- Reset profile state before critical regression runs.
- Keep session fixtures explicit (cookies, localStorage, auth seeds).
- Archive known-good profiles for reproducible bug repro.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
