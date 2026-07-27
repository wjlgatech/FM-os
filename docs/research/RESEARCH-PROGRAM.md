# The research program — one mile deep, not one mile wide

**The thesis (one line):** *eval gates are training-signal factories* — every honest gate
(no-evidence⇒No, maker≠checker, ship/rollback) both certifies quality AND labels preference
data, so evaluation and post-training are one closed loop, not two teams.

Everything below is a probe of that single thesis. This is the depth discipline: new work
must either deepen a probe or sharpen the thesis — a project that does neither gets a brief
and a kill criterion, not a repo.

## The probes and their homes (decided 2026-07-27)

| probe | question it tests | home | why THIS home (depth rationale) | status |
|---|---|---|---|---|
| **P1 RewardForge** | can gate-labeled failures train a better model? | [`FM-os/labs/rewardforge`](../../labs/rewardforge/) | it consumes FM-os's certified gates as its label source; a standalone repo earns itself only after a HF dataset + external users | **M1 shipped** — real LoRA-DPO, halluc 0.398→0.287, honest rollback first (PR #22) |
| **P2 MCP-Arena** | can evidence-gating separate models on real tool-use? | [`wjlgatech/mcp-arena`](https://github.com/wjlgatech/mcp-arena) (new repo — the one width exception) | a benchmark's PMF **is** being a standalone schelling point (BFCL, τ-bench are standalone); it consumes cli-judge + printing-press as satellites, never vendored | **M0 shipped** — 12 tasks × 6 categories as data, self-testing harness (golden=1.0, evidence-hallucinator fails) |
| **P3 Proactive Twin** | does proactivity pay rent (net of interruption cost)? | [`super-u/docs/PROACTIVE-TWIN-BRIEF.md`](https://github.com/wjlgatech/dreammaketrue) | super-u already owns the Digital Twin, memory layer, and telemetry — a new repo would fork our own personalization effort | **brief shipped** — five gates, kill criteria, 60%-built asset map |
| **VSS / BARE case studies** | do the gate disciplines transfer to VLM research papers? | [`research-anything/case-studies`](https://github.com/wjlgatech/research-anything) + FM-os skills | research-anything owns the *method*; FM-os certifies the *tooling* (vlm-failure-probe 98, syndata-bare 98) | live-measured (claude-sonnet-5 5/5 vs VSS 0/5) |

## The role of each hub (so efforts compound instead of spread)

- **research-anything** — the METHOD: how a research question becomes a falsifiable loop
  (its case-studies feed FM-os skills; its playbook governs every probe's write-up).
- **FM-os** — the CERTIFIER + case-study index: skills/labs with evidence-scored tiers;
  this document; jd-fit ties probes to the OpenAI Personal AGI campaign.
- **loop-engineering-anything** — the LOOP MACHINERY: maker≠checker, cli-judge referee,
  convergence policy; probes borrow its organs (vlm-probe demo, arena's judge lineage).
- **rsi-os** — the FIELD MAP: automated-research knowledge base the program cites.
- **super-u** — the PERSONALIZATION PRODUCT surface where P3 lives.

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
