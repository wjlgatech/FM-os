# FM-os Launch Copy

Ready-to-post copy for the 6-step sequence in [GROWTH.md](GROWTH.md). Post value-first,
put the link in a comment where the subreddit norm expects it, and reply to everyone in
the first 2 hours.

> **Before posting:** seed 5-10 stars from your own network so it's not sitting at 0, and
> make sure `make check` is green on `main`. Don't claim traction FM-os doesn't have yet —
> the hook is the *usefulness*, not the star count.

---

## 1. r/LocalLLaMA (Day 1 — highest ROI, your exact audience)

**Title:**
`I mapped the whole Small Language Model ops stack into one auto-updating repo (SLM-first, not another everything-list)`

**Body:**
> I kept re-finding the same scattered links every time I wanted to train, fine-tune, quantize, or serve a small model — so I built **FM-os**, a curated map of the *Small Language Model* stack, organized by what you're actually trying to do: pre-train → post-train → fine-tune → RL → serve on-device.
>
> What's in it right now:
> - **35 repos** (SmolLM, Phi, Gemma, Qwen, nanoGPT, Unsloth, TRL/verl for GRPO, llama.cpp, BitNet…) with a 🤏 marker for the ones that are directly SLM-relevant
> - **35 papers** filed by lifecycle stage — SLM surveys, Chinchilla, DPO, GRPO/DeepSeek-R1, LoRA/QLoRA, distillation & quantization
> - **17 free courses** (Stanford CS336, Karpathy, HF, DeepLearning.AI post-training/GRPO)
> - job sources for people trying to break into pre/post-training/RL work
>
> Two things I did differently:
> 1. **It stays fresh automatically** — a weekly GitHub Action re-pulls every repo's stars/latest release, link-checks, and opens a PR. No stale awesome-list rot.
> 2. **It's data-driven** — every entry is a couple of lines of YAML, the README is generated. Adding a resource is a 2-line PR, no formatting fights.
>
> It's CC0. I'd love corrections and additions — especially SLM training/quantization repos I've missed. What's the one SLM resource you always end up re-searching for?

*(link in first comment): https://github.com/wjlgatech/FM-os*

---

## 2. Hacker News — Show HN (Day 2, Tue–Thu ~8:00am ET)

**Title:**
`Show HN: FM-os – a curated, auto-refreshed hub for Small Language Model operations`

**Text:**
> I built FM-os to stop re-searching the same links for training, fine-tuning, and deploying small language models. It's SLM-first and organized by the real pipeline (pre-train → post-train → fine-tune → RL → serve).
>
> The part HN might find interesting is the engineering: the README is a *build artifact*. Every entry lives in `data/*.yml`; `scripts/build_readme.py` renders the README; CI drift-gates the two so they can never disagree. A weekly Action refreshes live repo stats and opens a PR, so the list doesn't rot. It's ~$0 to run — no server.
>
> CC0. Corrections and PRs very welcome. https://github.com/wjlgatech/FM-os

*(HN rewards the automation/architecture angle — lead with it, keep it plain, no hype.)*

---

## 3. LinkedIn + X thread (Day 2–3, `love12xfuture` brand)

**Hook post:**
> Small Language Models are quietly eating the LLM's lunch for ~80% of real tasks — cheaper, faster, private, on-device.
>
> But the knowledge is scattered across 50 repos, arXiv, and course pages.
>
> So I mapped the entire SLM ops stack into one open, auto-updating hub. 🧵

**Thread:**
> 2/ The lens: don't collect *everything* — organize by what you're doing. Pre-train → post-train → fine-tune → RL → serve. Every repo, paper, and course is filed under a stage.
>
> 3/ Start-here path is built for a beginner with one GPU: train a tiny model (nanoGPT), fine-tune it (Unsloth/LoRA), align it (DPO), try an RL loop (GRPO via TRL/verl), quantize it (llama.cpp/AWQ), ship it (Ollama/MLC).
>
> 4/ It stays fresh by itself. A weekly GitHub Action re-checks every repo's stars + latest release, verifies links, and opens a PR. An awesome-list that doesn't rot.
>
> 5/ It's fully open (CC0) and data-driven — adding a resource is a 2-line YAML PR. Built it as a sibling to my rsi and FDE-os projects.
>
> 6/ If you build with small models — or want to — this is your map. Star it, and tell me the one resource I'm missing. 👇
> https://github.com/wjlgatech/FM-os

*(Tag the toolmakers you list — HF, Unsloth, Ollama — they often reshare. Attach a star-history screenshot once it starts moving.)*

---

## 4. Ecosystem backlinks (Day 3–7)

- PR the awesome badge / a one-line entry into: `Hannibal046/Awesome-LLM`, `ml-tooling/best-of-ml-python`, `kelvins/awesome-mlops`, any `awesome-local-llm`.
- Submit to newsletters: **TLDR AI**, **Ben's Bites**, **The Batch**, **Ahead of AI** (tip form / reply).
- Post in r/MachineLearning's "What are you reading/using" weekly thread.

## 5. Sustain (Week 2+)

Every Monday the sync PR merges → a fresh commit. Turn that into a recurring micro-post:
`SLM Ops weekly: N resources added, biggest mover this week was <repo> (+X★)`. After **30 days**,
submit to `sindresorhus/awesome` for the permanent authority backlink (see awesome.re notes in GROWTH.md).
