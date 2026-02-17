# git-master

MUST USE for ANY git operations. Atomic commits, rebase/squash, history search (blame, bisect, log -S). STRONGLY RECOMMENDED: Use with task(category='quick', load_skills=['git-master'], ...) to save context. Triggers: 'commit', 'rebase', 'squash', 'who wrote', 'when was X added', 'find the commit that'.

## Quick Facts
- id: `git-master--9a9f5c818e`
- worth_using_score: `50/100`
- tags: `ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/automation/devtools/oh-my-opencode/src/features/builtin-skills/git-master/SKILL.md`

## Workflow / Steps
- *THIS PHASE HAS MANDATORY OUTPUT** - You MUST print the commit plan before moving to Phase 4.
- *If your planned commit count < min_commits -> WRONG. SPLIT MORE.**
- *RULE: Different directories = Different commits (almost always)**
- app/[locale]/page.tsx
- app/[locale]/layout.tsx
- components/demo/browser-frame.tsx
- components/demo/shopify-full-site.tsx
- components/pricing/pricing-table.tsx
- e2e/navbar.spec.ts
- messages/en.json

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `50`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
