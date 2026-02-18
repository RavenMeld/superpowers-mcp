# playwright

Playwright E2E testing patterns. Trigger: When writing E2E tests - Page Objects, selectors, MCP workflow.

## Quick Facts
- id: `playwright--7ae3fe3fb6`
- worth_using_score: `55/100`
- tags: `mcp, playwright, typescript, go, testing, ci, docs, rag`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/gentleman-programming-playwright/SKILL.md`

## Workflow / Steps
- *⚠️ If you have Playwright MCP tools, ALWAYS use them BEFORE creating any test:**
- **Navigate** to target page
- **Take snapshot** to see page structure and elements
- **Interact** with forms/elements to verify exact user flow
- **Take screenshots** to document expected states
- **Verify page transitions** through complete flow (loading, success, error)
- **Document actual selectors** from snapshots (use real refs and labels)
- **Only after exploring** create test code with verified selectors
- *If MCP NOT available:** Proceed with test creation based on docs and code analysis.
- *Why This Matters:**

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `9`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
