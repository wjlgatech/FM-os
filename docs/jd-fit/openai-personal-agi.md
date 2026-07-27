# OpenAI — Research Engineer / Research Scientist, Personal AGI (Post-Training) · FM-os dossier

**Role:** Research Engineer / Research Scientist — Personal AGI ·
[official posting](https://openai.com/careers/research-engineer-research-scientist-personal-agi-(post-training)-san-francisco/) ·
San Francisco (hybrid, 3 days/week).

**The team & the job in one line:** the Personal AGI team is a **post-training team** —
it takes pre-trained models the last mile into ChatGPT and the API, using research that
**combines reinforcement learning and products**: preference signal from millions of
users, robust evaluations to track capability improvements, and the safety/efficiency/
reliability bar a deployment to that scale demands. Public signals of the direction:
ChatGPT memory & personalization (user-inspectable memory summaries, automatic memory
updates) and letting customers optimize their own models.

This dossier records how the FM-os flywheel equips a candidate for it: what the hub
curates, what runs, and where the honest edges are. Regenerate the score with
`make jdfit JD=docs/jd-fit/_openai-personal-agi.jd.txt`.

---

## Coverage scorecard (generated, not hand-written)

> The taxonomy (`data/jd_taxonomy.yml`) was extended with the four capabilities this
> role actually turns on — product-driven / deployment research, personalization &
> memory, owning a research agenda (automated AI research), and large-ML-codebase
> engineering. Before that, the scorer reported a **false 100/100 over 4 generic
> capabilities** — it had no keywords for the role's specialty, so it could not see the
> gap. Two capabilities then scored *partial* (knowledge, no tooling); the two skills
> below closed them. This is the honest score.

<!-- BEGIN jdfit -->
# FM-os JD-fit report — **100/100** (8 capabilities required)

| Capability | Coverage | FM-os knowledge | FM-os tooling |
|---|:--:|---|---|
| Training / fine-tuning foundation models | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | slm-quickstart (certified 94), vlm-quickstart (certified 94) |
| Post-training / RL / alignment | ✅ covered | TRL, OpenRLHF, verl | slm-quickstart (certified 94), continual-rl-eval (certified 98), product-rl-loop (certified 98) |
| Agentic evaluation / benchmarking | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), continual-rl-eval (certified 98), vlm-failure-probe (certified 98), syndata-bare (certified 98), product-rl-loop (certified 98), personalization-loop (certified 91) |
| Publishing research (NeurIPS / CVPR) | ✅ covered | CS336: Language Modeling from Scratch, LLM101n: Let's build a Storyteller, Post-training of LLMs | n/a |
| Product-driven research / deployment research | ✅ covered | TRL, OpenRLHF, verl | product-rl-loop (certified 98) |
| Personalization / memory (personal models) | ✅ covered | SmolLM / SmolLM2 / SmolLM3, Phi Cookbook, Gemma (DeepMind) | personalization-loop (certified 91) |
| Owning a research agenda / automated AI research | ✅ covered | AI-Scientist, AI-Scientist-v2, Agent Laboratory | n/a |
| Large ML codebase engineering & debugging | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | n/a |
<!-- END jdfit -->

---

## What was built for this JD (tooling with teeth)

| Asset | What it proves for the role | Evidence |
|---|---|---|
| [`skills/product-rl-loop`](../../skills/product-rl-loop/) (**certified 98**) | The team's core loop — post-train on product preference signal WITHOUT shipping its biases: DPO-style update → held-out frozen judge (win-rate over decided comparisons vs deployed baseline) → safety-regression check → ship/rollback. The demo makes reward hacking a measured weight (+1.9 on a worthless verbosity feature) that the gate catches. | `python reference/product_rl_demo.py` — raw signal ROLLBACK (win 0.07), bias-blind update SHIP (win ≥0.95); 5 tests |
| [`skills/personalization-loop`](../../skills/personalization-loop/) (**certified 91**) | The "Personal" in Personal AGI — per-user memory graded by four gates: lift ≥ floor, cold-start parity, bit-exact cross-user isolation, and memory-pays-rent (wrong-user memory must HURT). Kills adaptivity theater. | `python reference/personal_memory_demo.py` — lift +0.55, cold-start 0.00, leakage 0.0, rent −0.11; 6 tests |

## The wider arsenal this role draws on (already built, cross-repo)

- **Robust evaluations for tracking modeling improvements** (JD bullet 3): FM-os
  `agentic-eval` (per-axis CI gates), `vlm-failure-probe` (failure taxonomy as data →
  gated probe suite; live-measured claude-sonnet-5 5/5 vs VSS baseline 0/5),
  `continual-rl-eval`, `syndata-bare` (twin diversity/alignment gates).
- **Own and pursue a research agenda** (JD bullet 1): `research-loop` (falsifiable
  hypothesis → pre-registered thresholds → ≥3 seeds → ablation → adversarial critique)
  + the **[rsi-os](https://github.com/wjlgatech/rsi-os)** knowledge base — the living
  map of automated AI research (AI-Scientist v1/v2, Agent Laboratory, MLE-bench,
  agent-as-a-judge, Darwin Gödel Machine) with per-paper citation/reproducibility
  status. FM-os curates AI-Scientist/Agent-Laboratory under `category: research`.
- **RL × product closed loops in production shape**:
  **[loop-engineering-anything](https://github.com/wjlgatech/loop-engineering-anything)**
  — maker≠checker enforced fail-closed, independent referee (cli-judge), plateau
  detection + regression rollback + budget; two live_verified F→A demos including a
  cross-repo run over FM-os's own probe suite.
- **Personalization systems already shipped**: super-u's Digital Twin (per-user
  alignment/drift observability, dual heuristic + LLM-judge scoring) and Skillfy
  (per-user knowledge-graph memory with dedup gates).

## Interview prep — the five stories to lead with

1. **"I run the loop this team runs, at hobby scale, with the same discipline"** —
   product-rl-loop's ship/rollback gate; name the bias you projected out and the weight
   it would have learned.
2. **"Evals are my native language"** — the VSS failure-probe suite: taxonomy-as-data,
   no-evidence⇒No, a mitigation must move a measured baseline-vs-patched scorecard.
3. **"Maker ≠ checker, enforced"** — loop-engineering-anything's integrity assertion;
   why a refiner's self-report is never a quality source (KTD4).
4. **"Personalization must pay rent"** — the four gates; wrong-user memory as the
   falsifier of personalization claims.
5. **"Deployed to millions" instinct** — Accenture OpenAI-DSI engagement (FDE),
   confidence-calibrated selective verification (~90% annotation cost cut), zero-downtime
   replanning in agentic production systems.

## Honest edges (know them before the interview)

- No frontier-scale pretraining/post-training run on the resume — the loops are proven
  at demo scale with the correct *discipline*; the scale story leans on the eval and
  deployment work (6+ VLM production eval framework, live client systems).
- The `personalization-loop` skill certifies at 91 with a relevance note (54) — the
  certifier's keyword net under-reads personalization as an FM-ops capability;
  a future certifier iteration should learn the `personalization` topic.
- The two demos are numpy-scale by design (swap-seam to TRL/OpenRLHF/verl documented);
  nobody should claim they are RLHF at scale — they are the *gates* RLHF at scale
  ships through.

## Sources

- Official posting: openai.com/careers (Personal AGI, Post-Training, San Francisco)
- ChatGPT memory/personalization public direction: OpenAI Help Center Memory FAQ ·
  OpenAI Academy "Personalizing ChatGPT" · third-party analyses of the memory system
- Team-adjacent signal: OpenAI agent-team interviews naming personalization + memory
  as the push-on areas (Sequoia Training Data podcast)
