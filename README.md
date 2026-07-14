# 🛠️ FM-os — the Foundation Model Operating System

<div align="center">

[![Awesome](https://awesome.re/badge-flat2.svg)](https://awesome.re)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](CONTRIBUTING.md)
[![Stars](https://img.shields.io/github/stars/wjlgatech/FM-os?style=flat-square)](https://github.com/wjlgatech/FM-os/stargazers)
[![Contributors](https://img.shields.io/github/contributors/wjlgatech/FM-os?style=flat-square)](https://github.com/wjlgatech/FM-os/graphs/contributors)
[![Last Updated](https://img.shields.io/github/last-commit/wjlgatech/FM-os?style=flat-square&label=updated)](https://github.com/wjlgatech/FM-os/commits/main)
[![Weekly Sync](https://img.shields.io/github/actions/workflow/status/wjlgatech/FM-os/sync.yml?style=flat-square&label=weekly%20sync)](https://github.com/wjlgatech/FM-os/actions/workflows/sync.yml)
[![License](https://img.shields.io/github/license/wjlgatech/FM-os?style=flat-square)](LICENSE)

The most comprehensive, community-driven, **living** map of how modern language models are actually built and shipped — pre-training · post-training · fine-tuning · RL — with a first, sharp focus on **Small Language Models (SLM)**.

*From a 135M model you can train on one GPU to the RL recipes behind frontier reasoning — every repo, course, paper, and job worth your time, cross-linked and kept fresh automatically.*

[Start Here](#start-here) • [Repos](#open-source-repos) • [Courses](#courses) • [Papers](#papers) • [Jobs](#jobs--careers) • [Roadmap](#learning-roadmap) • [Contribute](#contribute)

</div>

---

> **⚡ Why FM-os and not the other lists?**

> 1. **SLM-first.** Not another everything-list — organized around small, efficient, trainable-on-a-budget models and the exact ops that make them work.
> 2. **Lifecycle-structured.** Everything filed under the real FM pipeline: pre-training → post-training → fine-tuning → RL → serving.
> 3. **Cross-linked.** Papers point to code, code points to courses, courses point to jobs — follow a thread from idea to hire.
> 4. **Auto-fresh.** A weekly GitHub Action re-checks every repo's stars, latest release, and links, then opens a PR — this list is never stale.
> 5. **Data-driven & forkable.** Every entry lives in a plain `data/*.yml` file; the README is generated. Adding a resource is a two-line PR.

---

<h2 id="start-here">🚀 Start Here</h2>

New to foundation-model ops? Read this in order:

1. **Understand the lifecycle** → *pre-training → post-training → fine-tuning → RL → serving*. Every section below follows it.
2. **Pick a small model you can actually run** → jump to [Small & Efficient Models](#open-source-repos).
3. **Learn from scratch** → the [Courses](#courses) section starts with from-scratch, one-GPU-friendly material.
4. **Go deep** → [Papers](#papers) are filed by lifecycle stage, SLM first.
5. **Get hired** → [Jobs & Careers](#jobs--careers) points at the labs and boards that hire for this work.

🤏 = directly Small-Language-Model relevant.

---

<h2 id="-table-of-contents">📚 Table of Contents</h2>

- [🚀 Start Here](#start-here)
- [🤖 SLM Model Zoo](#model-zoo) `13`
- [🏅 FM-os Certified](#fm-os-certified) `4`
- [🧰 Open-Source Repos](#open-source-repos) `35`
- [🎓 Courses](#courses) `17`
- [📄 Papers](#papers) `35`
- [💼 Jobs & Careers](#jobs--careers) `11`
- [🗺️ Learning Roadmap](#learning-roadmap)
- [🤝 Contribute](#contribute)

---

<h2 id="model-zoo">🤖 SLM Model Zoo</h2>

The small open models worth knowing, smallest first. `⚠️` = non-commercial / restricted license — check before shipping.

| Model | Org | Params | License | Context | On-device |
|---|---|--:|---|--:|:--:|
| [Llama-3.2-1B](https://huggingface.co/meta-llama/Llama-3.2-1B) | Meta | 1B | Llama 3.2 Community | 128K | ✅ |
| [OLMo-2-1B](https://huggingface.co/allenai/OLMo-2-0425-1B) | Allen Institute for AI | 1B | Apache-2.0 | 4K | ✅ |
| [Falcon3-1B](https://huggingface.co/tiiuae/Falcon3-1B-Base) | TII | 1B | TII Falcon-LLM 2.0 | 4K | ✅ |
| [MobileLLM-1B](https://huggingface.co/facebook/MobileLLM-1B) | Meta | 1B | ⚠️ FAIR Noncommercial Research | 2K | ✅ |
| [TinyLlama-1.1B](https://huggingface.co/TinyLlama/TinyLlama-1.1B-Chat-v1.0) | TinyLlama (community) | 1.1B | Apache-2.0 | 2K | ✅ |
| [Qwen2.5-1.5B](https://huggingface.co/Qwen/Qwen2.5-1.5B) | Alibaba (Qwen) | 1.5B | Apache-2.0 | 32K | ✅ |
| [SmolLM2-1.7B](https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B) | Hugging Face | 1.7B | Apache-2.0 | 8K | ✅ |
| [Gemma-2-2B](https://huggingface.co/google/gemma-2-2b) | Google | 2B | Gemma | 8K | ✅ |
| [Llama-3.2-3B](https://huggingface.co/meta-llama/Llama-3.2-3B) | Meta | 3B | Llama 3.2 Community | 128K | ✅ |
| [StableLM-Zephyr-3B](https://huggingface.co/stabilityai/stablelm-zephyr-3b) | Stability AI | 3B | ⚠️ Stability AI Community | 4K | ✅ |
| [Phi-3-mini (3.8B)](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct) | Microsoft | 3.8B | MIT | 4K | ✅ |
| [H2O-Danube3-4B](https://huggingface.co/h2oai/h2o-danube3-4b-base) | H2O.ai | 4B | Apache-2.0 | 8K | ✅ |
| [MiniCPM3-4B](https://huggingface.co/openbmb/MiniCPM3-4B) | OpenBMB | 4B | Apache-2.0 (weights: registration) | 32K | ✅ |

<sub>[↑ back to top](#-table-of-contents)</sub>

---

<h2 id="fm-os-certified">🏅 FM-os Certified</h2>

Trust, not just a list. Every tool below is scored by an **automated, evidence-based rubric** ([`data/certify.yml`](data/certify.yml)) — provenance, a security scan, docs, SLM/FM-ops relevance, and more. Security is a blocking gate; no evidence ⇒ no pass. Authors self-certify in CI — see [docs/CERTIFY.md](docs/CERTIFY.md).

| Tool | Kind | Score | Status |
|---|---|--:|:--|
| [slm-quickstart](https://github.com/wjlgatech/FM-os/tree/main/skills/slm-quickstart) | skill | 94/100 | ✅ certified |
| [fm-os-sync](https://github.com/wjlgatech/FM-os/tree/main/scripts) | workflow | 80/100 | ✅ certified |
| [eval-llm](https://github.com/topics/claude-skill) | skill | — | ⏳ submitted |
| [continual-learning-research](https://github.com/topics/claude-skill) | skill | — | ⏳ submitted |

> **Earn the badge for your tool:** add the FM-os Certify action to your CI (see [docs/CERTIFY.md](docs/CERTIFY.md)) and embed:
> ```md
> ![FM-os Certified](https://img.shields.io/endpoint?url=https://wjlgatech.github.io/FM-os/badges/YOUR-TOOL.json)
> ```

<sub>[↑ back to top](#-table-of-contents)</sub>

---

<h2 id="open-source-repos">🧰 Open-Source Repos</h2>

### Small & Efficient Models
- **[SmolLM / SmolLM2 / SmolLM3](https://github.com/huggingface/smollm)** 🤏 `★ 3,844` — Fully open recipes, data, and weights for the 135M-3B SmolLM family, the reference open SLM line.
- **[Phi Cookbook](https://github.com/microsoft/PhiCookBook)** 🤏 `★ 3,767` — Microsoft's official hub for the Phi SLM family with inference, fine-tuning, quantization, and edge-deployment recipes.
- **[Gemma (DeepMind)](https://github.com/google-deepmind/gemma)** 🤏 `★ 5,555` — Official JAX library for Gemma open weights including the 1B/2B and 3n on-device small variants.
- **[Qwen3](https://github.com/QwenLM/Qwen3)** 🤏 `★ 27,393` — Alibaba's Qwen series spanning 0.6B/1.7B/4B dense SLMs with strong multilingual and reasoning quality.
- **[gemma_pytorch](https://github.com/google/gemma_pytorch)** 🤏 `★ 5,711` — Official PyTorch inference implementation of Gemma (incl. small text-only variants) for CPU/GPU/TPU.
- **[TinyLlama](https://github.com/jzhang38/TinyLlama)** 🤏 `★ 9,011` — Compact 1.1B Llama pretrained on 3T tokens; a canonical, reproducible sub-2B pretraining reference.
- **[MobileLLM](https://github.com/facebookresearch/MobileLLM)** 🤏 `★ 1,451` — Meta research on sub-billion-parameter, deep-thin architectures optimized for on-device use (ICML 2024).
- **[OLMo](https://github.com/allenai/OLMo)** 🤏 `★ 6,587` — AI2's fully open model+data+training stack including small 1B variants for reproducible SLM research.
- **[Llama Models](https://github.com/meta-llama/llama-models)** 🤏 `★ 7,651` — Meta's official utilities and model cards for Llama, including the 1B/3B Llama 3.2 on-device SLMs.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Pre-training & Training Frameworks
- **[nanoGPT](https://github.com/karpathy/nanoGPT)** 🤏 `★ 61,156` — Minimal ~300-line GPT training/finetuning loop; the standard starting point for training small GPTs from scratch.
- **[LitGPT](https://github.com/Lightning-AI/litgpt)** 🤏 `★ 13,482` — 20+ hackable LLM implementations with pretrain/finetune/deploy recipes, including small Phi/Qwen/Gemma models.
- **[GPT-NeoX](https://github.com/EleutherAI/gpt-neox)** `★ 7,443` — EleutherAI's Megatron+DeepSpeed training stack for autoregressive transformers with 3D parallelism.
- **[Megatron-LM](https://github.com/NVIDIA/Megatron-LM)** `★ 17,064` — NVIDIA's GPU-optimized library and building blocks for large-scale transformer pretraining.
- **[TorchTitan](https://github.com/pytorch/torchtitan)** `★ 5,532` — PyTorch-native platform for generative-model pretraining with composable FSDP2/TP/PP/CP parallelism.
- **[Nanotron](https://github.com/huggingface/nanotron)** `★ 2,747` — Minimalistic 3D-parallelism pretraining library from Hugging Face, basis of the Ultrascale Playbook.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Fine-tuning & PEFT
- **[PEFT](https://github.com/huggingface/peft)** 🤏 `★ 21,394` — Reference library for LoRA/QLoRA and other parameter-efficient methods, enabling SLM tuning on consumer GPUs.
- **[Unsloth](https://github.com/unslothai/unsloth)** 🤏 `★ 68,200` — 2x-faster, ~70%-less-VRAM finetuning for small models, ideal for LoRA/QLoRA on single-GPU setups.
- **[Axolotl](https://github.com/axolotl-ai-cloud/axolotl)** 🤏 `★ 12,197` — Config-driven post-training framework covering SFT/LoRA/DPO across many small and large model families.
- **[LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory)** 🤏 `★ 73,271` — Unified zero-code fine-tuning of 100+ LLMs/VLMs with LoRA/QLoRA/DPO and a web UI, common for SLM tuning.
- **[torchtune](https://github.com/meta-pytorch/torchtune)** 🤏 `★ 5,783` — PyTorch-native post-training recipes (SFT, distillation, DPO/PPO/GRPO, QAT) tuned for memory-limited hardware.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Post-training & RL (RLHF / DPO / GRPO)
- **[TRL](https://github.com/huggingface/trl)** 🤏 `★ 18,840` — Hugging Face post-training library with SFT/DPO/GRPO trainers widely used to align small reasoning models.
- **[OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)** 🤏 `★ 9,788` — Ray+vLLM RLHF framework (PPO/GRPO/RLOO) that scales from small models up to 70B+, agent-friendly.
- **[verl](https://github.com/verl-project/verl)** 🤏 `★ 22,468` — ByteDance HybridFlow RL post-training (PPO/GRPO/DAPO) with vLLM/SGLang; popular for GRPO on small models.
- **[trlX](https://github.com/CarperAI/trlx)** `★ 4,753` — Distributed RLHF framework (PPO, ILQL) via Accelerate/NeMo; an early, widely-cited RLHF reference.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Evaluation
- **[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)** 🤏 `★ 13,279` — De-facto standard few-shot eval harness (60+ benchmarks) backing the Open LLM Leaderboard, ideal for SLM benchmarking.
- **[LightEval](https://github.com/huggingface/lighteval)** 🤏 `★ 2,476` — Hugging Face all-in-one evaluator across vLLM/Accelerate/TGI backends with 1000+ tasks for small-model eval.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Serving, Inference & On-Device
- **[llama.cpp](https://github.com/ggml-org/llama.cpp)** 🤏 `★ 120,340` — C/C++ GGUF inference engine that runs quantized SLMs efficiently on CPUs, laptops, and edge devices.
- **[vLLM](https://github.com/vllm-project/vllm)** `★ 86,247` — High-throughput PagedAttention serving engine; the default for scalable OpenAI-compatible model serving.
- **[Ollama](https://github.com/ollama/ollama)** 🤏 `★ 176,100` — One-command local runner for small open models, the easiest path to running SLMs on a personal machine.
- **[MLC-LLM](https://github.com/mlc-ai/mlc-llm)** 🤏 `★ 22,948` — ML-compilation deployment engine that compiles SLMs to iOS, Android, WebGPU, and diverse GPUs/CPUs.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Distillation & Compression
- **[BitNet](https://github.com/microsoft/BitNet)** 🤏 `★ 39,724` — Official 1-bit (1.58-bit) LLM inference framework with optimized CPU/GPU kernels for extreme efficiency.
- **[LLM-AWQ](https://github.com/mit-han-lab/llm-awq)** 🤏 `★ 3,589` — Activation-aware INT3/4 weight quantization (MLSys 2024) plus TinyChat for on-device/edge SLM inference.
- **[GPTQModel](https://github.com/ModelCloud/GPTQModel)** 🤏 `★ 1,205` — Actively maintained GPTQ quantization toolkit with HF/vLLM/SGLang support across NVIDIA/AMD/Intel/Apple hardware.
- **[LightCompress (LLMC)](https://github.com/ModelTC/LightCompress)** 🤏 `★ 733` — Broad model-compression toolkit (quantization, sparsity, pruning) for shrinking LLMs/VLMs to deployable sizes.
- **[DistillKit](https://github.com/arcee-ai/DistillKit)** 🤏 `★ 976` — Open toolkit for knowledge distillation, training smaller student models from larger teachers (logit + hidden-state).

<sub>[↑ back to top](#-table-of-contents)</sub>

---

<h2 id="courses">🎓 Courses</h2>

### Foundations & From-Scratch
- **[Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)** — Eureka Labs · Andrej Karpathy (2023) · _free_ — Code-along video series building neural nets from backprop up to a GPT, following Attention Is All You Need and GPT-2/3.
- **[CS224N: NLP with Deep Learning](https://web.stanford.edu/class/cs224n/)** — Stanford · Christopher Manning (2024) · _free_ — Foundational NLP-with-deep-learning course covering word vectors, attention, transformers, and pretraining; lecture videos are public.
- **[CS 11-711: Advanced NLP](https://www.phontron.com/class/anlp-fall2024/)** — Carnegie Mellon University · Graham Neubig (2024) · _free_ — Graduate NLP course rebuilt around LLMs, including a build-your-own-LLaMa assignment; slides and videos are public.
- **[6.S191: Introduction to Deep Learning](https://introtodeeplearning.com/)** — MIT · Alexander Amini, Ava Soleimany (2025) · _free_ — Fast-paced intro to deep learning with labs, now including large language models and generative AI.
- **[The Full Stack LLM Bootcamp](https://fullstackdeeplearning.com/llm-bootcamp/)** — Full Stack Deep Learning · Charles Frye, Sergey Karayev, Josh Tobin (2023) · _free_ — Recorded bootcamp on building LLM applications: prompt engineering, LLMOps, augmented models, and shipping an app.
- **[Generative AI with Large Language Models](https://www.deeplearning.ai/courses/generative-ai-with-llms/)** — DeepLearning.AI & AWS · Antje Barth, Chris Fregly, et al. (2023) · _free_ — Covers the LLM lifecycle: pretraining, scaling laws, instruction tuning, and RLHF (free to audit on Coursera).

<sub>[↑ back to top](#-table-of-contents)</sub>

### Pre-training
- **[CS336: Language Modeling from Scratch](https://cs336.stanford.edu/spring2025/)** — Stanford · Percy Liang, Tatsunori Hashimoto (2025) · _free_ — Implementation-heavy course that builds a language model end to end: tokenization, transformer, training, systems, scaling, data, and alignment.
- **[LLM101n: Let's build a Storyteller](https://github.com/karpathy/LLM101n)** — Eureka Labs · Andrej Karpathy (2024) · _free_ — Public syllabus/repo (in development) for building a Storyteller LLM end to end in Python, C, and CUDA.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Post-training & Alignment
- **[Post-training of LLMs](https://www.deeplearning.ai/courses/post-training-of-llms/)** — DeepLearning.AI · Banghua Zhu (2025) · _free_ — When and how to apply SFT, DPO, and online RL, including data curation for post-training.
- **[Fine-tuning & RL for LLMs: Intro to Post-training](https://www.deeplearning.ai/courses/fine-tuning-and-reinforcement-learning-for-llms-intro-to-post-training/)** — DeepLearning.AI (with AMD) · Sharon Zhou (2025) · _free_ — Covers fine-tuning, reward modeling, RLHF, and RL algorithms (PPO, GRPO) for shaping behavior and reasoning.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Fine-tuning
- **[Hugging Face LLM Course](https://huggingface.co/learn/llm-course)** — Hugging Face · Hugging Face team (2024) · _free_ — Free hands-on course on transformers, tokenizers, fine-tuning pretrained models, and building LLM applications.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Reinforcement Learning
- **[CS234: Reinforcement Learning](https://web.stanford.edu/class/cs234/)** — Stanford · Emma Brunskill (2024) · _free_ — Graduate RL course spanning tabular methods, deep RL, policy gradients, and the basics of RL from human feedback.
- **[Deep Reinforcement Learning Course](https://huggingface.co/learn/deep-rl-course)** — Hugging Face · Thomas Simonini (2023) · _free_ — Free self-paced Deep RL course with practical training in Stable-Baselines3, CleanRL, and Sample Factory; optional certificate.
- **[Reinforcement Learning from Human Feedback](https://learn.deeplearning.ai/courses/reinforcement-learning-from-human-feedback/)** — DeepLearning.AI · Nikita Namjoshi (2024) · _free_ — Short course on the RLHF pipeline, tuning an open model with reward and preference data.
- **[Reinforcement Fine-Tuning LLMs with GRPO](https://www.deeplearning.ai/short-courses/reinforcement-fine-tuning-llms-grpo/)** — DeepLearning.AI (with Predibase) · Travis Addair, Arnav Garg (2025) · _free_ — Short course on using GRPO with programmable reward functions to improve LLM reasoning.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Agents & Applications
- **[CS294/194-196: Large Language Model Agents](https://rdi.berkeley.edu/llm-agents/f24)** — UC Berkeley · Dawn Song, Xinyun Chen (2024) · _free_ — MOOC-available course on LLM agent foundations, reasoning, tool use, and applications, with frontier-lab guest lectures.
- **[CS294/194-280: Advanced LLM Agents](https://rdi.berkeley.edu/adv-llm-agents/sp25)** — UC Berkeley · Dawn Song, Xinyun Chen (2025) · _free_ — Spring 2025 follow-on covering advanced agent reasoning, math/theorem-proving, code generation, and safety.

<sub>[↑ back to top](#-table-of-contents)</sub>

---

<h2 id="papers">📄 Papers</h2>

### Small Language Models & Surveys
- **[SmolLM2: When Smol Goes Big — Data-Centric Training of a Small Language Model](https://arxiv.org/abs/2502.02737)** (Ben Allal et al., Hugging Face, 2025) · arXiv:2502.02737 — A 1.7B model trained via careful data curation and overtraining, with the dataset recipe documented openly.
- **[A Survey of Small Language Models](https://arxiv.org/abs/2410.20011)** (Van Nguyen et al., multi-institution, 2024) · arXiv:2410.20011 — Taxonomy of SLM architectures, training, and compression methods, plus benchmark datasets and evaluation metrics.
- **[Small Language Models: Survey, Measurements, and Insights](https://arxiv.org/abs/2409.15790)** (Lu et al., multi-institution, 2024) · arXiv:2409.15790 — Empirical survey measuring capabilities and on-device runtime cost across a large set of released SLMs.
- **[Textbooks Are All You Need (phi-1)](https://arxiv.org/abs/2306.11644)** (Gunasekar et al., Microsoft, 2023) · arXiv:2306.11644 — phi-1 (1.3B), showing high-quality synthetic 'textbook' data lets small models match far larger ones on HumanEval.
- **[Textbooks Are All You Need II: phi-1.5 Technical Report](https://arxiv.org/abs/2309.05463)** (Li et al., Microsoft, 2023) · arXiv:2309.05463 — Extends the textbook-data approach to a 1.3B general reasoning model competitive with models 5x its size.
- **[Phi-3 Technical Report: A Highly Capable Language Model Locally on Your Phone](https://arxiv.org/abs/2404.14219)** (Abdin et al., Microsoft, 2024) · arXiv:2404.14219 — phi-3-mini (3.8B) rivals Mixtral 8x7B and GPT-3.5 on benchmarks while being small enough to run on a phone.
- **[Gemma: Open Models Based on Gemini Research and Technology](https://arxiv.org/abs/2403.08295)** (Mesnard et al., Google DeepMind, 2024) · arXiv:2403.08295 — Open 2B and 7B models derived from Gemini research, released with pretrained and instruction-tuned checkpoints.
- **[Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118)** (Gemma Team, Google DeepMind, 2024) · arXiv:2408.00118 — Trains the 2B/9B models with knowledge distillation over next-token prediction for strong quality at small size.
- **[MobileLLM: Optimizing Sub-billion Parameter Language Models for On-Device Use Cases](https://arxiv.org/abs/2402.14905)** (Liu et al., Meta, 2024) · arXiv:2402.14905 (ICML 2024) — Shows deep-and-thin architecture, embedding sharing, and grouped-query attention matter most below 1B parameters.
- **[TinyLlama: An Open-Source Small Language Model](https://arxiv.org/abs/2401.02385)** (Zhang et al., SUTD, 2024) · arXiv:2401.02385 — A 1.1B Llama-architecture model pretrained on ~3T tokens with a fully open training pipeline.
- **[TinyStories: How Small Can Language Models Be and Still Speak Coherent English?](https://arxiv.org/abs/2305.07759)** (Eldan & Li, Microsoft Research, 2023) · arXiv:2305.07759 — Sub-10M-parameter models trained on a constrained synthetic story corpus can generate coherent, consistent English.
- **[Distilling Step-by-Step! Outperforming Larger LMs with Less Data and Smaller Sizes](https://arxiv.org/abs/2305.02301)** (Hsieh et al., Google, 2023) · arXiv:2305.02301 (Findings of ACL 2023) — Uses LLM-generated rationales as extra supervision so small models beat much larger ones with less data.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Pre-training & Data
- **[The FineWeb Datasets: Decanting the Web for the Finest Text Data at Scale](https://arxiv.org/abs/2406.17557)** (Penedo et al., Hugging Face, 2024) · arXiv:2406.17557 (NeurIPS 2024) — Ablates deduplication and filtering to build a 15T-token open web corpus plus the FineWeb-Edu subset.
- **[The Llama 3 Herd of Models](https://arxiv.org/abs/2407.21783)** (Dubey et al., Meta, 2024) · arXiv:2407.21783 — Documents the pretraining, scaling, and post-training of the Llama 3 family, including the 405B dense flagship.
- **[GPT-4 Technical Report](https://arxiv.org/abs/2303.08774)** (OpenAI, OpenAI, 2023) · arXiv:2303.08774 — A multimodal transformer with human-level exam performance and predictable scaling from small proxy models.
- **[DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437)** (DeepSeek-AI, DeepSeek, 2024) · arXiv:2412.19437 — A 671B MoE (37B active) with MLA, auxiliary-loss-free load balancing, and multi-token prediction, trained efficiently.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Scaling Laws
- **[Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361)** (Kaplan et al., OpenAI, 2020) · arXiv:2001.08361 — Establishes power-law relationships between loss and model size, data, and compute across many orders of magnitude.
- **[Training Compute-Optimal Large Language Models (Chinchilla)](https://arxiv.org/abs/2203.15556)** (Hoffmann et al., DeepMind, 2022) · arXiv:2203.15556 (NeurIPS 2022) — The Chinchilla result: model size and training tokens should scale equally; most large models are undertrained.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Post-training & Alignment
- **[Training Language Models to Follow Instructions with Human Feedback (InstructGPT)](https://arxiv.org/abs/2203.02155)** (Ouyang et al., OpenAI, 2022) · arXiv:2203.02155 (NeurIPS 2022) — Introduces the SFT + reward model + RLHF recipe; a 1.3B tuned model was preferred over 175B GPT-3.
- **[Direct Preference Optimization: Your Language Model Is Secretly a Reward Model](https://arxiv.org/abs/2305.18290)** (Rafailov et al., Stanford, 2023) · arXiv:2305.18290 (NeurIPS 2023) — Replaces the RLHF reward model and PPO loop with a single classification loss on preference pairs.
- **[Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073)** (Bai et al., Anthropic, 2022) · arXiv:2212.08073 — Trains a harmless assistant using AI-generated critiques and preferences guided by written principles (RLAIF).
- **[RLAIF: Scaling RLHF with AI Feedback](https://arxiv.org/abs/2309.00267)** (Lee et al., Google, 2023) · arXiv:2309.00267 (ICML 2024) — Shows LLM-generated preference labels can match human-labeled RLHF across summarization and dialogue tasks.
- **[Chain-of-Thought Prompting Elicits Reasoning in Large Language Models](https://arxiv.org/abs/2201.11903)** (Wei et al., Google, 2022) · arXiv:2201.11903 (NeurIPS 2022) — Intermediate reasoning steps in prompts unlock arithmetic, commonsense, and symbolic reasoning at scale.

<sub>[↑ back to top](#-table-of-contents)</sub>

### RL & Reasoning
- **[Training a Helpful and Harmless Assistant with RLHF](https://arxiv.org/abs/2204.05862)** (Bai et al., Anthropic, 2022) · arXiv:2204.05862 — Applies preference modeling and iterated online RLHF to align an assistant, analyzing the reward/KL trade-off.
- **[DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models](https://arxiv.org/abs/2402.03300)** (Shao et al., DeepSeek, 2024) · arXiv:2402.03300 — Introduces GRPO, a critic-free RL algorithm using group-relative advantages, later central to DeepSeek-R1.
- **[DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948)** (DeepSeek-AI, DeepSeek, 2025) · arXiv:2501.12948 (Nature, 2025) — Elicits reasoning purely via RL (R1-Zero) and distills it into smaller dense models — a key SLM-reasoning recipe.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Parameter-Efficient Fine-tuning
- **[LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685)** (Hu et al., Microsoft, 2021) · arXiv:2106.09685 (ICLR 2022) — Freezes base weights and trains injected low-rank matrices, cutting trainable parameters by orders of magnitude.
- **[QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/abs/2305.14314)** (Dettmers et al., University of Washington, 2023) · arXiv:2305.14314 (NeurIPS 2023) — Backpropagates through a frozen 4-bit (NF4) model into LoRA adapters, finetuning a 65B model on one 48GB GPU.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Distillation & Compression
- **[Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531)** (Hinton et al., Google, 2015) · arXiv:1503.02531 — Foundational knowledge distillation: training a small student on the soft targets of a larger teacher.
- **[Sequence-Level Knowledge Distillation](https://arxiv.org/abs/1606.07947)** (Kim & Rush, Harvard, 2016) · arXiv:1606.07947 (EMNLP 2016) — Extends distillation from token-level to sequence-level, yielding student NMT models ~10x faster with little loss.
- **[DistilBERT: Smaller, Faster, Cheaper and Lighter](https://arxiv.org/abs/1910.01108)** (Sanh et al., Hugging Face, 2019) · arXiv:1910.01108 — Distills BERT during pretraining to a 40% smaller model that retains ~97% of language understanding.
- **[GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers](https://arxiv.org/abs/2210.17323)** (Frantar et al., IST Austria, 2022) · arXiv:2210.17323 (ICLR 2023) — One-shot 3-4 bit weight quantization using approximate second-order information, no retraining required.
- **[AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration](https://arxiv.org/abs/2306.00978)** (Lin et al., MIT, 2023) · arXiv:2306.00978 (MLSys 2024) — Protects a small fraction of salient weights via activation-aware scaling for accurate low-bit quantization.
- **[LLM.int8(): 8-bit Matrix Multiplication for Transformers at Scale](https://arxiv.org/abs/2208.07339)** (Dettmers et al., University of Washington, 2022) · arXiv:2208.07339 (NeurIPS 2022) — Int8 inference for billion-scale transformers with no accuracy loss by isolating emergent outlier features.
- **[SparseGPT: Massive Language Models Can Be Accurately Pruned in One-Shot](https://arxiv.org/abs/2301.00774)** (Frantar & Alistarh, IST Austria, 2023) · arXiv:2301.00774 (ICML 2023) — Prunes GPT-scale models to 50-60% sparsity in one shot without retraining and minimal perplexity increase.

<sub>[↑ back to top](#-table-of-contents)</sub>

---

<h2 id="jobs--careers">💼 Jobs & Careers</h2>

### Frontier Labs (careers pages)
- **[Anthropic Careers](https://www.anthropic.com/careers)** — Frontier lab; alignment, pretraining, RL, and fine-tuning research and engineering roles.
- **[OpenAI Careers](https://openai.com/careers/)** — Frontier lab; research, post-training/RLHF, and applied ML roles.
- **[Google DeepMind Careers](https://deepmind.google/careers/)** — Frontier lab; research scientist and engineering roles across pretraining, RL, and alignment.
- **[Mistral AI Careers](https://mistral.ai/careers/)** — European frontier lab; open-weight model pretraining, fine-tuning, and inference roles.
- **[Hugging Face Careers](https://apply.workable.com/huggingface/)** — Open-source ML platform; ML research/engineering on training, datasets, and model deployment.
- **[DeepSeek Talent](https://talent.deepseek.com)** — AGI-focused lab; pretraining, RL-for-reasoning, and infrastructure roles (official talent portal).

<sub>[↑ back to top](#-table-of-contents)</sub>

### Specialized AI Job Boards
- **[ai-jobs.net](https://aijobs.net/)** — Large dedicated AI/ML/data-science job board with research and engineering filters.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Aggregators
- **[80,000 Hours Job Board](https://jobs.80000hours.org/)** — Curated board emphasizing frontier-lab and AI-safety roles across pretraining, RL, and alignment.

<sub>[↑ back to top](#-table-of-contents)</sub>

### Newsletters & Signals
- **[Import AI](https://jack-clark.net/)** — Weekly research-analysis newsletter (Jack Clark); tracks frontier labs and hiring signals.
- **[Ahead of AI](https://magazine.sebastianraschka.com/)** — Sebastian Raschka's newsletter; deep technical coverage of LLM training and fine-tuning methods.
- **[The Batch (DeepLearning.AI)](https://www.deeplearning.ai/the-batch)** — Weekly AI news/insights from Andrew Ng's team; useful for tracking labs and the talent market.

<sub>[↑ back to top](#-table-of-contents)</sub>

---

<h2 id="learning-roadmap">🗺️ Learning Roadmap</h2>

**Beginner → practitioner (SLM track):**

1. Watch a from-scratch course and train a tiny model (see Courses → Foundations).
2. Fine-tune a small open model with LoRA/QLoRA on your own data (Repos → Fine-tuning).
3. Align it with DPO, then try a GRPO-style RL loop (Repos → Post-training & RL).
4. Evaluate honestly (Repos → Evaluation) and serve it on-device (Repos → Serving).
5. Read the SLM surveys + the model tech reports to understand the design space (Papers).

---

<h2 id="contribute">🤝 Contribute</h2>

This list is **data-driven** — every entry is a few lines of YAML in `data/`.
Adding a resource is a two-line PR; you never touch the README (it's generated).

```bash
# 1. add your entry to the right file, e.g. data/repos.yml
# 2. regenerate + check locally
make check
# 3. open a PR
```

See **[CONTRIBUTING.md](CONTRIBUTING.md)** for the entry schema and the one rule
(every entry needs a working `url`). A weekly Action re-verifies links and refreshes
repo stats automatically.

---

<div align="center">

### ⭐ Star History

<a href="https://star-history.com/#wjlgatech/FM-os&Date">
  <img src="https://api.star-history.com/svg?repos=wjlgatech/FM-os&type=Date" alt="Star history chart" width="600">
</a>

### 🙌 Contributors

<a href="https://github.com/wjlgatech/FM-os/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=wjlgatech/FM-os" alt="Contributors">
</a>

FM-os is maintained by [@wjlgatech](https://github.com/wjlgatech) and the community. Sibling projects: [rsi](https://github.com/wjlgatech/rsi) · [FDE-os](https://github.com/wjlgatech/FDE-os).

<sub>README generated from <code>data/*.yml</code> by <code>scripts/build_readme.py</code> — do not edit by hand.</sub>

</div>
