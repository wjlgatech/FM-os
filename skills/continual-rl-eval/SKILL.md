---
name: continual-rl-eval
description: >-
  Stand up a PERSISTENT (no-reset) reinforcement-learning environment for continual RL:
  world state that carries across episodes, structured non-stationarity (typed failure
  injection + async config shifts), a composite verifier reward, and continual-adaptation
  metrics (adaptation speed, forgetting, recovery, stability, gap-to-upper-bound). Answers
  the real question: is the agent actually learning, or just fitting the first regime?
kind: skill
license: CC0-1.0
runtimes: [claude-code, codex, hermes]
---

# continual-rl-eval

A cross-runtime skill that builds a **continual-RL harness** — a world that never resets, so you
measure durable learning instead of episodic overfitting. It reproduces the load-bearing ideas of
the MORPHEUS continual-RL benchmark as your own runnable tooling, grounded in the RL stack vetted in
[FM-os](https://github.com/wjlgatech/FM-os) (Gymnasium, Verifiers, SkyRL). The point is honest
evaluation: most benchmarks reset after every episode, real operations never do.

## When to use (trigger)

Invoke when the user says "continual RL", "no-reset / persistent environment", "non-stationary
benchmark", "does my agent actually learn", "catastrophic forgetting eval", "continual adaptation",
or "test an agent under drift."

## What it does

1. **Persist the world** — build a Gymnasium-API environment whose state carries across episodes
   and whose actions compound (no reset, no task IDs, no predefined curriculum).
2. **Inject structured non-stationarity** — two knobs, both reproducible: a *failure-injection
   engine* (typed disruptions — `missing_data`, `dependency_failure`, `rate_limit`, … at preset
   rates 5 / 8 / 15 / 30%) and a *config-shift controller* that changes presets on fixed timestamps
   *independent of the training loop*, so the agent can't use update periodicity as a signal.
3. **Score with a composite verifier reward** — combine operational verifiers (failure severity,
   cost-vs-plan ledger ratio clipped to [-1,1], throughput clipped to [0,1]) with explicit weights;
   the reward is evidence-checked, not vibes.
4. **Measure continual adaptation** — six metrics per non-stationary horizon: per-config reward,
   adaptation speed (steps to half the upper bound), **forgetting**, recovery time, stability, and
   gap-to-upper-bound; plus relative-adaptation-advantage and plasticity (effective rank).
5. **Sweep baselines honestly** — PPO / HER / EWC / LCM from one shared SFT checkpoint (frontier
   traces distilled into a small model). Report the null: if no family closes the gap, say so.

## Example

A **runnable reference** ships in [`reference/`](reference/) — pure stdlib Python, no deps, so it
runs anywhere including CI. A persistent warehouse world whose optimal staffing shifts by regime:

```bash
python3 reference/run_demo.py --policy adaptive   # a continual learner   -> PASS (exit 0)
python3 reference/run_demo.py --policy static      # coasts on hard regimes -> FAIL (exit 1)
python3 reference/test_env.py                       # 12 property tests, all green
```

`run_demo.py` drives one policy across a schedule of regime shifts (calm → surge → storm → calm)
applied by the harness on fixed timesteps, and reports per-config reward, gap-to-upper-bound,
recovery, and forgetting. Swap in a real PPO/EWC policy by implementing the same `act`/`update`
interface; the env is Gymnasium-shaped.

## Reference implementation

- `reference/env.py` — the persistent `WarehouseEnv`: no reset, compounding state, failure-injection
  engine (typed failures at 5/8/15/30%), composite verifier reward (failure + ledger + throughput).
- `reference/run_demo.py` — the config-shift harness, two baseline policies (static vs adaptive),
  the continual-adaptation metrics, and the gate.
- `reference/test_env.py` — 12 property tests: persistence, failure-rate accuracy, reward bounds,
  the shifting optimum, and that the gate actually discriminates a learner from a coaster.

## Verification (eval-with-teeth)

A run only "passes" if **the worst regime's gap-to-upper-bound stays under threshold AND forgetting
stays low** — an agent that aces the calm regime but coasts through the hard one is a fail, not a
ship (the `static` baseline fails exactly here). No durable adaptation in the metrics ⇒ no claim of
learning. The gate exits non-zero so it blocks CI, exactly like `agentic-eval`.

## Safety

Operates on the user's own environments / simulations; HTTPS downloads only; no secrets; no
untrusted code executed as part of scoring. Reward weights are declared config, not hidden.

## Cross-runtime

One `SKILL.md`; thin manifests for Claude Code, Codex, and Hermes. Pairs with `agentic-eval` (single
-shot grading) and `curation-loop` (the data half) — this skill is the *did-it-durably-learn* half.
