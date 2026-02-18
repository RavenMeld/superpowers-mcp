---
name: log-summarizer
description: Summarize noisy logs into likely causes and next steps. Use when a junior developer needs help interpreting logs.
---

# Log Summarizer

## When to use
- Logs are too long/noisy to reason about quickly.
- Multiple errors are present and you need to identify the “first domino”.

## Inputs to request
- Log snippet and time window (or full file path)
- Component/service name + version/commit SHA
- Any correlation context (run id, trace id, session name, terminal id)
- Recent changes (deploy/config/dependency update)

## Workflow
1. Build a timeline.
- Identify start, first warning, first error, then cascades.
2. Group by error signature.
- Same exception/class/message grouped together with counts.
3. Identify the earliest root-cause candidate.
- The error that explains the rest, not the loudest error.
4. Translate into actionable next steps.
- “Check X” and “run Y” style, with commands where possible.
5. Call out missing data.
- What extra logs/metrics would make this definitive next time.

## Outputs
- Top error groups (signature + count)
- Likely root cause (with evidence lines referenced)
- Next actions (fastest-to-validate first)

## Safety
- Redact secrets (API keys, auth headers, tokens).
- Don’t paste large logs when a summarized excerpt + file path is enough.

