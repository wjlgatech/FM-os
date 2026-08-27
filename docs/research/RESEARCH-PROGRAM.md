# The research program — one mile deep, not one mile wide

**The thesis (one line):** *eval gates are training-signal factories* — every honest gate
(no-evidence⇒No, maker≠checker, ship/rollback) both certifies quality AND labels preference
data, so evaluation and post-training are one closed loop, not two teams.

Everything below is a probe of that single thesis. This is the depth discipline: new work
must either deepen a probe or sharpen the thesis — a project that does neither gets a brief
and a kill criterion, not a repo.

> **External confirmation (2026-08-13).** The thesis stopped being only ours. Thomson Reuters'
> Andrew M. Bean is *Evaluations Lead **for LLM post-training*** — one team, not two — and that
> org ships a frontier-competitive professional model. Full reconstruction, with 12 scored
> predictions: [`CASE-STUDY-thomson-stack.md`](CASE-STUDY-thomson-stack.md).

## The probes and their homes (decided 2026-07-27)

| probe | question it tests | home | why THIS home (depth rationale) | status |
|---|---|---|---|---|
| **P1 RewardForge** | can gate-labeled failures train a better model? | [`FM-os/labs/rewardforge`](../../labs/rewardforge/) | it consumes FM-os's certified gates as its label source; a standalone repo earns itself only after a HF dataset + external users | **M1 shipped** — real LoRA-DPO, halluc 0.398→0.287, honest rollback first (PR #22) |
| **P2 MCP-Arena** | can evidence-gating separate models on real tool-use? | [`wjlgatech/mcp-arena`](https://github.com/wjlgatech/mcp-arena) (new repo — the one width exception) | a benchmark's PMF **is** being a standalone schelling point (BFCL, τ-bench are standalone); it consumes cli-judge + printing-press as satellites, never vendored | **M0 shipped** — 12 tasks × 6 categories as data, self-testing harness (golden=1.0, evidence-hallucinator fails) |
| **P3 Proactive Twin** | does proactivity pay rent (net of interruption cost)? | [`super-u/docs/PROACTIVE-TWIN-BRIEF.md`](https://github.com/wjlgatech/dreammaketrue) | super-u already owns the Digital Twin, memory layer, and telemetry — a new repo would fork our own personalization effort | **brief shipped** — five gates, kill criteria, 60%-built asset map |
| **VSS / BARE case studies** | do the gate disciplines transfer to VLM research papers? | [`research-anything/case-studies`](https://github.com/wjlgatech/research-anything) + FM-os skills | research-anything owns the *method*; FM-os certifies the *tooling* (vlm-failure-probe 98, syndata-bare 98) | both live-measured (VSS: claude-sonnet-5 5/5 vs VSS 0/5 · BARE 2026-08-14: mode collapse reproduced 0.23 vs 0.62; the pipeline claim's first "not substantiated" was **retracted as UNDERPOWERED** (rule of three, 0/18 ⇒ CI [0, 16.7%]), then **re-resolved at n=66 + n=72 as a genuine negative** — 0 hallucinations, CIs [0, 4.5%] / [0, 4.2%], both excluding the 4.62% reference rate: [`POWER-AND-THE-ZERO-NUMERATOR.md`](POWER-AND-THE-ZERO-NUMERATOR.md)) |
| **P4 Thomson-1 stack** | can you predict a lab's training stack from its publications — and is that reading *scored*, not asserted? | [`docs/research/CASE-STUDY-thomson-stack.md`](CASE-STUDY-thomson-stack.md) | it is a direct existence proof of THIS program's thesis: Thomson Reuters' evaluations lead reports into post-training, i.e. eval and post-training are literally one team | **12 predictions registered 2026-08-13**, Brier UNSCORED pending the technical report; `eval-subset` skill certified 98 |
| **P5 Interpretability ledger** | when a source asserts a fact, can a gate tell a checked claim from an unchecked one — including when the CHECKER is the one that is wrong? | [`docs/research/INTERPRETABILITY.md`](INTERPRETABILITY.md) + [`data/interp_ledger.yml`](../../data/interp_ledger.yml) | it is the certifier thesis applied to a source instead of a repo, and it needs FM-os's `make check` to be fail-closed; a standalone repo would be a bibliography with opinions | **32 claims ledgered 2026-08-27**, Verified Claim Coverage **28/32 (87.5%)**; the seed summary was wrong on **8 of 25** asserted claims, and **1 of our 9 corrections was itself refuted** (corrector accuracy 89%) |

## The role of each hub (so efforts compound instead of spread)

- **research-anything** — the METHOD: how a research question becomes a falsifiable loop
  (its case-studies feed FM-os skills; its playbook governs every probe's write-up).
- **FM-os** — the CERTIFIER + case-study index: skills/labs with evidence-scored tiers;
  this document; jd-fit ties probes to the OpenAI Personal AGI campaign.
- **loop-engineering-anything** — the LOOP MACHINERY: maker≠checker, cli-judge referee,
  convergence policy; probes borrow its organs (vlm-probe demo, arena's judge lineage).
- **rsi-os** — the FIELD MAP: automated-research knowledge base the program cites.
- **super-u** — the PERSONALIZATION PRODUCT surface where P3 lives.

**Inbound collaborations** are read against this program, never absorbed into it:
[`COLLAB-intern-projects.md`](COLLAB-intern-projects.md) maps three Physical AI intern
projects onto existing probes — trajectory labels feed **P1 RewardForge**, thread memory
meets **P3 Proactive Twin**, spatial grounding tests the **VSS** probe suite. None earns a
new probe, which is the depth discipline working rather than being recited.

## The discipline the program nearly failed (2026-08-14)

The thesis says an honest gate is a training-signal factory. A gate that reports an
**unsupported negative** is as broken as one that reports an unsupported positive — and it is the
failure an eval-focused repo is most likely to wave through, because a negative reads as
modesty. `syndata-bare` shipped exactly that: `NOT SUBSTANTIATED` on 0 events in 18 trials, a
sample size that could not have detected the effect it was denying.

**The rule now, everywhere a gate reports a negative:** state the *n*, and state the smallest
effect that *n* could have resolved. A negative without a power statement is an opinion.
It has a tool — `make power` (`scripts/power.py`: Wilson CIs, the rule of three, and the
minimum detectable difference for a two-arm design) — because a rule without one is a slogan.

**The rule the interpretability section adds (2026-08-27): a corrector must be able to report
its own error rate.** P5 checked 25 asserted claims from an AI-generated summary and corrected
eight. One of those corrections — "Weird Chat must be a mis-hearing of WildChat" — was refuted
by the primary source: WeirdChat is a real Transluce project, so the summary was right and the
correction was the hallucination. Had that row been deleted once it was disproved, the ledger
would report **100%** corrector accuracy by construction. It reports **89%**, and the gate
rejects a `refuted_correction` entry that does not preserve the wrong correction verbatim.
A verification pass with no measurable miss rate is a verification pass with no evidence
behind it — the same shape as the unsupported negative above, wearing a lab coat.

**The rule that keeps us deep:** a new idea lands as (1) a brief with kill criteria in an
existing home, then (2) a gated lab/module, and only then (3) a standalone repo — and only
if standalone-ness is load-bearing for its PMF (as with a benchmark). Repos are earned, not
scaffolded on enthusiasm.

## The compounding flywheel across probes

```
mcp-arena failures ─┐
                    ├──> RewardForge pairs ──> gated fine-tune ──> re-scored on mcp-arena
proactive-twin      │
accept/reject ──────┘         every claim regenerable · every gate exits non-zero
```

Provenance: the 10X roadmap (`~/Downloads/OpenAI Personal AGI — … — 10X.md`) chose the
probes; this doc fixes their homes. Scores regenerate via `make jdfit`; probe gates via
each home's `make check`.
