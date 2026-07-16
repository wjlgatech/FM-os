# Transfer Prompt — FDE-os, zero-edit

*Open a fresh session on `wjlgatech/FDE-os` and paste everything from the `/anyagent` line down.*

---

/anyagent

**Harden `FDE-os` into an AI-native, self-verifying compounding flywheel** — port the machinery I proved
in `github.com/wjlgatech/FM-os` and `github.com/wjlgatech/longevity-loop`. Reverse-engineer their
`data/*.yml` + `scripts/` FIRST (spec-as-data generator + drift gate, rubric-as-data certifier,
AI-native self-audit, JD-fit engine, weekly tracker); reuse the machinery, adapt to FDE-os's domain:
**becoming/operating as a Forward Deployed Engineer — shipping production agentic systems inside the
customer's environment.** Goal-10x loop; small green committed increments; verify at the artifact; honest ❌ over fake ✅.

FDE-os is already strong — it has the three doors (Course / Toolkit / Community), a live agentic webapp,
a Claude Code plugin, cross-runtime skills, and a field-practice feedback flywheel. The gap is that its
content and claims aren't yet **enforced as a self-verifying loop**. Do these three first, in order:

**1. Spec-as-data + drift gate across the three doors.**
Move the course curriculum, the toolkit (skills/plugin/workflow inventory), and the community/field-notes
into `data/*.yml` (`course.yml`, `toolkit.yml`, `skills.yml`, `fieldnotes.yml`, `meta.yml`). Write
`scripts/build.py` to GENERATE the README + the three-door pages from them, and `validate.py` (required
fields + working URLs). `make check` = validate + `build --check` (drift gate) in CI. Now the site can't
drift from the source, and adding a lesson/skill is a two-line PR.

**2. FDE-Certified — a rubric-as-data certifier for the toolkit's skills (its natural trust layer).**
`data/certify.yml` + `scripts/certify.py --target <skill-dir> --gate N`, scoring each FDE skill on
evidence: **security** (untrusted-code scan — an FDE skill runs in a customer env; block `curl|bash`,
secret exfil, unscoped shell), **docs/trigger**, **cross-runtime** (Claude/Codex/Hermes — FDE-os's core
promise), **eval/verification** (does it ship a check?), **provenance** (hash + author). no evidence ⇒
No; maker≠checker; exit non-zero → CI gate; emit a shields badge + a self-cert composite action. Dogfood
on FDE-os's own ten skills. (This is the exact pattern behind FM-os Certified.)

**3. AI-native self-audit + JD-fit (make "JD-validated course" executable) + tracker + cross-link.**
`data/ainative.yml` + `scripts/ainative.py --gate 85` in `make check`. Then the killer FDE-os feature:
turn its *"given a JD, does this course train the person to land it?"* claim into a real engine —
`scripts/jdfit.py` + `data/jd_taxonomy.yml` mapping a pasted FDE job description → coverage over the
course modules + certified skills → a 0-100 readiness report with gaps (exactly FM-os's JD-fit, retargeted
to FDE competencies: agent frameworks, deployment, evals, customer-env ops, MCP/tooling). Add a weekly
`track.py` (GitHub API) refreshing the agentic-engineering frontier the toolkit tracks. Cross-link FM-os
(SLM/FM-ops method) + longevity-loop (a sibling application) at the top.

**Non-negotiable discipline (bake into `make check` + CI):** verified research only (URL-verify, never
invent, content-check not just HTTP 200); honest-by-construction (report the null; human-gate outward/
irreversible actions; scaffolds raise rather than fabricate); `make check` exercises write-paths; tests
don't mutate tracked files; serve `site/` from inside `site/`; lychee accept
`[200,202,206,403,405,406,415,429]` + exclude slow hosts.

**Done =** `make check` green (validate + tests + self-audit + drift), CI + Pages green, every claim backed
by a committed artifact, one clear next turn.
