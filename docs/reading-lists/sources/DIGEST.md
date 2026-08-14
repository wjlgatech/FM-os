# The digest plan — depth ≫ width

Primary sources for the reading lists, one folder per essay. Regenerate or repair with:

```bash
python3 scripts/fetch_reading_sources.py          # fetch what is missing
python3 scripts/fetch_reading_sources.py --check  # status only, no downloads
```

## The contract (Paul's rule, 2026-08-01)

Digest **one at a time**, paragraph by paragraph, concept by concept, algo by algo. No rush.
Success is measured on four axes, none of which is coverage:

| axis | what it means | what proves it |
|---|---|---|
| **experience** | you have *run* the idea, not just read it | a minimal implementation or a re-derivation by hand |
| **conviction** | you know which claims you would defend under attack, and which you would not | you can name the paper's weakest claim and say why |
| **understanding** | you can rebuild the argument without the text | you can derive the key equation/algorithm from its motivation |
| **connection** | it is wired to what you already know | ≥2 explicit links to other entries here or to a live FM-os probe |

**Finishing a paper is not the goal.** One paper genuinely absorbed beats five skimmed. If a
session ends with a summary and no new capability, the session failed.

## How to run one

`allin-anything` routes "master this" / "understand deeply" to **`master-anything`**
(`data/registry.yml`). Point it at a single folder:

```
master this: docs/reading-lists/sources/frontier-ai-reading-list/05-the-transformer-attention-is-all-you-need
```

Every folder carries:

- `SOURCE.md` — provenance, honest status, licence posture
- `PRIOR.md` — **what the reading list already claims about this work, verbatim.** This is not
  a summary to absorb; it is a **prior to test.** Confirm it, sharpen it, or refute it against
  the primary text. A digest that never contradicts its prior probably was not a digest.
- the source itself (`paper.pdf` / `page.txt` / `page.html`)

## Order (dependency, not list order)

The frontier list is close to chronological, which is also close to dependency order. Two
pairings are worth doing back-to-back because the second only makes sense against the first:

1. **01 Bitter Lesson** — the thesis every later entry is evidence for or against. Read first,
   then re-read *last*, and see whether 12 papers changed your reading of it.
2. **02 Brook for GPUs** → **03 AlexNet** — the substrate, then the first thing that exploited it.
3. **04 ResNet** → **05 Transformer** — the two architectural primitives. Do them adjacent: both
   are answers to "how do you train something deep without it falling apart".
4. **06 AlphaGo Zero** — self-play; the strongest counterexample to "data is the moat".
5. **07 InstructGPT** → **09 Chain of Thought** — the two moves that turned a model into an
   assistant. One changes the weights, one changes only the prompt. Ask why both were needed.
6. **08 Stable Diffusion** — latent space as a compute argument, not an image argument.
7. **10 APTAMI** → **11 RT-2** → **12 π0** — blueprint, then two attempts at embodying it.

The math list's entry 01 (Quanta) is the *narrative* for its entries 02–04, whose primaries are
unresolved (below) — so read it as journalism, and treat its claims as leads, not evidence.

## Honest status

| status | meaning |
|---|---|
| `full` | the primary text is here (open-access PDF or full article) |
| `landing-only` | only the public abstract/landing page — the full text was **not** retrieved and **no paywall or block was circumvented** |
| `unresolved` | the list names the work but gives no public URL, and no citation was invented |

Two are `landing-only` and three are `unresolved` — see each `SOURCE.md` for the specific reason
and how to read it legitimately. Downloaded for personal study; copyright stays with the authors
and publishers, and nothing here is redistributed.
