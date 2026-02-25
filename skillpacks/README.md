# skillpacks/

This folder contains **repo-contained** `SKILL.md` packs intended to be indexed by:

```bash
cd projects/awesome-skills-database
python -m awesome_skills build --root .
```

Why keep skills here:
- Shareable (can publish this repo and rebuild anywhere).
- Deterministic (no network required to build/search).
- Easy to extend (add a new folder with a `SKILL.md`).

## Superpowers Snapshot

This repo can vendor a snapshot of `superpowers` skills under `skillpacks/superpowers`.

Sync command:

```bash
bash scripts/sync_superpowers_skillpack.sh
```

The sync uses `git archive` from the source repository `HEAD` commit, so uncommitted
working-tree changes in the source repo are not imported.
