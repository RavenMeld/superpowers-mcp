# render-deploy

Deploy applications to Render by analyzing codebases, generating render.yaml Blueprints, and providing Dashboard deeplinks. Use when the user wants to deploy, host, publish, or set up their application on Render's cloud platform.

## Quick Facts
- id: `render-deploy--ca3d146899`
- worth_using_score: `73/100`
- tags: `mcp, github, git, ssh, browser, postgres, node, docker, ci, docs, linux, render`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/render-deploy/SKILL.md`

## Use When
- Deploy an application to Render
- Create a render.yaml Blueprint file
- Set up Render deployment for their project
- Host or publish their application on Render's cloud platform
- Create databases, cron jobs, or other Render resources

## Workflow / Steps
- *Key Points:**
- Always use `plan: free` unless user specifies otherwise
- Include ALL environment variables the app needs
- Mark secrets with `sync: false` (user fills these in Dashboard)
- Use appropriate service type: `web`, `worker`, `cron`, `static`, or `pserv`
- Use appropriate runtime: [references/runtimes.md](references/runtimes.md)
- *Basic Structure:**
- type: web
- key: DATABASE_URL
- key: JWT_SECRET

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `26`
- has_scripts: `False`
- has_references: `True`
- has_assets: `True`
