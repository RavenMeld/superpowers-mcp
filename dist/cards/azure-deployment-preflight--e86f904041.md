# azure-deployment-preflight

Performs comprehensive preflight validation of Bicep deployments to Azure, including template syntax validation, what-if analysis, and permission checks. Use this skill before any deployment to Azure to preview changes, identify potential issues, and ensure the deployment will succeed. Activate when users mention deploying to Azure, validating Bicep files, checking deployment permissions, previ...

## Quick Facts
- id: `azure-deployment-preflight--e86f904041`
- worth_using_score: `60/100`
- tags: `mcp, azure, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/azure-deployment-preflight/SKILL.md`

## Use When
- Before deploying infrastructure to Azure
- When preparing or reviewing Bicep files
- To preview what changes a deployment will make
- To verify permissions are sufficient for deployment
- Before running `azd up`, `azd provision`, or `az deployment` commands

## Workflow / Steps
- **Check for azd project**: Look for `azure.yaml` in the project root
- If found → Use **azd workflow**
- If not found → Use **az CLI workflow**
- **Locate Bicep files**: Find all `.bicep` files to validate
- For azd projects: Check `infra/` directory first, then project root
- For standalone: Use the file specified by the user or search common locations (`infra/`, `deploy/`, project root)
- **Auto-detect parameter files**: For each Bicep file, look for matching parameter files:
- `<filename>.bicepparam` (Bicep parameters - preferred)
- `<filename>.parameters.json` (JSON parameters)
- `parameters.json` or `parameters/<env>.json` in same directory

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `6`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
