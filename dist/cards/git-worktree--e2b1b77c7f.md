# git-worktree

This skill manages Git worktrees for isolated parallel development. It handles creating, listing, switching, and cleaning up worktrees with a simple interactive interface, following KISS principles.

## Quick Facts
- id: `git-worktree--e2b1b77c7f`
- worth_using_score: `65/100`
- tags: `ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/compound-engineering-plugin/plugins/compound-engineering/skills/git-worktree/SKILL.md`

## Use When
- **Code Review (`/workflows:review`)**: If NOT already on the target branch (PR branch or requested branch), offer worktree for isolated review
- **Feature Work (`/workflows:work`)**: Always ask if user wants parallel worktree or live branch work
- **Parallel Development**: When working on multiple features simultaneously
- **Cleanup**: After completing work in a worktree

## Workflow / Steps
- The skill is automatically called from `/workflows:review` and `/workflows:work` commands:
- ```

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `16`
- has_scripts: `True`
- has_references: `False`
- has_assets: `False`
