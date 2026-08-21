# Paul Jialiang Wu, PhD

**Forward Deployed AI Engineer — Enterprise Agentic Systems · Grounded RAG · LLMOps Gates**

wjlgatech@gmail.com · github.com/wjlgatech · linkedin.com/in/paul-jialiang-wu-phd · [live portfolio](https://agentic-portfolio-lovat.vercel.app)

## SUMMARY

I embed with customers and take agentic systems from prototype to production-grade, and I ship the evidence with the system: golden datasets as permanent CI gates, every decision citing the clause it relied on, escalation to a human gated at exactly 1.0, and refusal as a first-class outcome. Then I codify what worked into tooling the next engineer installs in one command.

## WHY CLOUDERA — FORWARD DEPLOYED AI ENGINEER (SENIOR/PRINCIPAL)

- **Enterprise agentic app taken from brief to gated evidence — HITL, retries, audit trail:** Triages purchase requests against six fragmented policy documents — role-based approval limits, vendor risk tiers, PII addenda, a v3→v4 amendment that supersedes prior rules. Durable-execution StateGraph from the primitive up (~170 lines): checkpoint per super-step, human-in-the-loop interrupt/resume, per-node retry, bounded self-correction on ungrounded decisions. 59 labeled cases across 11 tag families incl. prompt injection. decision_accuracy 1.0 · escalation_recall 1.0 (gated at exactly 1.0) · citation_validity 1.0 · trace_completeness 1.0, a permanent CI gate. Its first golden run FAILED (0.889) and exposed an unimplemented policy rule — a golden set that cannot fail you is not measuring anything. Live playground on a real API. (github.com/wjlgatech/FDE-os/tree/main/take-home/enterprise-agentic-triage · enterprise-triage-brief.vercel.app)
- **Grounded RAG over real filings where refusal is a first-class outcome:** Natural-language questions over real SEC filings as PDFs (Tesla 10-K + two 10-Qs, Apple 10-K) — SHA256-pinned, extracted to page-anchored JSON. Verbatim quotes with page anchors, deterministic arithmetic instead of model arithmetic, refusal as an explicit path. 26 hand-verified golden cases, four gates all 1.0: answer_accuracy, refusal_recall (unanswerable questions MUST refuse), refusal_precision, citation_validity (every quote re-verified verbatim). Cross-filing reconciliation: Q1+Q2 = 6M YTD exact on revenue and net income across two independent documents. Shipped behind an edge-middleware access gate; CI fully offline. (github.com/wjlgatech/FDE-os/tree/main/take-home/sec-filing-intelligence)
- **The eval framework that decided production model selection:** Primary technical interface on an executive-level enterprise AI deployment (Accenture OpenAI-DSI). Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS, Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes and integration cost — the basis for production model selection. Shipped a confidence-calibrated selective-verification pipeline routing only high-uncertainty outputs to human review: ~90% annotation cost reduction. (Accenture, Physical AI Team (2024–present))
- **Codified the delivery patterns into installable tooling other engineers run:** FDE-os turns engagement patterns into reusable product: eleven skills + two composition workflows, exposed as a dependency-free MCP server (eleven callable tools), installable as a one-command Claude Code plugin and running unchanged on Codex and Hermes from one skills tree. Includes an offline RAG/agent eval harness (precision@k, recall@k, MRR, grounding proxy, citation coverage, CI gate), a self-improving eval-loop primitive that reverts regressions, and an enterprise doc parser with a parse-quality NO-GO gate. Live no-login webapp plus a shared-key model proxy, running at ~$0. (github.com/wjlgatech/FDE-os · wjlgatech.github.io/FDE-os)
- **Multi-agent business-process automation in production for enterprise clients:** Event-sourced state management for concurrent-agent consistency, idempotent retry across distributed agents, and a full audit trail — live autonomous workflows with zero-downtime replanning. The core agentic failure mode is that agents over partially observable state must replan without losing context; the event-sourced consistency model solves it and doubles as the tracing/observability surface. (Accenture, WorkflowX / Agenticom (2024–present))

## ALSO SHIPPED

- **Compiled a data platform's whole curriculum into a staffing GO/NO-GO** — github.com/wjlgatech/FDE-os/tree/main/snowflake-os
- **Self-improving harness with an independent referee** — github.com/wjlgatech/loop-engineering-anything
- **Evidence-gated tool-use benchmark over real MCP servers** — github.com/wjlgatech/mcp-arena
- **Spatial AI deployed to Fortune 500 field technicians** — Accenture, Physical AI Team

## EXPERIENCE

**Applied AI Scientist / Forward Deployed Engineer — Accenture, Physical AI Team** · Jan 2024–Present
- Primary technical interface for an executive-level enterprise AI deployment (OpenAI-DSI engagement); recognized for a "no surprises" standard built on deep model understanding and contextual judgment at decision points.
- Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS, Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes and integration cost — the basis for production model selection.
- Shipped a confidence-calibrated selective-verification pipeline routing only high-uncertainty outputs to human review: ~90% annotation cost reduction.
- Technical lead on 4 simultaneous production systems: synthetic data generation, zero-shot safety detection, adaptive evaluation under distribution shift, vision-language reasoning over live sensor streams.
- Led technical discovery and white-glove deployment: translated ambiguous customer requirements into shipped agentic workflows, and co-built with customer engineering teams to instill rigorous development practices and drive end-user adoption.
- Designed and shipped a multi-agent business-process automation engine for enterprise clients (WorkflowX / Agenticom): event-sourced state for concurrent-agent consistency, idempotent retry across distributed agents, full audit trail, zero-downtime replanning.

**Principal Data Scientist — Genentech** · Jun 2021–Dec 2022
- Production ML for biomedical research; 3 open-source PyPI packages for multimodal learning; 85% reduction in unproductive process time.

**Principal Data Scientist — Galvanize Inc.** · Sep 2019–Jun 2021
- Technical lead across 13+ end-to-end ML systems for Fortune 500 clients; 5-star-rated delivery.

## PUBLICATIONS

- **Self-Calibrating World Models (NeurIPS 2026, under review)** — Online Bayesian calibration for sim-to-real transfer; 40% transfer-error reduction vs domain randomization.
- **Physical AI: The Next Frontier in AI and Robotics** — Preprints.org, Apr 2026. DOI: 10.20944/preprints202604.0549.v1.

## TECHNICAL SKILLS

**Agentic Systems:** Multi-agent orchestration (ReAct, self-reflection, hierarchical delegation), durable-execution state graphs (checkpoint/resume, HITL interrupt, retry policy, bounded self-correction), event-sourced agent state, MCP servers and clients, LangGraph/CrewAI/ADK-class patterns

**Retrieval, RAG & Data:** RAG over structured + unstructured enterprise data, semantic search, embeddings and vector databases, page-anchored citation verification, deterministic arithmetic over retrieved facts, DOCX/XLSX/PDF/web/transcript ingestion with parse-quality gates, provenance-pinned corpora

**LLMOps / MLOps:** Independent-referee eval pipelines, golden datasets as permanent CI gates, grounding/hallucination and citation-validity metrics, prompt-injection probes, granular tracing and audit trails, confidence calibration, distribution-shift detection, cost/latency/token budgets, regression rollback, model-provider seams for portable swaps

**Cloud & Infrastructure:** GCP (hands-on ML + Gemini evaluation), Azure ML (production), AWS; NVIDIA AI stack (NIM, Cosmos, VSS); Docker, Kubernetes, CI/CD, Vercel edge middleware and RBAC gating, FastAPI, React, SQLite/Postgres

**Forward-Deployed Delivery:** Technical discovery, executive stakeholder alignment, white-glove deployment, prototype → production hardening, customer engineering enablement, reference architectures and starter kits, field-pattern → reusable module → product feedback loop

## EDUCATION

**Yale University** — National BioMed Fellow, Computational Immunology · **Georgia Tech** — PhD, Bioinformatics · **University of South Carolina** — MS, Mathematics & CS · **Sun Yat-Sen University** — BS, Applied Mathematics

## THE EDGE I'D BE LEARNING, NOT TEACHING

I have not run the Cloudera platform itself, and my big-data-infrastructure depth is the real edge: I have built RAG and agentic pipelines over enterprise documents and live sensor streams, but I have not owned a Spark/Iceberg/NiFi data platform in production, and my inference work is model selection, cost/latency budgeting and serving seams rather than GPU kernel-level optimization. That is the part of this role I would be ramping on in the first weeks, not teaching.
