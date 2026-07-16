# Transfer Prompt — money-os, zero-edit

*Open a fresh session on `wjlgatech/money-os` and paste everything from the `/anyagent` line down.*

---

/anyagent

**Harden `money-os` into an AI-native, self-verifying compounding flywheel** — port the machinery I
proved in `github.com/wjlgatech/FM-os` and `github.com/wjlgatech/longevity-loop`. Reverse-engineer their
`data/*.yml` + `scripts/` FIRST (spec-as-data generator + drift gate, rubric-as-data certifier with a
security gate, AI-native self-audit, weekly tracker, Pages dashboard); reuse the machinery, adapt to
money-os's domain: **a zero-trust, local-only AI financial co-pilot — 17 skills for wealth building.**
Goal-10x loop; small green committed increments; verify at the artifact; honest ❌ over fake ✅.

money-os's whole promise is **zero-trust, local-only, evidence-backed money moves** — which is exactly
what a rubric-as-data certifier can *enforce* instead of merely claim. Do these three first, in order:

**1. Spec-as-data + drift gate for the 17-skill catalog + content.**
Move the skills inventory and content into `data/*.yml` (`skills.yml` — name, what it does, trigger,
risk-tier, data-touched; `meta.yml` — branding/sections). `scripts/build.py` GENERATES the README + any
site from them; `validate.py` checks required fields + URLs. `make check` = validate + `build --check`
(drift gate) in CI. Adding/auditing a skill becomes a two-line, drift-gated PR.

**2. Money-OS-Certified — a rubric-as-data certifier that ENFORCES the zero-trust + evidence promise
(the highest-leverage fit).**
`data/certify.yml` + `scripts/certify.py --target <skill-dir> --gate N`, scoring each finance skill on:
- **Zero-trust / local-only** (BLOCKING) — scan for any network exfil, data upload, hardcoded
  keys/tokens, or telemetry. money-os says "your data stays local" — make that a gate a skill must pass.
- **Human-gated money moves** (BLOCKING) — any skill that could move money / place a trade / make an
  irreversible financial action must require an explicit human confirm; auto-execute ⇒ fail.
- **Evidence-backed claims** — no return/savings claim without a reproducible backtest or a cited source
  (**no evidence ⇒ No**; a "$898/yr saved" number needs a shown calculation, not a vibe).
- **provenance** (hash + author), **docs/trigger**, **cross-runtime** (Claude/Cowork).
maker≠checker; exit non-zero → CI gate; emit a shields "Money-OS Certified" badge + a self-cert composite
action. Dogfood on the 17 skills (incl. the OpenD/trading ones — those most need the money-move gate).

**3. AI-native self-audit + a "financial-readiness coverage" engine + tracker + cross-link.**
`data/ainative.yml` + `scripts/ainative.py --gate 85` in `make check`. Then a JD-fit-style coverage
engine retargeted to money: `data/coverage.yml` mapping a user's situation/goal ("retirement? debt?
HYSA? employer match?") → which of the 17 skills + resources cover it → a 0-100 "money-health coverage"
report with gaps (the same taxonomy-as-data pattern as FM-os JD-fit). Optional weekly `track.py` for the
market-data/skill ecosystem (GitHub API; if it uses moomoo/OpenD, keep those calls local-only + gated).
Cross-link FM-os (the method) + longevity-loop (a sibling application) at the top.

**Non-negotiable discipline (bake into `make check` + CI):** verified only (URL-verify, never invent,
content-check not just HTTP 200); **finance honesty — no evidence ⇒ No claim, human-gate every
money-moving/irreversible action, never present a projected return as realized**; `make check` exercises
write-paths; tests don't mutate tracked files; serve `site/` from inside `site/`; lychee accept
`[200,202,206,403,405,406,415,429]` + exclude slow hosts.

**Done =** `make check` green (validate + tests + self-audit + drift), CI + Pages green, the zero-trust +
human-gate gates enforced on all 17 skills, one clear next turn.
