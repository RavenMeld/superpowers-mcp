# kubernetes-debugging

Debug Kubernetes workloads quickly with kubectl: pods, logs, describe, events, exec, port-forward, and rollout control.

## Quick Facts
- id: `kubernetes-debugging--9d82fc9f76`
- worth_using_score: `70/100`
- tags: `node, kubernetes, ci, figma`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/kubernetes-debugging/SKILL.md`

## Use When
- Pods are crashlooping or stuck pending.
- Requests fail and you need logs/events fast.
- You need to test a service locally via port-forward.

## Workflow / Steps
- Identify the broken namespace/context.
- Find the failing pod and reason (events, status).
- Read logs (current + previous).
- Describe pod and inspect env/volumes/probes.
- Exec in for a minimal diagnosis (dns, config files, connectivity).
- Fix and watch rollout.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `8`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
