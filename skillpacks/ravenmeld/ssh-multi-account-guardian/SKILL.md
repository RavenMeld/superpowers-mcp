---
name: ssh-multi-account-guardian
description: |
  Prevent account/key mixups when using multiple SSH identities (for example default GitHub + RavenMeld) across WSL and Windows.
---

# SSH Multi Account Guardian

## Use When

- You use multiple GitHub accounts and separate SSH keys.
- Push/pull operations hit the wrong account or permission scope.
- You need deterministic host alias routing across WSL and Windows.

## Workflow

1. Generate one keypair per account/use-case.
2. Define explicit `Host` aliases in `~/.ssh/config`.
3. Pin each git remote to the intended alias.
4. Verify auth identity before push.
5. Keep key names and repo remotes clearly labeled.

## Copy/Paste Examples

```bash
ssh-keygen -t ed25519 -f ~/.ssh/github-ravenmeld -C "ravenmeld@github"
```

```bash
ssh -T git@github-ravenmeld
```

```bash
git remote set-url origin git@github-ravenmeld:RavenMeld/awesome-skills-database.git
```

## Config Pattern

- Use `IdentityFile` per host alias.
- Set `IdentitiesOnly yes` to avoid key spillover.
- Keep existing working identities untouched when adding new ones.

## Safety Notes

- Never share private keys.
- Back up `~/.ssh/config` before major edits.
