# Prior claims — AI-assisted proof of Nesterov's Accelerated Method

> Extracted verbatim from `docs/reading-lists/ai-enabled-research-reading-list-07-30-2026.md`. This is what the
> reading list ALREADY asserts about this work. Your deep pass is not a summary —
> it is a test: confirm, sharpen, or refute each line against the primary text.

**Context:** Case study in Quanta's article. [8]

**Statement:** An LLM-assisted workflow enabled the first convergence proof for Nesterov's accelerated gradient method, solving a 42-year-old optimization problem with human–AI collaboration. [8]

**Essential Quote:** "It's a concrete instance where the use of ChatGPT really accelerated the discovery." [8]

**Detailed Reasoning and Evidence:**
- Nesterov's method is central to optimization and ML training; convergence was long conjectured but unproved. [8]
- Ryu used ChatGPT to iteratively refine partial arguments: the model repeatedly produced incorrect full proofs but contained useful, correct intermediate lemmas and steps. [8]
- By acting as verifier and integrator, Ryu assembled a correct proof in days instead of months, a result suitable for top optimization journals on its own merits. [8]

**Detailed Actionable Steps:**
- Use AI to **fill in technical details** and generate candidate lemmas; you validate each step, preserving mathematical rigor. [8]
- Design prompts that **focus the model** on specific sub-lemmas or transformations; avoid broad "prove the theorem" prompts until you've scaffolded structure. [8]

**Patterns + Anti-patterns:**
- **Pattern:** Human as verifier; AI as prolific but error-prone proof assistant. [8]
- **Anti-pattern:** Delegating the entire proof to AI without step-by-step human checking; current models still misstep in subtle ways. [8]

**1st Principle:** Treat AI as high-bandwidth mathematical "muscle" that generates many candidate steps, with humans providing the "brain" for correctness and taste.

---
