# Prior claims — ResNet (Deep Residual Learning for Image Recognition)

> Extracted verbatim from `docs/reading-lists/ai-reading-list-07-30-2026.md`. This is what the
> reading list ALREADY asserts about this work. Your deep pass is not a summary —
> it is a test: confirm, sharpen, or refute each line against the primary text.

**Statement:** ResNet introduced the Residual Block, allowing for the training of extremely deep networks (hundreds or thousands of layers) by solving the degradation problem.

**Essential Quote:** "It completely solved the problem of model degradation… enabling the training of very, very deep networks".

**Detailed Reasoning and Evidence:**
- As networks grew deeper, performance began to drop (degradation) due to vanishing gradients.
- ResNet introduced "skip connections" that allowed layers to learn the residual mapping ($F(x) = H(x) - x$) rather than the full underlying mapping, making optimization significantly easier.

**Detailed Actionable Steps:**
- **Simplify Learning Targets:** If a model struggles to learn a complex mapping, restructure it to learn only the "delta" or residual from the input.
- **Mechanism:** Gradient Shortcuts. Skip connections provide a direct path for gradients to flow during backpropagation, preventing them from disappearing in deep layers.

**1st Principle:** Residual learning enables depth; depth enables representation power.

---
