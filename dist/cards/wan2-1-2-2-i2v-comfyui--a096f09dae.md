# Wan2.1/2.2 I2V ComfyUI

This skill should be used when the user asks to "implement Wan I2V", "set up Wan2.1", "configure Wan2.2", "image to video with Wan", "ComfyUI video generation", "low VRAM video generation", "GGUF Wan model", "setup video diffusion model", "Wan I2Vを実装", "Wan2.1をセットアップ", "Wan2.2を設定", "画像から動画生成", "ComfyUIで動画生成", "低VRAMで動画生成", "GGUFモデルを使用", "動画生成モデルのセットアップ", or needs guidance on Wan2.1/2.2 image-to...

## Quick Facts
- id: `wan2-1-2-2-i2v-comfyui--a096f09dae`
- worth_using_score: `40/100`
- tags: `github, comfyui, node, ci`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/wan2122-i2v-comfyui/SKILL.md`

## Workflow / Steps
- ### 基本的なI2Vワークフロー構成
- ```
- [Load Image] → [CLIP Vision Encode] ─┐
- │
- [Load Text Encoder] → [Text Encode] ──┤
- ├→ [WanVideo Sampler] → [VAE Decode] → [Save Video]

## Signal Summary
- has_description: `True`
- has_use_when: `False`
- has_workflow: `True`
- code_examples: `3`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
