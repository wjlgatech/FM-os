# Research Engineer, Human Understanding — Google DeepMind

**Fit:** 100/100 · **Location:** Mountain View, CA / Los Angeles, CA
**Apply:** https://www.google.com/about/careers/applications/jobs/results/107269257477137094-research-engineer-human-understanding-deepmind
**Resume:** [`resumes/gdm-human-understanding.pdf`](resumes/gdm-human-understanding.pdf)

> **Note:** Requires 5 yrs ML model development (audio/speech-visual), VLM tuning, and JAX/Flax. JAX/Flax is the honest edge — curated knowledge, no shipped JAX artifact.

## The angle

Understanding people from multimodal signal is an evaluation problem before it is a modelling problem: I built the multi-model VLM evaluation that decided production selection, and I audit the grader before trusting any model score.

## Scorecard

<!-- BEGIN jdfit -->
# FM-os JD-fit report — **100/100** (11 capabilities required)

| Capability | Coverage | FM-os knowledge | FM-os tooling |
|---|:--:|---|---|
| Python / PyTorch / large-scale ML workflows | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | n/a |
| Vision-Language / multi-modal models | ✅ covered | Qwen2.5-VL, LLaVA-NeXT, InternVL | vlm-quickstart (certified 94), vlm-failure-probe (certified 98), syndata-bare (certified 98) |
| Training / fine-tuning foundation models | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | slm-quickstart (certified 94), vlm-quickstart (certified 94), tinker-loop (certified 98) |
| Post-training / RL / alignment | ✅ covered | TRL, OpenRLHF, verl | slm-quickstart (certified 94), continual-rl-eval (certified 98), product-rl-loop (certified 98), tinker-loop (certified 98) |
| Framework breadth (JAX / TensorFlow / Flax) | ✅ covered | JAX, Flax, Keras | n/a |
| Agentic evaluation / benchmarking | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), continual-rl-eval (certified 98), vlm-failure-probe (certified 98), syndata-bare (certified 98), product-rl-loop (certified 98), personalization-loop (certified 91), hci-study-gate (certified 93), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
| Research judgment & empirical rigor (experiment loop) | ✅ covered | AI-Scientist, AI-Scientist-v2, Agent Laboratory | research-loop (certified 92), bayesopt-loop (certified 98), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
| Publishing research (NeurIPS / CVPR) | ✅ covered | CS336: Language Modeling from Scratch, LLM101n: Let's build a Storyteller, Post-training of LLMs | n/a |
| Active learning & closed-loop optimization (DBTL cycles) | ✅ covered | BoTorch, Ax (Adaptive Experimentation), GPyTorch | bayesopt-loop (certified 98) |
| Automated eval pipelines capturing real-world quality beyond lab benchmarks | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), vlm-failure-probe (certified 98) |
| AGI safety & alignment — interpretability, RLHF, eval awareness | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), continual-rl-eval (certified 98), vlm-failure-probe (certified 98), syndata-bare (certified 98), product-rl-loop (certified 98), personalization-loop (certified 91), hci-study-gate (certified 93), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
<!-- END jdfit -->

## The honest edge — say it before they find it

My deep-learning framework depth is PyTorch, not JAX/Flax — I have curated the JAX ecosystem but shipped no production JAX model. I would be ramping on Flax in the first weeks, and my audio/speech-visual work is evaluation-side rather than training speech models from scratch.

## Five stories

_Situation → what I did → result → **what it cost**. The last line is the one that gets probed; a story without it sounds rehearsed._

### 1. The eval framework that decided production model selection

Primary technical interface on an executive-level enterprise AI deployment (Accenture OpenAI-DSI). Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS, Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes and integration cost — the basis for production model selection. Shipped a confidence-calibrated selective-verification pipeline routing only high-uncertainty outputs to human review: ~90% annotation cost reduction.

- **Evidence:** Accenture, Physical AI Team (2024–present)

### 2. Audited my own benchmark and it demoted my own published result

A VLM failure taxonomy as data → gated probe suite. Then a 3-repeat variance run found the grader, not the model, was the least reliable component: three harness bugs were MANUFACTURING failures (an empty API response scored 0.0; a truncated answer graded as complete; the suite's own tests never gated by CI). Fixing them cut instability from 5 unstable probe/model pairs to 1, and forced a correction to a capability claim I had already put in a paper table. Every spec change was pre-registered with falsifiable per-probe predictions BEFORE the run that tested it.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/vlm-failure-probe

### 3. A gate that refuses a human-study claim the design cannot support

Required N from the target effect size, counterbalancing against order effects, one pre-registered primary metric — and NOT-MEASURED instead of a p-value an underpowered study cannot earn. Power math pinned to the conventional values and rounded toward MORE participants, because for a gate one too few is a false pass. Certified 93/100, 18 tests.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/hci-study-gate

### 4. Self-Calibrating World Models (NeurIPS 2026, under review)

Online Bayesian calibration for sim-to-real transfer; 40% transfer-error reduction vs domain randomization.

- **Evidence:** NeurIPS 2026 under review

### 5. Evidence-gated tool-use benchmark over real MCP servers

12 tasks × 6 failure-mode categories as data, over REAL MCP servers; the tool-call trace is asserted, so "right words, no tool calls" scores zero by construction. The harness ships its own falsifier — an EvidenceHallucinator mock that must score 0 in CI. Failures export as DPO preference pairs.

- **Evidence:** github.com/wjlgatech/mcp-arena

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
