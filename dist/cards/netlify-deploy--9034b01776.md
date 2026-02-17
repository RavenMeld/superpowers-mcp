# netlify-deploy

Deploy web projects to Netlify using the Netlify CLI (`npx netlify`). Use when the user asks to deploy, host, publish, or link a site/repo on Netlify, including preview and production deploys.

## Quick Facts
- id: `netlify-deploy--9034b01776`
- worth_using_score: `63/100`
- tags: `github, testing, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/netlify-deploy/SKILL.md`

## Workflow / Steps
- *Expected output patterns**:
- ✅ Authenticated: Shows logged-in user email and site link status
- ❌ Not authenticated: "Not logged into any site" or authentication error
- *If not authenticated**, guide the user:
- *Alternative: API Key authentication**
- **Linked**: Site already connected to Netlify (shows site name/URL)
- **Not linked**: Need to link or create site
- *If already linked** → Skip to step 4
- *If not linked**, attempt to link by Git remote:

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `10`
- has_scripts: `False`
- has_references: `True`
- has_assets: `True`
