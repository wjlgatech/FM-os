# Thinking Machines Lab — Research Engineer, Developer Experience, Tinker

Campaign dossier · JD: [`_thinking-machines-tinker-dx.jd.txt`](_thinking-machines-tinker-dx.jd.txt) ·
[Greenhouse posting](https://job-boards.greenhouse.io/thinkingmachines/jobs/5202369008) ·
$350–475k · SF · run under [`docs/PLAYBOOK-jobapp-flywheel.md`](../PLAYBOOK-jobapp-flywheel.md)

## Honest scoring trajectory (the false-100 trap, again)

The unextended taxonomy scored this JD **100/100 over 7 caps** — false comfort: it was blind
to the four capabilities the role is actually about. Extending `data/jd_taxonomy.yml` with
`dev_experience`, `technical_writing`, `oss_library`, `finetune_service_api` dropped the honest
score to **82/100 (4 partial)**. Building [`skills/tinker-loop`](../../skills/tinker-loop/SKILL.md)
(certified **98/100**) + curating the Tinker Cookbook into `data/repos.yml` closed all four:

**Final: 100/100 over 11 capabilities** — regenerate with
`make jdfit JD=docs/jd-fit/_thinking-machines-tinker-dx.jd.txt`.

| Capability | Coverage | Tooling highlight |
|---|:--:|---|
| Training / fine-tuning FMs | ✅ | slm-quickstart 94, vlm-quickstart 94, tinker-loop 98 |
| Post-training / RL / alignment | ✅ | product-rl-loop 98, continual-rl-eval 98, tinker-loop 98 |
| Agentic evaluation / benchmarking | ✅ | agentic-eval 94, vlm-failure-probe 98, syndata-bare 98 |
| Developer experience / API ergonomics / onboarding | ✅ | **tinker-loop 98** (new) |
| Code examples / tutorials / cookbook recipes | ✅ | **tinker-loop 98** (new) |
| OSS library development & community | ✅ | **tinker-loop 98** (new) |
| Fine-tuning-service API primitives | ✅ | **tinker-loop 98** (new) |
| Python/PyTorch · GPU/inference · distributed · publishing | ✅ | knowledge base |

## What was built this campaign

- **`skills/tinker-loop`** — the Tinker mental model (forward_backward / optim_step / sample /
  save_state + LoRA on a frozen base) in pure numpy, keyless, <2 s. Composes SFT **and** DPO
  from the four primitives; three held-out gates (domain gain ≥15%, forgetting ≤10%,
  preference-margin flip). The demo ships the honest story: naive domain-only SFT is
  **ROLLED BACK** (+208% forgetting caught by G2), replay-mixing **SHIPs** (+29.1% domain gain,
  −11.9% generic). 7/7 tests green. Certified 98/100.
- **Knowledge**: Tinker Cookbook (Apache-2.0) curated into `data/repos.yml`; +4 taxonomy caps.
- **Resume**: `~/Downloads/Paul Jialiang Wu — Resume — Thinking Machines Tinker DX.md` + print
  `.html` — every claim traces to repo artifacts or the base resume; nothing invented.
- **Playbook**: this campaign is the first run of
  [`PLAYBOOK-jobapp-flywheel.md`](../PLAYBOOK-jobapp-flywheel.md) (stages 0–8).

## Reverse-engineering ruling

**Do not reverse-engineer the Tinker service — there is a sanctioned lane that's strictly better.**

- The moat is the **managed distributed-training infrastructure and hosted open-weights pool**
  (LoRA multiplexing across a shared compute pool). None of that is observable from the client
  side, and probing a beta service's internals would violate ToS and poison the relationship
  with the exact team being applied to.
- Everything worth learning is **already public by design**: the API surface is documented, the
  [tinker-cookbook](https://github.com/thinking-machines-lab/tinker-cookbook) is Apache-2.0, and
  the company runs an official
  [Call for Community Projects](https://thinkingmachines.ai/news/call-for-community-projects/)
  that explicitly invites *"high-level libraries built on top of Tinker"* and product prototypes.
- Contrast with the NomadicML campaign (`labs/nomadicml`): there, clean-room reconstruction was
  the only way to demonstrate product understanding. Here, building **on** the product through
  the official channel demonstrates more, costs less, and is visible to the hiring team.

## High-ROI projects (ranked; named competitors + kill criteria per rc0011 discipline)

1. **`tinker-gates` — ship/rollback gates for Tinker recipes** (community-project submission).
   A thin library + cookbook recipe wrapping any Tinker training loop in FM-os discipline:
   held-out judge gate, catastrophic-forgetting gate, reward-hack probe, honest ship/rollback —
   `rewardforge` + `product-rl-loop` generalized onto the real API. *PMF:* their call asks for
   exactly this class of library; every Tinker user burns GPU credit on runs a gate would have
   rolled back. *Builder-product fit:* gates are the through-line of the entire portfolio.
   *Competitors:* inspect-ai / lm-evaluation-harness integrations (eval only — none do gated
   ship/rollback around the training loop). *Kill criteria:* cookbook already ships equivalent
   gate discipline on inspection of its eval recipes, or the PR/submission draws zero maintainer
   engagement in 30 days.
2. **`tinker-local` — a keyless mock backend for the Tinker client** (grow `tinker-loop`'s
   reference into a pip-installable drop-in, like `moto` is to AWS). Lets any cookbook recipe
   run in CI with zero keys/GPU — the single biggest DX gap of any credit-metered training API.
   *Competitors:* none known for Tinker (verify at build time); nearest analogue is vLLM's mock
   engines. *Kill criteria:* TML ships an official emulator/dry-run mode, or recipe coverage
   beyond toy scale proves misleading to users.
3. **Article pair** (stage-6 marketing, through /viral-loop's human gate): *"Tinker in 200
   lines of numpy — the mental model behind fine-tuning-service APIs"* and *"The gate that
   caught catastrophic forgetting — post-training recipes need ship/rollback."* Long-form on
   the agentic portfolio first, then 1-click syndication to LinkedIn + X with backlinks.

## Interview prep — 5 stories

1. **The gate that rolled back its maker** — rewardforge attempt 1 (lr 1e-4) collapsed; the
   same held-out gate that shipped attempt 2 (halluc 0.398→0.287) rolled attempt 1 back.
   DX lesson: users trust cookbooks whose failure modes are part of the artifact.
2. **Keyless-by-construction demos** — tinker-loop runs the full SFT+DPO+gates story in CI in
   <2 s with zero keys; that's the onboarding bar a recipe should meet before it asks for credit.
3. **Docs as build artifacts** — FM-os README generated from `data/*.yml` with drift gates;
   docs that can't drift are the only docs that stay true at cookbook scale.
4. **Forward-deployed debugging** — primary technical interface on an enterprise OpenAI
   engagement; the debug-user-pipelines half of this JD is the current day job.
5. **Honest self-scoring** — the jdfit engine extends its own rubric before scoring itself
   (100-false → 82 → 100-earned); the same no-fake-pass discipline Tinker's users need from
   their eval loops.

## Outreach

See [`thinking-machines-tinker-dx-outreach.md`](thinking-machines-tinker-dx-outreach.md) —
collaborator-caliber shortlist, give-before-ask, all messages drafted-never-sent.

## Outcome log

| Date | Event | Notes |
|---|---|---|
| 2026-07-27 | Campaign run: artifacts built, resume ready | Application NOT yet submitted — human gate (Paul) |
