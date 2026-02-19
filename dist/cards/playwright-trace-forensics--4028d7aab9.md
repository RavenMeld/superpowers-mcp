# playwright-trace-forensics

Perform deep Playwright failure forensics from trace artifacts, network logs, and console/runtime errors.

## Quick Facts
- id: `playwright-trace-forensics--4028d7aab9`
- worth_using_score: `60/100`
- tags: `playwright, browser, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/playwright-trace-forensics/SKILL.md`

## Use When
- A CI failure needs precise proof of what happened in browser state.
- You have trace artifacts but no clear diagnosis yet.
- A regression only reproduces under CI timing/network conditions.

## Workflow / Steps
- Open the failing trace and map each action to assertion failure.
- Inspect network waterfall for blocked/failed requests.
- Correlate console/runtime errors with the failing step timestamp.
- Classify failure type: selector drift, race, auth/session, backend error.
- Produce minimal code fix plus a regression assertion.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
