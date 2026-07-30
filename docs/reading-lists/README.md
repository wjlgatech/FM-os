# Community Reading-List Track

Curated, **trackable** reading lists for the FM-os community — one list per discipline, each a
dated markdown doc in this directory, each integrated into the hub README via `data/readinglists.yml`
(spec-as-data: the README section is generated, never hand-edited).

## The contract (what makes a list belong here)

1. **Trackable** — a dated file (`<focus>-reading-list-MM-DD-YYYY.md`); revisions are new dated
   files or logged edits, so the community can diff what changed.
2. **Every link verified** — curl-checked at intake; dead links are fixed with an annotation or
   removed, never left silently broken (same rule as the resume trackability gate,
   [PLAYBOOK-jobapp-flywheel Stage 5](../PLAYBOOK-jobapp-flywheel.md)).
3. **Entries earn their place** — each entry carries Statement · Essential Quote · Reasoning &
   Evidence · Actionable Steps · Patterns + Anti-patterns · 1st Principle. Secondary-source
   quotes are labeled as such until verified against the primary text.
4. **Honest gaps** — missing sections and truncated entries are marked ❌ in the doc, not papered
   over.

## Tracks

| Track | Status | Doc |
|---|---|---|
| **AI** (deep-learning canon → Physical AI → AGI/ASI) | 🟢 live (Layer 3 pending) | [ai-reading-list-07-30-2026.md](ai-reading-list-07-30-2026.md) |
| **Math** | 📋 planned | — |
| **Physics** | 📋 planned | — |
| **Computer Science** | 📋 planned | — |
| **Biology / BioMed / BioTech** | 📋 planned | — |

## Adding a track or revision

1. Write `docs/reading-lists/<focus>-reading-list-MM-DD-YYYY.md` following the contract above.
2. Verify every link: `curl -sIL -o /dev/null -w '%{http_code}' <url>` per URL.
3. Add/update its entry in `data/readinglists.yml`, then `make build` (regenerates README) and
   `make check` (drift + schema gates must stay green).
