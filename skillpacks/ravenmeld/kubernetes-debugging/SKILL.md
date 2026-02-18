---
name: kubernetes-debugging
description: |
  Debug Kubernetes workloads quickly with kubectl: pods, logs, describe, events, exec, port-forward, and rollout control.
---

# Kubernetes Debugging

## Use When

- Pods are crashlooping or stuck pending.
- Requests fail and you need logs/events fast.
- You need to test a service locally via port-forward.

## Workflow

1. Identify the broken namespace/context.
2. Find the failing pod and reason (events, status).
3. Read logs (current + previous).
4. Describe pod and inspect env/volumes/probes.
5. Exec in for a minimal diagnosis (dns, config files, connectivity).
6. Fix and watch rollout.

## Core Commands

Select context and namespace:

```bash
kubectl config get-contexts
kubectl config use-context <context>
kubectl get ns
```

List pods (wide):

```bash
kubectl -n <ns> get pods -o wide
```

Events (often the fastest clue):

```bash
kubectl -n <ns> get events --sort-by=.lastTimestamp | tail -50
```

Logs:

```bash
kubectl -n <ns> logs <pod> --tail 200
kubectl -n <ns> logs <pod> --previous --tail 200
```

Describe:

```bash
kubectl -n <ns> describe pod <pod>
```

Exec:

```bash
kubectl -n <ns> exec -it <pod> -- sh
```

Port-forward a service:

```bash
kubectl -n <ns> port-forward svc/<service> 8080:80
```

Rollout status:

```bash
kubectl -n <ns> rollout status deploy/<deploy>
kubectl -n <ns> rollout history deploy/<deploy>
```

## Common Failure Modes

- ImagePullBackOff (auth or tag typo).
- CrashLoopBackOff (bad config, missing env, migrations).
- Pending (no nodes fit, missing PVC, insufficient resources).
- Liveness/readiness probes too strict (kills healthy but slow startup).

## Safety Notes

- Avoid `kubectl delete pod` as a first move; understand why it’s failing.
- Don’t dump secrets from env/configmaps into tickets/logs.

