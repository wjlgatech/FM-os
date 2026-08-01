# Prior claims — AlphaGo Zero

> Extracted verbatim from `docs/reading-lists/ai-reading-list-07-30-2026.md`. This is what the
> reading list ALREADY asserts about this work. Your deep pass is not a summary —
> it is a test: confirm, sharpen, or refute each line against the primary text.

**Statement:** AlphaGo Zero demonstrated that AI can achieve superhuman performance without human data by relying purely on reinforcement learning from scratch.

**Essential Quote:** "Mastering the game of Go without human knowledge".

**Detailed Reasoning and Evidence:**
- Unlike its predecessor, AlphaGo Zero learned only from the rules of the game and self-play.
- It proved that human data (expert games) actually acts as a "ceiling" that limits AI performance.
- By searching 1,600 nodes per move during inference (Monte Carlo Tree Search), it achieved superior results with fewer resources.

**Detailed Actionable Steps:**
- **Define Clear Rules:** Use pure reinforcement learning in domains with deterministic, verifiable rules (like coding or games) to exceed human capability.
- **Test-Time Scaling:** Increase compute during inference (letting the model "think" longer) to improve the quality of the output.

**Mechanism:** Test-Time Search. Using search algorithms (like MCTS) during inference allows the model to verify its "intuition" with logical reasoning.

**1st Principle:** Self-play + Search can surpass human data; rules + compute beat intuition.

---
