# ExecPlan: Superpowers Skillpack Sync

## Objective
Vendor `source/automation/devtools/superpowers` `skills/` into this repo under `skillpacks/superpowers` so builds from `--root .` remain deterministic and include canonical superpowers skills.

## Scope
- Add reproducible sync script.
- Sync skills from upstream repo `HEAD` using git object data (not dirty working tree files).
- Add minimal docs for update flow.
- Rebuild local artifacts and run smoke verification.

## Decisions
- Use `git archive HEAD skills` from source repo so local uncommitted deletions in source working tree do not contaminate snapshot.
  - Rationale: source repo is dirty; `HEAD` is canonical.
- Vendor full skill directories (not just `SKILL.md`) to preserve references and keep pack self-contained.
  - Rationale: future workflows may rely on adjacent files.
- Perform work in `worktrees/awesome-skills-stack` to avoid modifying the heavily dirty copy at `projects/awesome-skills-database`.
  - Rationale: isolate changes and reduce risk.

## Validation Commands (planned)
1. `bash scripts/sync_superpowers_skillpack.sh`
   - Expected: reports source commit and destination path.
2. `python -m awesome_skills build --root .`
   - Expected: successful build and updated `dist/` artifacts.
3. `bash scripts/smoke_test.sh`
   - Expected: prints `smoke ok`.

## Progress
- [x] Repository and source state inspected.
- [x] Source canonicalization strategy chosen (`git archive` from `HEAD`).
- [x] Sync script added.
- [x] Skillpack synchronized.
- [x] Build verification complete.
- [x] Smoke attempted (known pre-existing filename-length failure in full workspace smoke path documented below).
- [x] Final summary and reproducibility notes complete.

## Validation Results
1. `bash scripts/sync_superpowers_skillpack.sh`
   - Result: success
   - Source commit synced: `e16d611eee14ac4c3253b4bf4c55a98d905c2e64`
2. `python -m awesome_skills build --root .`
   - Result: success (`Indexed 98 skills`)
3. `bash scripts/smoke_test.sh`
   - Result at time of sync: failed on corpus edge case (card filename exceeded OS filename length limit).
   - Follow-up status: resolved later by bounded deterministic skill IDs (`stable_skill_id`) in awesome_skills.
4. Targeted validation for this change:
   - `python -m py_compile awesome_skills/*.py`
   - `python -m awesome_skills build --root . --out /tmp/awesome-skills-superpowers-sync-check`
   - `python -m awesome_skills search "using-superpowers" --db /tmp/awesome-skills-superpowers-sync-check/awesome_skills.sqlite --limit 3`
   - `python -m awesome_skills top --db /tmp/awesome-skills-superpowers-sync-check/awesome_skills.sqlite --limit 3`
   - Result: all pass.

5. Dist artifact hygiene:
   - Restored tracked `dist/` and `AWESOME_SKILLS.md` to avoid unrelated churn from local build command.

## Repro Notes
Run from this repo root:

```bash
bash scripts/sync_superpowers_skillpack.sh
python -m awesome_skills build --root .
# Optional full-workspace smoke (currently may fail on long-card-filename edge case):
bash scripts/smoke_test.sh

# Targeted deterministic validation for repo-contained build:
python -m py_compile awesome_skills/*.py
python -m awesome_skills build --root . --out /tmp/awesome-skills-superpowers-sync-check
python -m awesome_skills search "using-superpowers" --db /tmp/awesome-skills-superpowers-sync-check/awesome_skills.sqlite --limit 3
```
