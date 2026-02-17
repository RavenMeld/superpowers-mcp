# sql-pro

Use when optimizing SQL queries, designing database schemas, or tuning database performance. Invoke for complex queries, window functions, CTEs, indexing strategies, query plan analysis.

## Quick Facts
- id: `sql-pro--dcb36f463b`
- worth_using_score: `55/100`
- tags: `ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/claude-skills/skills/sql-pro/SKILL.md`

## Use When
- Optimizing slow queries and execution plans
- Designing complex queries with CTEs, window functions, recursive patterns
- Creating and optimizing database indexes
- Implementing data warehousing and ETL patterns
- Migrating queries between database platforms
- Analyzing and tuning database performance

## Workflow / Steps
- **Schema Analysis** - Review database structure, indexes, query patterns, performance bottlenecks
- **Design** - Create set-based operations using CTEs, window functions, appropriate joins
- **Optimize** - Analyze execution plans, implement covering indexes, eliminate table scans
- **Verify** - Test with production data volume, ensure linear scalability, confirm sub-100ms targets
- **Document** - Provide query explanations, index rationale, performance metrics

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
