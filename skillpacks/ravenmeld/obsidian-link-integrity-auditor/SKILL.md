---
name: obsidian-link-integrity-auditor
description: |
  Audit and repair Obsidian wikilinks, embeds, and backlinks after large vault refactors.
---

# Obsidian Link Integrity Auditor

## Use When

- You renamed or moved many notes in a vault.
- Wikilinks or embeds are breaking after refactors.
- You need confidence before publishing/exporting notes.

## Workflow

1. Build an inventory of all markdown links and embeds.
2. Detect broken targets and orphaned backlinks.
3. Apply deterministic replacements for moved notes.
4. Re-scan until broken-link count reaches zero.
5. Record fix summary for future vault migrations.

## Copy/Paste Examples

```bash
rg -n "\[\[.*\]\]|!\[\[.*\]\]" /path/to/vault
```

```bash
rg -n "\]\(([^)]+)\)" /path/to/vault
```

```bash
git diff --stat
```

## Integrity Rules

- Prefer canonical note names over ambiguous aliases.
- Keep one stable redirect/alias strategy during migrations.
- Re-run link checks after every bulk rename batch.

## Safety Notes

- Back up vault before automated replacements.
- Avoid global replace without exact match validation.
