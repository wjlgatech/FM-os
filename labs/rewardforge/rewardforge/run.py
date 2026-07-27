#!/usr/bin/env python3
"""RewardForge M1 end-to-end: eval-derived pairs -> LoRA-DPO -> held-out gate.

    python -m rewardforge.run [--model HuggingFaceTB/SmolLM2-135M-Instruct]
                              [--epochs 2] [--seed 0] [--samples 3]

Writes out/RESULTS.md (scorecard + sample generations as evidence) and exits
non-zero on ROLLBACK, so the run itself is a gate.
"""
from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

import torch

from . import dpo, gates, pairs

OUT = Path(__file__).resolve().parents[1] / "out"
DEFAULT_MODEL = "HuggingFaceTB/SmolLM2-135M-Instruct"


def generate_captions(model, tokenizer, prompts: list[str], seed: int) -> list[str]:
    torch.manual_seed(seed)
    outs = []
    model.eval()
    for prompt in prompts:
        ids = tokenizer(prompt, return_tensors="pt").input_ids.to(model.device)
        with torch.no_grad():
            gen = model.generate(ids, max_new_tokens=24, do_sample=False,
                                 pad_token_id=tokenizer.eos_token_id)
        outs.append(tokenizer.decode(gen[0][ids.shape[1]:], skip_special_tokens=True).split("\n")[0])
    return outs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--lr", type=float, default=1e-5)
    ap.add_argument("--beta", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--n-per-image", type=int, default=25)
    args = ap.parse_args()

    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer

    dev = dpo.device()
    print(f"device={dev} model={args.model}")
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.float32).to(dev)

    train = pairs.training_pairs(seed=args.seed)
    train = [dict(p) for p in train]
    for p in train:
        p["_enc_w"] = dpo.encode_pair(tokenizer, p["prompt"], p["chosen"])
        p["_enc_l"] = dpo.encode_pair(tokenizer, p["prompt"], p["rejected"])
    print(f"pairs={len(train)} (bare={sum('syndata' in p['provenance'] for p in train)}, "
          f"probe={sum('probe' in p['provenance'] for p in train)})")

    held = pairs.heldout_prompts()
    prompts = [h["prompt"] for h in held]
    images = [h["image"] for h in held]

    # BEFORE: base model on held-out worlds
    before_caps = generate_captions(model, tokenizer, prompts, args.seed)
    before = gates.evaluate(before_caps, images)
    print(f"before: halluc={before['halluc_rate']:.3f} words={before['avg_words']:.1f}")

    # frozen reference log-probs, then attach LoRA
    ref_w = dpo.reference_logprobs(model, [p["_enc_w"] for p in train])
    ref_l = dpo.reference_logprobs(model, [p["_enc_l"] for p in train])
    for p, w, l in zip(train, ref_w, ref_l):
        p["_ref"] = (w, l)
    lora = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
                      lora_dropout=0.0, task_type="CAUSAL_LM")
    model = get_peft_model(model, lora)
    model.print_trainable_parameters()

    stats = dpo.train_dpo(model, tokenizer, train, epochs=args.epochs, seed=args.seed,
                          lr=args.lr, beta=args.beta)
    print(f"trained {stats['steps']} steps; last losses: "
          + ", ".join(f"{h['loss']:.3f}" for h in stats["history"][-3:]))

    # AFTER: tuned model on the same held-out worlds
    after_caps = generate_captions(model, tokenizer, prompts, args.seed)
    after = gates.evaluate(after_caps, images)
    print(f"after:  halluc={after['halluc_rate']:.3f} words={after['avg_words']:.1f}")

    ok, reasons = gates.gate(before, after)
    verdict = "SHIP" if ok else "ROLLBACK — " + "; ".join(reasons)
    print(f"gate: {verdict}")

    OUT.mkdir(exist_ok=True)
    stamp = datetime.date.today().isoformat()
    lines = [
        "# RewardForge M1 — eval-derived preference pairs → LoRA-DPO → held-out gate",
        "",
        f"- **model**: `{args.model}` (LoRA r=16 on q/v_proj, lr={args.lr}, beta={args.beta}, epochs={args.epochs}) · device `{dev}` · {stamp}",
        f"- **pairs**: {len(train)} — chosen/rejected labeled by FM-os's certified gates "
        "(syndata-bare alignment gate + vlm-failure-probe paper failures), zero human labels",
        f"- **held-out**: {len(held)} fact worlds sharing no content words with training",
        "",
        "| metric | before (base) | after (DPO) |",
        "|---|---|---|",
        f"| hallucination rate | {before['halluc_rate']:.3f} | {after['halluc_rate']:.3f} |",
        f"| avg words | {before['avg_words']:.1f} | {after['avg_words']:.1f} |",
        "",
        f"**Gate:** {verdict}",
        "",
        "## Sample held-out generations (evidence)",
        "",
    ]
    for h, b, a in list(zip(held, before_caps, after_caps))[:6]:
        lines += [f"**{h['image']['id']}** — facts: {sorted(h['image']['objects'])}",
                  f"- before: {b.strip()!r}", f"- after:  {a.strip()!r}", ""]
    lines += ["## Training telemetry", "", "```json",
              json.dumps(stats["history"], indent=1), "```", ""]
    (OUT / "RESULTS.md").write_text("\n".join(lines))
    print(f"wrote {OUT / 'RESULTS.md'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
