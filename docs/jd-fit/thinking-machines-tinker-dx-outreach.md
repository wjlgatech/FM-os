# Tinker DX campaign — high-impact outreach (drafted, never sent)

Discipline (playbook stage 7): **collaborator/co-founder caliber only** — no cold "hire me"
notes, no student/employee framing. Every touch **gives before it asks** (a working artifact,
a measured result, a PR). All messages below are DRAFTS behind the human gate: Paul reviews,
re-verifies each person's current role/handle, personalizes, and sends manually.
Log every send + response in the dossier's `## Outcome log`.

## Tier A — Tinker's own gravity (community engagement, relationship ≠ application)

The JD's team reads its own repo. The highest-signal outreach is a **good PR**.

| Who | Why them | The give | The ask |
|---|---|---|---|
| tinker-cookbook maintainers (GitHub) | The team this role joins; the repo the role maintains | `tinker-gates` recipe PR or issue-with-prototype: ship/rollback gates around a cookbook SFT recipe, keyless CI mode via the numpy shim | Feedback + whether a community-project submission is welcome |
| John Schulman (TML co-founder/chief scientist; drives Tinker + cookbook) | Wrote the book on the algorithms the cookbook teaches | Nothing direct — engagement happens through the PR above and the community-projects channel; name only appears if he responds there | none (no cold DM) |

## Tier B — post-training OSS peers (collaborator caliber; verify current roles before sending)

| Who | Why them | The give | The ask |
|---|---|---|---|
| Lewis Tunstall (Hugging Face, TRL / smol-course) | Owns the OSS fine-tuning DX benchmark FM-os curates against | The forgetting-gate pattern (tinker-loop G2) as a TRL example or smol-course aside; measured naive-vs-replay numbers | Would a "gated recipe" pattern fit TRL docs? Co-author? |
| Nathan Lambert (AI2 post-training; RLHF book, Interconnects) | The field's honest-eval conscience; writes about exactly this failure class | The honest-rollback case study (rewardforge + tinker-loop): a gate that rolled back its own maker, with numbers | Is "ship/rollback gates for post-training" worth a deeper joint write-up? |
| Benjamin Anderson (wrote "Anatomy of a Modern Finetuning API") | Independently mapped the same API-primitive territory | tinker-loop as the runnable companion to his essay | Compare notes; cross-link if he finds it faithful |

## Tier C — co-founder pipeline (for Paul's ventures, not for TML)

Profile spec, not names (names surface from the channels below and get re-verified):
**builds in public on post-training/eval infra · has shipped an OSS tool with real users ·
domain distribution (enterprise, bio, robotics) Paul lacks · allergic to vibes-based evals.**
Sourcing channels: Tinker community-project authors (TML features them on its channels),
tinker-cookbook contributor graph, early-adopter groups (Princeton PLI, Stanford, Berkeley,
Redwood Research), authors of eval-gate-adjacent tools in `data/repos.yml`.
Qualification gate: one 30-min working session building on a shared artifact — a person who
won't co-build a small thing won't co-found a big one.

## Draft 1 — cookbook issue/PR opener (Tier A)

> **Title:** Recipe proposal: ship/rollback gates for fine-tuning runs (keyless CI mode included)
>
> Every fine-tuning run answers "did it get better?" — few recipes answer "should this ship?"
> I've been running post-training behind held-out gates (domain gain, catastrophic-forgetting
> cap, preference-margin flip) with honest rollback: in my LoRA-DPO lab the same gate that
> shipped the good run rolled back my own bad-lr attempt (held-out hallucination 0.398→0.287
> on the run that passed).
>
> Two artifacts, both runnable now:
> 1. A gated-recipe pattern that wraps any Tinker training loop (prototype: [link]).
> 2. A keyless numpy implementation of the four primitives so the recipe runs in CI without
>    credits — the naive recipe gets caught (+208% forgetting), the replay recipe ships: [link].
>
> Happy to shape either into a cookbook recipe or a community-project submission if the
> pattern is welcome. What would maintainers want changed first?

## Draft 2 — peer note (Tier B, e.g. Nathan Lambert; personalize per target)

> Your writing on evaluation honesty is the closest thing my work has to a citation trail, so
> a data point you might enjoy: I've been enforcing "no evidence ⇒ no ship" on my own
> post-training runs, and the gate's best moment was rolling back *me* — a bad-lr DPO attempt
> died at the held-out gate while the fixed run shipped (0.398→0.287 hallucination, zero human
> labels). I've since distilled the pattern into a keyless demo of Tinker-style primitives
> where the classic domain-only SFT mistake is caught by a forgetting gate (+208%) and the
> replay fix ships. Repo: [link]. If "ship/rollback gates as first-class post-training
> citizens" is a thread worth pulling, I'd genuinely enjoy comparing notes — and there's a
> concrete joint write-up in it if the data holds up under your skepticism.

## Send checklist (human gate)

- [ ] Re-verify person's current role, handle, and preferred channel (roles above are as-known 2026-07; people move)
- [ ] `make check` green and links live before anything ships
- [ ] Personalize the give to their latest public work (read it first)
- [ ] Log send + any response in the dossier `## Outcome log` within 48h
