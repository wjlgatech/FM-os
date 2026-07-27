---
name: personalization-loop
description: >-
  Ship model personalization (per-user memory, preference profiles, custom
  model adaptation) through a four-gate eval harness: measured lift over the
  stateless baseline, cold-start parity, bit-exact cross-user isolation, and
  memory-pays-rent (wrong-user memory must hurt). Personalization that can't
  pass these gates is adaptivity theater, not a personal model.
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# personalization-loop

A cross-runtime skill for the **personal-model half of Personal AGI**: per-user memory
that provably improves each user's experience without leaking across users, regressing
new users, or faking lift through generic adaptivity. The four gates are the eval
harness personalization ships through — at toy scale here, unchanged at product scale.

## When to use (trigger)

Invoke when the user says "personalize the model", "per-user memory", "user preference
profile", "custom models per customer", "does memory actually help", "personalization
without leakage", or "cold-start regression".

## The four gates (each is a measured number)

1. **Lift** — mean per-user reward in steady state must beat the stateless global
   baseline by a floor. No lift ⇒ the memory is dead weight.
2. **Cold-start parity** — a brand-new user (memory = global prior) must never be
   served worse than the baseline. Personalization may only add.
3. **Isolation** — a user's trajectory must be *bit-identical* whether they are the
   only user or one of millions: memory reads/writes key on the user's own data only.
   Tested, not assumed — guards against anyone later adding shared state.
4. **Rent** — the memory *content* must drive the lift: serving user A with user B's
   memory must underperform the stateless baseline. If wrong memory doesn't hurt, the
   "personalization" was never personal.

## Example

```bash
# self-contained proof (numpy only): online per-user memory beats stateless,
# cold-start parity exact, leakage 0.0, wrong-user memory hurts — exit non-zero otherwise
python reference/personal_memory_demo.py
# offline gate:
python -m pytest reference/test_personal_memory_demo.py -q
```

```python
from reference.personal_memory_demo import run_cohort, leakage, gate_cohort
r = run_cohort()
ok, reasons = gate_cohort(r, leakage())   # lift +0.55 · cold-start 0.00 · leak 0.0 · rent −0.11
assert ok, reasons
```

## Discipline (why this is trustworthy)

- **Adaptivity ≠ personalization** — the rent gate kills the classic false positive
  (any online learner "improves"; only real memory content helps *this* user).
- **Privacy is a graded property** — isolation is asserted at bit level in CI, not
  promised in a doc.
- **Scale seam** — swap the linear scorer for a reranker / LoRA-per-user / system-prompt
  memory (MemGPT-style); the four gates and the harness are unchanged.

## Deeper reference (FM-os knowledge base)

Packer et al., *MemGPT* (memory-augmented personal models) · Ouyang et al.,
*InstructGPT* — in [`data/papers.yml`](../../data/papers.yml) · siblings:
[`product-rl-loop`](../product-rl-loop/) (the RL × product half),
[`vector-rag`](../vector-rag/) (retrieval memory), [`agentic-eval`](../agentic-eval/)
(eval gates). JD dossier:
[`docs/jd-fit/openai-personal-agi.md`](../../docs/jd-fit/openai-personal-agi.md).
