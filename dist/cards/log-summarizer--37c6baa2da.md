# log-summarizer

Summarize noisy logs into likely causes and next steps. Use when a junior developer needs help interpreting logs.

## Quick Facts
- id: `log-summarizer--37c6baa2da`
- worth_using_score: `45/100`
- tags: `terminal`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/spinnybot-selected/log-summarizer/SKILL.md`

## Use When
- Logs are too long/noisy to reason about quickly.
- Multiple errors are present and you need to identify the “first domino”.

## Workflow / Steps
- Build a timeline.
- Identify start, first warning, first error, then cascades.
- Group by error signature.
- Same exception/class/message grouped together with counts.
- Identify the earliest root-cause candidate.
- The error that explains the rest, not the loudest error.
- Translate into actionable next steps.
- “Check X” and “run Y” style, with commands where possible.
- Call out missing data.
- What extra logs/metrics would make this definitive next time.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
