# security-secrets

Review secret detection patterns and scanning workflows. Use for identifying high-signal secrets like AWS keys, GitHub tokens, and DB passwords. Use proactively during all security audits to scan code and history.
Examples:
- user: "Scan for secrets in this repo" → run high-signal rg patterns and gitleaks
- user: "Check for AWS keys" → scan for AKIA patterns and server-side exposure
- user: "Au...

## Quick Facts
- id: `security-secrets--9f69a48a4e`
- worth_using_score: `45/100`
- tags: `github, git, ssh, sql, postgres, go, docker, aws, security, ci`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/igorwarzocha-security-secrets/SKILL.md`

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `False`
- code_examples: `2`
- has_scripts: `True`
- has_references: `False`
- has_assets: `False`
