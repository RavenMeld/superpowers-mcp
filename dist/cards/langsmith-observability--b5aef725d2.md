# langsmith-observability

LLM observability platform for tracing, evaluation, and monitoring. Use when debugging LLM applications, evaluating model outputs against datasets, monitoring production systems, or building systematic testing pipelines for AI applications.

## Quick Facts
- id: `langsmith-observability--b5aef725d2`
- worth_using_score: `75/100`
- tags: `github, git, python, go, testing, ci, docs, observability, rag, llm, eval`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/davila7-langsmith-observability/SKILL.md`

## Use When
- *Use LangSmith when:**
- Debugging LLM application issues (prompts, chains, agents)
- Evaluating model outputs systematically against datasets
- Monitoring production LLM systems
- Building regression testing for AI features
- Analyzing latency, token usage, and costs
- Collaborating on prompt engineering
- *Key features:**
- **Tracing**: Capture inputs, outputs, latency for all LLM calls
- **Evaluation**: Systematic testing with built-in and custom evaluators

## Workflow / Steps
- ```python
- def sanitize_inputs(inputs: dict) -> dict:
- if "password" in inputs:
- inputs["password"] = "***"
- return inputs
- @traceable(process_inputs=sanitize_inputs)

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `22`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
