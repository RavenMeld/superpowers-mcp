# microservices-architect

Use when designing distributed systems, decomposing monoliths, or implementing microservices patterns. Invoke for service boundaries, DDD, saga patterns, event sourcing, service mesh, distributed tracing.

## Quick Facts
- id: `microservices-architect--630aef777d`
- worth_using_score: `55/100`
- tags: `kubernetes, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/claude-skills/skills/microservices-architect/SKILL.md`

## Use When
- Decomposing monoliths into microservices
- Defining service boundaries and bounded contexts
- Designing inter-service communication patterns
- Implementing resilience patterns (circuit breakers, retries, bulkheads)
- Setting up service mesh (Istio, Linkerd)
- Designing event-driven architectures
- Implementing distributed transactions (Saga, CQRS)
- Establishing observability (tracing, metrics, logging)

## Workflow / Steps
- **Domain Analysis** - Apply DDD to identify bounded contexts and service boundaries
- **Communication Design** - Choose sync/async patterns, protocols (REST, gRPC, events)
- **Data Strategy** - Database per service, event sourcing, eventual consistency
- **Resilience** - Circuit breakers, retries, timeouts, bulkheads, fallbacks
- **Observability** - Distributed tracing, correlation IDs, centralized logging
- **Deployment** - Container orchestration, service mesh, progressive delivery

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
