# rag-pipeline-basics

Build a practical RAG pipeline: document ingestion, chunking, embeddings, retrieval, reranking, and evaluation.
Focuses on “what works” patterns and failure modes.

## Quick Facts
- id: `rag-pipeline-basics--5e17ad92f1`
- worth_using_score: `50/100`
- tags: `rust, ci, docs, rag, eval`
- source: `agent_playground`
- source_path: `/home/wolvend/codex/agent_playground/projects/awesome-skills-database/skillpacks/ravenmeld/rag-pipeline-basics/SKILL.md`

## Use When
- You need grounded answers over a private corpus (docs/repos/notes).
- You need citations or traceability to source documents.
- The model’s raw knowledge is insufficient or out of date.

## Workflow / Steps
- Ingest documents (normalize text + metadata).
- Chunk the docs (size + overlap tuned per doc type).
- Embed chunks and store in a vector index.
- Retrieve top-k candidates for a query.
- Rerank candidates (optional but often worth it).
- Answer with citations (include source ids/paths/URLs).
- Evaluate with a small suite of real questions.

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
