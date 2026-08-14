# Research Engineer, Humanoids — Google DeepMind

**Fit:** 100/100 · **Location:** Mountain View, CA
**Apply:** https://www.google.com/about/careers/applications/jobs/results/105870811830592198-research-engineer-humanoids-deepmind
**Resume:** [`resumes/gdm-humanoids.pdf`](resumes/gdm-humanoids.pdf)

## The angle

Sim-to-real is a calibration problem, and calibration is a measurement problem: my NeurIPS submission cuts transfer error 40% by calibrating the world model online rather than randomizing the domain.

## Scorecard

<!-- BEGIN jdfit -->
# FM-os JD-fit report — **100/100** (9 capabilities required)

| Capability | Coverage | FM-os knowledge | FM-os tooling |
|---|:--:|---|---|
| Python / PyTorch / large-scale ML workflows | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | n/a |
| Training / fine-tuning foundation models | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | slm-quickstart (certified 94), vlm-quickstart (certified 94), tinker-loop (certified 98) |
| Framework breadth (JAX / TensorFlow / Flax) | ✅ covered | JAX, Flax, Keras | n/a |
| Autonomous-driving / robotics datasets | ✅ covered | nuScenes devkit, Waymo Open Dataset, BDD100K | n/a |
| Research judgment & empirical rigor (experiment loop) | ✅ covered | AI-Scientist, AI-Scientist-v2, Agent Laboratory | research-loop (certified 92), bayesopt-loop (certified 98), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
| Publishing research (NeurIPS / CVPR) | ✅ covered | CS336: Language Modeling from Scratch, LLM101n: Let's build a Storyteller, Post-training of LLMs | n/a |
| Automated eval pipelines capturing real-world quality beyond lab benchmarks | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), vlm-failure-probe (certified 98) |
| Cross-engagement learning — generalize insights from one deployment to all | ✅ covered | Post-training of LLMs, Fine-tuning & RL for LLMs: Intro to Post-training, Training Language Models to Follow Instructions with Human Feedback (InstructGPT) | research-loop (certified 92), bayesopt-loop (certified 98), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
| Humanoid / robot learning, sim-to-real, physics simulators | ✅ covered | Qwen2.5-VL, LLaVA-NeXT, InternVL | vlm-quickstart (certified 94), vlm-failure-probe (certified 98), syndata-bare (certified 98) |
<!-- END jdfit -->

## The honest edge — say it before they find it

My robotics work is world-model and perception-side; I have not shipped whole-body-control or locomotion policies on hardware.

## Five stories

_Situation → what I did → result → **what it cost**. The last line is the one that gets probed; a story without it sounds rehearsed._

### 1. Self-Calibrating World Models (NeurIPS 2026, under review)

Online Bayesian calibration for sim-to-real transfer; 40% transfer-error reduction vs domain randomization.

- **Evidence:** NeurIPS 2026 under review

### 2. Physical AI: The Next Frontier in AI and Robotics

Preprints.org, Apr 2026. DOI: 10.20944/preprints202604.0549.v1.

- **Evidence:** DOI 10.20944/preprints202604.0549.v1

### 3. The eval framework that decided production model selection

Primary technical interface on an executive-level enterprise AI deployment (Accenture OpenAI-DSI). Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS, Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes and integration cost — the basis for production model selection. Shipped a confidence-calibrated selective-verification pipeline routing only high-uncertainty outputs to human review: ~90% annotation cost reduction.

- **Evidence:** Accenture, Physical AI Team (2024–present)

### 4. Audited my own benchmark and it demoted my own published result

A VLM failure taxonomy as data → gated probe suite. Then a 3-repeat variance run found the grader, not the model, was the least reliable component: three harness bugs were MANUFACTURING failures (an empty API response scored 0.0; a truncated answer graded as complete; the suite's own tests never gated by CI). Fixing them cut instability from 5 unstable probe/model pairs to 1, and forced a correction to a capability claim I had already put in a paper table. Every spec change was pre-registered with falsifiable per-probe predictions BEFORE the run that tested it.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/vlm-failure-probe

### 5. A training API's primitives, keyless, with a forgetting gate

Four primitives + LoRA implemented keyless in numpy; a forgetting gate catches +208% catastrophic forgetting and rolls the naive recipe back. Certified 98/100.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/tinker-loop

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
