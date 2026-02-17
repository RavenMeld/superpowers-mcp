# n8n-workflow-patterns

Proven workflow architectural patterns from real n8n workflows. Use when building new workflows, designing workflow structure, choosing workflow patterns, planning workflow architecture, or asking about webhook processing, HTTP API integration, database operations, AI agent workflows, or scheduled tasks.

## Quick Facts
- id: `n8n-workflow-patterns--77b98183f5`
- worth_using_score: `55/100`
- tags: `mcp, github, python, node, testing, ci, docs`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/.agents/skills/n8n-workflow-patterns/SKILL.md`

## Use When
- *Webhook Processing** - Use when:
- Receiving data from external systems
- Building integrations (Slack commands, form submissions, GitHub webhooks)
- Need instant response to events
- Example: "Receive Stripe payment webhook → Update database → Send confirmation"
- *HTTP API Integration** - Use when:
- Fetching data from external APIs
- Synchronizing with third-party services
- Building data pipelines
- Example: "Fetch GitHub issues → Transform → Create Jira tickets"

## Workflow / Steps
- --
- **[Webhook Processing](webhook_processing.md)** (Most Common)
- Receive HTTP requests → Process → Output
- Pattern: Webhook → Validate → Transform → Respond/Notify
- **[HTTP API Integration](http_api_integration.md)**
- Fetch from REST APIs → Transform → Store/Use
- Pattern: Trigger → HTTP Request → Transform → Action → Error Handler
- **[Database Operations](database_operations.md)**
- Read/Write/Sync database data
- Pattern: Schedule → Query → Transform → Write → Verify

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `12`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
