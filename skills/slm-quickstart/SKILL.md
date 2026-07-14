---
name: slm-quickstart
description: >-
  Take a Small Language Model from zero to running: pick a small open model for
  your hardware, fine-tune it with LoRA/QLoRA, align it (DPO/GRPO), quantize to
  GGUF, and serve it locally. Grounded in the FM-os curated knowledge base.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# slm-quickstart

A cross-runtime skill that walks a user through the full Small Language Model
lifecycle using only vetted, open tooling from [FM-os](https://github.com/wjlgatech/FM-os).

## When to use (trigger)

Invoke when the user says "fine-tune a small model", "run an SLM on my laptop",
"quantize a model", "train a tiny language model", or asks how to post-train /
align a small open model. Also activates on "which small model fits my GPU".

## What it does

1. **Choose a model** — recommends a small open model (SmolLM2, Qwen2.5-1.5B,
   Gemma-2-2B, Llama-3.2-1B/3B) that fits the user's VRAM, checking license.
2. **Fine-tune** — scaffolds a LoRA/QLoRA run with Unsloth or TRL's `SFTTrainer`.
3. **Align** — optional DPO or GRPO post-training pass via `trl`.
4. **Quantize** — converts to GGUF and quantizes to 4-bit with `llama.cpp`.
5. **Serve** — runs the result locally with Ollama or an OpenAI-compatible endpoint.
6. **Evaluate** — sanity-checks quality with `lm-evaluation-harness` before shipping.

## Example

```bash
# fit check -> fine-tune -> quantize -> serve
python -c "print('Qwen2.5-1.5B fits 8GB at 4-bit (~1GB)')"
pip install unsloth trl
# ...LoRA SFT on your dataset, then:
python convert_hf_to_gguf.py ./out --outfile model.gguf
./llama-quantize model.gguf model-q4.gguf Q4_K_M
ollama create my-slm -f Modelfile && ollama run my-slm
```

## Verification (eval-with-teeth)

Before declaring success the skill runs a quick eval and asserts the tuned model
does not regress below the base model on a held-out benchmark:

```bash
lm_eval --model hf --model_args pretrained=./out --tasks arc_easy,hellaswag
```

## Safety

Uses only declared, open tools. No network calls beyond model/dataset download.
No shell beyond the documented commands. No secrets required.

## Cross-runtime

One `SKILL.md`; thin manifests wrap it for Claude Code, Codex, and Hermes.
