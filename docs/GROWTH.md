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

## Article playbook — earned writing the Happy College draft (2026-07-30)

Lessons from `docs/marketing/happy-college-article-07-30-2026.md` (the reading-club launch
article), now standing rules for every FM-os article:

1. **Fact-check every attribution BEFORE drafting.** The brief said "ADEPT by Richard Freman
   (Nobel Physic Laurate)" — the verified truth is Kalid Azad (BetterExplained), *inspired by*
   Feynman. A wrong Nobel attribution in a viral post is a community-note magnet; the fact-check
   is the first rep, not a polish step. Same gate as resume trackability: curl the source.
2. **No apocryphal quotes.** If the famous quote can't be sourced, paraphrase the idea and
   attribute the *method*, not the sentence.
3. **The shareable unit is a table or a one-liner, not a paragraph.** Design the stealable asset
   first (here: the sports→ML mapping table + "your jump shot is your syllabus"), then write the
   article around it.
4. **Link only what resolves; name the rest.** Private repos (super-u, DreamMakeTrue) are named
   as products, never linked — a 404 in a launch post burns trust at the exact moment you have
   attention.
5. **CTA must land on an owned, verified asset.** Here: the reading-list track. Gap discovered:
   a club needs a signup surface before syndication — build the conversion page BEFORE the post
   goes out, not after.
6. **Route through the human gate.** Drafts live in `docs/marketing/` with a DRAFT banner;
   long-form to the agentic portfolio first, then 1-click prefilled syndication (LinkedIn link
   in first comment; X link as last post). Auto-review rubric ≥4/5 before the gate.
7. **The 5-S reviewer gate (2026-07-30).** Before the human gate, every article is scored by an
   independent reviewer (maker ≠ checker) against the 5-S rubric — Simple (15-yo story + mental
   model) · Solid (survival-test research + verified academic citations) · Sharp (verbatim insider
   quotes, patterns/anti-patterns, mechanism, 1st principle) · SMART (optional) · Surprise
   (belly-laugh beat). All mandatory ≥4/5 or it doesn't ship. Canonical rubric:
   agentic-portfolio `docs/ARTICLE_AUTHORING.md` § "The 5-S reviewer".

## Mailing-list viral growth — the community loop (added 2026-07-30)

Researched against the survival test (what the durable newsletter operations — beehiiv/Kit
operators, Viral Loops' k-factor mechanics, deliverability guides — all converge on), and
wired into the live system at agentic-portfolio (`/api/newsletter`, double opt-in, Postgres
store). Sources: [beehiiv referral guide](https://www.beehiiv.com/blog/newsletter-referral-program),
[Viral Loops newsletter referral](https://viral-loops.com/newsletter-referral),
[Kit newsletter best practices](https://kit.com/resources/blog/email-newsletter-best-practices),
[Maestra opt-in practices](https://maestra.io/blog/q-and-a/opt-in-email-example).

**The loop, in order of leverage:**

1. **Double opt-in is the foundation, not friction.** Confirmed subscribers are real humans
   who chose twice — that engagement signal IS deliverability (inbox providers rank senders
   by engagement; bots and typos poison it). Our implementation: pending → confirmation
   email → confirmed, unsubscribed rows kept as a suppression list forever.
2. **The community address is the brand.** All reader email comes from ONE consistent
   community sender (openheavenclaw@gmail.com), never a personal address — consistent
   from-address builds sender reputation and keeps the personal inbox private. Gmail
   handles SPF/DKIM for its own domain.
3. **The welcome email is the highest-open email you will ever send** (opens 4-10x a normal
   send). Ours delivers the member-edition link immediately — the reward lands while
   attention is peak — and carries the referral ask.
4. **Member link ≠ forwardable file = built-in referral mechanic.** The member edition is
   HMAC-keyed to the subscriber's email ("please don't redistribute — invite friends to
   sign up instead"), which converts sharing impulse into signups instead of leakage.
   This is the k-factor seed: each member is a potential inviter.
5. **Milestone referrals when the list earns it (≥500 confirmed):** give each member a
   referral link + counter, rewards at 3/10/25 referrals (exclusive content beats swag —
   Morning Brew's ratio). k-factor = invites-per-member × conversion; measure it before
   scaling any paid channel.
6. **Every article is a funnel mouth:** the ✉️ Free list / Join free buttons on all 35+
   articles route to `/newsletter?src=<article-slug>` — the `source` field tells us which
   content converts, so writing effort follows measured conversion, not vibes.
7. **List hygiene is growth:** one-click token-gated unsubscribe in every email (CAN-SPAM +
   trust), scrub hard bounces, and never import a list — a bought list destroys the sender
   reputation that steps 1-3 built.
8. **The honest gate applies here too:** never fake counts, never "1,000+ readers" without
   the owner-gated `/api/newsletter` GET showing it. Traction claims follow the same
   no-evidence⇒No rule as everything else.

**Operational contract:** signups → Postgres (`newsletter:subscribers`, owner-gated GET,
rate-limited POST, consent required) · confirmation + welcome from MAIL_FROM via Gmail app
password (`GMAIL_APP_PASSWORD`) · articles carry `?src=` attribution · metrics = confirmed
count, pending→confirmed rate, source breakdown, unsubscribe rate.
