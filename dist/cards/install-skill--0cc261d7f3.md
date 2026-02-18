# install-skill

Search and install skills from skills.sh and GitHub repos. Use when users ask to find skills, install skills, download skills, add skills from GitHub, search for skills, browse skills, get a skill, or want new capabilities. Trigger phrases include "install skill", "find skill", "search skills", "add skill", "download skill", "get skill from github", "skills.sh", "browse skills", "what skills ar...

## Quick Facts
- id: `install-skill--0cc261d7f3`
- worth_using_score: `45/100`
- tags: `github, git, node, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/install-skill/SKILL.md`

## Workflow / Steps
- If the user gives a specific repo and skill name, skip to step 3.
- **Search**: Run `search.mjs` with the user's query. Show the top results as a numbered list with name, repo, and install count. Ask which one they want.
- **Install**: Run `install.mjs` with the chosen repo, skill name, and the project's `skills/` directory path.
- **Confirm**: Show what was installed — skill name, source, files downloaded, and path.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `4`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
