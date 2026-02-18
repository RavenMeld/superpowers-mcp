# obsidian-developer

Expert guide for inspecting and automating Obsidian using the obsidian-devtools MCP server.

## Quick Facts
- id: `obsidian-developer--8a94f4b2a3`
- worth_using_score: `35/100`
- tags: `mcp, python, node, java, security, ci, obsidian, rag, eval`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/neversight-obsidian-developer/SKILL.md`

## Workflow / Steps
- **Connect**: Ensure Obsidian is running with debug flags.
- Run `obsidian_launch_debug()` to start or attach.
- **Inspect**: Understand the current state.
- Use `obsidian_inspect_dom()` to see the UI structure.
- Use `obsidian_discover_api()` to explore internal APIs.
- Refer to `knowledge/dom-patterns.md` for class names.
- **Execute**: Run automation or queries.
- Use `obsidian_eval()` to interact with the `app` object.
- Refer to `knowledge/api-basics.md` for common API calls.
- Refer to `knowledge/cdp-protocol.md` for data passing rules.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
