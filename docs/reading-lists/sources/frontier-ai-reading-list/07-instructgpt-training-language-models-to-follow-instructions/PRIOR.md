# Prior claims — InstructGPT (Training language models to follow instructions)

> Extracted verbatim from `docs/reading-lists/ai-reading-list-07-30-2026.md`. This is what the
> reading list ALREADY asserts about this work. Your deep pass is not a summary —
> it is a test: confirm, sharpen, or refute each line against the primary text.

**Statement:** Large models are not useful assistants by default; Reinforcement Learning from Human Feedback (RLHF) is required to align model outputs with human intent and helpfulness.

**Essential Quote:** "A 1.3B parameter model, after this adjustment, was better at following instructions than a 175B parameter GPT-3".

**Detailed Reasoning and Evidence:**
- Pure "next-token prediction" models (like GPT-3) often produce toxic or unhelpful content because they only aim to imitate the internet.
- InstructGPT used human ranking of outputs to train a Reward Model, which then guided the fine-tuning of the policy via PPO (Proximal Policy Optimization).

**Detailed Actionable Steps:**
- **Collect Ranking Data:** Don't just collect "correct" answers; collect human preferences between multiple model outputs to build a reward signal.

**Patterns + Anti-patterns:**
- **Pattern:** Alignment as Value-Unlock. Post-training (SFT and RLHF) is what transforms raw "latent knowledge" into a usable product.

**1st Principle:** Helpfulness, Honesty, and Harmlessness (HHH). A model's utility is defined by its alignment with these human values rather than its raw accuracy.

---
