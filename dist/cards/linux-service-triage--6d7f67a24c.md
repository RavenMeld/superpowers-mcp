# linux-service-triage

Diagnoses common Linux service issues using logs, systemd/PM2, file permissions, Nginx reverse proxy checks, and DNS sanity checks. Use when a server app is failing, unreachable, or misconfigured.

## Quick Facts
- id: `linux-service-triage--6d7f67a24c`
- worth_using_score: `65/100`
- tags: `ci, linux`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/openclaw-linux-service-triage/SKILL.md`

## Use When
- TRIGGERS:
- Show me why this service is failing using logs, then give the exact fix commands.
- Restart this app cleanly and confirm it is listening on the right port.
- Fix the permissions on this folder so the service can read and write safely.
- Set up Nginx reverse proxy for this port and verify DNS and TLS are sane.
- Create a systemd service for this script and make it survive reboots.
- DO NOT USE WHEN…
- You need kernel debugging or deep performance profiling.
- You want to exploit systems or bypass access controls.

## Workflow / Steps
- Confirm scope and safety:
- identify service name and whether changes are permitted.
- Gather evidence:
- status output + recent logs (see `references/triage-commands.md`).
- Classify failure:
- config error, dependency missing, permission denied, port conflict, upstream unreachable, DNS mismatch.
- Propose minimal fix + verification steps.
- Validate network path (if web service):
- app listens → Nginx proxies → DNS resolves → (TLS sanity if applicable).
- Provide restart/reload plan and confirm health checks.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `1`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
