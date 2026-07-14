# FM-os Growth Playbook

Reverse-engineered from the top awesome-list / knowledge-hub repos
(`sindresorhus/awesome`, `Hannibal046/Awesome-LLM`, `mlabonne/llm-course`,
`ml-tooling/best-of-ml-python`, `f/awesome-chatgpt-prompts`) and the
[awesome.re](https://awesome.re) guidelines. This is the marketing spine — the
"why FM-os can reach top-3" plan.

## The 12 tactics (ranked) and where each lives

| # | Tactic | Status in this repo |
|---|--------|---------------------|
| 1 | Killer one-liner hook above the fold | ✅ `meta.yml → tagline` |
| 2 | "Updated weekly" freshness promise + auto-update Action | ✅ `sync.yml` + Weekly-Sync badge |
| 3 | Single-file, low-friction contribution (edit YAML → PR) | ✅ `data/*.yml` + CONTRIBUTING.md |
| 4 | Awesome.re badge + get listed on parent lists | ✅ badge; ⏳ submit upstream after 30 days |
| 5 | Trust badge row (stars, contributors, last-commit, license) | ✅ generated header |
| 6 | TOC + "back to top" links | ✅ generated |
| 7 | Quality/relevance legend (the 🤏 SLM marker) | ✅ Start Here |
| 8 | Star-history chart | ✅ generated footer |
| 9 | Keyword-rich description + 15-20 topics | ✅ `meta.yml → description/topics` |
| 10 | Comparison tables for flagship sections | ⏳ v0.2 (models table: params/license/context/on-device) |
| 11 | Contribution funnel (issue template, good-first-issue) | ✅ issue + PR templates; ⏳ label issues |
| 12 | Section icons + roadmap graphic | ✅ emoji icons; ⏳ banner + roadmap SVG |

## Repo description (set in GitHub "About")

> 🛠️ FM-os: the living, SLM-first map of foundation-model operations — pre-training,
> post-training, fine-tuning & RL. Curated repos, courses, papers & jobs, auto-refreshed weekly.

Topics: see `data/meta.yml → topics` (kept in sync with the About section).

## 6-step launch / promotion sequence

1. **Pre-launch polish (Day −3→0).** README with all tactics live, ≥60 quality entries (done:
   ~90), CC0 license, CONTRIBUTING, auto-sync Action live. Seed a handful of stars from your
   network so it's not at 0.
2. **Reddit soft launch (Day 1).** r/LocalLLaMA (exact SLM/on-device audience — highest ROI) +
   r/MachineLearning. Angle: *"I built a curated, weekly-updated map of the Small Language Model
   ops stack."* Value-first post, link in a comment, reply to everyone.
3. **Show HN (Day 2, Tue–Thu ~8am ET).** `Show HN: FM-os – a curated, auto-refreshed hub for
   Small Language Model operations`. Lead with the automation angle (HN loves it).
4. **X + LinkedIn thread (Day 2–3, love12xfuture brand).** *"SLMs are eating LLMs' lunch for 80%
   of tasks. I mapped the whole SLM ops stack in one repo 🧵."* Tag the toolmakers you list; end
   each post with the star CTA + a star-history screenshot.
5. **Ecosystem backlinks (Day 3–7).** PR the awesome badge into `Awesome-LLM`, `best-of-ml-python`,
   `awesome-mlops`, `awesome-local-llm`. Submit to TLDR AI, Ben's Bites, The Batch.
6. **Sustain the flywheel (Week 2+).** The Monday sync PR = a fresh commit every week → repost a
   "SLM Ops weekly: N new resources" micro-thread. After 30 days, submit to `sindresorhus/awesome`
   for the permanent authority backlink. Add a "featured in" section as citations arrive.

## awesome.re compliance notes (for the upstream submission later)

- Repo slug lowercase; if dual-branding, an `awesome-slm` alias helps discovery.
- Section named exactly `Contents`, ≤1 nesting level, entries `[Name](url) - Description.`
- CC0 license (✅) + `contributing` file (✅). Wait 30 days before submitting upstream.
