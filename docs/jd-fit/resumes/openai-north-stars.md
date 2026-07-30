# Paul Jialiang Wu, PhD

**Research Engineer — Tool-Use & Agent Harnesses · Post-Training (RL) · Model Evaluation**

wjlgatech@gmail.com · github.com/wjlgatech · linkedin.com/in/paul-jialiang-wu-phd · [live portfolio](https://agentic-portfolio-lovat.vercel.app)

## SUMMARY

Product-driven research engineer whose daily practice is the North Stars mandate: tool-use,
connectors, instruction following — and translating model-behavior bottlenecks into **robust
evals, training data, and reward signals**. I ship gated closed loops: an evidence-gated
tool-use benchmark over real MCP servers where a plausible answer with hallucinated tool
calls scores zero by construction (mcp-arena); a real LoRA-DPO fine-tune from eval-derived
preference pairs — zero human labels — that a held-out gate shipped after honestly rolling
back a bad-lr attempt (FM-os/rewardforge); and a self-improving agent harness with an
independent maker≠checker referee, plateau detection, and regression rollback
(loop-engineering-anything, 543 tests). Currently the primary technical interface on an
**OpenAI enterprise engagement** (Accenture OpenAI-DSI) where I built the multi-model
evaluation framework that decides production model selection. PhD-trained; 8+ years of
production ML; comfortable owning a research agenda and debugging deep inside large ML
codebases.

## WHY NORTH STARS — CLOSING THE CAPABILITY OVERHANG IS MY DAILY BUILD

- **Tool-use & connectors, benchmarked with teeth:** [mcp-arena](https://github.com/wjlgatech/mcp-arena)
  — 12 tasks × 6 failure-mode categories (tool discovery, selection among overlapping tools,
  multi-step chaining, error recovery, instruction following, feature discovery) **as data**,
  over REAL MCP servers; the tool-call trace is asserted, so "right words, no tool calls"
  fails by construction — the harness ships its own falsifier (an EvidenceHallucinator mock
  that must score 0 in CI). Failures export as DPO preference pairs.
- **Evals → training data → reward signals, executed for real:**
  [FM-os/labs/rewardforge](https://github.com/wjlgatech/FM-os/tree/main/labs/rewardforge) —
  162 preference pairs labeled by certified eval gates (zero human labels) → from-scratch
  DPO loss (torch+peft) → LoRA on a small open model → held-out hallucination 0.398→0.287
  **SHIP**; the same gate rolled back a collapsed run (honest ❌ first).
  [product-rl-loop](https://github.com/wjlgatech/FM-os/tree/main/skills/product-rl-loop)
  (certified 98/100): biased product preference signal → DPO → frozen-judge win-rate gate;
  reward hacking caught as a measured weight (+1.9 on a worthless feature) and rolled back.
- **Instruction following & model-behavior probes:**
  [vlm-failure-probe](https://github.com/wjlgatech/FM-os/tree/main/skills/vlm-failure-probe)
  (98/100) — a failure taxonomy as data (incl. multi-part-prompt compliance) → gated probe
  suite; measured a frontier model at 5/5 on the exact probes a production pipeline fails
  5/5. [tinker-loop](https://github.com/wjlgatech/FM-os/tree/main/skills/tinker-loop) (98/100)
  — a training API's four primitives + LoRA, keyless in numpy; a forgetting gate catches
  +208% catastrophic forgetting and rolls the naive recipe back.
- **Harness improvements as a discipline:**
  [loop-engineering-anything](https://github.com/wjlgatech/loop-engineering-anything) —
  generate → judge → refactor loops where quality comes ONLY from an independent referee
  (maker ≠ checker enforced fail-closed); convergence policy (plateau detection, regression
  rollback, budgets); live-verified F→A runs.

## OPEN SOURCE — SELECTED (github.com/wjlgatech, 12 active repos, 280+ commits/month)

**FM-os** — *Spec-as-data FM-ops hub · Creator* — 14 certified skills (evidence-based
rubric-as-data certifier: no evidence ⇒ No); README generated from spec data with drift
gates; home of rewardforge and the jdfit self-scoring engine.
**mcp-arena** — *Evidence-gated tool-use benchmark · Creator* — see above.
**cli-judge** — *LLM-as-judge scoring harness · Creator* — reproducible Definition-of-Done
scorecards; the independent referee the loops ship through.
**super-u** — *Personalization platform · Creator (private)* — per-user Digital Twin
alignment/drift scoring; four-gate personalization eval (lift, cold-start parity, bit-exact
isolation, memory-pays-rent).

## EXPERIENCE

**Applied AI Scientist / Forward Deployed Engineer — Accenture, Physical AI Team** · Jan 2024–Present
- Primary technical interface for an executive-level enterprise AI deployment (OpenAI-DSI
  engagement); recognized for a "no surprises" standard built on deep model understanding
  and contextual judgment at decision points.
- Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS,
  Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes, and
  integration cost — the basis for production model selection.
- Shipped a confidence-calibrated selective-verification pipeline routing only
  high-uncertainty outputs to human review: ~90% annotation cost reduction.
- Technical lead on 4 simultaneous production systems: synthetic data generation, zero-shot
  safety detection, adaptive evaluation under distribution shift, vision-language reasoning
  over live sensor streams.

**Principal Data Scientist — Genentech** · Jun 2021–Dec 2022 — production ML for biomedical
research; 3 open-source PyPI packages for multimodal learning; 85% reduction in
unproductive process time.

**Principal Data Scientist — Galvanize Inc.** · Sep 2019–Jun 2021 — technical lead across
13+ end-to-end ML systems for Fortune 500 clients; 5-star-rated delivery.

## PUBLICATIONS & RESEARCH

- **SCWM: Self-Calibrating World Models** — NeurIPS 2026 (under review). Online Bayesian
  calibration for sim-to-real transfer; 40% transfer-error reduction vs domain randomization.
- **Physical AI: The Next Frontier in AI and Robotics** — Preprints.org, Apr 2026.
  DOI: 10.20944/preprints202604.0549.v1.

## TECHNICAL SKILLS

**Tool-Use & Harnesses:** MCP servers/benchmarks, agent harness design, evidence-gated
trace verification, instruction-following probes, connector generation (OpenAPI→CLI/MCP)
**Post-Training & RL:** DPO from scratch (torch+peft), LoRA/QLoRA, preference-data
pipelines from eval failures, reward-hack detection, win-rate gates, ship/rollback
**Evaluation:** LLM-as-judge referees (maker≠checker), failure-taxonomy-as-data suites,
held-out gated benchmarks, confidence calibration, distribution-shift detection
**Engineering:** Python, PyTorch, numpy, FastAPI, Docker/K8s, CI/CD, large-codebase
debugging (543-test OSS), Go, SQLite/Postgres

## EDUCATION

**Yale University** — National BioMed Fellow, Computational Immunology · **Georgia Tech** —
PhD, Bioinformatics · **University of South Carolina** — MS, Mathematics & CS ·
**Sun Yat-Sen University** — BS, Applied Mathematics
