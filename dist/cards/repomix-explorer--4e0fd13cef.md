# repomix-explorer

Use this skill when the user wants to analyze or explore a codebase (remote repository or local repository) using Repomix. Triggers on: 'analyze this repo', 'explore codebase', 'what's the structure', 'find patterns in repo', 'how many files/tokens'. Runs repomix CLI to pack repositories, then analyzes the output.

## Quick Facts
- id: `repomix-explorer--4e0fd13cef`
- worth_using_score: `55/100`
- tags: `github, git, typescript, rust, go, java, security, ci, vercel`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/repomix-explorer/SKILL.md`

## Workflow / Steps
- *For Remote Repositories:**
- *IMPORTANT**: Always output to `/tmp` for remote repositories to avoid polluting the user's current project directory.
- *For Local Directories:**
- *Common Options:**
- `--style <format>`: Output format (xml, markdown, json, plain) - **xml is default and recommended**
- `--compress`: Enable Tree-sitter compression (~70% token reduction) - use for large repos
- `--include <patterns>`: Include only matching patterns (e.g., "src/**/*.ts,**/*.md")
- `--ignore <patterns>`: Additional ignore patterns
- `--output <path>`: Custom output path (default: repomix-output.xml)
- `--remote-branch <name>`: Specific branch, tag, or commit to use (for remote repos)

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `10`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
