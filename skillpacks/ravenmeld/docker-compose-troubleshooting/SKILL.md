---
name: docker-compose-troubleshooting
description: |
  Run and debug multi-service dev stacks with Docker Compose: logs, exec, rebuilds, volumes, networking, and safe cleanup.
---

# Docker Compose Troubleshooting

## Use When

- A local dev stack (db + api + worker) won’t start.
- You need to inspect logs, env, and connectivity between services.
- You need safe cleanup without nuking unrelated Docker state.

## Workflow

1. Start cleanly and watch logs.
2. Identify the failing service (exit code, crash loop, healthcheck).
3. Inspect container config (env, ports, volumes).
4. Exec into the container to run the failing command manually.
5. Fix the minimal root cause (config, deps, migrations) and restart.

## Core Commands

Start (foreground logs):

```bash
docker compose up
```

Start (detached) and tail logs:

```bash
docker compose up -d
docker compose logs -f --tail 200
```

Restart a single service after edits:

```bash
docker compose up -d --build <service>
```

Shell into a service:

```bash
docker compose exec <service> sh
```

## Networking Debug

List containers and ports:

```bash
docker compose ps
```

Test service-to-service DNS from inside a container:

```bash
docker compose exec <service> sh -lc 'getent hosts db && getent hosts api'
```

## Safe Cleanup

Stop stack (keeps volumes by default):

```bash
docker compose down
```

Remove volumes (destructive for databases):

```bash
docker compose down -v
```

## Common Failure Modes

- Migrations not run (db starts but app crashes).
- Port conflict on host.
- Wrong env var names or missing secrets.
- Volume permissions mismatch (WSL/Linux vs Windows mounts).

