# npm-proxy

Manage Nginx Proxy Manager (NPM) hosts, certificates, and access lists. Use when the user wants to add a new domain, point a domain to a server/port, enable SSL, or check the status of proxy hosts.

## Quick Facts
- id: `npm-proxy--a9394e6ce6`
- worth_using_score: `40/100`
- tags: `python, ci`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/openclaw-npm-proxy/SKILL.md`

## Workflow / Steps
- List certs with `certs` to see if one exists.
- Update the host with `certificate_id` and `ssl_forced: true`.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `2`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
