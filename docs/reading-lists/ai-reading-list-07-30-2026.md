# Frontier AI Reading List: From Deep Learning Canon to AGI & ASI

> **Trackable doc** · added 2026-07-30 · part of the FM-os [community reading-list track](README.md)
> (AI · math · physics · CS · bio-biomed-biotech).
>
> **Provenance & verification (2026-07-30):** all 15 external links curl-verified; two were
> fixed during intake — the LeCun APTAMI link on ai.meta.com returned 404 (replaced with the
> canonical OpenReview page) and the RT-2 entry pointed at the RT-X site (replaced with the
> RT-2 project page). Entry quotes marked with a source link (substack / changxu / lesswrong)
> are **secondary-source paraphrases, not verified verbatim quotes from the papers** — treat
> them as summaries until checked against the primary text.
>
> **Known gaps (honest ❌):** the intake snapshot **cuts off mid-entry #12** and the Layer 3
> announced in the intro (**AGI & ASI Research** — Carlsmith, Bostrom, Russell, lab safety
> reports) is **not yet present**. Layer 3 + the completion of #12 are the next revision.

This document compiles seminal papers, blogs, and reports for an AI engineer focused on
**Physical AI**, **AGI**, and **ASI**. Each entry contains:

- **Statement**
- **Essential Quote**
- **Detailed Reasoning and Evidence**
- **Detailed Actionable Steps**
- **Patterns + Anti-patterns**
- **1st Principle**

The list is divided into three layers:

1. **Compute & Scaling Foundations** (the "deep learning canon")
2. **World Models & Embodied Intelligence** (Physical AI frontier)
3. **AGI & ASI Research** (paths to superintelligence, safety, and alignment) — *pending, see Known gaps*

Leading researchers referenced include **Andrej Karpathy**, **Yann LeCun**, **Pieter Abbeel**,
**Chelsea Finn**, **Sergey Levine**, **Joe Carlsmith**, **Nick Bostrom**, **Stuart Russell**,
and teams at **DeepMind**, **OpenAI**, **Anthropic**, and **Physical Intelligence**.

---

## LAYER 1 — COMPUTE & SCALING FOUNDATIONS

### 1. [The Bitter Lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html) (2019)

**Statement:** The most significant lesson in AI research is that general methods that leverage computation (search and learning) consistently outperform methods that incorporate human domain knowledge or "hand-crafted" features.

**Essential Quote:** "Building systems based on how we think we think… in the long run, tracks failure."

**Detailed Reasoning and Evidence:**
- Over 70 years, researchers found that methods relying on human intuition (e.g., identifying specific visual features or chess strategies) provided short-term gains but eventually hit a "plateau".
- As computation costs decreased exponentially (Moore's Law), raw search and learning algorithms (like Gradient Descent) "surpassed" human-centric systems.

**Detailed Actionable Steps:**
- **Prioritize Scalability:** Invest in algorithms that improve linearly or better as compute increases.
- **Avoid Over-engineering:** Do not try to "teach" the model human logic (like symmetry or specific object definitions); let the model discover complexities itself.

**Patterns + Anti-patterns:**
- **Pattern:** Betting on Compute. Success comes to those who wait for hardware to catch up to general algorithms.
- **Anti-pattern:** Human-centric priors. Using specialized knowledge to "short-cut" learning often limits the ultimate performance ceiling.

**1st Principle:** Search and Learning are the only two methods that scale indefinitely with compute.

---

### 2. [Brook for GPUs](https://graphics.stanford.edu/projects/brookgpu/) (2004)

**Statement:** This paper transformed the GPU from a fixed-function graphics unit into a programmable streaming processor, enabling general-purpose scientific computing (GPGPU).

**Essential Quote:** "Transforming a computing unit that was very difficult to program into one that could be programmed and driven using high-level languages".

**Detailed Reasoning and Evidence:**
- In 2004, GPUs already had higher FLOPS than CPUs but required low-level "shader" assembly language, making them nearly impossible for non-graphics developers to use.
- Brook introduced a high-level language that abstracted hardware as "streams" and "kernels," allowing code to be portable and efficient. This work directly led to the development of NVIDIA's CUDA.

**Detailed Actionable Steps:**
- **Hardware/Software Co-design:** Abstract low-level hardware complexity into high-level, developer-friendly frameworks to unlock dormant compute power.

**Patterns + Anti-patterns:**
- **Pattern:** Winning the "Hardware Lottery." Algorithms that naturally fit existing high-performance hardware (GPUs) will dominate the industry.
- **Mechanism:** Virtualization of Parallel Hardware. Treating the GPU as a "streaming processor" allows the mapping of massive parallel tasks (like neural network matrix multiplication) onto graphics hardware.

**1st Principle:** Algorithms that align with hardware trends win; abstraction layers unlock dormant compute.

---

### 3. [AlexNet (ImageNet Classification with Deep CNNs)](https://proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf) (2012)

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

### 4. [ResNet (Deep Residual Learning for Image Recognition)](https://arxiv.org/abs/1512.03385) (2015)

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

### 5. [The Transformer (Attention Is All You Need)](https://arxiv.org/abs/1706.03762) (2017)

**Statement:** The Transformer architecture replaced sequential recurrent networks with a pure Attention mechanism, enabling massive parallelization and better global modeling of sequences.

**Essential Quote:** "If the model works, we attribute it to 'God's Mercy'" (Noam Shazeer on the black-box nature of the architecture).

**Detailed Reasoning and Evidence:**
- Recurrent Neural Networks (RNNs) were sequential and "hardware-unfriendly" because they required waiting for the previous step's output.
- Transformers allow every token in a window to interact with every other token simultaneously via Self-Attention, making them perfect for GPUs.

**Detailed Actionable Steps:**
- **Unify Data as Sequences:** Treat images, audio, and text as sequences of "tokens" to leverage the Transformer's scaling power.
- **Positional Encoding:** Since Attention is order-agnostic, explicitly add position information so the model can perceive sequence order.

**Patterns + Anti-patterns:**
- **Pattern:** The Attention Window. Directly calculating relationships within a context window is more efficient than passing information through a sequential bottleneck.

**1st Principle:** Contextual Connectivity. Intelligence arises from the model's ability to "attend" to the most relevant parts of the input sequence regardless of distance.

---

### 6. [AlphaGo Zero](https://www.nature.com/articles/nature24270) (2017)

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

### 7. [InstructGPT (Training language models to follow instructions)](https://arxiv.org/abs/2203.02155) (2022)

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

### 8. [Stable Diffusion (Latent Diffusion Models)](https://arxiv.org/abs/2112.10752) (2022)

**Statement:** Generative AI becomes computationally efficient by moving the diffusion process from pixel space into a compressed Latent Space.

**Essential Quote:** "Compression produces intelligence… the process of turning a thick book into a thin one is the process of learning".

**Detailed Reasoning and Evidence:**
- Working in high-resolution pixel space is too expensive.
- Stable Diffusion uses an autoencoder to compress images into a 128x128 latent representation. This allows the model to learn the "essence" of an image with 100x less compute.

**Detailed Actionable Steps:**
- **Use Latent Representations:** For any high-dimensional data (video, audio), compress it into a latent space before applying generative modeling.
- **Cross-Attention Guidance:** Use text encoders (like CLIP) to inject language signals into the generative process to "steer" the output.

**Mechanism:** Iterative Denoising. The model learns to remove "noise" step-by-step to reveal a structured image that matches the text prompt.

**1st Principle:** Latent compression is the key to scalable generation; diffusion in latent space is the engine.

---

### 9. [Chain of Thought (CoT)](https://arxiv.org/abs/2201.11903) (2022)

**Statement:** Large models can solve complex reasoning tasks if they are prompted to show their intermediate reasoning steps ("think step by step").

**Essential Quote:** "We can significantly improve the performance of a model on reasoning tasks by showing it intermediate steps".

**Detailed Reasoning and Evidence:**
- Researchers discovered that models like GPT-3 had "latent" reasoning abilities that were not triggered by direct answers.
- By adding magic words like "Let's think step by step," the model allocates more tokens (compute) to the reasoning process, leading to a "reasoning breakthrough".

**Detailed Actionable Steps:**
- **Encourage Verbosity in Reasoning:** When asking the model to solve math or logic, insist that it output its full line of thinking.

**Pattern:** System 2 Thinking. Forcing a model to output intermediate steps is the AI equivalent of human "slow, deliberate thinking".

**1st Principle:** Reasoning is a generative process; more tokens for thought = better answers.

---

## LAYER 2 — WORLD MODELS & EMBODIED INTELLIGENCE (PHYSICAL AI)

### 10. [A Path Towards Autonomous Machine Intelligence (APTAMI)](https://openreview.net/forum?id=BZ5a1r-kVsf) (2022)

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

### 11. [RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control](https://robotics-transformer2.github.io/) (2023)

> *Link fixed at intake: the original URL pointed at the RT-X project site; this is the RT-2 project page ([paper](https://arxiv.org/abs/2307.15818)).*

**Statement:** RT-2 established the VLA paradigm: co-fine-tuning large vision-language models on robot data to get policies that transfer web knowledge to physical actions. [lesswrong](https://www.lesswrong.com/posts/j3KuXBhXFteW8BFPo/why-asi-alignment-is-hard-an-overview)

**Essential Quote:** "RT-2 shows that vision-language-action models can transfer semantic knowledge from the web to robotic control." [lesswrong](https://www.lesswrong.com/posts/j3KuXBhXFteW8BFPo/why-asi-alignment-is-hard-an-overview)

**Detailed Reasoning and Evidence:**
- RT-2 builds on PaLI and PaLI-X VLMs, then fine-tunes them on multi-robot manipulation data, yielding a single model that can follow natural-language instructions and manipulate objects. [changxu](https://changxu.dev/radar/robotics)
- It demonstrated emergent behaviors like "pick up the object that represents kindness," showing semantic generalization beyond literal training tasks. [lesswrong](https://www.lesswrong.com/posts/j3KuXBhXFteW8BFPo/why-asi-alignment-is-hard-an-overview)
- This work catalyzed the entire VLA family (OpenVLA, π0, Gemini Robotics, etc.). [lesswrong](https://www.lesswrong.com/posts/j3KuXBhXFteW8BFPo/why-asi-alignment-is-hard-an-overview)

**Detailed Actionable Steps:**
- For product teams: start from a strong open VLM (e.g., LLaVA-style or SigLIP-backed) and treat robot data as an additional "modality" to fine-tune, not a separate system. [changxu](https://changxu.dev/radar/robotics)
- Invest in data pipelines that interleave vision, language, and action tokens; this is the "ImageNet moment" for robotics. [lesswrong](https://www.lesswrong.com/posts/j3KuXBhXFteW8BFPo/why-asi-alignment-is-hard-an-overview)

**Patterns + Anti-patterns:**
- **Pattern:** "VLA as robot foundation model." One model, many bodies, many tasks, with web-scale priors. [lesswrong](https://www.lesswrong.com/posts/j3KuXBhXFteW8BFPo/why-asi-alignment-is-hard-an-overview)
- **Anti-pattern:** Task-specific models per skill or per robot. These don't scale and can't leverage web knowledge.

**1st Principle:** Vision + language + action, trained jointly at scale, is the primary route to generalist robot policies.

---

### 12. [π0: A Vision-Language-Action Flow Model for General Robot Control](https://www.physicalintelligence.company/blog/pi0) (2024)

**Statement:** π0 (pi-zero) from Physical Intelligence shows that flow-matching–based VLA policies can achieve high-frequency, dexterous, real-world control across tasks and embodiments. [lesswrong](https://www.lesswrong.com/posts/j3KuXBhXFteW8BFPo/why-asi-alignment-is-hard-an-overview)

**Essential Quote:** "π0 is a flow-based VLA that generates continuous, high-frequency actions for dexterous manipulation."

> **⚠️ Intake snapshot ends here — entry #12 is incomplete** (Reasoning/Steps/Patterns/1st Principle missing).

---

## LAYER 3 — AGI & ASI RESEARCH

> **Not yet included.** The intake snapshot announced this layer (Carlsmith, Bostrom, Russell,
> and lab safety/alignment reports) but did not contain it. Next revision adds it — tracked in
> the [reading-list track index](README.md).
