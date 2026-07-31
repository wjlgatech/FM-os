#!/usr/bin/env python3
"""RewardForge M2 — the research-loop rigor pass: multi-seed + ablation.

    python -m rewardforge.sweep [--seeds 0 1 2] [--epochs 1]

Two arms under identical budgets:
  treatment  eval-derived pairs (chosen = gate-approved, rejected = gate-failed)
  shuffled   ABLATION control: same pairs, chosen/rejected randomly swapped per
             pair (50%, seeded) — destroys the label signal, preserves the data
             distribution. If this arm "improves" too, the claim is dead.

Pre-registered verdicts (research-loop discipline, declared before running):
  CONFIRMED   every treatment seed drops held-out hallucination by >= 0.05 AND
              the best (lowest) shuffled drop is worse than the worst treatment drop
  NO-EFFECT   treatment and shuffled ranges overlap — reported as no effect, never inflated
  REFUTED     shuffled matches/beats treatment — the pairs' labels carry no signal

Writes out/M2-RESULTS.md with per-seed numbers, mean±std, and the verdict.
"""
from __future__ import annotations

import argparse
import datetime
import json
import random
import statistics
import sys
from pathlib import Path

import torch

from . import dpo, gates, pairs

OUT = Path(__file__).resolve().parents[1] / "out"
MODEL = "HuggingFaceTB/SmolLM2-135M-Instruct"
MIN_DROP = 0.05  # pre-registered treatment floor (same as the M1 ship gate)


def run_arm(seed: int, shuffled: bool, epochs: int) -> dict:
    from peft import LoraConfig, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from .run import generate_captions

    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.float32).to(dpo.device())

    train = [dict(p) for p in pairs.training_pairs(seed=seed)]
    if shuffled:  # ablation: kill the label signal, keep the distribution
        rng = random.Random(1000 + seed)
        for p in train:
            if rng.random() < 0.5:
                p["chosen"], p["rejected"] = p["rejected"], p["chosen"]
    for p in train:
        p["_enc_w"] = dpo.encode_pair(tokenizer, p["prompt"], p["chosen"])
        p["_enc_l"] = dpo.encode_pair(tokenizer, p["prompt"], p["rejected"])

    held = pairs.heldout_prompts()
    prompts = [h["prompt"] for h in held]
    images = [h["image"] for h in held]

    before = gates.evaluate(generate_captions(model, tokenizer, prompts, seed), images)
    ref_w = dpo.reference_logprobs(model, [p["_enc_w"] for p in train])
    ref_l = dpo.reference_logprobs(model, [p["_enc_l"] for p in train])
    for p, w, l in zip(train, ref_w, ref_l):
        p["_ref"] = (w, l)
    model = get_peft_model(model, LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj", "v_proj"],
                                             lora_dropout=0.0, task_type="CAUSAL_LM"))
    rng = random.Random(seed)
    rng.shuffle(train)
    dpo.train_dpo(model, tokenizer, train, epochs=epochs, seed=seed, lr=1e-5, beta=0.2)
    after = gates.evaluate(generate_captions(model, tokenizer, prompts, seed), images)

    drop = before["halluc_rate"] - after["halluc_rate"]
    row = {"seed": seed, "arm": "shuffled" if shuffled else "treatment",
           "before": round(before["halluc_rate"], 4), "after": round(after["halluc_rate"], 4),
           "drop": round(drop, 4), "avg_words_after": round(after["avg_words"], 2)}
    print(json.dumps(row))
    del model
    return row


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    ap.add_argument("--epochs", type=int, default=1)
    args = ap.parse_args()

    rows = []
    for seed in args.seeds:
        for shuffled in (False, True):
            rows.append(run_arm(seed, shuffled, args.epochs))

    treat = [r["drop"] for r in rows if r["arm"] == "treatment"]
    shuf = [r["drop"] for r in rows if r["arm"] == "shuffled"]
    t_mean, t_std = statistics.mean(treat), statistics.stdev(treat) if len(treat) > 1 else 0.0
    s_mean, s_std = statistics.mean(shuf), statistics.stdev(shuf) if len(shuf) > 1 else 0.0

    if min(treat) >= MIN_DROP and max(shuf) < min(treat):
        verdict = "CONFIRMED — every treatment seed clears the floor and the best control is worse than the worst treatment"
    elif max(shuf) >= min(treat):
        verdict = ("REFUTED — the shuffled control matches or beats a treatment seed; the labels carry no signal"
                   if s_mean >= t_mean else
                   "NO-EFFECT — treatment and control ranges overlap; reported as no effect, not inflated")
    else:
        verdict = "NO-EFFECT — treatment below the pre-registered floor on at least one seed"

    stamp = datetime.date.today().isoformat()
    lines = [
        "# RewardForge M2 — multi-seed + shuffled-pair ablation (research-loop rigor pass)",
        "",
        f"- **model**: `{MODEL}` (LoRA r=16, lr=1e-5, beta=0.2, {args.epochs} epoch) · seeds {args.seeds} · {stamp}",
        "- **treatment**: eval-derived pairs (labels from FM-os certified gates)",
        "- **ablation control**: identical pairs, chosen/rejected randomly swapped 50% per pair (seeded)",
        f"- **pre-registered**: treatment floor drop ≥ {MIN_DROP}; verdict rules declared in `rewardforge/sweep.py` before running",
        "",
        "| seed | arm | halluc before | after | drop |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(f"| {r['seed']} | {r['arm']} | {r['before']:.3f} | {r['after']:.3f} | {r['drop']:+.3f} |")
    lines += [
        "",
        f"**treatment drop: {t_mean:+.3f} ± {t_std:.3f}** (n={len(treat)}) · **shuffled drop: {s_mean:+.3f} ± {s_std:.3f}** (n={len(shuf)})",
        "",
        f"## Verdict: {verdict}",
        "",
        "Threats to validity: single small model (135M); toy grounding task; 8 held-out worlds;",
        "greedy decoding (deterministic eval). Reproduce: `python -m rewardforge.sweep`.",
    ]
    OUT.mkdir(exist_ok=True)
    (OUT / "M2-RESULTS.md").write_text("\n".join(lines))
    print(f"wrote {OUT / 'M2-RESULTS.md'}")
    print(f"verdict: {verdict}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
