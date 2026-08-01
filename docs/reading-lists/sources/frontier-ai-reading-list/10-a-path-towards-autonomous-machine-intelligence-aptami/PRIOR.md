# Prior claims — A Path Towards Autonomous Machine Intelligence (APTAMI)

> Extracted verbatim from `docs/reading-lists/ai-reading-list-07-30-2026.md`. This is what the
> reading list ALREADY asserts about this work. Your deep pass is not a summary —
> it is a test: confirm, sharpen, or refute each line against the primary text.

> *Link fixed at intake: the original ai.meta.com publication URL returns 404; this is the canonical OpenReview page.*

**Statement:** LeCun's blueprint for AGI centers on a hierarchical world model that learns via self-supervised predictive learning (JEPA), with a separate "intrinsic cost" module for alignment and drives. [jakobnielsenphd.substack](https://jakobnielsenphd.substack.com/p/agi-to-asi)

**Essential Quote:** "The key missing ingredient for human-level AI is the ability to learn world models via self-supervised learning." [jakobnielsenphd.substack](https://jakobnielsenphd.substack.com/p/agi-to-asi)

**Detailed Reasoning and Evidence:**
- LeCun argues that LLM-style next-token prediction is insufficient for robust agency in the physical world; agents need predictive models of how the world changes under actions. [jakobnielsenphd.substack](https://jakobnielsenphd.substack.com/p/agi-to-asi)
- The proposed architecture has: (1) perception modules, (2) a world model predicting future latent states, (3) an actor/planner, and (4) an intrinsic cost module encoding drives like pain, curiosity, and prosociality. [jakobnielsenphd.substack](https://jakobnielsenphd.substack.com/p/agi-to-asi)
- JEPA (Joint-Embedding Predictive Architecture) avoids pixel-level prediction; instead, it predicts future embeddings, making learning tractable and scalable. [changxu](https://changxu.dev/radar/robotics)

**Detailed Actionable Steps:**
- Treat world modeling as your core capability for any Physical AI system: ask "What latent state does my robot need to predict to act safely and effectively?"
- Design architectures with explicit separation between: perception, world model, planner/actor, and cost/reward modules — this modularity is critical for debugging and alignment. [jakobnielsenphd.substack](https://jakobnielsenphd.substack.com/p/agi-to-asi)

**Patterns + Anti-patterns:**
- **Pattern:** "World model in the middle." All serious Physical AI stacks will have an internal simulator of physics, objects, and agents. [changxu](https://changxu.dev/radar/robotics)
- **Anti-pattern:** Pure reactive policies with no internal prediction. These fail under partial observability, long horizons, and safety-critical constraints.

**1st Principle:** Predictive world models are to Physical AI what transformers are to language: the scalable substrate for reasoning, planning, and control.

---
