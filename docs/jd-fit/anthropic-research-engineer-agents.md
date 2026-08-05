# Research Engineer, Agents — Anthropic

**Fit:** 100/100 · **Location:** Remote-friendly (travel required) | San Francisco | Seattle | New York
**Apply:** https://job-boards.greenhouse.io/anthropic/jobs/4017544008
**Resume:** [`resumes/anthropic-research-engineer-agents.pdf`](resumes/anthropic-research-engineer-agents.pdf)

> **Note:** 26 form fields, 4 of them REQUIRED free-text essays. Paul writes the first drafts (employer policy); the agent supplies the evidence map and refines afterwards.

## The angle

Agent harnesses are my daily build, and I judge them the hard way: quality comes only from an independent referee, benchmarks assert the tool-call trace rather than the prose, and a run that fails the gate gets rolled back rather than reframed.

## Scorecard

<!-- BEGIN jdfit -->
# FM-os JD-fit report — **100/100** (11 capabilities required)

| Capability | Coverage | FM-os knowledge | FM-os tooling |
|---|:--:|---|---|
| Vision-Language / multi-modal models | ✅ covered | Qwen2.5-VL, LLaVA-NeXT, InternVL | vlm-quickstart (certified 94), vlm-failure-probe (certified 98), syndata-bare (certified 98) |
| Training / fine-tuning foundation models | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | slm-quickstart (certified 94), vlm-quickstart (certified 94), tinker-loop (certified 98) |
| Agentic evaluation / benchmarking | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), continual-rl-eval (certified 98), vlm-failure-probe (certified 98), syndata-bare (certified 98), product-rl-loop (certified 98), personalization-loop (certified 91), hci-study-gate (certified 93), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
| Retrieval, embeddings & vector databases | ✅ covered | FAISS, Milvus, Qdrant | vector-rag (certified 94), personalization-loop (certified 91) |
| Distributed training & ML orchestration | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | n/a |
| Dataset curation loops ("AI training AI") | ✅ covered | nuScenes devkit, Waymo Open Dataset, BDD100K | curation-loop (certified 91) |
| Research judgment & empirical rigor (experiment loop) | ✅ covered | AI-Scientist, AI-Scientist-v2, Agent Laboratory | research-loop (certified 92), bayesopt-loop (certified 98), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
| Publishing research (NeurIPS / CVPR) | ✅ covered | CS336: Language Modeling from Scratch, LLM101n: Let's build a Storyteller, Post-training of LLMs | n/a |
| Personalization / memory (personal models) | ✅ covered | SmolLM / SmolLM2 / SmolLM3, Phi Cookbook, Gemma (DeepMind) | personalization-loop (certified 91) |
| Automated eval pipelines capturing real-world quality beyond lab benchmarks | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), vlm-failure-probe (certified 98) |
| AGI safety & alignment — interpretability, RLHF, eval awareness | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), continual-rl-eval (certified 98), vlm-failure-probe (certified 98), syndata-bare (certified 98), product-rl-loop (certified 98), personalization-loop (certified 91), hci-study-gate (certified 93), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
<!-- END jdfit -->

## The honest edge — say it before they find it

I have shipped no interpretability tooling, and my RL is DPO-scale on small open models rather than large-scale RL on frontier language models. Multi-agent coordination I have built as harnesses and referees, not as many-agent systems at scale — that is the part of this role I would be growing into.

## Five stories

_Situation → what I did → result → **what it cost**. The last line is the one that gets probed; a story without it sounds rehearsed._

### 1. Self-improving harness with an independent referee

generate → judge → refactor loops where quality comes ONLY from an independent referee (maker ≠ checker, enforced fail-closed); convergence policy with plateau detection, regression rollback and budgets; live-verified F→A runs. 543 tests.

- **Evidence:** github.com/wjlgatech/loop-engineering-anything

### 2. Evidence-gated tool-use benchmark over real MCP servers

12 tasks × 6 failure-mode categories as data, over REAL MCP servers; the tool-call trace is asserted, so "right words, no tool calls" scores zero by construction. The harness ships its own falsifier — an EvidenceHallucinator mock that must score 0 in CI. Failures export as DPO preference pairs.

- **Evidence:** github.com/wjlgatech/mcp-arena

### 3. Audited my own benchmark and it demoted my own published result

A VLM failure taxonomy as data → gated probe suite. Then a 3-repeat variance run found the grader, not the model, was the least reliable component: three harness bugs were MANUFACTURING failures (an empty API response scored 0.0; a truncated answer graded as complete; the suite's own tests never gated by CI). Fixing them cut instability from 5 unstable probe/model pairs to 1, and forced a correction to a capability claim I had already put in a paper table. Every spec change was pre-registered with falsifiable per-probe predictions BEFORE the run that tested it.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/vlm-failure-probe

### 4. Eval gates → preference data → a REAL gated fine-tune

162 preference pairs labeled by certified eval gates (zero human labels) → DPO loss written from scratch (torch+peft) → LoRA on a small open model → held-out hallucination 0.398→0.287, SHIP. Under a median+separation criterion committed to git BEFORE the 5-seed run: treatment +0.098±0.028 vs shuffled-label control −0.046±0.055, complete arm separation. The same gate rolled back a collapsed run first: the honest negative result was reported before the positive one.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/labs/rewardforge

### 5. The eval framework that decided production model selection

Primary technical interface on an executive-level enterprise AI deployment (Accenture OpenAI-DSI). Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS, Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes and integration cost — the basis for production model selection. Shipped a confidence-calibrated selective-verification pipeline routing only high-uncertainty outputs to human review: ~90% annotation cost reduction.

- **Evidence:** Accenture, Physical AI Team (2024–present)

## Outreach — DRAFTED, NEVER SENT

| Who | Why them | The give | The ask |
|---|---|---|---|
| _(fill from the team's published work)_ | a specific paper/repo of theirs this role touches | the artifact above that is closest to their problem | one 20-minute question, not "can I pick your brain" |

## Submission gate

Not submitted until ALL hold:

1. This dossier's scorecard regenerated (never a remembered number).
2. The resume is the one tailored to THIS role, not a generic copy.
3. Every resume claim traces to a shipped artifact.
4. The honest edge above is stated in the application, not hidden.
5. The apply URL is verified ✓.

## Outcome log

| Date | Event | Artifact that carried it |
|---|---|---|
| — | not yet submitted | — |
