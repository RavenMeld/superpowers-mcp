---
name: wsl-network-recovery
description: |
  Recover WSL networking issues (DNS, proxy, localhost forwarding, firewall interactions) with a repeatable diagnostic flow.
---

# WSL Network Recovery

## Use When

- WSL cannot resolve hosts while Windows can.
- Localhost services are unreachable across WSL and Windows.
- Proxy/firewall settings intermittently break package installs or API calls.

## Workflow

1. Verify DNS resolution and route reachability inside WSL.
2. Compare proxy/firewall settings between Windows and WSL.
3. Validate localhost forwarding direction and bound address.
4. Restart WSL networking stack only after capturing baseline diagnostics.
5. Re-run connectivity checks and record the working config.

## Copy/Paste Examples

```bash
getent hosts github.com && ping -c 1 1.1.1.1
```

```bash
ss -tulpen | rg ':3000|:8000|:5173'
```

```bash
powershell.exe -Command "Get-NetFirewallProfile | Format-Table Name,Enabled"
```

## Recovery Notes

- Prefer binding local dev servers to `127.0.0.1` unless sharing is required.
- Keep proxy config documented per shell (`bash`, `pwsh`, app-level).
- Record known-good DNS settings after fixes.

## Safety Notes

- Do not expose services to LAN/public during troubleshooting.
- Snapshot critical network config before editing.
