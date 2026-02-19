# evaluating-llms-harness

Evaluates LLMs across 60+ academic benchmarks (MMLU, HumanEval, GSM8K, TruthfulQA, HellaSwag). Use when benchmarking model quality, comparing models, reporting academic results, or tracking training progress. Industry standard used by EleutherAI, HuggingFace, and major labs. Supports HuggingFace, vLLM, APIs.

## Quick Facts
- id: `evaluating-llms-harness--3951f5327c`
- worth_using_score: `75/100`
- tags: `github, git, python, ci, docs, llm, eval, benchmark`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/davila7-evaluating-llms-harness/SKILL.md`

## Use When
- *Use lm-evaluation-harness when:**
- Benchmarking models for academic papers
- Comparing model quality across standard tasks
- Tracking training progress
- Reporting standardized metrics (everyone uses same prompts)
- Need reproducible evaluation
- *Use alternatives instead:**
- **HELM** (Stanford): Broader evaluation (fairness, efficiency, calibration)
- **AlpacaEval**: Instruction-following evaluation with LLM judges
- **MT-Bench**: Conversational multi-turn evaluation

## Workflow / Steps
- [ ] Step 1: Choose benchmark suite
- [ ] Step 2: Configure model
- [ ] Step 3: Run evaluation
- [ ] Step 4: Analyze results
- *Step 1: Choose benchmark suite**
- *Core reasoning benchmarks**:
- **MMLU** (Massive Multitask Language Understanding) - 57 subjects, multiple choice
- **GSM8K** - Grade school math word problems
- **HellaSwag** - Common sense reasoning
- **TruthfulQA** - Truthfulness and factuality

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `35`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
