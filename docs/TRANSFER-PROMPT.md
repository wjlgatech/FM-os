# Transfer Prompt — apply the compounding-flywheel method to any repo

*Carry this into a fresh session opened on the target repo (e.g. `wjlgatech/rsi`). It ports the
patterns proven in [FM-os](https://github.com/wjlgatech/FM-os) + [longevity-loop](https://github.com/wjlgatech/longevity-loop).
Paste from the line below.*

---

/anyagent

**Turn this repo into an AI-native, self-verifying, build-in-public compounding flywheel** — the same
architecture I proved in `github.com/wjlgatech/FM-os` and `github.com/wjlgatech/longevity-loop`.
Reverse-engineer those two repos' `data/*.yml` + `scripts/` first; reuse the pattern, don't reinvent.
Adapt every piece to THIS repo's domain (read its README to learn the domain). Work in the goal-10x
loop; ship in small, green, committed increments; verify at the artifact (browser/curl/CI), never vibe.

**Build these, in order — each data-driven and gated:**

1. **Spec-as-data + generated artifact + drift gate.** Move the repo's content into `data/*.yml` as the
   single source of truth; write `scripts/build.py` to GENERATE the README (and any site) from it;
   `make check` runs a drift gate (`build --check` fails if committed output ≠ generated). Never
   hand-edit generated files.
2. **A rubric-as-data ClosedLoop for this repo's core judgment.** Pick the standard this domain cares
   about (quality? readiness? certification? trust?) and encode it as `data/<rubric>.yml`; a
   `scripts/*.py` scorer gathers EVIDENCE (a file exists / a regex matches / an API returns), scores it,
   and exits non-zero below a threshold. Discipline: **no evidence ⇒ No** (unmeasured is excluded, never
   a fake pass); **maker ≠ checker** (the thing graded isn't the grader); a blocking gate can't pass on
   unmeasured items. (See FM-os `certify.py`/`certify.yml`, `jdfit.py`/`jd_taxonomy.yml`, `ainative.yml`.)
3. **An AI-native self-audit**, gated in CI. `data/ainative.yml` = the operating principles (loop-not-
   oneshot · independent-referee · no-evidence⇒No · regression-gated · spec-as-data · agent-native-harness ·
   iteration-recorded · compounding-memory · human-gated-irreversible · verify-live), each with real
   in-repo evidence; `scripts/ainative.py --gate 85` in `make check`. So a regression in HOW you operate
   also fails the build.
4. **A refreshable "living" pipeline.** A weekly GitHub Action (`sync`/`track`) that pulls live signal
   from OPEN APIs (GitHub, arXiv — NOT scrapers), regenerates, and opens a PR with "what moved." Degrade
   gracefully (rate-limit/429-safe; record "none found", never fabricate).
5. **A "compounding" surface + build-in-public.** A GitHub Pages dashboard generated from the same
   `data.json`; a Turns/Changelog ledger where `done` REQUIRES evidence (a PROOF); an Anthropic-brand
   infographic of the flywheel (brand-as-code); shields badges.
6. **A readiness/coverage engine** (the JD-fit pattern) if the domain has "am I ready / does this cover
   X" questions: a taxonomy-as-data that maps a pasted query → coverage over the repo's knowledge/tooling
   → a 0-100 report with gaps.
7. **A field graph** (optional, if there are people/orgs/topics evolving over time): a spatiotemporal
   knowledge graph (`build_graph.py` → `graph.json` + a force-graph page), modeled after
   `getzep/graphiti` (bi-temporal; edges carry `since`).

**Non-negotiable discipline (bake into `make check` + CI):**
- Verified research only: fan out parallel agents for REAL, URL-verified entries; dedup; flag
  dead/uncertain; **never invent a URL** (content-check, don't trust HTTP 200).
- Honest-by-construction: scaffolds that can't fabricate (raise on missing data); report the null;
  human-gate outward/irreversible actions (publish, posting) — draft, the human ships.
- Tests must not mutate tracked files; `make check` must exercise WRITE paths (write-path bugs hide
  behind read-only `--check`); serve a `site/` dir from inside `site/`.
- Link-check config: accept bot-unfriendly codes `[200,202,206,403,405,406,415,429]` and exclude
  slow/timeout hosts — don't let false-negative link checks block CI.

**Definition of done:** `make check` green (validate + tests + self-audit + drift), CI + Pages green,
every claim backed by a committed artifact, and one clear "next turn." Report status honestly (an
honest ❌ beats a fake ✅). Then cross-link this repo with FM-os + longevity-loop as siblings.
