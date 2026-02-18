# ticket-breakdown

Break a task or ticket into small steps. Use when a junior developer needs guidance on how to start.

## Quick Facts
- id: `ticket-breakdown--1534be8e92`
- worth_using_score: `45/100`
- tags: `go, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/spinnybot-selected/ticket-breakdown/SKILL.md`

## Use When
- The task is vague and you need a concrete implementation plan.
- The work spans multiple repos/components and needs sequencing.

## Workflow / Steps
- Rewrite the ticket as acceptance criteria.
- What must be true for “done”.
- Decompose into steps (small and testable).
- Each step should have an owner file/path and a validation command.
- Identify dependencies and ordering.
- What blocks what.
- Define a test plan.
- Unit tests, integration tests, smoke tests.
- Decide rollout/guardrails.
- Feature flags, safe defaults, logging, and rollback plan if needed.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
