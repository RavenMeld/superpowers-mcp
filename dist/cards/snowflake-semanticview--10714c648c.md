# snowflake-semanticview

Create, alter, and validate Snowflake semantic views using Snowflake CLI (snow). Use when asked to build or troubleshoot semantic views/semantic layer definitions with CREATE/ALTER SEMANTIC VIEW, to validate semantic-view DDL against Snowflake via CLI, or to guide Snowflake CLI installation and connection setup.

## Quick Facts
- id: `snowflake-semanticview--10714c648c`
- worth_using_score: `50/100`
- tags: `sql, ci, docs, terminal, rag`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/snowflake-semanticview/SKILL.md`

## Workflow / Steps
- Confirm the target database, schema, role, warehouse, and final semantic view name.
- Confirm the model follows a star schema (facts with conformed dimensions).
- Draft the semantic view DDL using the official syntax:
- https://docs.snowflake.com/en/sql-reference/sql/create-semantic-view
- Populate synonyms and comments for each dimension, fact, and metric:
- Read Snowflake table/view/column comments first (preferred source):
- https://docs.snowflake.com/en/sql-reference/sql/comment
- If comments or synonyms are missing, ask whether you can create them, whether the user wants to provide text, or whether you should draft suggestions for approval.
- Use SELECT statements with DISTINCT and LIMIT (maximum 1000 rows) to discover relationships between fact and dimension tables, identify column data types, and create more meaningful comments and synonyms for columns.
- Create a temporary validation name (for example, append `__tmp_validate`) while keeping the same database and schema.

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `4`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
