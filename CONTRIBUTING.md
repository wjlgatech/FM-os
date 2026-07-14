# Contributing to FM-os

FM-os is **data-driven**: the `README.md` is *generated* from the `data/*.yml` files by
`scripts/build_readme.py`. You never edit the README — you edit a data file, and CI
regenerates + drift-checks it. Adding a resource is a two-line PR.

## Add a resource (the whole flow)

1. **Find the right file** in `data/`:
   - `repos.yml` — open-source repos (`category:` models / frameworks / finetuning / rl / eval / serving / compression)
   - `courses.yml` — courses (`topic:` foundations / pretraining / posttraining / finetuning / rl / agents)
   - `papers.yml` — papers (`topic:` slm / pretraining / scaling / posttraining / rl / peft / distillation / compression)
   - `jobs.yml` — job sources & boards (`type:` company / board / aggregator / newsletter)
2. **Append your entry** in the shape shown below.
3. **Regenerate + check locally:**
   ```bash
   make check     # validates the data, rebuilds the README, and drift-gates it
   ```
4. **Open a PR.** CI runs the same `make check` plus a link-check.

## The one rule

**Every entry needs a working `url`.** A weekly Action re-verifies links and refreshes repo
stats, so please double-check the URL resolves before you submit.

## Entry shapes

```yaml
# data/repos.yml
- name: SmolLM2
  repo: huggingface/smollm         # owner/name — enables automatic ★ star-sync
  url: https://github.com/huggingface/smollm
  category: models                 # models|frameworks|finetuning|rl|eval|serving|compression
  slm: true                        # true if directly Small-Language-Model relevant (adds the 🤏 marker)
  blurb: "One tight, non-hypey sentence on why it matters."
```

```yaml
# data/papers.yml
- title: "..."
  authors: "Lastname et al."
  org: "..."
  year: 2024
  venue: "arXiv:2402.03300"        # or a conference
  url: https://arxiv.org/abs/2402.03300
  topic: rl                        # slm|pretraining|scaling|posttraining|rl|peft|distillation|compression
  blurb: "One concrete sentence."
```

See existing entries in each file for `courses.yml` and `jobs.yml` shapes.

## What belongs here

FM-os is **SLM-first**. General foundation-model ops resources are welcome, but the bar is:
*does it help someone build, train, tune, evaluate, or ship a small/efficient model?* Prefer
primary sources (official repos, arXiv, university course pages). No dead links, no marketing pages.

## Style

- Blurbs are one sentence, concrete, non-hypey. Start with a capital; no trailing period is fine
  (be consistent within a file).
- Don't add a `stars:` field by hand — it's generated into `data/_stars.yml`.
- Don't edit `README.md` or `data/_stars.yml` — both are generated.
