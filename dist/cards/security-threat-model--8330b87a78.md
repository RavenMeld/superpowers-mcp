# security-threat-model

Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations, and writes a concise Markdown threat model. Trigger only when the user explicitly asks to threat model a codebase or path, enumerate threats/abuse paths, or perform AppSec threat modeling. Do not trigger for general architecture summaries, code review, or non-securi...

## Quick Facts
- id: `security-threat-model--8330b87a78`
- worth_using_score: `40/100`
- tags: `rust, go, security, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/security-threat-model/SKILL.md`

## Workflow / Steps
- Identify primary components, data stores, and external integrations from the repo summary.
- Identify how the system runs (server, CLI, library, worker) and its entrypoints.
- Separate runtime behavior from CI/build/dev tooling and from tests/examples.
- Map the in-scope locations to those components and exclude out-of-scope items explicitly.
- Do not claim components, flows, or controls without evidence.
- Enumerate trust boundaries as concrete edges between components, noting protocol, auth, encryption, validation, and rate limiting.
- List assets that drive risk (data, credentials, models, config, compute resources, audit logs).
- Identify entry points (endpoints, upload surfaces, parsers/decoders, job triggers, admin tooling, logging/error sinks).
- List the assets that drive risk (credentials, PII, integrity-critical state, availability-critical components, build artifacts).
- Describe realistic attacker capabilities based on exposure and intended usage.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
