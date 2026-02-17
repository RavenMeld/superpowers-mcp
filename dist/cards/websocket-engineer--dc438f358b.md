# websocket-engineer

Use when building real-time communication systems with WebSockets or Socket.IO. Invoke for bidirectional messaging, horizontal scaling with Redis, presence tracking, room management.

## Quick Facts
- id: `websocket-engineer--dc438f358b`
- worth_using_score: `40/100`
- tags: `security, testing, ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/claude-skills/skills/websocket-engineer/SKILL.md`

## Use When
- Building WebSocket servers (Socket.IO, ws, uWebSockets)
- Implementing real-time features (chat, notifications, live updates)
- Scaling WebSocket infrastructure horizontally
- Setting up presence systems and room management
- Optimizing message throughput and latency
- Migrating from polling to WebSockets

## Workflow / Steps
- **Analyze requirements** - Identify connection scale, message volume, latency needs
- **Design architecture** - Plan clustering, pub/sub, state management, failover
- **Implement** - Build WebSocket server with authentication, rooms, events
- **Scale** - Configure Redis adapter, sticky sessions, load balancing
- **Monitor** - Track connections, latency, throughput, error rates

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
