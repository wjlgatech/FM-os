# Prior claims — AlphaEvolve / "Mathematical Exploration and Discovery at Scale

> Extracted verbatim from `docs/reading-lists/ai-enabled-research-reading-list-07-30-2026.md`. This is what the
> reading list ALREADY asserts about this work. Your deep pass is not a summary —
> it is a test: confirm, sharpen, or refute each line against the primary text.

**Reference overview:** Described in the Quanta article and associated preprint. [8]

**Statement:** AlphaEvolve uses LLMs (Gemini) to write and evolve Python programs that search for improved solutions to mathematical problems, demonstrating scalable, semi-autonomous exploration in math. [8]

**Essential Quote:** "We were able to obtain comparable results in the span of a day or two" to what an expert might obtain in months, across many problems. [8]

**Detailed Reasoning and Evidence:**
- AlphaEvolve prompts Gemini to generate algorithmic approaches, then uses genetic algorithms to evolve these programs to optimize mathematical objectives (e.g., configurations, combinatorial quantities). [8]
- On 67 problems, AlphaEvolve improved on best-known solutions for 23, matched previous results for 36, and failed on the rest, showing a realistic mix of successes and failures. [8]
- The pipeline reveals that AI can efficiently mine "low-hanging fruit" across diverse math domains that humans would not systematically explore at scale. [8]

**Detailed Actionable Steps:**
- Build **AI-augmented search pipelines**: use LLMs to auto-generate code and strategies, then wrap them in evolutionary or Bayesian optimization loops for math/algorithmic problems. [8]
- Treat models as **idea generators**; your role is to define objectives, constraints, and evaluation/verification, not to manually program every search heuristic. [8]

**Patterns + Anti-patterns:**
- **Pattern:** "LLM + optimizer" loops for math exploration — LLM proposes; meta-optimizer evaluates and evolves; humans curate and formalize. [8]
- **Anti-pattern:** One-shot Q&A with LLMs on hard math and taking first answers at face value; iterative, programmatic search works better. [8]

**1st Principle:** Combine generative models with search/optimization to scale mathematical exploration beyond human bandwidth.

---
