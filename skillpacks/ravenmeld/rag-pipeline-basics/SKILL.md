---
name: rag-pipeline-basics
description: |
  Build a practical RAG pipeline: document ingestion, chunking, embeddings, retrieval, reranking, and evaluation.
  Focuses on “what works” patterns and failure modes.
---

# RAG Pipeline Basics

## Use When

- You need grounded answers over a private corpus (docs/repos/notes).
- You need citations or traceability to source documents.
- The model’s raw knowledge is insufficient or out of date.

## Workflow

1. Ingest documents (normalize text + metadata).
2. Chunk the docs (size + overlap tuned per doc type).
3. Embed chunks and store in a vector index.
4. Retrieve top-k candidates for a query.
5. Rerank candidates (optional but often worth it).
6. Answer with citations (include source ids/paths/URLs).
7. Evaluate with a small suite of real questions.

## Chunking Defaults (Start Here)

- Docs: 400-800 tokens per chunk, 50-150 token overlap.
- Code: chunk by file + function/class boundaries if possible.
- Keep metadata:
  - `source_path`
  - `title`
  - `timestamp`
  - `tags`

## Retrieval Defaults (Start Here)

- Use hybrid retrieval when possible:
  - vector similarity + keyword/FTS
- Use reranking for better precision on broad corpora.

## Evaluation Checklist

- Can the system answer “where is this documented?” with citations?
- Does it hallucinate sources?
- Does it miss obvious matches because chunking is wrong?
- Does retrieval drift to irrelevant but semantically similar chunks?

## Safety Notes

- Do not ingest secrets unless the store is access-controlled.
- Redact known token patterns before indexing if the corpus is untrusted.

