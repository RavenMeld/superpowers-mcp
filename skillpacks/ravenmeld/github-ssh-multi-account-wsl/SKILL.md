---
name: github-ssh-multi-account-wsl
description: |
  Create and use multiple GitHub SSH identities from WSL without breaking your existing GitHub SSH setup.
  Uses per-host aliases so each repo can target the right key deterministically.
---

# GitHub SSH Multi-Account (WSL)

## Use When

- You need a **second GitHub account** (or org) on the same WSL machine.
- You want to keep existing `git@github.com:...` remotes working unchanged.
- You want predictable key usage (no agent guessing).

## Workflow

1. Generate a new keypair (one key per account).
2. Add a dedicated `Host` alias in `~/.ssh/config` that points at that key.
3. Add the **public** key to the target GitHub account.
4. Use the alias in your git remotes (clone or `remote set-url`).
5. Verify with `ssh -T`.

## Key Generation (WSL)

Example: create a new key named `github-ravenmeld`:

```bash
ssh-keygen -t ed25519 -C "github-ravenmeld" -f ~/.ssh/github-ravenmeld
chmod 600 ~/.ssh/github-ravenmeld
chmod 644 ~/.ssh/github-ravenmeld.pub
```

Copy public key to Windows clipboard:

```bash
cat ~/.ssh/github-ravenmeld.pub | clip.exe
```

## SSH Config (Keep Existing github.com Working)

Add a **new host alias**; do not change your existing `Host github.com` block:

```sshconfig
Host github-ravenmeld
  HostName ssh.github.com
  Port 443
  User git
  IdentityFile ~/.ssh/github-ravenmeld
  IdentitiesOnly yes
```

Notes:
- Using `ssh.github.com` + `Port 443` helps on networks that block port 22.
- `IdentitiesOnly yes` prevents SSH from trying other keys and confusing GitHub.

## Use the Alias in Git Remotes

Clone using the alias:

```bash
git clone git@github-ravenmeld:ORG_OR_USER/REPO.git
```

Switch an existing repo:

```bash
git remote -v
git remote set-url origin git@github-ravenmeld:ORG_OR_USER/REPO.git
```

## Verify / Troubleshooting

Verify which identity SSH will use:

```bash
ssh -G github-ravenmeld | rg -n '^(hostname|port|user|identityfile|identitiesonly) '
```

Test auth (expects a “successfully authenticated” style message):

```bash
ssh -vT git@github-ravenmeld
```

If you see “permission denied (publickey)”:
- Confirm you added the **right** `*.pub` key to the **right** GitHub account.
- Confirm `~/.ssh/config` points to the correct `IdentityFile`.
- Confirm key permissions (`600` for private key).

## Safety Notes

- Never share the private key (`~/.ssh/github-ravenmeld`).
- Consider adding a passphrase later:

```bash
ssh-keygen -p -f ~/.ssh/github-ravenmeld
```

