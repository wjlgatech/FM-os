# Prior claims — AlexNet (ImageNet Classification with Deep CNNs)

> Extracted verbatim from `docs/reading-lists/ai-reading-list-07-30-2026.md`. This is what the
> reading list ALREADY asserts about this work. Your deep pass is not a summary —
> it is a test: confirm, sharpen, or refute each line against the primary text.

**Statement:** AlexNet proved that scaling data, computation, and model size simultaneously can achieve a breakthrough in visual recognition.

**Essential Quote:** "To make deep neural networks work, they need more labeled data and more computation".

**Detailed Reasoning and Evidence:**
- Before 2012, computer vision was dominated by hand-crafted feature extraction.
- AlexNet used a massive dataset (ImageNet with 14M images), specialized GPU kernels for efficiency, and a model with 62.5M parameters.
- It outperformed the previous state-of-the-art by over 10 percentage points, marking the start of the "Deep Learning Era".

**Detailed Actionable Steps:**
- **Scale Simultaneously:** Do not just increase parameters; ensure data volume and compute efficiency (via GPUs) scale at the same pace.
- **In-house Infra Talent:** Hire "Infra Experts" who can write specialized GPU kernels when existing libraries are insufficient.

**Patterns + Anti-patterns:**
- **Pattern:** "The Scale-Out Solution." Large-scale models learn better from raw data than small models learn from human instructions.

**1st Principle:** Data + Compute + Model = Intelligence. Scaling all three factors is the primary driver of performance gains.

---
