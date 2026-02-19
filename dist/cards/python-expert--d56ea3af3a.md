# python-expert

Senior Python developer expertise for writing clean, efficient, and well-documented code.
Use when: writing Python code, optimizing Python scripts, reviewing Python code for best practices,
debugging Python issues, implementing type hints, or when user mentions Python, PEP 8, or needs help
with Python data structures and algorithms.

## Quick Facts
- id: `python-expert--d56ea3af3a`
- worth_using_score: `60/100`
- tags: `python, sql, go, security, testing, ci, docs, rag`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/shubhamsaboo-python-expert/SKILL.md`

## Use When
- **Review [AGENTS.md](AGENTS.md)** for a complete compilation of all rules with examples
- **Reference specific rules** from `rules/` directory for deep dives
- **Follow priority order**: Correctness → Type Safety → Performance → Style
- *Correctness (CRITICAL)**
- [Avoid Mutable Default Arguments](rules/correctness-mutable-defaults.md)
- [Proper Error Handling](rules/correctness-error-handling.md)
- *Type Safety (HIGH)**
- [Use Type Hints](rules/type-hints.md)
- [Use Dataclasses](rules/type-dataclasses.md)
- *Performance (HIGH)**

## Workflow / Steps
- Understand the problem completely
- Choose appropriate data structures
- Plan function interfaces and types
- Consider edge cases early
- Type hints for all function signatures
- Return type annotations
- Generic types using `TypeVar` when needed
- Import types from `typing` module
- Handle all edge cases
- Use proper error handling with specific exceptions

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `2`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
