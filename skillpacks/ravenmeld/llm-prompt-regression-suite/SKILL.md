---
name: llm-prompt-regression-suite
description: |
  Run prompt regression tests with golden cases, drift thresholds, and failure triage to keep LLM behavior stable.
---

# LLM Prompt Regression Suite

## Use When

- Prompt updates cause inconsistent output quality.
- You need before/after evidence for prompt changes.
- Model upgrades require behavior drift checks.

## Workflow

1. Curate representative golden prompts and expected traits.
2. Score outputs with deterministic rubric checks.
3. Compare new runs against baseline thresholds.
4. Classify failures by prompt design, model drift, or data shift.
5. Gate prompt releases on regression score floors.

## Copy/Paste Examples

```bash
python -m awesome_skills search "prompt engineering patterns"
```

```bash
python -m awesome_skills search "llm evaluation"
```

```bash
rg -n "golden|baseline|regression|rubric" .
```

## Regression Rules

- Keep goldens task-diverse and periodically refreshed.
- Track both pass/fail and quality trend deltas.
- Store run metadata (model/version/prompt hash) for audits.

## Safety Notes

- Do not optimize only for benchmark-like prompts.
- Keep sensitive user data out of test corpora.
