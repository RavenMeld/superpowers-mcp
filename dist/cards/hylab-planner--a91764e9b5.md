# hylab-planner

Coverage planning for Hylab (pairwise/weighted planning, deterministic seeds, coverage metrics, directed sets). Use when implementing or modifying mod set planning or plan.json outputs.

## Quick Facts
- id: `hylab-planner--a91764e9b5`
- worth_using_score: `40/100`
- tags: `github, git, hytale, testing, ci, windows, rag`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/hylab-planner/SKILL.md`

## Workflow / Steps
- `paper.md` sections on planning and coverage strategy.
- `modlab.ps1` for current pairwise implementation.
- `references/hytale-policy.md` for official constraints and scope.
- `references/github-pairwise.md` for pairwise test design inspiration.
- Pairwise random groups (baseline).
- Weighted pairwise (risk-based or popularity-based weights).
- Directed sets (explicit user-provided combinations).
- Rolling windows (ordered load tests).
- Regression sets (known failing combos).
- Given the same input list, seed, and parameters, plan output must be stable.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
