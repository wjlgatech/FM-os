# Transfer Prompt — animate-anything, zero-edit

*Open a fresh session on `wjlgatech/animate-anything` and paste everything from the `/anyagent` line down.*

---

/anyagent

**Harden `animate-anything` into an AI-native, self-verifying compounding flywheel** — port the machinery
I proved in `github.com/wjlgatech/FM-os` and `github.com/wjlgatech/longevity-loop`. Reverse-engineer their
`data/*.yml` + `scripts/` FIRST (spec-as-data generator + drift gate, rubric-as-data certifier, AI-native
self-audit, weekly tracker, field graph). Domain: **the ranked, living map of animation tooling — CSS →
AI-authored video — made machine-readable for agents (graph + llms.txt) and kept fresh.** Goal-10x loop;
small green committed increments; verify at the artifact; honest ❌ over fake ✅.

animate-anything already *is* this shape — a ranked living map + a machine-readable graph + `llms.txt`,
promising freshness. So the job is to make those claims **enforced, not asserted**. Assess what's already
there before adding; do these three in order:

**1. Spec-as-data + drift gate (make "ranked / living / machine-readable" enforced).**
Ensure the README, the machine-readable graph, AND `llms.txt` are all GENERATED from one `data/*.yml`
source of truth by `scripts/build.py` (if they're hand-maintained today, invert that). `make check` =
`validate.py` (required fields + working URLs) + `build --check` (drift gate) in CI, so the three
representations can never disagree. Then the weekly freshness is real: a `track.py` on the GitHub API
refreshing stars/latest-release/last-commit for every listed animation-tool repo → a weekly PR.

**2. Animate-Certified — a rubric-as-data certifier that makes "ranked" evidence-based.**
`data/certify.yml` + `scripts/certify.py --target <tool> --gate N` scoring each animation tool/skill on
evidence: **agent-usability** (does it ship an `llms.txt` / machine-readable API a coding agent can drive
headlessly?), **reproducibility** (does the example actually render output?), **license** (safe to use in
generated video?), **provenance** (hash + source), **docs/trigger**, **freshness**. no evidence ⇒ No;
maker≠checker; exit non-zero → CI gate; emit a shields badge + a self-cert composite action. This turns a
subjective "ranked list" into a defensible, gated ranking.

**3. AI-native self-audit + an agent-readiness engine + a spatiotemporal graph + cross-link.**
`data/ainative.yml` + `scripts/ainative.py --gate 85` in `make check`. Then the killer feature for a
"hand-it-to-your-agent" hub: a coverage engine (FM-os JD-fit pattern) — paste an animation brief ("author
a 30s explainer from CSS/SVG → video") → which listed tools + skills cover each step → a 0-100
agent-readiness report with gaps. Upgrade the existing machine-readable graph to a **bi-temporal** one
(`build_graph.py` → `graph.json` + force-graph page, modeled after `getzep/graphiti`; edges carry `since`)
so trends over time show. Cross-link FM-os (the method) + longevity-loop (a sibling application) at the top.

**Non-negotiable discipline (bake into `make check` + CI):** verified only (URL-verify, never invent,
content-check not just HTTP 200); honest-by-construction (report the null; human-gate outward/irreversible
actions; scaffolds raise rather than fabricate); `make check` exercises write-paths; tests don't mutate
tracked files; serve `site/` from inside `site/`; lychee accept `[200,202,206,403,405,406,415,429]` +
exclude slow hosts.

**Done =** `make check` green (validate + tests + self-audit + drift), CI + Pages green, the README + graph
+ llms.txt all generated + drift-gated from one source, one clear next turn.
