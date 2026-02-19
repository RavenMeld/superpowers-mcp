# playwright-network-chaos-suite

Stress Playwright E2E flows with network latency, failures, and offline scenarios to harden client behavior.

## Quick Facts
- id: `playwright-network-chaos-suite--47ec63065b`
- worth_using_score: `60/100`
- tags: `playwright, testing`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/playwright-network-chaos-suite/SKILL.md`

## Use When
- UI behavior breaks under slow/unstable network.
- Retries and fallback UX are untested.
- You need resilience gates before release.

## Workflow / Steps
- Identify critical user journeys for resilience testing.
- Inject latency, timeout, and intermittent failure scenarios.
- Validate fallback UI states and retry controls.
- Verify telemetry/error reporting under degraded conditions.
- Promote fixes into standard regression suite.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
