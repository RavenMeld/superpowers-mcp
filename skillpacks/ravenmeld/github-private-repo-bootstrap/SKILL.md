---
name: github-private-repo-bootstrap
description: |
  Bootstrap a private GitHub repo safely: SSH remote, branch setup, first push, and verification (including multi-account SSH aliases).
---

# GitHub Private Repo Bootstrap

## Use When

- You created a new private repo and need to push code from WSL/Linux.
- You have multiple GitHub accounts and need deterministic SSH identity selection.
- You want a clean `main` branch setup with minimal footguns.

## Workflow

1. Create the repo in GitHub (private).
2. Initialize git locally (or enter an existing repo).
3. Add the SSH remote using the right host alias.
4. Push `main` and verify by fetching.
5. Lock in the remote URL and branch upstream.

## Add Remote (Single Account)

```bash
git remote add origin git@github.com:OWNER/REPO.git
git push -u origin main
```

## Add Remote (Multi-Account via Host Alias)

If you configured a dedicated host alias (example `github-ravenmeld`):

```bash
git remote add origin git@github-ravenmeld:OWNER/REPO.git
git push -u origin main
```

## Verify

Show remotes:

```bash
git remote -v
```

Fetch from origin:

```bash
git fetch origin
git branch -vv
```

## Common Fixes

- Remote already exists:

```bash
git remote set-url origin git@github-ravenmeld:OWNER/REPO.git
```

- Pushed the wrong branch name:

```bash
git branch -M main
git push -u origin main
```

## Safety Notes

- Use SSH aliases per account to avoid the wrong key being tried.
- Don’t paste private keys or tokens into repo files.

