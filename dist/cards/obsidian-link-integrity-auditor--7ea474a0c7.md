# obsidian-link-integrity-auditor

Audit and repair Obsidian wikilinks, embeds, and backlinks after large vault refactors.

## Quick Facts
- id: `obsidian-link-integrity-auditor--7ea474a0c7`
- worth_using_score: `60/100`
- tags: `git, obsidian`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/obsidian-link-integrity-auditor/SKILL.md`

## Use When
- You renamed or moved many notes in a vault.
- Wikilinks or embeds are breaking after refactors.
- You need confidence before publishing/exporting notes.

## Workflow / Steps
- Build an inventory of all markdown links and embeds.
- Detect broken targets and orphaned backlinks.
- Apply deterministic replacements for moved notes.
- Re-scan until broken-link count reaches zero.
- Record fix summary for future vault migrations.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
