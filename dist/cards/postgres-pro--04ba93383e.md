# postgres-pro

Use when optimizing PostgreSQL queries, configuring replication, or implementing advanced database features. Invoke for EXPLAIN analysis, JSONB operations, extension usage, VACUUM tuning, performance monitoring.

## Quick Facts
- id: `postgres-pro--04ba93383e`
- worth_using_score: `55/100`
- tags: `ci`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/source/agents/tooling/claude-skills/skills/postgres-pro/SKILL.md`

## Use When
- Analyzing and optimizing slow queries with EXPLAIN
- Implementing JSONB storage and indexing strategies
- Setting up streaming or logical replication
- Configuring and using PostgreSQL extensions
- Tuning VACUUM, ANALYZE, and autovacuum
- Monitoring database health with pg_stat views
- Designing indexes for optimal performance

## Workflow / Steps
- **Analyze performance** - Use EXPLAIN ANALYZE, pg_stat_statements
- **Design indexes** - B-tree, GIN, GiST, BRIN based on workload
- **Optimize queries** - Rewrite inefficient queries, update statistics
- **Setup replication** - Streaming or logical based on requirements
- **Monitor and maintain** - VACUUM, ANALYZE, bloat tracking

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
