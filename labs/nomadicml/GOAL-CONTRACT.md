# Goal Contract — NomadicML Interview Proof-of-Capability

> Original ask, evaluated and 10X'd per the goal-10x discipline. 2026-07-21.

## The original request (verbatim intent)

Interview prep for **Member of Technical Staff, Machine Learning — NomadicML** (via Pear VC board).
Build the knowledge + tooling the JD requires; prove qualification by reverse-engineering their
product at small scale (a few of their public examples), deeply understand their SDK/docs, test
their live API, and compare term-by-term — "prove our capacity is real and not a surface-level demo."

## Evaluation of the request

**What's strong (keep):**
- Proof-by-construction instinct — building a working replica beats reciting the docs.
- "Term-by-term" comparison — demands verbatim schema fidelity, which is checkable, not vibes.
- Explicit anti-demo stance — the deliverable must survive scrutiny by the founders (ONNX
  Runtime / DeepSpeed contributor; navigation-AI researcher). They will probe.

**What's weak (fix):**
1. **Unbounded** — "build knowledge, tooling required by this JD" spans VLM training, GPU
   pipelines, agentic evals, curation loops, retrieval. Un-scoped = unverifiable.
2. **No definition of done** — no gates; "deeply understand" is not measurable.
3. **Hidden human-gated dependency** — testing their live API requires an account + API key
   (signup is yours to do; the harness must degrade gracefully without it).
4. **Aims at the wrong altitude, alone** — replicating *product output* proves you understand
   what they sell. The JD is about *how they build it*: agentic evaluation frameworks, curation
   loops, VLM fine-tuning. A clone without an eval harness is exactly the surface demo you fear.
5. **Missing the interview surface** — capability that can't be presented in 5 minutes doesn't
   transfer in an interview.

**Boundary (explicit):** everything here uses public docs, the published PyPI SDK, and our own
implementation. No auth-walled scraping, no ToS violations — clean-room comparable capability,
which is also the honest interview story.

## The 10X'd contract — 5 gates, each machine- or artifact-verifiable

| # | Deliverable | Gate (verify, don't vibe) |
|---|---|---|
| G1 | **Recon corpus**: SDK surface map (from source), docs KB (from llms.txt), examples inventory | Files exist with verbatim endpoints/field names, each claim cited to file:line or doc slug |
| G2 | **`nomadic_mini`** — working small-scale clone: video → VLM → structured motion events (turns, lane changes, anomalies) → embedding search. Gemini video-native primary, frames+Claude fallback | `make check` green: unit tests + end-to-end run on ≥2 real CC-licensed driving clips emitting events in **their** schema (verbatim field names) |
| G3 | **Parity harness** — the same clip through their live API and our clone; term-by-term diff (API surface, request/response schemas, event vocabulary, output agreement) | Schema-contract tests always run; live tests auto-run when `NOMADICML_API_KEY` is set, `skip` (never fake-pass) otherwise. This harness **is** a JD bullet ("agentic evaluation frameworks") |
| G4 | **JD evidence pack** — every JD requirement → concrete artifact (FM-os skills: agentic-eval, curation-loop, vector-rag, vlm-quickstart, continual-rl-eval; the clone; the harness). Gaps named honestly + study plan | Zero unmapped JD bullets; gaps listed, not hidden |
| G5 | **Interview surface** — 5-minute demo script + anticipated technical questions with artifact-grounded answers | Every claim in the script traces to a runnable artifact |

**Where the 10X lives:** the comparison harness is not just a check on G2 — it is itself the
strongest exhibit. "I built an agentic eval framework that benchmarks my clean-room clone against
your production API, term by term" is a line no other candidate will have, and it is literally
the third bullet of the role's responsibilities.

## Status log
- G1: in progress (3 parallel recon agents: SDK source, docs, examples)
- G2–G5: pending G1
- Note: generic `anyagent reverse` on the SPA gated itself 0/100 (honest ✗) — custom pipeline is the path.
