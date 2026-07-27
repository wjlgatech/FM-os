---
name: product-rl-loop
description: >-
  Run product-driven post-training as a gated closed loop: collect user
  preference signal from a live product, update the policy (DPO/GRPO-style),
  judge on a HELD-OUT independent gate (win-rate vs the frozen deployed
  baseline + safety regression), and ship or roll back. Makes reward hacking
  from biased product signal a measured, caught failure — not a shipped one.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# product-rl-loop

A cross-runtime skill for the **RL × product** discipline a post-training team runs at
frontier scale (the OpenAI Personal-AGI-style loop): product telemetry is the cheapest
preference signal you have and the most biased. This skill turns "train on user feedback"
into a **gated deployment loop** where the bias is measured and the gate — not optimism —
decides what ships.

## When to use (trigger)

Invoke when the user says "post-train on user feedback", "RLHF/DPO from product signal",
"preference optimization", "reward hacking", "ship or rollback a model update", "win-rate
gate", "A/B the new checkpoint", or "product-driven research".

## What it does

1. **Frame the signal** — what product event is the preference (thumbs, regen, choice
   between candidates)? What KNOWN biases ride on it (length, sycophancy, position,
   recency)? Each named bias becomes a measured quantity, not a vibe.
2. **Update the policy** — DPO-style pairwise objective on the preference pairs
   (scale: TRL / OpenRLHF / verl — all curated in FM-os `data/repos.yml`).
3. **Blind the update to known biases** — project the bias direction out of the update
   (or debias pairs) so the optimizer *cannot* express it; verify the bias weight stayed
   put.
4. **Gate on held-out, frozen judgment** — win-rate vs the deployed baseline over
   *decided* comparisons (ties carry no signal) on prompts the training never saw, PLUS
   a safety-regression check (unsafe pick-rate must not rise). The judge is independent
   of the maker (maker ≠ checker).
5. **Ship or roll back** — a failing gate is a rollback to the deployed baseline, exit
   non-zero so it gates CI. An honest ❌ beats a fake ✅.

## Example

```bash
# self-contained proof (numpy only): raw biased product signal gets reward-hacked
# and ROLLED BACK; the bias-blind update SHIPS — exits non-zero if either flips
python reference/product_rl_demo.py
# offline gate:
python -m pytest reference/test_product_rl_demo.py -q
```

```python
from reference.product_rl_demo import run_arm
raw = run_arm(debias=False)   # learns verbosity ≈ +1.9 (true worth: 0) → win-rate 0.07 → ROLLBACK
fix = run_arm(debias=True)    # bias direction frozen → win-rate ≥ 0.95 → SHIP
assert fix["ship"] and not raw["ship"]
```

## Discipline (why this is trustworthy)

- **Reward hacking is a measured weight** — the demo's biased arm visibly learns the
  worthless verbosity feature (+1.9); no anecdote, a number.
- **The gate is held-out and frozen** — the judge never sees training pairs and compares
  against the *deployed* baseline, so "preference accuracy up" cannot masquerade as
  "model better".
- **Safety is a blocking check** — an unsafe pick-rate regression fails the gate
  regardless of win-rate (the FM-os Certified no-fake-pass discipline).

## Deeper reference (FM-os knowledge base)

Ouyang et al., *InstructGPT* (RLHF from human feedback) · Rafailov et al., *DPO* — both in
[`data/papers.yml`](../../data/papers.yml) · scale stacks: TRL, OpenRLHF, verl
(`data/repos.yml`) · siblings: [`personalization-loop`](../personalization-loop/)
(the Personal-AGI memory half), [`agentic-eval`](../agentic-eval/) (eval axes + CI gates),
[`research-loop`](../research-loop/) (pre-registered experiments). JD dossier:
[`docs/jd-fit/openai-personal-agi.md`](../../docs/jd-fit/openai-personal-agi.md).
