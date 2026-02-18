# git-worktree

This skill manages Git worktrees for isolated parallel development. It handles creating, listing, switching, and cleaning up worktrees with a simple interactive interface, following KISS principles.

## Quick Facts
- id: `git-worktree--e3d54110ec`
- worth_using_score: `80/100`
- tags: `git, go, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/git-worktree/SKILL.md`

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
