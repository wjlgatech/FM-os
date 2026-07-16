# Transfer Prompt — rsi (awesome-auto-ai-research), zero-edit

*Open a fresh session on `wjlgatech/rsi` and paste everything from the `/anyagent` line down.*

---

/anyagent

**Turn `rsi` (awesome-auto-ai-research) into an AI-native, self-verifying, build-in-public compounding
flywheel** — port the architecture I proved in `github.com/wjlgatech/FM-os` and
`github.com/wjlgatech/longevity-loop`. Reverse-engineer those two repos' `data/*.yml` + `scripts/`
FIRST (spec-as-data generator, rubric-as-data certifier, AI-native self-audit, weekly tracker, Pages
dashboard, field graph); reuse the machinery, adapt to rsi's domain: **automated AI research / recursive
self-improvement / AI-Scientists** (Sakana AI-Scientist v1/v2, Google AI co-scientist, Agent Laboratory,
ADAS, Gödel Agent, MLAgentBench, Recursive Lab, DeepMind). Work the goal-10x loop; ship small, green,
committed increments; verify at the artifact (browser/curl/CI), never vibe; honest ❌ over fake ✅.

rsi today is a hand-maintained awesome-list whose README *claims* a "living knowledge graph,"
"automated weekly freshness checks," and "reproducibility status + impact scores." **Make those claims
real and enforced.** Do these three first, in order:

**1. Spec-as-data + drift gate (make the "living" claim true).**
Move rsi's content into `data/*.yml` — `papers.yml` (with its groups: foundational/visionary,
automated scientific discovery, automated agentic system design…), `tools.yml`, `people.yml`,
`labs.yml`, `benchmarks.yml`, `roadmaps.yml`, plus `meta.yml` (title, badges, sections). Write
`scripts/build_readme.py` to GENERATE the README from them and `scripts/validate.py` (required fields +
working URLs). `make check` = validate + `build_readme.py --check` (drift gate). CI fails if the
committed README ≠ generated. Now "living knowledge graph" is enforced, not aspirational.

**2. RSI-Certified — a rubric-as-data certifier for auto-AI-research tooling (realize the "reproducibility
status + impact scores" claim).**
`data/certify.yml` = the rubric; `scripts/certify.py --target <dir|repo> --gate N` scores an
AI-Scientist-style repo on evidence: **reproducibility** (does it run / ship a result?), **provenance**
(content-hash + author/source), **autonomy level** (how much of hypothesis→experiment→writeup is
automated?), **eval-with-teeth** (ships a benchmark score, e.g. on MLAgentBench/TGB?), **safety** (a
self-modifying/recursive agent that could act unsafely — flag it; maker≠checker), **cross-runtime**.
Discipline: no evidence ⇒ No; blocking gates can't pass on unmeasured items; exit non-zero → CI gate.
Emit a shields badge + a `.github/actions/rsi-certify` composite action so tool authors self-certify.
Dogfood on 2-3 real repos (SakanaAI/AI-Scientist, ShengranHu/ADAS, …) with verified evidence.

**3. AI-native self-audit + a real frontier tracker (make "weekly freshness" true) + cross-link.**
`data/ainative.yml` + `scripts/ainative.py --gate 85` in `make check` (loop-not-oneshot ·
independent-referee · no-evidence⇒No · spec-as-data · agent-native · compounding-memory · verify-live).
`scripts/track.py` on OPEN APIs (arXiv q-bio/cs.AI + GitHub) refreshing recent works + repo activity for
the RSI frontier into a generated `_frontier.yml`; a weekly `track.yml` Action opens a "what moved" PR.
Render a Frontier Radar + (optional) a spatiotemporal field graph (`build_graph.py` → `graph.json` +
force-graph page, modeled after `getzep/graphiti`) for researchers↔labs↔topics↔papers over time.
Add a top banner cross-linking FM-os (the method) + longevity-loop (a sibling application).

**Non-negotiable discipline (bake into `make check` + CI):**
- Verified research only — fan out parallel agents for REAL, URL-verified entries; dedup; flag
  dead/uncertain; never invent a URL (content-check, not just HTTP 200).
- Honest-by-construction — report the null; human-gate anything outward/irreversible; scaffolds raise
  rather than fabricate.
- `make check` must exercise write-paths (not only `--check`); tests must not mutate tracked files;
  serve `site/` from inside `site/`.
- lychee: accept `[200,202,206,403,405,406,415,429]` + exclude slow/timeout hosts.

**Done =** `make check` green (validate + tests + self-audit + drift), CI + Pages green, every claim
backed by a committed artifact, one clear next turn. Then post the honest launch note.
