# Agent Development

This skill should be used when the user asks to "create an agent", "add an agent", "write a subagent", "agent frontmatter", "when to use description", "agent examples", "agent tools", "agent colors", "autonomous agent", or needs guidance on agent structure, system prompts, triggering conditions, or agent development best practices for Claude Code plugins.

## Quick Facts
- id: `agent-development--e1238b5b0f`
- worth_using_score: `85/100`
- tags: `go, security, testing, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/agent-identifier/SKILL.md`

## Use When
- Write agent with specific triggering examples
- Use similar phrasing to examples in test
- Check Claude loads the agent
- Verify agent provides expected functionality

## Workflow / Steps
- Define agent purpose and triggering conditions
- Choose creation method (AI-assisted or manual)
- Create `agents/agent-name.md` file
- Write frontmatter with all required fields
- Write system prompt following best practices
- Include 2-4 triggering examples in description
- Validate with `scripts/validate-agent.sh`
- Test triggering with real scenarios
- Document agent in plugin README

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `8`
- has_scripts: `True`
- has_references: `True`
- has_assets: `False`
