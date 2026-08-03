# Paul Jialiang Wu, PhD

**Research Engineer — Self-Improving Agent Systems · Automated Failure Diagnosis · Eval Beyond Benchmarks**

wjlgatech@gmail.com · github.com/wjlgatech · linkedin.com/in/paul-jialiang-wu-phd · [live portfolio](https://agentic-portfolio-lovat.vercel.app)

## SUMMARY

This role's three duties are my daily build: diagnose agent failure modes automatically, build eval pipelines that capture real-world quality beyond lab benchmarks, and characterize model limitations with empirical evidence. I have shipped each — including the uncomfortable version, where the audit demoted my own published claim.

## WHY GOOGLE DEEPMIND — RESEARCH ENGINEER, DEEPMIND (SCIENCE & STRATEGIC INITIATIVES)

- **Audited my own benchmark and it demoted my own published result:** A VLM failure taxonomy as data → gated probe suite. Then a 3-repeat variance run found the grader, not the model, was the least reliable component: three harness bugs were MANUFACTURING failures (an empty API response scored 0.0; a truncated answer graded as complete; the suite's own tests never gated by CI). Fixing them cut instability from 5 unstable probe/model pairs to 1, and forced a correction to a capability claim I had already put in a paper table. Every spec change was pre-registered with falsifiable per-probe predictions BEFORE the run that tested it. (github.com/wjlgatech/FM-os/tree/main/skills/vlm-failure-probe)
- **Eval gates → preference data → a REAL gated fine-tune:** 162 preference pairs labeled by certified eval gates (zero human labels) → DPO loss written from scratch (torch+peft) → LoRA on a small open model → held-out hallucination 0.398→0.287, SHIP. Under a median+separation criterion committed to git BEFORE the 5-seed run: treatment +0.098±0.028 vs shuffled-label control −0.046±0.055, complete arm separation. The same gate rolled back a collapsed run first: the honest negative result was reported before the positive one. (github.com/wjlgatech/FM-os/tree/main/labs/rewardforge)
- **Evidence-gated tool-use benchmark over real MCP servers:** 12 tasks × 6 failure-mode categories as data, over REAL MCP servers; the tool-call trace is asserted, so "right words, no tool calls" scores zero by construction. The harness ships its own falsifier — an EvidenceHallucinator mock that must score 0 in CI. Failures export as DPO preference pairs. (github.com/wjlgatech/mcp-arena)
- **Self-improving harness with an independent referee:** generate → judge → refactor loops where quality comes ONLY from an independent referee (maker ≠ checker, enforced fail-closed); convergence policy with plateau detection, regression rollback and budgets; live-verified F→A runs. 543 tests. (github.com/wjlgatech/loop-engineering-anything)
- **The eval framework that decided production model selection:** Primary technical interface on an executive-level enterprise AI deployment (Accenture OpenAI-DSI). Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS, Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes and integration cost — the basis for production model selection. Shipped a confidence-calibrated selective-verification pipeline routing only high-uncertainty outputs to human review: ~90% annotation cost reduction. (Accenture, Physical AI Team (2024–present))

## ALSO SHIPPED

- **FM-os — spec-as-data FM-ops hub (creator)** — github.com/wjlgatech/FM-os
- **Self-Calibrating World Models (NeurIPS 2026, under review)** — NeurIPS 2026 under review

## EXPERIENCE

**Applied AI Scientist / Forward Deployed Engineer — Accenture, Physical AI Team** · Jan 2024–Present
- Primary technical interface for an executive-level enterprise AI deployment (OpenAI-DSI engagement); recognized for a "no surprises" standard built on deep model understanding and contextual judgment at decision points.
- Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS, Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes and integration cost — the basis for production model selection.
- Shipped a confidence-calibrated selective-verification pipeline routing only high-uncertainty outputs to human review: ~90% annotation cost reduction.
- Technical lead on 4 simultaneous production systems: synthetic data generation, zero-shot safety detection, adaptive evaluation under distribution shift, vision-language reasoning over live sensor streams.

**Principal Data Scientist — Genentech** · Jun 2021–Dec 2022
- Production ML for biomedical research; 3 open-source PyPI packages for multimodal learning; 85% reduction in unproductive process time.

**Principal Data Scientist — Galvanize Inc.** · Sep 2019–Jun 2021
- Technical lead across 13+ end-to-end ML systems for Fortune 500 clients; 5-star-rated delivery.

## PUBLICATIONS

- **Self-Calibrating World Models (NeurIPS 2026, under review)** — Online Bayesian calibration for sim-to-real transfer; 40% transfer-error reduction vs domain randomization.
- **Physical AI: The Next Frontier in AI and Robotics** — Preprints.org, Apr 2026. DOI: 10.20944/preprints202604.0549.v1.

## TECHNICAL SKILLS

**Tooluse:** MCP servers/benchmarks, agent harness design, evidence-gated trace verification, instruction-following probes, connector generation (OpenAPI→CLI/MCP)

**Posttraining:** DPO from scratch (torch+peft), LoRA/QLoRA, preference-data pipelines from eval failures, reward-hack detection, win-rate gates, ship/rollback

**Evaluation:** LLM-as-judge referees (maker≠checker), failure-taxonomy-as-data suites, held-out gated benchmarks, pre-registered criteria, variance reporting, confidence calibration, distribution-shift detection

**Engineering:** Python, PyTorch, numpy, JAX-adjacent, FastAPI, Docker/K8s, CI/CD, large-codebase debugging (543-test OSS), Go, SQLite/Postgres

## EDUCATION

**Yale University** — National BioMed Fellow, Computational Immunology · **Georgia Tech** — PhD, Bioinformatics · **University of South Carolina** — MS, Mathematics & CS · **Sun Yat-Sen University** — BS, Applied Mathematics

## THE EDGE I'D BE LEARNING, NOT TEACHING

My distributed-systems depth is the real edge here: I have curated and used large-scale training infrastructure, but I have not owned a MapReduce/Spark/BigQuery data platform in production. I would be learning that stack, not teaching it.
