---
name: ticket-breakdown
description: Break a task or ticket into small steps. Use when a junior developer needs guidance on how to start.
---

# Ticket Breakdown

## When to use
- The task is vague and you need a concrete implementation plan.
- The work spans multiple repos/components and needs sequencing.

## Inputs to request
- Ticket goal + acceptance criteria
- Constraints (time, scope, “don’t change X”, compatibility)
- Target code paths (if known)

## Workflow
1. Rewrite the ticket as acceptance criteria.
- What must be true for “done”.
2. Decompose into steps (small and testable).
- Each step should have an owner file/path and a validation command.
3. Identify dependencies and ordering.
- What blocks what.
4. Define a test plan.
- Unit tests, integration tests, smoke tests.
5. Decide rollout/guardrails.
- Feature flags, safe defaults, logging, and rollback plan if needed.

## Outputs
- A step-by-step plan (3-10 steps) with validation per step
- A short risk list + mitigations
- Open questions that must be answered before implementation

