---
name: readme-polish
description: Improve a README for clarity and completeness. Use when a junior developer needs guidance on documenting setup and usage.
---

# README Polish

## When to use
- README is missing “how do I run this” or “how do I test this”.
- Setup is tribal knowledge and needs to be made reproducible.

## Inputs to request
- Current README content
- Expected audience (new contributor vs user)
- Prereqs and common failure modes

## Workflow
1. Add a “Quick Start” that works.
- Install, run, smoke in the smallest number of steps.
2. Document configuration.
- Required env vars, optional tuning vars, defaults, and examples.
3. Add validation commands.
- `npm test`, `pytest`, smoke scripts, and expected outputs.
4. Add troubleshooting.
- 3-5 top failure modes and how to diagnose them.
5. Keep it honest.
- If something is optional or flaky, say so and explain why.

## Outputs
- A concrete patch list (sections to add/change)
- Copy/paste examples and commands

## Stack Notes (agent_playground)
- If documenting multi-repo workflows, note that each repo is pushed independently (workspace root is not a git repo).

