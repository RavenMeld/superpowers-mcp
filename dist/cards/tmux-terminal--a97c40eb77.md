# tmux-terminal

Interactive terminal control via tmux for TUI apps, prompts, and long-running CLI workflows.

## Quick Facts
- id: `tmux-terminal--a97c40eb77`
- worth_using_score: `70/100`
- tags: `terminal, go, testing, ci`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/mikeyobrien-tmux-terminal/SKILL.md`

## Use When
- Testing `ralph-tui` or any interactive CLI prompts
- Managing long-running processes (web server, loops, watch mode)
- Capturing live terminal output for QA reports
- Interacting with applications that redraw the screen

## Workflow / Steps
- Start servers or loops in a tmux session to keep them alive.
- Use `capture-pane` to confirm health (look for "listening" or "ready" text).
- Stop cleanly with `C-c` then `kill-session`.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `10`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
