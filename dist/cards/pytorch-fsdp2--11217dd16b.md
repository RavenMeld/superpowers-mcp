# pytorch-fsdp2

Adds PyTorch FSDP2 (fully_shard) to training scripts with correct init, sharding, mixed precision/offload config, and distributed checkpointing. Use when models exceed single-GPU memory or when you need DTensor-based sharding with DeviceMesh.

## Quick Facts
- id: `pytorch-fsdp2--11217dd16b`
- worth_using_score: `55/100`
- tags: `node, ci, docs`
- source: `codex_skills`
- source_path: `/home/wolvend/.codex/skills/orchestra-research-pytorch-fsdp2/SKILL.md`

## Use When
- Your model **doesn’t fit** on one GPU (parameters + gradients + optimizer state).
- You want an eager-mode sharding approach that is **DTensor-based per-parameter sharding** (more inspectable, simpler sharded state dicts) than FSDP1.
- You may later compose DP with **Tensor Parallel** using **DeviceMesh**.
- You need strict backwards-compatible checkpoints across PyTorch versions (DCP warns against this).
- You’re forced onto older PyTorch versions without the FSDP2 stack.

## Workflow / Steps
- Prefer a recent stable PyTorch where the docs show FSDP2 and DCP updated recently.
- Use `torchrun --nproc_per_node <gpus_per_node> ...` and ensure `RANK`, `WORLD_SIZE`, `LOCAL_RANK` are visible.
- --
- `dist.init_process_group(backend="nccl")`
- `torch.cuda.set_device(int(os.environ["LOCAL_RANK"]))`
- Optionally create a `DeviceMesh` to describe the data-parallel group(s)
- --
- `with torch.device("meta"): model = ...`
- apply `fully_shard(...)` on submodules, then `fully_shard(model)`
- `model.to_empty(device="cuda")`

## Signal Summary
- has_description: `True`
- has_use_when: `True`
- has_workflow: `True`
- code_examples: `0`
- has_scripts: `False`
- has_references: `True`
- has_assets: `False`
