# Paul Jialiang Wu, PhD

**Research Engineer — Human Understanding · Audio-Visual Models · VLM Evaluation**

wjlgatech@gmail.com · github.com/wjlgatech · linkedin.com/in/paul-jialiang-wu-phd · [live portfolio](https://agentic-portfolio-lovat.vercel.app)

## SUMMARY

Understanding people from multimodal signal is an evaluation problem before it is a modelling problem: I built the multi-model VLM evaluation that decided production selection, and I audit the grader before trusting any model score.

## WHY GOOGLE DEEPMIND — RESEARCH ENGINEER, HUMAN UNDERSTANDING

- **The eval framework that decided production model selection:** Primary technical interface on an executive-level enterprise AI deployment (Accenture OpenAI-DSI). Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS, Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes and integration cost — the basis for production model selection. Shipped a confidence-calibrated selective-verification pipeline routing only high-uncertainty outputs to human review: ~90% annotation cost reduction. (Accenture, Physical AI Team (2024–present))
- **Audited my own benchmark and it demoted my own published result:** A VLM failure taxonomy as data → gated probe suite. Then a 3-repeat variance run found the grader, not the model, was the least reliable component: three harness bugs were MANUFACTURING failures (an empty API response scored 0.0; a truncated answer graded as complete; the suite's own tests never gated by CI). Fixing them cut instability from 5 unstable probe/model pairs to 1, and forced a correction to a capability claim I had already put in a paper table. Every spec change was pre-registered with falsifiable per-probe predictions BEFORE the run that tested it. (github.com/wjlgatech/FM-os/tree/main/skills/vlm-failure-probe)
- **A gate that refuses a human-study claim the design cannot support:** Required N from the target effect size, counterbalancing against order effects, one pre-registered primary metric — and NOT-MEASURED instead of a p-value an underpowered study cannot earn. Power math pinned to the conventional values and rounded toward MORE participants, because for a gate one too few is a false pass. Certified 93/100, 18 tests. (github.com/wjlgatech/FM-os/tree/main/skills/hci-study-gate)
- **Self-Calibrating World Models (NeurIPS 2026, under review):** Online Bayesian calibration for sim-to-real transfer; 40% transfer-error reduction vs domain randomization. (NeurIPS 2026 under review)
- **Evidence-gated tool-use benchmark over real MCP servers:** 12 tasks × 6 failure-mode categories as data, over REAL MCP servers; the tool-call trace is asserted, so "right words, no tool calls" scores zero by construction. The harness ships its own falsifier — an EvidenceHallucinator mock that must score 0 in CI. Failures export as DPO preference pairs. (github.com/wjlgatech/mcp-arena)

## ALSO SHIPPED

- **FM-os — spec-as-data FM-ops hub (creator)** — github.com/wjlgatech/FM-os
- **Physical AI: The Next Frontier in AI and Robotics** — DOI 10.20944/preprints202604.0549.v1

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

My deep-learning framework depth is PyTorch, not JAX/Flax — I have curated the JAX ecosystem but shipped no production JAX model. I would be ramping on Flax in the first weeks, and my audio/speech-visual work is evaluation-side rather than training speech models from scratch.
