# dspy-ruby

Build type-safe LLM applications with DSPy.rb — Ruby's programmatic prompt framework with signatures, modules, agents, and optimization. Use when implementing predictable AI features, creating LLM signatures and modules, configuring language model providers, building agent systems with tools, optimizing prompts, or testing LLM-powered functionality in Ruby applications.

## Quick Facts
- id: `dspy-ruby--41c758879d`
- worth_using_score: `63/100`
- tags: `github, git, node, go, testing, ci, observability, rag, llm, eval`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/dspy-ruby/SKILL.md`

## Use When
- *Use schemas (T::Struct/T::Enum)** for:
- Multi-field outputs with specific types
- Enums with defined values the LLM must pick from
- Nested structures, arrays of typed objects
- Outputs consumed by code (not displayed to users)
- *Use string descriptions** for:
- Simple single-field outputs where the type is `String`
- Natural language generation (summaries, answers)
- Fields where constraint guidance helps (e.g., `description: "YYYY-MM-DD format"`)
- *Rule of thumb**: If you'd write a `case` statement on the output, it should be a `T::Enum`. If you'd call `.each` on it, it should be `T::Array[SomeStruct]`.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `False`
- code_examples: `32`
- has_scripts: `False`
- has_references: `True`
- has_assets: `True`
