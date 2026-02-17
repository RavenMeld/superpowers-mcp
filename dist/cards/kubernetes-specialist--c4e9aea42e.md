# kubernetes-specialist

Use when deploying or managing Kubernetes workloads requiring cluster configuration, security hardening, or troubleshooting. Invoke for Helm charts, RBAC policies, NetworkPolicies, storage configuration, performance optimization.

## Quick Facts
- id: `kubernetes-specialist--c4e9aea42e`
- worth_using_score: `40/100`
- tags: `kubernetes, security, testing, ci, figma`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/claude-skills/skills/kubernetes-specialist/SKILL.md`

## Use When
- Deploying workloads (Deployments, StatefulSets, DaemonSets, Jobs)
- Configuring networking (Services, Ingress, NetworkPolicies)
- Managing configuration (ConfigMaps, Secrets, environment variables)
- Setting up persistent storage (PV, PVC, StorageClasses)
- Creating Helm charts for application packaging
- Troubleshooting cluster and workload issues
- Implementing security best practices

## Workflow / Steps
- **Analyze requirements** - Understand workload characteristics, scaling needs, security requirements
- **Design architecture** - Choose workload types, networking patterns, storage solutions
- **Implement manifests** - Create declarative YAML with proper resource limits, health checks
- **Secure** - Apply RBAC, NetworkPolicies, Pod Security Standards, least privilege
- **Test & validate** - Verify deployments, test failure scenarios, validate security posture

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
