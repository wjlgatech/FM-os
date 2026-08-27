# AI Interpretability & Alignment — a focused section

**Status:** open, 2026-08-27 · **North star:** Verified Claim Coverage — **28/32 (87.5%)**
· **Gate:** `make interp` (floor 80, in `make check`)
· **Spec:** [`data/interp_ledger.yml`](../../data/interp_ledger.yml)

---

## Why this section exists, and why it is shaped like this

It started with an artifact, not a topic. An AI-generated summary of a
[podcast on interpretability](https://www.youtube.com/watch?v=J5_90lWxM_o) —
speech recognition, then LLM summarisation into headings, quotes and
"patterns / anti-patterns". It is a genuinely good summary. Its structure is
clean, its technical explanations are mostly right, and it reads with total
confidence.

**Eight of the twenty-five factual claims it asserts are materially wrong.**

Not vague-wrong. Wrong in the way that breaks a reader: a lab's name spelled
three different ways and none of them correct; a professor moved from
Northeastern to Northwestern; a word swapped inside quotation marks. Reading it
more carefully does not help, because the eight wrong entries are written in
exactly the same voice as the seventeen right ones. The artifact carries **no
internal signal** about which of the steps that produced it were reliable.

That sentence is also a one-line summary of the field the podcast is about. A
language model's fluent output tells you nothing about the computation that
produced it; Transluce measured a behavioural shift in 21–22 of 24 frontier
models that the models verbalised in **0.84%** of their reasoning traces
([Transluce, 2026](https://transluce.org/user-awareness)). The failure mode at
the document level and the failure mode at the activation level are the same
failure mode, and they have the same fix: **do not read the output, check it
against something outside itself.**

So this section is not a reading list about interpretability. It is a ledger
that refuses to hand you a claim it has not checked.

---

## The five statuses

Every claim from a source lands in exactly one. Each one exists because its
absence would let an unchecked claim pass as a checked one.

| Status | Means | Why it is separate |
|---|---|---|
| `verified` | the source said it, a primary source confirms it | the baseline |
| `corrected` | the source was wrong; **both** forms are kept | deleting the wrong form hides the error rate |
| `refuted_correction` | **we** proposed a correction and were wrong | see below — this is the load-bearing one |
| `omitted` | a caveat the primary source states and the summary dropped | the error you cannot see by reading the artifact |
| `unverified` | we could not check it; **never citable** | "could not look" is never "all clear" |

### `refuted_correction`, and why the ledger grades itself

The summary mentioned an auditing dataset called **"Weird Chat"**. That is
obviously a mis-hearing of **WildChat** — Allen AI's million-conversation
dataset, famous, and a near-perfect phonetic match. I recorded the correction.

WildChat is real. **So is [WeirdChat](https://transluce.org/weirdchat)** — a
Transluce project that surfaces pathological model behaviours. The summary was
right and the correction was wrong.

That row stays in the ledger with the bad correction preserved, because a
corrector that keeps only the corrections that held reports **100% accuracy by
construction**. The gate refuses a `refuted_correction` entry that does not
record what was wrongly proposed. Current corrector accuracy: **8 of 9, 89%.**

The lesson generalises past this file: a plausible correction is not a verified
correction, and confident revision is the same failure as confident assertion
wearing a lab coat.

---

## What the gate does

```bash
make interp                              # the ledger, scored
python3 scripts/interp.py --errors       # only what the source got wrong
python3 scripts/interp.py --cite jspace  # emit a claim in citable form
python3 scripts/interp.py --cite sushi_japanese
# REFUSED — sushi_japanese is not citable. status is 'unverified': …
```

That refusal is the product. The table is only how you read it.

Fail-closed rules, each mutation-tested in
[`tests/test_interp.py`](../../tests/test_interp.py) (19 tests):

1. a checked claim with no primary-source URL is rejected
2. a `corrected` entry whose replacement equals the original is rejected — that
   is a claim of work that never happened
3. a `refuted_correction` with no `proposed` field is rejected
4. an `unverified` entry must say **what** stopped the check, and must **not**
   carry a source URL — a source that was read is a check that happened
5. a claim past its kind's half-life goes **stale** and stops being citable;
   "it was true when I looked" is how a live registry rots quietly

**The gate floor is 80, deliberately below the current 87.5%.** A coverage floor
set at the current number punishes you for recording a claim you could not
verify, which is the exact behaviour this section exists to prevent. The failure
being studied is unrecorded uncertainty; the gate must never make honesty
expensive.

---

## What the ledger found

Scored over the 25 claims the summary actually asserted:

- **8 materially wrong (32%)** — `arora`, `bau`, `wu_zen`, `transluce`,
  `uk_aisi`, `biology`, `glu_quote`, `axbench`
- **3 material caveats dropped** — including the J-lens's own stated limit
  (it "can only identify concepts that correspond to single tokens"), and
  AxBench's actual measurement, which the summary reduced to the word "fragile"
- **1 case where the summary was right and we were wrong** — `weirdchat`
- **4 unverified**, and they stay that way

Two of the errors are worth separating, because they fail differently:

**Phonetic misses** (`Transloose` → Transluce, `Zen Ju` → Zhengxuan Wu) come
from the speech-recognition stage. They are recoverable — a reader who searches
the wrong string finds nothing and knows something is off.

**Fluent substitutions** are not. "Northwestern" for "Northeastern" produces a
real university with a real CS department; a reader who searches it finds a
page and stops. The summary also states Aryaman Arora is advised by Chris
Potts. He is co-advised by Dan Jurafsky *and* Christopher Potts — nobody
misheard "and Dan Jurafsky"; a detail was dropped and the sentence still parsed
as complete. **The second class is the one no plausibility check catches,
because the wrong answer is exactly as plausible as the right one.**

And the reverse holds. The single strangest-sounding item in the summary — that
Anthropic can edit a word the model never said — checks out exactly
([Anthropic, 2026-07-06](https://www.anthropic.com/research/global-workspace)):
swap the `spider` pattern for `ant` in J-space and Claude answers "6" instead of
"8", with "spider" appearing in neither the input nor the output. Implausibility
is not a detector either.

---

## Open work — named, not hidden

- **The four unverified claims stay unverified.** Two are unsourceable as
  stated (`sushi_japanese`, `lab_cot_audits`), one needs the original talk
  located (`sutskever_worldmodel`), one needs a person to confirm their own
  affiliation (`wu_transluce`).
- **The ledger checks one source.** A second source would test whether the 32%
  error rate is a property of this pipeline or of this episode. Until then it
  is one observation, and n=1 rates carry the interval to prove it
  ([`docs/research/POWER-AND-THE-ZERO-NUMERATOR.md`](POWER-AND-THE-ZERO-NUMERATOR.md)).
- **Nothing here has been checked by anyone but me.** Every `verified` is one
  person reading one primary source once. That is better than not looking and
  worse than review.

---

## The reader-facing half

Season 2 of *Intelligence Engineering Adventures* —
**[The Glass Engine](https://github.com/wjlgatech)** — is the writing arm of
this section. Episode 1, *The Word That Was Never Said*, is the article this
ledger backs: every number in it resolves to a row here, and the episode's
Failure Room is the `weirdchat` row.

- season contract: `intelligence-engineering-adventures/interp-adventure-series/series.yml`
- published: [/articles/the-word-that-was-never-said.html](https://agentic-portfolio-lovat.vercel.app/articles/the-word-that-was-never-said.html)
