# Happy College: Learn Transformers the Way You Learned Your Jump Shot

> **DRAFT — human gate pending.** Canonical home when published: the
> [agentic portfolio](https://agentic-portfolio-lovat.vercel.app) (long-form first), then 1-click
> syndication to LinkedIn + X with backlinks. Shorts: [happy-college-shorts-07-30-2026.md](happy-college-shorts-07-30-2026.md).
> All links curl-verified 2026-07-30; private repos (super-u, DreamMakeTrue) are deliberately
> unlinked. Fact-check note: ADEPT is Kalid Azad's method (BetterExplained), built in the spirit
> of Richard Feynman's teaching — the attribution below is the verified one.

---

You have already mastered something harder than linear algebra.

Maybe it was a jump shot that finally stopped clanking. An armbar escape you can hit with your
eyes closed. A flip turn, a clean vibrato, the crux move on a V4 you fell off of thirty times.
Thousands of reps. Brutal, instant feedback. And — be honest — *joy*.

Nobody called that studying. That's the whole problem.

## The lie we learned in school

School taught us that learning technical material means sitting still while information happens
to you. Your body knows better. Every hard physical skill you own was built by the same loop:

**attempt → honest feedback → small adjustment → another attempt, at the edge of your ability.**

Learning science has names for the pieces — *deliberate practice* (Ericsson), *retrieval
practice*, *desirable difficulties* (Bjork), the *zone of proximal development* (Vygotsky). A
basketball court implements all of them natively. A lecture hall implements none of them. The
gym gives you the one thing a lecture never will: **a feedback loop you can't argue with.** The
rim doesn't care about your excuses. The water doesn't grade on a curve. You can't negotiate
with a tap-out.

So the question isn't *"can we learn transformers while playing basketball?"* It's sharper than
that: **you already run the world's best learning algorithm every time you train — Happy College
just points it at technical subjects.**

## The mapping (steal this table)

| When you… | You're running… | The technical equivalent |
|---|---|---|
| Groove a free-throw routine | spaced, deliberate reps against a fixed target | a training loop with a frozen eval — you don't move the rim to feel better |
| Spar in MMA | adversarial testing under pressure; the tap is data | red-teaming your understanding; an honest ❌ beats a fake ✅ |
| Swim laps | continuous feedback from resistance; efficiency beats effort | simplify until the concept stops fighting back — drag is confusion |
| Slow-practice violin or piano | chunking + tempo scaling: slow is smooth, smooth is fast | curriculum learning — master the passage at 50% before performance speed |
| Sing on pitch | instant, unfakeable feedback | tight eval loops; you either hit the note or you don't — no vibes |
| Read a climbing route, then project it | plan the beta, attempt at your edge, fall safely, adjust | work in the zone of proximal development with cheap rollback |

Pin that table. It's the club's constitution: **every study session must feel like a training
session — reps, feedback you can't argue with, and an edge you're actually on.**

## The method: ADEPT, done properly

The concept-level tool we drill is **ADEPT** — created by [Kalid Azad of
BetterExplained](https://betterexplained.com/articles/adept-method/), in the spirit of Richard
Feynman's teaching style (if you can't take a concept down to an analogy a friend follows,
you don't own it yet):

- **A**nalogy — anchor the new thing to something you've *trained*, not just read
- **D**iagram — draw it; if you can't draw it, you can't see it
- **E**xample — one concrete case, run end to end
- **P**lain language — explain it to your sparring partner, no jargon allowed
- **T**echnical — now the real definition, **mapped term by term back to the analogy**

Sixty seconds of ADEPT on *attention*, the mechanism inside every modern AI model: a point guard
brings the ball up and reads the floor (analogy). Every teammate is waving with some degree of
openness; the pass goes mostly to the most open player — but the guard's read is a weighted
blend of everyone (plain language). Draw five players with arrows thickened by openness
(diagram). Run one play: "the cat sat on the ___" — which earlier words does the model pass to?
(example). Technically: each word issues a *query*, every word offers a *key*; their match
scores, softmaxed, weight the *values* that get blended — `softmax(QKᵀ/√d)V` — where the query
is the guard's read, the keys are how open each teammate is, and the values are what each
teammate does with the ball (technical, term by term).

That's one rep. A Happy College session runs many.

## The AI stack (this part didn't exist five years ago)

A reading club with a group chat is a book club. Happy College is a **training facility**,
because the tooling finally exists:

- **A verified curriculum, not a link dump.** The [community reading-list
  track](https://github.com/wjlgatech/FM-os/blob/main/docs/reading-lists/README.md) (AI and
  AI-for-research live today; math, physics, CS, bio next): every link machine-verified, every
  entry carrying Statement · Quote · Evidence · Actions · Patterns · 1st Principle, every gap
  marked honestly instead of papered over.
- **Living knowledge, not dead notes.** Skills like `/living-knowledge` and `/graphify` turn
  each session into a knowledge graph that stays fresh — your notes become a map you can query,
  not a notebook you never reopen.
- **A twin that tracks your becoming.** Our participation engine (super-u's future-self work)
  models two selves — the one your habits are building and the one you intend — and makes the
  gap between them the syllabus.
- **Listener → participant → creator, in one session.** That's DreamMakeTrue's contract, and
  it's the club's exit criterion: you don't leave having *read about* attention; you leave
  having taught it, been sparred on it, and built one tiny artifact with it.
- **One front door.** [allin-anything](https://github.com/wjlgatech/allin-anything) routes any
  intent — "master this paper" — to the right tool, so the machinery never gets between you and
  the rep.

One rule holds it together, borrowed from how we certify software: **no evidence ⇒ no**. You
haven't learned it until you can rebuild it, teach it, or survive being sparred on it.

## What a session actually looks like (60 minutes)

1. **Warm-up (5 min):** retrieval, not review — write what you remember from last week, cold.
2. **ADEPT sprint (20 min):** one concept, five moves, ending in the term-by-term mapping.
3. **Sparring (20 min):** pairs. You teach; your partner attacks with "what breaks if…?"
   questions. Tapping is data, not defeat.
4. **Build rep (10 min):** one tiny artifact — 20 lines of code, one diagram, one worked
   example. Creators, not note-takers.
5. **Log (5 min):** the artifact goes into the living knowledge graph. Next week's warm-up is
   drawn from it.

You leave with an artifact, not annotations.

## Join

Happy College is what college should have been: the joy of the gym, the rigor of the lab, and an
AI stack that gives every learner what elite athletes have always had — a coach, a spar, and a
scoreboard that doesn't lie.

Start where we started: pick one item off the [AI reading
list](https://github.com/wjlgatech/FM-os/blob/main/docs/reading-lists/ai-reading-list-07-30-2026.md),
bring the hardest physical skill you ever built, and come ready to map one onto the other.

**Your jump shot is your syllabus. See you at Happy College.**
