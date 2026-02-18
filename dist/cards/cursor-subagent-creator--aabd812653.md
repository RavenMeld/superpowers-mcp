# cursor-subagent-creator

Creates Cursor-specific AI subagents with isolated context for complex multi-step workflows. Use when creating subagents for Cursor editor specifically, following Cursor's patterns and directories (.cursor/agents/). Triggers on "cursor subagent", "cursor agent".

## Quick Facts
- id: `cursor-subagent-creator--aabd812653`
- worth_using_score: `65/100`
- tags: `go, security, testing, ci, docs, render, rag, eval`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/tech-leads-club-cursor-subagent-creator/SKILL.md`

## Use When
- Create a new subagent/agent
- Create a specialized assistant
- Implement a complex workflow with multiple steps
- Create verifiers, auditors, or domain experts
- Tasks that require isolated context and multiple steps
- *DO NOT use for simple, one-off tasks** - for those, use skills.

## Workflow / Steps
- What specific responsibility does the subagent have?
- Why does it need isolated context?
- Does it involve multiple complex steps?
- Does it require deep specialization?
- **Project**: `.cursor/agents/agent-name.md` - project-specific
- **User**: `~/.cursor/agents/agent-name.md` - all projects
- *Naming convention:**
- Use kebab-case (words-separated-by-hyphens)
- Be descriptive of the specialization
- Examples: `security-auditor`, `test-runner`, `debugger`, `verifier`

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `21`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
