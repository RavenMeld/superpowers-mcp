# skillz-integration

Integration guide for Skillz MCP server with Docker, including setup, configuration, and skill execution safety notes.

## Quick Facts
- id: `skillz-integration--75b81d2b77`
- worth_using_score: `55/100`
- tags: `mcp, github, python, node, docker, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/skillz-integration/SKILL.md`

## Workflow / Steps
- *Key points:**
- Replace `/path/to/skills` with the actual path to your skills directory
- The skills directory is mounted at `/skillz` inside the container
- Pass `/skillz` as the argument to tell skillz where to find skills
- **`SKILL.md`** - Required file with YAML frontmatter describing the skill
- **Helper scripts** - Optional Python, Node.js, or other scripts
- **Resources** - Optional datasets, examples, prompts, etc.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `9`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
