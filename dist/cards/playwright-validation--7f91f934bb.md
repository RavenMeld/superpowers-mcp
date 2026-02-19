# playwright-validation

Use when validating UI changes in a branch require Playwright E2E testing. Reviews branch changes, validates UI with Playwright MCP, and adds missing test cases.

## Quick Facts
- id: `playwright-validation--7f91f934bb`
- worth_using_score: `65/100`
- tags: `mcp, git, playwright, browser, typescript, testing, ci, rag`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/open-metadata-playwright-validation/SKILL.md`

## Use When
- After completing UI feature development
- Before creating a PR for UI changes
- When reviewing UI-related branches
- To verify existing Playwright tests cover all scenarios

## Workflow / Steps
- **Identify changed files vs main:**
- **Focus on UI component changes:**
- **Check for existing Playwright tests:**
- **Read the changed component files** to understand the UI modifications
- **Locate relevant test files:**
- Check `playwright/e2e/Pages/` for page-level tests
- Check `playwright/e2e/Features/` for feature-specific tests
- Use Glob/Grep to find tests related to the feature
- **Analyze test coverage:**
- Read the existing test file(s)

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `4`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
