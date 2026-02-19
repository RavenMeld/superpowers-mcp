# wsl-network-recovery

Recover WSL networking issues (DNS, proxy, localhost forwarding, firewall interactions) with a repeatable diagnostic flow.

## Quick Facts
- id: `wsl-network-recovery--2c983c41a0`
- worth_using_score: `60/100`
- tags: `github, git, go, powershell, wsl, windows`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/wsl-network-recovery/SKILL.md`

## Use When
- WSL cannot resolve hosts while Windows can.
- Localhost services are unreachable across WSL and Windows.
- Proxy/firewall settings intermittently break package installs or API calls.

## Workflow / Steps
- Verify DNS resolution and route reachability inside WSL.
- Compare proxy/firewall settings between Windows and WSL.
- Validate localhost forwarding direction and bound address.
- Restart WSL networking stack only after capturing baseline diagnostics.
- Re-run connectivity checks and record the working config.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
