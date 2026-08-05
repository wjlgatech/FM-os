# Research Engineer, AGI Safety and Alignment — Google DeepMind

**Fit:** 100/100 · **Location:** Mountain View, CA
**Apply:** https://www.google.com/about/careers/applications/jobs/results/102552346151527110-research-engineer-agi-safety-and-alignment-deepmind
**Resume:** [`resumes/gdm-agi-safety-alignment.pdf`](resumes/gdm-agi-safety-alignment.pdf)

## The angle

Safety work fails the way evaluation fails: silently. My practice is no-evidence-no-pass, pre-registered criteria, and adversarial self-audit — including finding that three of my own harness bugs were manufacturing failures that looked like model limitations.

## Scorecard

<!-- BEGIN jdfit -->
# FM-os JD-fit report — **100/100** (6 capabilities required)

| Capability | Coverage | FM-os knowledge | FM-os tooling |
|---|:--:|---|---|
| Training / fine-tuning foundation models | ✅ covered | nanoGPT, LitGPT, GPT-NeoX | slm-quickstart (certified 94), vlm-quickstart (certified 94), tinker-loop (certified 98) |
| Post-training / RL / alignment | ✅ covered | TRL, OpenRLHF, verl | slm-quickstart (certified 94), continual-rl-eval (certified 98), product-rl-loop (certified 98), tinker-loop (certified 98) |
| Agentic evaluation / benchmarking | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), continual-rl-eval (certified 98), vlm-failure-probe (certified 98), syndata-bare (certified 98), product-rl-loop (certified 98), personalization-loop (certified 91), hci-study-gate (certified 93), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
| Publishing research (NeurIPS / CVPR) | ✅ covered | CS336: Language Modeling from Scratch, LLM101n: Let's build a Storyteller, Post-training of LLMs | n/a |
| AGI safety & alignment — interpretability, RLHF, eval awareness | ✅ covered | lm-evaluation-harness, LightEval, lmms-eval | agentic-eval (certified 94), continual-rl-eval (certified 98), vlm-failure-probe (certified 98), syndata-bare (certified 98), product-rl-loop (certified 98), personalization-loop (certified 91), hci-study-gate (certified 93), transfer-loop (certified 92), eval-awareness-probe (certified 93) |
| Human-AI perception & interaction research (HCI, user studies) | ✅ covered | jsPsych, PsychoPy, OpenFace | hci-study-gate (certified 93) |
<!-- END jdfit -->

## The honest edge — say it before they find it

I have shipped no interpretability tooling. My alignment contribution is evaluation-and-oversight discipline, not mechanistic interpretability, and I would say so on day one.

## Five stories

_Situation → what I did → result → **what it cost**. The last line is the one that gets probed; a story without it sounds rehearsed._

### 1. Audited my own benchmark and it demoted my own published result

A VLM failure taxonomy as data → gated probe suite. Then a 3-repeat variance run found the grader, not the model, was the least reliable component: three harness bugs were MANUFACTURING failures (an empty API response scored 0.0; a truncated answer graded as complete; the suite's own tests never gated by CI). Fixing them cut instability from 5 unstable probe/model pairs to 1, and forced a correction to a capability claim I had already put in a paper table. Every spec change was pre-registered with falsifiable per-probe predictions BEFORE the run that tested it.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/vlm-failure-probe

### 2. Eval gates → preference data → a REAL gated fine-tune

162 preference pairs labeled by certified eval gates (zero human labels) → DPO loss written from scratch (torch+peft) → LoRA on a small open model → held-out hallucination 0.398→0.287, SHIP. Under a median+separation criterion committed to git BEFORE the 5-seed run: treatment +0.098±0.028 vs shuffled-label control −0.046±0.055, complete arm separation. The same gate rolled back a collapsed run first: the honest negative result was reported before the positive one.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/labs/rewardforge

### 3. Reward hacking caught as a measured weight, then rolled back

Biased product preference signal → DPO → frozen-judge win-rate gate; reward hacking surfaced as a measured +1.9 on a worthless feature and the run was rolled back. Certified 98/100.

- **Evidence:** github.com/wjlgatech/FM-os/tree/main/skills/product-rl-loop

### 4. Self-improving harness with an independent referee

generate → judge → refactor loops where quality comes ONLY from an independent referee (maker ≠ checker, enforced fail-closed); convergence policy with plateau detection, regression rollback and budgets; live-verified F→A runs. 543 tests.

- **Evidence:** github.com/wjlgatech/loop-engineering-anything

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
