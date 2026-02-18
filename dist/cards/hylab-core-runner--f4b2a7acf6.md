# hylab-core-runner

Cross-platform runner lifecycle for Hylab (server start/stop, process trees, timeouts, log capture, port allocation, parallelism, templates, AOT cache). Use when implementing or modifying Hylab's core runner or OS-specific wrappers.

## Quick Facts
- id: `hylab-core-runner--f4b2a7acf6`
- worth_using_score: `40/100`
- tags: `github, git, rust, ci, windows`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/hylab-core-runner/SKILL.md`

## Workflow / Steps
- Create `run/<runId>/test-XXXX/` folder.
- Copy template to test server folder.
- Copy mod files into `server/mods`.
- Compose JVM args (Xms/Xmx, AOT cache, assets zip, auth mode).
- Start the process and capture stdout/stderr.
- Monitor logs for ready/error patterns and a hard timeout.
- Stop the process and record a result.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
