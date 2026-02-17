# story-roleplay

Parse and apply character cards and world info files in multiple formats (PNG, WebP, JSON), fully compatible with SillyTavern format. Supports automatic parsing, keyword triggering, and dynamic updates.

## Quick Facts
- id: `story-roleplay--d82f961258`
- worth_using_score: `75/100`
- tags: `node, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/story-roleplay/SKILL.md`

## Use When
- **Keyword detection**: Monitor conversation content, detect if it contains world info keywords
- **Content injection**: When keywords appear, integrate corresponding content into response, sorted by priority
- **Natural integration**: Do not insert world info content awkwardly, naturally integrate into conversation and narrative

## Workflow / Steps
- *Step 1: Copy Preset Tool**
- **Method 1 (Highest Priority)**: Relative path (if workspace is under project root):
- **Method 2**: Search upward for project root (up to 5 levels):
- **Method 3**: Global search (exclude temp directories):
- **Verify**: Confirm files copied
- If files don't exist, continue to next method or use fallback option
- *Step 2: Install Dependencies**
- Wait for completion, check if `node_modules` was created
- If fails: Check network/permission/Node.js environment
- *Step 3: Execute Parser**

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `5`
- has_scripts: `True`
- has_references: `False`
- has_assets: `False`
