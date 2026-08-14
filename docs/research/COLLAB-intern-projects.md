# Three intern projects, read against our research program

**Source:** *Summer Research Interns Report* (meeting transcript summaries, 2026-08-14) — Agent
Assurance (Abdi, Sibhi), ConcurTree (Ellyse), real-time 3D scene understanding (Daniel).
Owners listed include the **Physical AI team**, i.e. this is our own org, not an outside lab.

**Read this document as a proposal, not a verdict.** Everything here is derived from meeting
summaries — no code, no data, no papers were seen. Where a number is recomputed it says so, and
where the report did not give an *n* this document asks for it rather than assuming one.

---

## The one-sentence finding

**Project 1 built a gate and stopped at observability. Our whole thesis is that a gate is a
training-signal factory.** Their 1,152 trajectory-scored runs are, without a single additional
experiment, a labelled preference dataset — and we already have the loop that consumes it.

---

## 1. Agent Assurance (Abdi, Sibhi) — the closest thing to a ready-made collaboration

### What they found

Correctness does not imply safety. About half of adversarial runs used at least one attacker
tool, and about half of *those* still produced a correct answer. About 17% of runs never invoked
the expected tool, and 23% of those were still scored correct. Identical outcomes cost up to **3×
different token spend**.

### Why this lands on us specifically

This repo's research program is one line: *eval gates are training-signal factories* — an honest
gate both **certifies** quality and **labels** preference data, so evaluation and post-training
are one loop, not two teams
([`RESEARCH-PROGRAM.md`](RESEARCH-PROGRAM.md)).

Their report's own "10X question #1" asks whether trajectory signals can become real-time
controls instead of post-run analytics. That is a good question, and we think it is the **second**
best one. The first is:

> **Every trajectory violation is already a labelled preference pair.**
> A run that reached the right answer *via an attacker tool* is a `rejected` sample. The same task
> solved *without* it is `chosen`. That is DPO training data, produced by an eval they have
> already run, with no annotator in the loop.

We are not speculating that this works. **P1 RewardForge** in this repo does exactly that pipeline
end to end — gate-labelled failures → LoRA-DPO → measured improvement, with held-out hallucination
dropping **0.398 → 0.287**, and an honest rollback recorded before the run that worked
([`labs/rewardforge`](../../labs/rewardforge/)). It has never been fed a *security* label, because
we did not have one. They have 1,152 of them.

### The concrete ask

Their run logs, with per-run fields: task id, architecture, model, prompting strategy, tool
sequence, attacker-tool flag, expected-tool-invoked flag, correctness, tokens. Nothing else. From
those we can produce preference pairs and report, honestly, whether a model trained on
trajectory-labelled pairs is measurably safer at equal accuracy — or whether it is not.

**What they get back that they cannot get alone:** the answer to whether their signal is
*actionable*, not merely *diagnostic*. Detection that never changes a model is a dashboard.

### The design note we owe them — offered as help, not correction

Their aggregate rates are solidly supported. The claim we would protect with more runs is the
strategic one: *"different agent+model combinations exhibited very different attack susceptibility
profiles ... security assurance cannot be generalized across architectures."*

That is a claim about a **difference**, and differences need roughly 4× the sample a rate does.
Recomputed with `scripts/power.py` (Wilson intervals; exact counts were not in the report, so the
percentages were converted back to counts):

| reported | recomputed 95% CI | width |
|---|---|---|
| ~17% never invoked the expected tool (196/1152) | 15.0% – 19.3% | 4.3 pts |
| ~23% of those still correct (45/196) | 17.6% – 29.3% | 11.7 pts |

The second interval is already wide enough that "roughly a quarter" is the honest phrasing.

For the architecture comparison, the adversarial subset size was not reported, so here is the
whole curve rather than a guess:

| runs per arm | smallest detectable difference |
|---|---|
| 36 | 33.0% |
| 72 | 23.3% |
| 144 | 16.5% |
| 288 | 11.7% |
| 576 | 8.3% |

Resolving a 10-point difference needs **393 runs per arm**; 5 points needs **1,570**.

**None of this says the architectures do not differ.** It says a difference smaller than the
threshold cannot be told from noise by this design. We are raising it because it is the claim
their report leads with strategically, and because this repo published its own unsupported
negative *today* and had to retract it
([`POWER-AND-THE-ZERO-NUMERATOR.md`](POWER-AND-THE-ZERO-NUMERATOR.md)) — the tool exists because
we needed it on ourselves first.

Run it: `python3 scripts/power.py --intern-report`

### One more signal they already have and did not price

The **3× token variance at identical outcomes** is not just a cost-governance story. It is a
free efficiency label: same task, same result, one third the spend. Those are preference pairs
too, on an axis nobody has to define.

---

## 2. ConcurTree (Ellyse) — the missing half of our Proactive Twin probe

### What it is

Activity-**thread** memory instead of timeline memory for long egocentric video, under three
deployable constraints: streaming/causal, ~4K token budget, query-agnostic. An LLM judge decides
whether a scene change starts a new thread or resumes an old one. Reported gain **+0.8 to 2.5
points** over flat memory; the bottleneck is the reader, not the memory structure.

### Where it meets our work

Our **P3 Proactive Twin** brief asks one question: *does proactivity pay rent, net of the
interruption cost?* Ellyse's 10X question #3 is *can thread structure predict what the user does
next?* Those are the same question from opposite ends. She has the structure that knows **what**
should resume. The Proactive Twin brief has the gates that decide **whether it is worth saying**.

And as of today we have the other missing piece, built for an unrelated reason: a **presence
gate** that decides whether this is a good moment to speak at all — mic in use, meeting audio,
live-call traffic, screen locked, Focus on, or a stop the human made in the last 30 minutes
(`AnyAgent docs/VOICE.md`, rule 5). It exists because a card read itself aloud into a live Teams
meeting this morning.

> Thread structure answers *what to resume*.
> The interruption gate answers *when it is welcome*.
> Neither is a product alone. Together they are the Proactive Twin.

### The design note

**+0.8 to 2.5 points needs its *n*.** That is exactly the size of gain that is real about as often
as it is noise, and the report gives a range across evaluation setups without a sample size or an
interval. Before anyone builds on the number, `scripts/power.py --rate K N` costs nothing and
settles it. If the benchmark has a few hundred questions, a 0.8-point gain will not survive a
confidence interval — and it is far better to learn that from us than from a reviewer.

Her own diagnosis is the strong part of the report: the bottleneck is the **reader**, not the
memory. That is a well-formed negative result about her own architecture, and it is worth more
than the headline gain.

---

## 3. Real-time 3D scene understanding (Daniel) — a direct test for tooling we already shipped

### What it is

SLAM + SDF + Gaussian reconstruction at ~150 FPS, object segmentation lifted into 3D, and natural
language over the result ("lift all blue pillows"). The bottleneck is depth: replacing true depth
with estimated depth degrades pose, and once pose degrades, reconstruction collapses.

### The connection worth testing

We have measured, live, that vision-language models fail at exactly the spatial primitives this
system's language layer depends on. In our VSS failure-probe suite, `claude-haiku-4-5` read a
**rising forklift fork as descending** — score **0.00** on retrieval-and-grounding — while larger
models cleared it ([`CASE-STUDIES-research-anything.md`](CASE-STUDIES-research-anything.md)).

A language-addressable world model inherits its language model's spatial blind spots. "Lift the
pillow" and "put it down" are the same instruction to a model that cannot tell rising from
falling. **The probe suite is a skill (`skills/vlm-failure-probe`, certified 98) and runs against
any model in minutes.** Pointing it at whatever VLM sits behind the language layer is a cheap,
concrete contribution.

### The cascade is the interesting finding

"Depth error → pose error → reconstruction collapse" is a **cascade**, and cascades are where
per-stage evaluation lies to you: each stage can pass its own metric while the composition fails.
That is the same structure as the trajectory-vs-outcome argument in Project 1 — a system whose
final artifact looks acceptable while the path that produced it was not. If Projects 1 and 3
compared notes on *staged* evaluation, both would gain.

---

## What actually 10Xes our research

Ranked by how much it moves *our* program, and honest about what each costs.

1. **Trajectory labels → RewardForge.** The single highest-leverage item. It converts our thesis
   from a repo-scale claim into one tested on 1,152 real enterprise-flavoured runs with security
   labels we cannot generate ourselves. Cost: a data export. Risk: their logs may not retain tool
   sequences per run — that is the first question to ask, before anything is planned.
2. **ConcurTree threads + our interruption gate = the Proactive Twin.** Cost: a shared brief and
   one honest metric (does a resumed-thread prompt beat a silent one, net of annoyance?). Risk:
   the interruption gate has *no* recorded stops yet, so its own accuracy is UNMEASURED — we would
   be bringing a hypothesis, and should say so.
3. **The power tool, pointed at all three projects.** Cheapest of the three and already built.
   Every project above has at least one headline number without an interval.
4. **`vlm-failure-probe` against Daniel's language layer.** Cheap, concrete, and tests a real
   hypothesis: does spatial grounding failure survive into a 3D-grounded system, or does the
   geometry rescue it? Either answer is publishable.

## What we should NOT do

Absorb any of this into FM-os as a new probe. The depth discipline in
[`RESEARCH-PROGRAM.md`](RESEARCH-PROGRAM.md) says a new idea lands as a brief with kill criteria
in an existing home, then a gated module, and only then a repo. All four items above attach to
**existing** probes (P1, P3, and the VSS case study). None of them earns a new one.

---

*Recompute every number here: `python3 scripts/power.py --intern-report` · `make test`.*
