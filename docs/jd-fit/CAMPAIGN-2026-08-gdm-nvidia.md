# Campaign — Google DeepMind × Google × NVIDIA research-engineer roles (2026-08)

**Status: nothing submitted.** Stages 0–3 are done; per-role resumes (Stage 5) and
submission (Stage 7.5) are the remaining work, one role at a time. Quality over
quantity was the explicit instruction, so a role is submitted only after its own
dossier and custom resume pass the gate — never in a batch.

Regenerate every number here:

```bash
python3 scripts/campaign_graph.py --jds /tmp/jds        # the graph
python3 scripts/jdfit.py --jd /tmp/jds/<job_id>.txt     # one scorecard
```

## Stage 0 — dedupe BEFORE evaluating (10 postings → 7 roles)

The LinkedIn search returned 10 job ids. Evaluating them as 10 roles would have sent
two teams duplicate applications. Dedupe evidence is recorded in
[`data/campaign_roles.yml`](../../data/campaign_roles.yml), and it is textual, not
judgemental:

| Kept | Dropped as duplicate | Evidence |
|---|---|---|
| `4443139630` AGI Safety, Mountain View | `4443145447` (San Francisco) | extracted JD text **byte-identical** |
| `4435941809` NVIDIA Sr RS, Santa Clara | `4437932202` (same title/team) | near-identical posting, boilerplate diffs only |
| ″ | `4395479271` (PhD new-grad tier) | same team, lower tier — a fallback if senior is declined, not a parallel shot |

**The keyword lied.** The search phrase was *"Research Engineer, Human Understanding,
DeepMind"*, but `4437900123`'s actual JD is **Science & Strategic Initiatives**: a
self-improving agent framework, automated failure-mode diagnosis, eval pipelines beyond
lab benchmarks. Its `human_ai_interaction` capability does not even trigger. Tailoring a
resume to the search phrase would have missed the role entirely.

## Stage 1 — the false-100 trap, again

First scoring pass: **six of six roles returned 100/100.** A score that cannot rank its
inputs is not a score. Cause was the known one — `data/jd_taxonomy.yml` only recognised
capabilities it already had, so a JD dense with unfamiliar demands scored perfect on the
handful it happened to match (`4437900123`: 100/100 over just 6 caps).

Fix per the playbook: **+8 capabilities first, then score.** Three of the eight were
added with *no* `skill_tag` and one with neither knowledge nor tooling, so they were
guaranteed to read `partial`/`gap`. A capability invented to be green is worse than no
capability.

Honest scores after the taxonomy extension, and after the Stage 2–3 build below:

| Role | Company · Location | Caps | Before | After |
|---|---|:--:|:--:|:--:|
| `gdm-ssi-self-improving-agents` | Google DeepMind · Mountain View | **12** | 92 | **92** |
| `google-research-swe-multimodal` | Google · San Jose | **12** | 92 | **100** |
| `gdm-multimodal-information-literacy` | Google DeepMind | 11 | 100 | 100 |
| `nvidia-human-ai-perception` | NVIDIA · Santa Clara | 11 | 86 | **95** |
| `gdm-humanoids` | Google DeepMind · Mountain View | 9 | 94 | 94 |
| `gdm-winslow` | Google DeepMind · Mountain View | 9 | 100 | 100 |
| `gdm-agi-safety-alignment` | Google DeepMind · Mountain View | 6 | 75 | **92** |

**Read the denominator, not just the score.** `gdm-winslow` scores 100 over 9 caps from
the thinnest JD of the seven (552 words) — that is missing information, not strength.
`gdm-ssi-self-improving-agents` scores 92 over 12 caps, the densest demand set, and is
the strongest evidence match despite the lower number.

## The dependency graph — why all 7 beats the best 1

23 capabilities across 7 roles. The graph splits them:

- **Shared core** (≥3 roles): closing one pays across the campaign.
- **Role-specific** (exactly 1 role): the only legitimate per-role build, and the real
  material for a *custom* resume rather than a reworded one.
- **Leverage** = `#roles × openness` (gap 1.0, partial 0.5, covered 0.0) = the build order.

The top-leverage item was **`human_ai_interaction`: a hard GAP shared by 3 of 7 roles**
(Google Multimodal, AGI Safety, NVIDIA). Applying only to the single best-fit role would
have left the campaign's weakest edge untouched — the graph is what surfaced it.

**Result of closing it (one skill, three roles):**

```
google-research-swe-multimodal   92 → 100
nvidia-human-ai-perception       86 →  95
gdm-agi-safety-alignment         75 →  92
```

### Role-specific capabilities (the custom-resume material)

| Role | Its own capabilities |
|---|---|
| `gdm-ssi-self-improving-agents` | self-improving agent frameworks · automatic failure-mode diagnosis · distributed infra 🟡 · neuroscience/BCI |
| `google-research-swe-multimodal` | personalization / memory |
| `nvidia-human-ai-perception` | GPU optimization / efficient inference |
| `gdm-agi-safety-alignment` | AGI safety & alignment (interpretability, RLHF, eval awareness) 🟡 |

## Stage 2 — knowledge (done)

Four `hci` repos (jsPsych, PsychoPy, OpenFace, Lab Streaming Layer) and two
title-verified papers (Shneiderman *Human-Centered AI*; Gilpin et al. *Explaining
Explanations*).

**One paper was rejected during intake.** A third arXiv id returned HTTP 200, so it
looked fine — but reading the page title showed it was *"Percolation-induced PT symmetry
breaking"*, an unrelated physics paper. A reachable URL is not a verified citation.
The arXiv API returned nothing from this environment, so no further papers were added
rather than recalled from memory.

## Stage 3 — tooling (done)

[`skills/hci-study-gate`](../../skills/hci-study-gate/) — **certified 93/100** (campaign
bar ≥90). It gates a human-AI study on whether the design can support its claim:
required N from the target effect size, counterbalancing against order effects, one
pre-registered primary metric, and `NOT-MEASURED` instead of a p-value the study is too
small to earn. 18 tests; the power math is pinned to the conventional G*Power values
(d=0.5 → 64/arm), and it rounds toward *more* participants because for a gate, one too
few is a false pass.

## State as of 2026-08-04 — 8 of 9 roles at 100/100

Two shared builds closed the graph. Both were found by the graph, not by reading any one JD:

| Build | Certified | Closed | Effect |
|---|:--:|---|---|
| [`hci-study-gate`](../../skills/hci-study-gate/) | 93 | `human_ai_interaction` (3 roles) | 92→100 · 86→95 · 75→92 |
| [`transfer-loop`](../../skills/transfer-loop/) | 92 | `cross_deployment_transfer` (3 roles) | humanoids 94→100 · nvidia 95→100 · ssi 92→96 |
| [`eval-awareness-probe`](../../skills/eval-awareness-probe/) | 93 | `agi_safety_alignment` (3 roles) | agi-safety 92→100 |

Nine dossiers are generated from the same fact base as the resumes
(`python3 scripts/build_dossier.py`) so no dossier can contradict its own resume, and each
one regenerates its scorecard by RUNNING jdfit rather than pasting a remembered number.

**Dated checkpoints now live in [`data/campaign_checkpoints.yml`](../../data/campaign_checkpoints.yml)**
and are gated by `tests/test_campaign_checkpoints.py`: an overdue open checkpoint FAILS
`make check`. This closes a growth miss (F3) that three consecutive cards recorded — the
partials were always named with a leverage score, which reads like a plan and is only a
ranking.

**Honest scope limit:** `agi_safety_alignment` reads covered via eval-awareness, which
does **not** include mechanistic interpretability. One green cell is standing for two
capabilities, and the checkpoint dated 2026-09-01 is to split the cap rather than let it
imply coverage it does not have.

## Remaining build list (by leverage)

| Leverage | Capability | Roles |
|---|---|---|
| 1.5 | Cross-engagement learning — generalize insights from one deployment to all 🟡 | SSI · Humanoids · NVIDIA |
| 0.5 | Large-scale distributed systems / data infrastructure 🟡 | SSI |
| 0.5 | AGI safety & alignment — interpretability, RLHF, eval awareness 🟡 | AGI Safety |

## Per-role submission gate (Stage 5 → 7.5)

No role is submitted until **all** of these hold for that role:

1. Dossier at `docs/jd-fit/<slug>.md` with the pasted scorecard, honest edges, and 5 stories.
2. A resume genuinely tailored to *that* JD's cap profile — the role-specific caps above
   are the differentiator; a reworded generic resume fails this gate.
3. Every claim on the resume traceable to a shipped artifact (skill, lab, or card).
4. The honest weak edge named, not hidden. For `gdm-ssi-self-improving-agents` that is
   distributed infra (partial); for `gdm-agi-safety-alignment`, interpretability tooling.
5. Submission per Stage 7.5 — real-Chrome CDP, field-by-field verify before submit,
   evidence-of-submission captured.

## Outcome log

| Date | Role | Event | Artifact that carried it |
|---|---|---|---|
| 2026-08-02 | all 7 | campaign opened; dedupe + honest scoring + shared HCI build | `campaign_graph.py`, `hci-study-gate` (93) |
