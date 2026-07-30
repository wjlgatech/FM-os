# Paul Jialiang Wu, PhD

**Research Engineer — Developer Experience · Post-Training (SFT/RL) · Open-Source**

[wjlgatech@gmail.com](mailto:wjlgatech@gmail.com) · [github.com/wjlgatech](https://github.com/wjlgatech) · [linkedin.com/in/paul-jialiang-wu-phd](https://www.linkedin.com/in/paul-jialiang-wu-phd) · [live portfolio](https://agentic-portfolio-lovat.vercel.app)

## SUMMARY

Research engineer who is happiest in a code editor, building the recipes, docs, and tools
that make fine-tuning work for other people. I ship post-training as **runnable, eval-gated
cookbook recipes**: a real LoRA-DPO fine-tune with a from-scratch DPO loss (torch+peft) that
a held-out gate shipped — and that the same gate honestly rolled back when a bad learning
rate regressed it ([FM-os/rewardforge](https://github.com/wjlgatech/FM-os/tree/main/labs/rewardforge)). Creator of an open-source FM-ops hub ([FM-os](https://github.com/wjlgatech/FM-os)) of 14 certified
skills, each an evidence-gated recipe (no evidence ⇒ No), with a README generated as a
build artifact from spec data and kept honest by drift gates and weekly freshness CI.
Currently forward-deployed at Accenture as the primary technical interface on an enterprise
AI engagement — the person users call when their pipeline breaks — translating ambiguous
requirements into shipped workflows and instilling rigorous development practice in
customer engineering teams. PhD-trained; 8+ years of production ML; deep OSS habit
([loop-engineering-anything](https://github.com/wjlgatech/loop-engineering-anything): 543 passing tests with an independent maker≠checker referee).

## WHY TINKER DX — I ALREADY BUILD COOKBOOKS WITH GATES

- **Fine-tuning with SFT+RL, hands on the primitives:** [labs/rewardforge](https://github.com/wjlgatech/FM-os/tree/main/labs/rewardforge) (FM-os) — real
  LoRA-DPO of SmolLM2-135M with the DPO loss written from scratch (torch+peft); held-out
  hallucination 0.398→0.287 → SHIP; a bad-lr attempt rolled back by the same gate; 162
  preference pairs, zero human labels. [product-rl-loop](https://github.com/wjlgatech/FM-os/tree/main/skills/product-rl-loop) (certified 98/100): preference
  signal → DPO update → held-out frozen-judge win-rate gate → ship/rollback.
  [slm-quickstart](https://github.com/wjlgatech/FM-os/tree/main/skills/slm-quickstart) (94): LoRA/QLoRA → DPO/GRPO → GGUF → serve, end to end.
- **Docs and recipes as the product:** [FM-os](https://github.com/wjlgatech/FM-os) is a cookbook with teeth — 14 skills
  certified by an evidence-based rubric-as-data certifier; the README itself is a build
  artifact generated from data/*.yml with drift gates (make check), so docs cannot
  silently rot. Newest: [tinker-loop](https://github.com/wjlgatech/FM-os/tree/main/skills/tinker-loop) (FM-os, certified 98/100): the Tinker mental model —
  forward_backward / optim_step / sample / save_state + LoRA adapters — implemented
  keylessly in pure numpy as a teaching/CI artifact, cookbook-style recipe with an eval gate.
- **Developer ergonomics and onboarding, measured:** keyless demos that run in CI (no API
  key, no friction — [rewardforge](https://github.com/wjlgatech/FM-os/tree/main/labs/rewardforge), [tinker-loop](https://github.com/wjlgatech/FM-os/tree/main/skills/tinker-loop)); a [JD-fit engine](https://github.com/wjlgatech/FM-os/blob/main/scripts/jdfit.py) that machine-scores the
  hub's own readiness and extends its taxonomy before scoring itself (honest, no fake
  pass); quickstart skills built to get a newcomer from zero to a served model.
  Forward-deployed day job: debugging user pipelines directly and turning each fix into
  enablement.

## CURRENT WORK ON TINKER (July 2026)

- [**tinker-loop**](https://github.com/wjlgatech/FM-os/tree/main/skills/tinker-loop) — shipped, certified 98/100 (above): the four primitives + LoRA, keyless
  in numpy; the naive SFT recipe is honestly rolled back by a forgetting gate (+208%
  caught), the replay recipe ships.
- [**tinker-gates**](https://github.com/wjlgatech/FM-os/blob/main/docs/jd-fit/thinking-machines-tinker-dx.md) — in design for Tinker's [Call for Community Projects](https://thinkingmachines.ai/news/call-for-community-projects/): ship/rollback
  gates (held-out judge, forgetting cap, reward-hack probe) wrapping any cookbook training
  loop; kill criteria pre-registered.
- [**tinker-local**](https://github.com/wjlgatech/FM-os/blob/main/docs/jd-fit/thinking-machines-tinker-dx.md) — in design: a pip-installable keyless mock of the Tinker training
  client ("moto for Tinker") so cookbook recipes run in CI before spending GPU credit.

## OPEN SOURCE — SELECTED (github.com/wjlgatech, 12 active repos, 280+ commits/month)

[**FM-os**](https://github.com/wjlgatech/FM-os) — *Spec-as-data foundation-model-ops hub · Creator*
Registry-governed skills, each certified by an evidence-based rubric (security,
correctness, eval-with-teeth; no evidence ⇒ No): [slm-quickstart](https://github.com/wjlgatech/FM-os/tree/main/skills/slm-quickstart), [product-rl-loop](https://github.com/wjlgatech/FM-os/tree/main/skills/product-rl-loop),
[continual-rl-eval](https://github.com/wjlgatech/FM-os/tree/main/skills/continual-rl-eval), [agentic-eval](https://github.com/wjlgatech/FM-os/tree/main/skills/agentic-eval), [research-loop](https://github.com/wjlgatech/FM-os/tree/main/skills/research-loop), [bayesopt-loop](https://github.com/wjlgatech/FM-os/tree/main/skills/bayesopt-loop), and more — plus [tinker-loop](https://github.com/wjlgatech/FM-os/tree/main/skills/tinker-loop)
(certified 98/100). README generated from data/*.yml with drift gates; weekly freshness
CI; badges. Home of the [rewardforge](https://github.com/wjlgatech/FM-os/tree/main/labs/rewardforge) LoRA-DPO lab and the [jdfit](https://github.com/wjlgatech/FM-os/blob/main/scripts/jdfit.py) self-scoring engine.

[**loop-engineering-anything**](https://github.com/wjlgatech/loop-engineering-anything) — *Self-improving loop orchestrator · Creator*
Turns any API or codebase into a self-improving, agent-native CLI via a generate → judge →
refactor → re-judge loop. Quality comes ONLY from an independent referee (maker ≠ checker
enforced fail-closed); multi-signal convergence (plateau detection + regression rollback +
iteration/token budgets) prevents recursive degradation. 543 passing tests, CI on
3.11–3.13; live-verified F→A runs including a cross-repo loop over FM-os's own eval suite.

[**cli-judge**](https://github.com/wjlgatech/cli-judge) — *LLM-as-judge scoring harness · Creator*
Reproducible Definition-of-Done scorecards for ranking model/agent output quality — the
independent referee the loops above ship through.

**super-u** — *Multi-agent human-upgrade platform · Creator (private)*
Three agentic layers behind one LLM-provider seam; per-call efficiency telemetry as the
floor any model or prompt change must beat.

## EXPERIENCE

**Applied AI Scientist / Forward Deployed Engineer — Accenture, Physical AI Team** · Jan 2024–Present

*Forward-Deployed Delivery · User-Facing Debugging & Enablement*

- Primary technical interface for an executive-level enterprise AI deployment (OpenAI-DSI
  engagement) — the direct line for customer engineers when pipelines break; recognized
  for a "no surprises" standard built on deep model understanding and contextual judgment
  at decision points.
- Translated ambiguous customer requirements into shipped agentic workflows; co-built with
  customer engineering teams to instill rigorous development practice — the
  debug-then-enable loop this role runs at API scale.

*Evaluation & Foundation Models*

- Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS,
  Cosmos-Predict2) on accuracy, latency under real-world load, edge-case failure modes,
  and integration cost — the basis for production model selection and the
  training/inference tradeoff conversations that follow.
- Shipped a confidence-calibrated selective-verification pipeline routing only
  high-uncertainty outputs to human review: ~90% annotation cost reduction with coverage
  preserved where confidence is low.
- Technical lead on 4 simultaneous production systems: synthetic data generation,
  zero-shot safety detection, adaptive evaluation under distribution shift, hybrid
  vision-language reasoning over live sensor streams.

**Principal Data Scientist — Genentech** · Jun 2021–Dec 2022

- Production ML for biomedical research; 3 open-source PyPI packages for multimodal
  learning adopted by the research community; 85% reduction in unproductive process time
  via AI workflow optimization.

**Principal Data Scientist — Galvanize Inc.** · Sep 2019–Jun 2021

- Technical lead across 13+ end-to-end ML systems for Fortune 500 clients; 5-star-rated
  delivery.

## PUBLICATIONS & ACTIVE RESEARCH

- **Active research program — "eval gates are training-signal factories"** ([RESEARCH-PROGRAM](https://github.com/wjlgatech/FM-os/blob/main/docs/research/RESEARCH-PROGRAM.md)):
  every honest eval gate (no-evidence⇒No, maker≠checker, ship/rollback) both certifies
  quality **and** labels preference data, so evaluation and post-training become one loop.
  Three probes: **P1 [RewardForge](https://github.com/wjlgatech/FM-os/tree/main/labs/rewardforge)** (M1 shipped — eval-derived DPO pairs → real LoRA
  fine-tune, held-out hallucination 0.398→0.287); **P2 [MCP-Arena](https://github.com/wjlgatech/mcp-arena)** (M0 shipped —
  standalone gated benchmark for MCP agent harnesses); **P3 Proactive Twin** (design
  brief, private) — personalization that must pay rent under the same gates.
- **SCWM: Self-Calibrating World Models** — NeurIPS 2026 (under review). Online Bayesian
  calibration for sim-to-real transfer; 40% transfer-error reduction vs
  domain-randomization baseline.
- **Physical AI: The Next Frontier in AI and Robotics** — Preprints.org, Apr 2026.
  DOI: [10.20944/preprints202604.0549.v1](https://doi.org/10.20944/preprints202604.0549.v1).

## TECHNICAL SKILLS

**Post-Training & RL:** LoRA/QLoRA fine-tuning, DPO written from scratch (torch+peft),
DPO/GRPO-style preference optimization, RLHF pipelines (TRL / OpenRLHF / verl), held-out
win-rate gates, ship/rollback discipline, safety-regression checks

**Developer Experience:** quickstart recipes, keyless demos runnable in CI, docs-as-code
(README as a build artifact from spec data, drift gates, freshness CI), eval-gated
cookbook patterns, rubric-as-data self-scoring

**Evaluation:** independent-referee (LLM-as-judge) pipelines, failure-taxonomy-as-data
probe suites, held-out gated benchmarks, confidence calibration, distribution-shift
detection, LLM-native metrics (tokens/sec, cost-per-request, latency)

**Engineering:** Python, PyTorch, numpy, FastAPI, Docker/Kubernetes, CI/CD, large-codebase
debugging (543-test OSS systems), SQLite/Postgres, event-sourced systems, Go (generated
CLI stacks)

## EDUCATION

**Yale University** — National BioMed Fellow, Computational Immunology ·
**Georgia Tech** — PhD, Bioinformatics ·
**University of South Carolina** — MS, Mathematics & CS ·
**Sun Yat-Sen University** — BS, Applied Mathematics
