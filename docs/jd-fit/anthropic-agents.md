# Anthropic — Research Engineer, Agents · application dossier

**Apply:** https://job-boards.greenhouse.io/anthropic/jobs/4017544008 (Greenhouse, **no
account required** — the only one of the nine targets that is submittable without an
employer login)
**Fit:** 95/100 over 11 capabilities · **Location:** Remote-friendly (travel) | SF | Seattle | NYC
**Resume:** [`resumes/anthropic-research-engineer-agents.pdf`](resumes/anthropic-research-engineer-agents.pdf)

## Read this first — the four essays are yours to draft

Anthropic publishes [candidate AI guidance](https://www.anthropic.com/candidate-ai-guidance)
(read 2026-08-03). For application questions it says, plainly:

> Please create your first draft yourself, then use Claude to refine it. We want to see your
> real experience, but Claude can polish how you communicate about your work.

So this dossier deliberately contains **no drafted essay prose.** Handing you four polished
answers would break the employer's stated process at the one company most certain to care —
and their guidance names exactly what help *is* invited, with this example prompt:

> "Please review my resume and the job description. Identify the experiences I should
> highlight in my application responses that align most with the job requirements."

That is what everything below is. Write your first drafts from it, then bring them back and
I will refine the wording — which is the sanctioned second step.

## Why this role scores highest of the nine

The JD's own responsibilities, mapped to things you have already shipped:

| Their words | Your artifact | The number |
|---|---|---|
| "Ideate, develop, and **compare the performance of different agent harnesses**" | `loop-engineering-anything` — generate→judge→refactor with maker≠checker enforced fail-closed, plateau detection, regression rollback | 543 tests, live-verified F→A runs |
| "Design and implement **rigorous quantitative benchmarks for large scale agentic tasks**" | `mcp-arena` — 12 tasks × 6 failure-mode categories as data over REAL MCP servers; the tool-call trace is asserted, so "right words, no tool calls" scores zero | ships its own falsifier (EvidenceHallucinator must score 0 in CI) |
| "Assist with **automated evaluation of Claude models and prompts** across the training and product lifecycle" | `vlm-failure-probe` + the grader audit; multi-model eval that decided production model selection at Accenture | 6+ VLMs compared; 3-repeat variance run; ~90% annotation cost cut |
| "Help create and **optimize data mixes for model training**" | `rewardforge` — eval-gate-labeled preference pairs (zero human labels) → DPO from scratch → LoRA | held-out hallucination 0.398→0.287, pre-registered criterion |
| "Work with our **product org** to find solutions" | Primary technical interface on an executive enterprise AI deployment (OpenAI-DSI) | "no surprises" standard |
| bonus: "Large-scale RL on language models" | `product-rl-loop` — reward hacking caught as a measured +1.9 on a worthless feature, then rolled back | certified 98/100 |
| bonus: "Multi-agent systems" | harnesses and independent referees — **honest partial**, not many-agent at scale | see edge below |

## Raw material per essay question — YOUR first draft

### 1. "Why do you want to work at Anthropic?" (200–400 words, they say they value it highly)

**This one has to be yours.** I can map evidence, but your motivation is not mine to invent,
and a reader can tell. Some true things about your own record you may want to draw on —
verify each still feels like *your* reason, not a supplied one:

- Your practice already runs on the discipline Anthropic publishes about: no-evidence-⇒-no,
  pre-registered criteria, independent referees, honest rollback. You did not adopt that
  after reading a safety paper; it is how your repos gate themselves.
- The concrete proof you *live* it: you audited your own benchmark, found three harness bugs
  manufacturing failures, and **corrected a claim you had already put in a paper table**.
  Most candidates cannot point at a time their own tooling proved them wrong in public.
- You work on agents where the failure is silent, which is the argument for interpretable and
  steerable systems rather than a slogan about them.
- Do NOT write anything about admiring the mission in the abstract. Every applicant does.

### 2. "Most complex and interesting thing you have done with an LLM — the specific task, and the challenges"

Strongest candidate: **the grader audit** (`vlm-failure-probe`). It has a specific task, a
real adversary, and a punchline that flatters nobody:

- Task: turn a paper's VLM failure taxonomy into a gated probe suite, then measure three
  Claude tiers against a production pipeline's observed failures.
- The turn: a 3-repeat variance run showed the **grader**, not the model, was the least
  reliable component — an empty API response scored 0.0, a truncated answer graded as
  complete, and the suite's own tests were never gated by CI. Three bugs manufacturing
  failures.
- The discipline: every spec change pre-registered with falsifiable per-probe predictions
  *before* the run that tested them; instability 5 unstable pairs → 1; and one already-
  published capability claim retracted.
- Why it fits *this* role: automated evaluation of models and prompts is exactly where a
  silently-broken grader does the most damage.

Alternative if you want the harness angle instead: `mcp-arena`'s evidence gate (a benchmark
that ships its own falsifier). Pick one and go deep — the question rewards depth, not a tour.

### 3. "Examples of your work with LLMs — links or content"

- `github.com/wjlgatech/loop-engineering-anything` — agent harness, maker≠checker, 543 tests
- `github.com/wjlgatech/mcp-arena` — evidence-gated tool-use benchmark over real MCP servers
- `github.com/wjlgatech/FM-os` — 15 certified skills, rubric-as-data certifier, `rewardforge`
- `agentic-portfolio-lovat.vercel.app` — live portfolio
- SCWM (NeurIPS 2026, under review) · *Physical AI* (DOI 10.20944/preprints202604.0549.v1)

### 4. "Additional Information"

The honest place to name the edge rather than let them find it: no interpretability tooling
shipped; RL is DPO-scale on small open models, not large-scale RL on frontier models;
multi-agent built as harnesses and referees, not many-agent systems at scale. Naming it is
what makes the rest of the application credible — and it is the same move your resume makes.

## Mechanical fields (not essays — reuse verbatim)

| Field | Answer |
|---|---|
| First / Last name | Paul / Jialiang Wu |
| Email | wjlgatech@gmail.com |
| Phone | 650-656-3046 |
| Resume/CV | `resumes/anthropic-research-engineer-agents.pdf` |
| Website | https://agentic-portfolio-lovat.vercel.app |
| GitHub URL | https://github.com/wjlgatech |
| LinkedIn | https://linkedin.com/in/paul-jialiang-wu-phd |
| Publications URL | DOI 10.20944/preprints202604.0549.v1 |
| In-person 25% of the time? | **Yes** |
| Visa sponsorship required (both questions) | **No** |
| Personal projects using LLMs? | **Yes** |
| Python expertise? | **Yes** |
| Open to relocation? | your call — you are already Mountain View, CA |
| Address you'd work from | Mountain View, CA |
| Interviewed at Anthropic before? | your call — I do not know this |
| AI Policy for Application | **Yes** (and it is true: first drafts yours, refinement mine) |
| Earliest start / timeline | your call |

## Outcome log

| Date | Event | Notes |
|---|---|---|
| 2026-08-03 | dossier + tailored resume shipped; NOT submitted | 4 essays await Paul's first drafts, per employer policy |
