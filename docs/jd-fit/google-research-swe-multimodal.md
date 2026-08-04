# Research Software Engineer, Multimodal AI — Google

**Fit:** 100/100 · **Location:** San Jose, CA
**Apply:** https://www.google.com/about/careers/applications/apply/9e82448b-599e-4021-b51c-2d0c6800961c/role
**Resume:** [`resumes/google-research-swe-multimodal.pdf`](resumes/google-research-swe-multimodal.pdf)

## The angle

Multimodal systems judged by what a person actually gets: I build the eval that decides which VLM ships, and the personalization gates that make memory prove it pays rent.

## Scorecard

<!-- BEGIN jdfit -->
# FM-os JD-fit report — **100/100** (12 capabilities required)

| Capability | Coverage | FM-os knowledge | FM-os tooling |
|---|:--:|---|---|
| Python / PyTorch / large-scale ML workflows | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | n/a |
| Vision-Language / multi-modal models | ✅ covered | Qwen2.5-VL, LLaVA-NeXT, InternVL | vlm-quickstart (certified 94), vlm-failure-probe (certified 98), syndata-bare (certified 98) |
| Training / fine-tuning foundation models | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | slm-quickstart (certified 94), vlm-quickstart (certified 94), tinker-loop (certified 98) |
| Post-training / RL / alignment | ✅ covered | TRL, OpenRLHF, verl | slm-quickstart (certified 94), continual-rl-eval (certified 98), product-rl-loop (certified 98), tinker-loop (certified 98) |
| Framework breadth (JAX / TensorFlow / Flax) | ✅ covered | JAX, Flax, Keras | n/a |
| Agentic evaluation / benchmarking | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), continual-rl-eval (certified 98), vlm-failure-probe (certified 98), syndata-bare (certified 98), product-rl-loop (certified 98), personalization-loop (certified 91), hci-study-gate (certified 93), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
| Retrieval, embeddings & vector databases | ✅ covered | FAISS, Milvus, Qdrant | vector-rag (certified 94), personalization-loop (certified 91) |
| Distributed training & ML orchestration | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | n/a |
| Publishing research (NeurIPS / CVPR) | ✅ covered | CS336: Language Modeling from Scratch, LLM101n: Let's build a Storyteller, Post-training of LLMs | n/a |
| Personalization / memory (personal models) | ✅ covered | SmolLM / SmolLM2 / SmolLM3, Phi Cookbook, Gemma (DeepMind) | personalization-loop (certified 91) |
| Automated eval pipelines capturing real-world quality beyond lab benchmarks | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), vlm-failure-probe (certified 98) |
| Human-AI perception & interaction research (HCI, user studies) | ✅ covered | jsPsych, PsychoPy, OpenFace | hci-study-gate (certified 93) |
<!-- END jdfit -->

## The honest edge — say it before they find it

My multimodal work is evaluation- and deployment-side rather than pretraining a frontier multimodal model from scratch.

## Five stories

_Situation → what I did → result → **what it cost**. The last line is the one that gets probed; a story without it sounds rehearsed._

### 1. The eval framework that decided production model selection

Primary technical interface on an executive-level enterprise AI deployment (Accenture OpenAI-DSI). Built the multi-model evaluation framework comparing 6+ VLMs (Gemini-class, NVIDIA VSS, Cosmos-Predict2) on accuracy, latency under load, edge-case failure modes and integration cost — the basis for production model selection. Shipped a confidence-calibrated selective-verification pipeline routing only high-uncertainty outputs to human review: ~90% annotation cost reduction.

- **Evidence:** Accenture, Physical AI Team (2024–present)

### 2. super-u — personalization platform (creator, private)

Per-user Digital Twin alignment/drift scoring; four-gate personalization eval (lift, cold-start parity, bit-exact isolation, memory-pays-rent).

- **Evidence:** private repo

### 3. Audited my own benchmark and it demoted my own published result

A VLM failure taxonomy as data → gated probe suite. Then a 3-repeat variance run found the grader, not the model, was the least reliable component: three harness bugs were MANUFACTURING failures (an empty API response scored 0.0; a truncated answer graded as complete; the suite's own tests never gated by CI). Fixing them cut instability from 5 unstable probe/model pairs to 1, and forced a correction to a capability claim I had already put in a paper table. Every spec change was pre-registered with falsifiable per-probe predictions BEFORE the run that tested it.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/vlm-failure-probe

### 4. Reward hacking caught as a measured weight, then rolled back

Biased product preference signal → DPO → frozen-judge win-rate gate; reward hacking surfaced as a measured +1.9 on a worthless feature and the run was rolled back. Certified 98/100.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/product-rl-loop

### 5. A gate that refuses a human-study claim the design cannot support

Required N from the target effect size, counterbalancing against order effects, one pre-registered primary metric — and NOT-MEASURED instead of a p-value an underpowered study cannot earn. Power math pinned to the conventional values and rounded toward MORE participants, because for a gate one too few is a false pass. Certified 93/100, 18 tests.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/hci-study-gate

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
