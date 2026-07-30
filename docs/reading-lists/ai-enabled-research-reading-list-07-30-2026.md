# AI for Math & Science: Assisted and Autonomous Problem Solving

> **Trackable doc** · added 2026-07-30 · part of the FM-os [community reading-list track](README.md)
> · sibling of the [Frontier AI list](ai-reading-list-07-30-2026.md).
>
> **Provenance & verification (2026-07-30):** the list's single external source — the Quanta
> article all `[8]` citations point to — curl-verified 200. Every entry currently derives from
> that one source; primary links (AlphaEvolve preprint, Ryu's paper, the Bruhat-interval work)
> are **not yet in the list** — adding them is part of the next revision.
>
> **Known gaps (honest ❌):** the intake snapshot **cuts off mid-sentence in entry #4**, and
> Layers 2 (**AI for Autonomous Science & Experimental Discovery**) and 3 (**Meta-Frameworks &
> Benchmarks**) announced in the intro are **not yet present**. Related FM-os coverage until
> then: the [Autonomous Research Agents repos](../../README.md#open-source-repos) and
> [research-loop](../../skills/research-loop/SKILL.md) skill.

This reading list focuses on **how AI assists or autonomously solves mathematical and
scientific problems**. It emphasizes concrete systems, case studies, and frameworks that:

- Help prove theorems or discover new math.
- Automate parts of the scientific method (hypothesis → experiment → analysis → paper).
- Benchmark AI on research-level tasks beyond homework-style exercises.
- Combine neural models with symbolic and formal reasoning.

The list is organized into three layers:

1. AI for Mathematical Problem Solving & Proof
2. AI for Autonomous Science & Experimental Discovery — *pending, see Known gaps*
3. Meta-Frameworks & Benchmarks for AI Math/Science Reasoning — *pending, see Known gaps*

---

## LAYER 1 — AI FOR MATHEMATICAL PROBLEM SOLVING & PROOF

### 1. ["The AI Revolution in Math Has Arrived"](https://www.quantamagazine.org/the-ai-revolution-in-math-has-arrived-20260413/) (Quanta, 2026)

**Statement:** Modern LLM-based systems now assist mathematicians in discovering and proving new results, moving from contest-style math to genuine research-level contributions. [8]

**Essential Quote:** "Soon, mathematicians were using AI to discover and prove new results, accomplishing in a day what would have once taken them weeks or months." [8]

**Detailed Reasoning and Evidence:**
- By 2025–2026, AI models solved 5 of 6 problems at the International Mathematical Olympiad and then advanced to research-level problems via systems like AlphaEvolve and Gemini-based tooling. [8]
- Mathematicians such as Terence Tao, Ernest Ryu, and others use LLMs to co-develop proofs, find errors, and generate novel proof strategies, including results publishable in top journals (e.g., convergence of Nesterov's method). [8]
- AI-assisted discovery includes uncovering hidden structures (e.g., hypercube structures in Bruhat intervals) and accelerating exploration across dozens of problems simultaneously. [8]

**Detailed Actionable Steps:**
- Use LLMs as **exploratory collaborators**: ask them for alternative proof strategies, fill gaps in partial arguments, and generate candidate conjectures; you act as verifier and curator. [8]
- Integrate AI into your workflow for **search over problem spaces**: define families of problems, let AI search for low-hanging fruit, and then filter for mathematically interesting results. [8]

**Patterns + Anti-patterns:**
- **Pattern:** AI as a "jumping robot" exploring many foothills and low walls, while humans plan routes to mathematical Everests; good for large-scale exploration, less for ultra-deep singular problems. [8]
- **Anti-pattern:** Treating AI-generated proofs as final truth without verification; current systems still generate errors and "slop," so human or formal checking remains essential. [8]

**1st Principle:** Use AI to accelerate **breadth and exploration** in math, while preserving human-led depth and understanding.

---

### 2. AlphaEvolve / "Mathematical Exploration and Discovery at Scale" (DeepMind + Tao et al., 2025)

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

### 3. AI-assisted proof of Nesterov's Accelerated Method (Ernest Ryu, 2025)

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

### 4. AlphaEvolve's Bruhat Interval Hypercube Discovery (Ellenberg, Williamson et al., 2025–2026)

**Context:** Described in Quanta article as a key structural discovery. [8]

**Statement:** AlphaEvolve revealed unexpected hypercube structures in Bruhat intervals of permutation groups, uncovering a deep combinatorial pattern that humans had missed for decades. [8]

**Essential Quote:** "It's a structure that's been sitting there for 50 years in front of our nose. We just hadn't noticed it." [8]

**Detailed Reasoning and Evidence:**
- Bruhat intervals encode order relations in permutation groups, important in combinatorics and algebraic geometry. [8]
- When the number of elements is a—

> **⚠️ Intake snapshot ends here — entry #4 is incomplete** (Evidence cut mid-sentence;
> Actions/Patterns/1st Principle missing).

---

## LAYER 2 — AI FOR AUTONOMOUS SCIENCE & EXPERIMENTAL DISCOVERY

> **Not yet included** — announced in the intro but absent from the intake snapshot.

## LAYER 3 — META-FRAMEWORKS & BENCHMARKS FOR AI MATH/SCIENCE REASONING

> **Not yet included** — announced in the intro but absent from the intake snapshot.
