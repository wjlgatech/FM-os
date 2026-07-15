---
name: vlm-quickstart
description: >-
  Take a Vision-Language Model from zero to running on VIDEO: pick an open VLM,
  prepare video + sensor-metadata data, fine-tune it (LoRA/QLoRA) for motion
  understanding, evaluate spatiotemporal reasoning + localization, and serve it.
  Built for autonomous-driving / robotics multi-modal workflows.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# vlm-quickstart

A cross-runtime skill for the full **Vision-Language Model on video** lifecycle, using vetted
open tooling from [FM-os](https://github.com/wjlgatech/FM-os). Aimed at motion-understanding tasks
(turns, lane changes, interactions, anomalies) over autonomous-driving and robotics footage.

## When to use (trigger)

Invoke when the user says "fine-tune a VLM", "train a vision-language model on video", "motion
understanding", "spatiotemporal reasoning", or "multi-modal model for driving/robotics video".

## What it does

1. **Choose a VLM** — recommends an open model (Qwen2.5-VL, InternVL, LLaVA-NeXT-Video,
   VideoLLaMA) sized to the GPU budget.
2. **Prepare data** — builds a video+language(+sensor metadata) dataset: frame sampling, clip
   windows, and instruction pairs describing motion events.
3. **Fine-tune** — LoRA/QLoRA fine-tune via `ms-swift` or `LLaMA-Factory`, DeepSpeed for scale.
4. **Evaluate** — spatiotemporal reasoning, localization accuracy, and narrative consistency via
   `lmms-eval` / `VLMEvalKit` (see the sibling `agentic-eval` skill).
5. **Serve** — deploy with vLLM / SGLang behind an OpenAI-compatible multi-modal endpoint.

## Example

```bash
pip install ms-swift lmms-eval
# LoRA fine-tune Qwen2.5-VL on a video instruction dataset
swift sft --model Qwen/Qwen2.5-VL-7B-Instruct --dataset ./driving_clips.jsonl \
  --train_type lora --deepspeed zero2
# evaluate spatiotemporal reasoning
python -m lmms_eval --model qwen2_5_vl --tasks videomme,mmbench_video
```

## Verification (eval-with-teeth)

Asserts the fine-tuned VLM does not regress below the base model on a held-out video benchmark
(e.g. Video-MME) before shipping.

## Safety

Uses only declared open tools; downloads models/datasets over HTTPS. No secrets, no arbitrary
shell beyond the documented commands.

## Cross-runtime

One `SKILL.md`; thin manifests wrap it for Claude Code, Codex, and Hermes.
