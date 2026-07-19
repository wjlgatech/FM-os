# The Distillery — every cited repo → a knowledge graph + agentic tooling

FM-os is a hub of three things: **knowledge · tooling · experts**. The distillery is how the hub
turns each cited repo into all three, at scale, without drifting or fabricating.

`scripts/distill.py` reads `data/repos.yml` (the single source of truth) and, per repo, writes
`distill/<slug>/`:
- **`graph.json`** — a grounded knowledge graph (nodes: repo · category · concepts · lab/author ·
  related repos; edges carry a `provenance` string).
- **`SKILL.md`** — an agentic-tooling scaffold, gated by `scripts/certify.py`.

The three pillars fall out together: the KG's `maintained_by` edge (repo owner → `labs.yml` org) is
the **experts** pillar, emitted for free by the **knowledge** pass.

## Why it's honest (quality by construction)

- **No evidence ⇒ no node.** A concept node exists only if a `jd_taxonomy` keyword appears in the
  repo's blurb, or the repo's category matches — and the node records *which*. Nothing is invented.
- **Every node + edge has `provenance`.** `distill.py --check` fails CI on any missing-provenance
  node, orphan node, or dangling edge.
- **Tooling is gated, not asserted.** A generated `SKILL.md` is scored by `certify.py`; a scaffold
  too thin to clear the bar is simply *not* certified. `distill/` never claims a fake pass.

## Why it's fast + cheap

- Pure-stdlib, deterministic, no network, no model — **milliseconds per repo**. The whole 89-repo
  sweep is a `make distill` away.
- The semantic layer is concept-matching against a small taxonomy, not an LLM call. (A richer LLM
  analyzer is a *swappable seam* — see below — reserved for on-demand deep dives on a pinned repo.)

## Why it stays up-to-date

- Each `graph.json` pins a `source_hash` of its repo entry. `distill.py --check` flags **stale**
  graphs when the source changed.
- `sync.py` already refreshes stars/commits; a weekly CI cron runs `make distill` to regenerate
  only what changed. `repos.yml` is the trigger list.

## Why it's future-proof

- **Spec-as-data**: `repos.yml` → generated artifacts, drift-gated by `make distill-check` (wired
  into `make check`). Spec can't silently diverge from output.
- **Swappable analyzer seam**: `build_graph()` is the shallow, deterministic default; a deeper
  full-codebase analyzer (e.g. `understand-anything`) can replace it for pinned repos without
  changing the `graph.json` schema or any consumer.
- **Standard formats + identity**: plain JSON graph + `SKILL.md`, each hash-stamped, so any harness
  can read them and drift is detectable.

## Scaling from the slice (how to loop to all 89)

This shipped as a **thin slice** (`unsloth`, `vllm`, `verifiers`) proven end-to-end: KGs validate,
skills certify 88/100. To scale:

```bash
make distill            # generate KG + tooling scaffold for every cited repo
make distill-check      # validate all graphs + flag drift  (also runs inside `make check`)
# certify the tooling:  for d in distill/*/; do python3 scripts/certify.py --target "$d"; done
```

Promotion is a **human gate**: a distilled `SKILL.md` that certifies well and earns enrichment gets
moved into the curated `registry.yml`. The `distill/` factory stays separate from the hand-vetted
registry — automation proposes, a human promotes.
