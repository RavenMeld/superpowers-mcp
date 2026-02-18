# docker-compose-troubleshooting

Run and debug multi-service dev stacks with Docker Compose: logs, exec, rebuilds, volumes, networking, and safe cleanup.

## Quick Facts
- id: `docker-compose-troubleshooting--5de2468ab8`
- worth_using_score: `70/100`
- tags: `docker, wsl, windows, linux`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/docker-compose-troubleshooting/SKILL.md`

## Use When
- A local dev stack (db + api + worker) won’t start.
- You need to inspect logs, env, and connectivity between services.
- You need safe cleanup without nuking unrelated Docker state.

## Workflow / Steps
- Start cleanly and watch logs.
- Identify the failing service (exit code, crash loop, healthcheck).
- Inspect container config (env, ports, volumes).
- Exec into the container to run the failing command manually.
- Fix the minimal root cause (config, deps, migrations) and restart.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `8`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
