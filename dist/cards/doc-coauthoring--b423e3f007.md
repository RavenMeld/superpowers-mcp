# doc-coauthoring

Guide users through a structured workflow for co-authoring documentation. Use when user wants to write documentation, proposals, technical specs, decision docs, or similar structured content. This workflow helps users efficiently transfer context, refine content through iteration, and verify the doc works for readers. Trigger when user mentions writing docs, creating proposals, drafting specs,...

## Quick Facts
- id: `doc-coauthoring--b423e3f007`
- worth_using_score: `30/100`
- tags: `mcp, testing, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/doc-coauthoring/SKILL.md`

## Workflow / Steps
- *Trigger conditions:**
- User mentions writing documentation: "write a doc", "draft a proposal", "create a spec", "write up"
- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC"
- User seems to be starting a substantial writing task
- *Initial offer:**
- **Context Gathering**: User provides all relevant context while Claude asks clarifying questions
- **Refinement & Structure**: Iteratively build each section through brainstorming and editing
- **Reader Testing**: Test the doc with a fresh Claude (no context) to catch blind spots before others read it
- *Goal:** Close the gap between what the user knows and what Claude knows, enabling smart guidance later.
- What type of document is this? (e.g., technical spec, decision doc, proposal)

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
