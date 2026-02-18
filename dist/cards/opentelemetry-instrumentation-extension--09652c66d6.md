# OpenTelemetry Instrumentation Extension

Extend OpenTelemetry instrumentation when new functionality is added to the MCP Gateway. Use when (1) new operations/functions are added, (2) reviewing code for missing instrumentation, (3) user requests otel/telemetry additions, or (4) working with state-changing operations. Analyzes git diff, suggests instrumentation points following project standards in docs/telemetry/README.md, implements w...

## Quick Facts
- id: `opentelemetry-instrumentation-extension--09652c66d6`
- worth_using_score: `70/100`
- tags: `mcp, git, go, docker, testing, ci, docs, rag`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/docker-opentelemetry-instrumentation-extension/SKILL.md`

## Use When
- New state-changing operations added (Create, Update, Delete, Push, Pull, Add, Remove, etc.)
- New CLI commands added to `cmd/docker-mcp/`
- New packages with operations in `pkg/`
- User mentions "otel", "telemetry", "instrumentation", "metrics", or "tracing"
- Code changes that modify state (database, files, containers, configuration)
- Reviewing code for telemetry coverage

## Workflow / Steps
- **Read project telemetry standards**:
- Read `docs/telemetry/README.md` "Development Guidelines" section
- Read `pkg/telemetry/telemetry.go` to understand existing patterns and metrics
- **Identify scope** using git diff:
- Find new/changed files in `pkg/` and `cmd/docker-mcp/`
- Identify functions performing state-changing operations
- Infer domain from package structure (e.g., `pkg/foo/` → domain: `foo`)
- **Categorize findings**:
- Operations in existing domains (use existing metrics)
- Operations in new domains (need new metrics)

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `6`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
