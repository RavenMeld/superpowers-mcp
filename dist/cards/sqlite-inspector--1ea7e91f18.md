# sqlite-inspector

Проверка консистентности данных в SQLite базах данных MikoPBX после операций REST API. Использовать при валидации результатов API, отладке проблем с данными, проверке связей внешних ключей или инспектировании CDR записей для тестирования.

## Quick Facts
- id: `sqlite-inspector--1ea7e91f18`
- worth_using_score: `80/100`
- tags: `sql, sqlite, go, docker, security, testing, ci, rag`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/sqlite-inspector/SKILL.md`

## Use When
- **After API operations** - Verify create/update/delete operations modified database correctly
- **Debugging data issues** - Investigate inconsistencies between API responses and database state
- **Before integration tests** - Ensure database is in expected state
- **Validating foreign keys** - Check relationships between tables are correct
- **Inspecting CDR records** - Query call history for testing routing and recording

## Workflow / Steps
- docker exec <container_id> lsof /cf/conf/mikopbx.db

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `14`
- has_scripts: `True`
- has_references: `False`
- has_assets: `False`
