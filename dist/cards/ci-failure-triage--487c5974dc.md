# ci-failure-triage

Diagnose CI failures and stabilize pipelines. Use when a mid-level developer needs to resolve flaky or failing builds.

## Quick Facts
- id: `ci-failure-triage--487c5974dc`
- worth_using_score: `50/100`
- tags: `mcp, git, python, node, go, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/spinnybot-selected/ci-failure-triage/SKILL.md`

## Use When
- A CI run is red and you need the actual root cause (not the cascade of follow-on failures).
- Tests are flaky and need stabilization without hiding real failures.

## Workflow / Steps
- Identify the first failure.
- Ignore later failures caused by missing outputs or early aborts.
- Classify the failure.
- Deterministic vs flaky.
- Unit vs integration vs E2E.
- Infra (network/rate limits) vs code (logic/parsing) vs environment (toolchain versions).
- Reproduce locally with the narrowest command.
- Prefer a single test file or a single script invocation.
- If reproduction requires external services, add a stubbed test first.
- Isolate the change that introduced it.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
