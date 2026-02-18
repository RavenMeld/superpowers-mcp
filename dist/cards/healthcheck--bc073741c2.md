# healthcheck

Host security hardening and risk-tolerance configuration for OpenClaw deployments. Use when a user asks for security audits, firewall/SSH/update hardening, risk posture, exposure review, OpenClaw cron scheduling for periodic checks, or version status checks on a machine running OpenClaw (laptop, workstation, Pi, VPS).

## Quick Facts
- id: `healthcheck--bc073741c2`
- worth_using_score: `35/100`
- tags: `git, ssh, browser, go, security, ci, docs, windows, linux`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/healthcheck/SKILL.md`

## Workflow / Steps
- OS and version (Linux/macOS/Windows), container vs host.
- Privilege level (root/admin vs user).
- Access path (local console, SSH, RDP, tailnet).
- Network exposure (public IP, reverse proxy, tunnel).
- OpenClaw gateway status and bind address.
- Backup system and status (e.g., Time Machine, system images, snapshots).
- Deployment context (local mac app, headless gateway host, remote gateway, container/CI).
- Disk encryption status (FileVault/LUKS/BitLocker).
- OS automatic security updates status.
- Usage mode for a personal assistant with full access (local workstation vs headless/remote vs other).

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
