# labs/nomadicml — interview proof-of-capability lab

Target: **Member of Technical Staff, Machine Learning @ NomadicML** (Pear VC board).
Method: clean-room reverse-engineering of their video-analysis product at small scale,
gated by tests, compared term-by-term against their production surface.

## Map

| Artifact | What it is |
|---|---|
| `GOAL-CONTRACT.md` | The original ask, evaluated + 10X'd into 5 verifiable gates (G1–G5) |
| `recon/SDK-SURFACE.md` | Exhaustive API map of `nomadicml` 0.1.53 (from PyPI wheel source, file:line cited) |
| `recon/DOCS-KB.md` | Docs knowledge base (from docs.nomadicml.com llms.txt; raw pages in `recon/docs-raw/`) |
| `recon/EXAMPLES.md` | All 20 public examples + 7 dataset showcases, recovered verbatim from their site bundles |
| `nomadic_mini/` | The clone: upload → VLM analyze (thinking/fast) → events in their verbatim schema → embedding search |
| `COMPARISON.md` | Term-by-term matrix: their SDK/API vs ours, plus an honesty ledger of what's scoped out |
| `EVIDENCE-PACK.md` | JD → artifact mapping, 5-min demo script, gaps + study plan, likely questions |
| `data/` | Two CC-licensed driving clips (SOURCES.txt has provenance) |
| `out/` | Reproduction results: their example queries run on our clips (JSON + RESULTS.md) |
| `ARCHITECTURE.md` | System design, component spec, strengths/weaknesses, future plan (P0–P3) |
| `webapp/` | Visual demo page (`make webapp` → http://127.0.0.1:8787): pipeline, clickable event timelines on the real clips, docs-vs-production findings — plus a **lab copilot** whose system prompt is assembled live from every file above |

## Gates

```bash
make check    # offline: schema-contract + search tests (no keys)
make e2e      # real VLM run on a bundled clip (GEMINI_API_KEY or ANTHROPIC_API_KEY)
make parity   # live term-by-term vs api-prod.nomadicml.com (NOMADICML_API_KEY; skips honestly)
```

Provenance: public surfaces only (PyPI wheel, docs llms.txt, site-bundle example data).
