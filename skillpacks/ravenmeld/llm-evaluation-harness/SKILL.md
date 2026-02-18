---
name: llm-evaluation-harness
description: |
  Build a lightweight, repeatable evaluation harness for LLM/agent behavior: test cases, golden outputs, scoring rubrics, and regression gates.
---

# LLM Evaluation Harness

## Use When

- You’re changing prompts/tools/agents and want to prevent regressions.
- You need a “good enough” eval loop before investing in heavy infra.
- You want measurable progress (not vibes).

## Workflow

1. Define a small test set (10-50 tasks) that represent real usage.
2. Add a rubric per task (what “good” means).
3. Run the suite on every change (CI or local).
4. Save artifacts (inputs, outputs, scores, model/version metadata).
5. When something regresses: isolate, fix, and add a new test.

## Minimal Test Case Structure (Recommended)

```json
{
  "id": "ssh-keygen-wsl",
  "prompt": "Create a second GitHub SSH key in WSL without breaking the first.",
  "checks": [
    {"type": "must_include", "text": "ssh-keygen -t ed25519"},
    {"type": "must_include", "text": "Host github-ravenmeld"},
    {"type": "must_not_include", "text": "private key"}
  ]
}
```

## Scoring Ideas (Practical)

- Hard checks:
  - must include key commands
  - must not leak secrets
  - must produce syntactically valid JSON/YAML when required
- Soft checks:
  - step order is correct
  - avoids dangerous commands unless asked
  - includes verification step

## Example: CLI Skeleton

Run a small JSON suite and print failures:

```bash
python eval.py --suite evals/smoke.json --out evals/out/latest.json
```

Track deltas:

```bash
python eval_diff.py --baseline evals/out/baseline.json --candidate evals/out/latest.json
```

## Safety Notes

- Redact tokens/keys in logs (store raw outputs only in secure locations).
- Prefer deterministic tool outputs when possible (pin versions, stable inputs).

