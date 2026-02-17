# do-plan

Execute a phased implementation plan using subagents. Use when asked to execute, run, or carry out a plan — especially one created by make-plan.

## Quick Facts
- id: `do-plan--4b232a6e7d`
- worth_using_score: `35/100`
- tags: `ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/do-plan/SKILL.md`

## Workflow / Steps
- Each phase uses fresh subagents where noted (or when context is large/unclear)
- Assign one clear objective per subagent and require evidence (commands run, outputs, files changed)
- Do not advance to the next step until the assigned subagent reports completion and the orchestrator confirms it matches the plan
- Execute the implementation as specified
- COPY patterns from documentation, don't invent
- Cite documentation sources in code comments when using unfamiliar APIs
- If an API seems missing, STOP and verify — don't assume it exists
- **Run verification checklist** — Deploy a "Verification" subagent to prove the phase worked
- **Anti-pattern check** — Deploy an "Anti-pattern" subagent to grep for known bad patterns from the plan
- **Code quality review** — Deploy a "Code Quality" subagent to review changes

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
