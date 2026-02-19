---
name: git-signing-ops
description: |
  Configure and verify Git commit signing (SSH or GPG) across Linux/WSL/Windows with reliable verification checks.
---

# Git Signing Ops

## Use When

- You need verified commits for protected branches or org policy.
- Signing works in one shell but fails in another (WSL vs Windows).
- You are standardizing commit signing for multiple repos.

## Workflow

1. Choose signing mode (SSH signing preferred for simple GitHub workflows).
2. Configure git signing keys and enable `commit.gpgsign`.
3. Test a signed commit locally.
4. Verify signature status in `git log --show-signature`.
5. Repeat verification in each shell environment you use.

## Copy/Paste Examples

```bash
git config --global gpg.format ssh
git config --global user.signingkey ~/.ssh/github-ravenmeld.pub
git config --global commit.gpgsign true
```

```bash
git commit -m "test: signing check" --allow-empty
```

```bash
git log --show-signature -1
```

## Operational Notes

- Keep signing key paths absolute to avoid shell ambiguity.
- Document per-machine bootstrap steps for fast recovery.
- Validate signing after key rotation.

## Safety Notes

- Do not rotate keys without updating account trust settings first.
- Never commit private key material.
