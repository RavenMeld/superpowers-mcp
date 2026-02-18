# obsidian-performance-tuning

Optimize Obsidian plugin performance for smooth operation.
Use when experiencing lag, memory issues, or slow startup,
or when optimizing plugin code for large vaults.
Trigger with phrases like "obsidian performance", "obsidian slow",
"optimize obsidian plugin", "obsidian memory usage".

## Quick Facts
- id: `obsidian-performance-tuning--c57f6bd919`
- worth_using_score: `55/100`
- tags: `typescript, node, go, java, ci, docs, obsidian, render, rag, benchmark`
- source: `agents_skills`
- source_path: `/home/wolvend/.agents/skills/jeremylongshore-obsidian-performance-tuning/SKILL.md`

## Workflow / Steps
- ```typescript
- // src/utils/file-processor.ts
- import { TFile, Vault } from 'obsidian';
- export class EfficientFileProcessor {
- private vault: Vault;
- private cache: Map<string, { content: string; mtime: number }> = new Map();

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `8`
- has_scripts: `False`
- has_references: `False`
- has_assets: `False`
