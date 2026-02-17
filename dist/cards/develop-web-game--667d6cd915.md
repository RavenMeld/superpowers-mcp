# develop-web-game

Use when Codex is building or iterating on a web game (HTML/JS) and needs a reliable development + testing loop: implement small changes, run a Playwright-based test script with short input bursts and intentional pauses, inspect screenshots/text, and review console errors with render_game_to_text.

## Quick Facts
- id: `develop-web-game--667d6cd915`
- worth_using_score: `68/100`
- tags: `mcp, playwright, node, testing, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/develop-web-game/SKILL.md`

## Workflow / Steps
- **Pick a goal.** Define a single feature or behavior to implement.
- **Implement small.** Make the smallest change that moves the game forward.
- **Ensure integration points.** Provide a single canvas and `window.render_game_to_text` so the test loop can read state.
- **Add `window.advanceTime(ms)`.** Strongly prefer a deterministic step hook so the Playwright script can advance frames reliably; without it, automated tests can be flaky.
- **Initialize progress.md.** If `progress.md` exists, read it first and confirm the original user prompt is recorded at the top (prefix with `Original prompt:`). Also note any TODOs and suggestions left by the previous agent. If missing, create it and write `Original prompt: <prompt>` at the top before appending updates.
- **Verify Playwright availability.** Ensure `playwright` is available (local dependency or global install). If unsure, check `npx` first.
- **Run the Playwright test script.** You must run `$WEB_GAME_CLIENT` after each meaningful change; do not invent a new client unless required.
- **Use the payload reference.** Base actions on `$WEB_GAME_ACTIONS` to avoid guessing keys.
- **Inspect state.** Capture screenshots and text state after each burst.
- **Inspect screenshots.** Open the latest screenshot, verify expected visuals, fix any issues, and rerun the script. Repeat until correct.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `True`
- has_references: `True`
- has_assets: `True`
