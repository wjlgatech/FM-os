#!/usr/bin/env python3
"""Gate a human-AI interaction study on whether its DESIGN can support its claim.

An ML benchmark's measuring instrument is deterministic. A user study's instrument is
people, so a result can be void for reasons a benchmark never faces: too few
participants to detect the effect, an order that confounds the condition, or a headline
metric chosen after seeing the data.

Each is checkable BEFORE anyone is recruited, so each is a gate here. The discipline is
FM-os's: no evidence ⇒ No. A design that cannot support a claim returns NOT-MEASURED —
never a fake pass, and never a fake failure.
"""
from __future__ import annotations

import math
import sys
from dataclasses import dataclass, field
from itertools import permutations

# Two-sided normal-approximation quantiles. Kept explicit rather than importing scipy so
# the reference demo is keyless AND dependency-free; the tests pin the results against
# the textbook answers, so a drift here fails loudly.
_Z = {0.10: 1.2815515655446004, 0.05: 1.9599639845400545, 0.01: 2.5758293035489004}
_Z_POWER = {0.80: 0.8416212335729143, 0.90: 1.2815515655446004, 0.95: 1.6448536269514722}

SUPPORTED, UNDERPOWERED, CONFOUNDED, NOT_MEASURED = (
    "SUPPORTED", "UNDERPOWERED", "CONFOUNDED", "NOT-MEASURED")


def required_n_per_arm(effect_size: float, alpha: float = 0.05, power: float = 0.80) -> int:
    """N per arm for a two-sample comparison of means (Cohen's d).

        n = ceil( 2 (z_{1-α/2} + z_{power})² / d² ) + 1

    The closed form is the NORMAL approximation; the exact requirement uses the
    noncentral t and is about one participant per arm higher. The `+ 1` recovers it, and
    is not a fudge factor — it reproduces the conventional (G*Power) answers exactly
    across the canonical cases, all three pinned in the tests:

        d=0.5, α=.05, power=.80 →  64   (normal approximation alone gives 63)
        d=0.8                   →  26                                    (25)
        d=0.2                   → 394                                   (393)

    Rounding toward MORE participants is also the only safe direction for a gate: one
    participant too many costs a little recruiting, while one too few is a false pass —
    exactly the failure this module exists to prevent.
    """
    if effect_size <= 0:
        raise ValueError("effect_size must be > 0 — 'we expect some difference' is not a design")
    if alpha not in _Z:
        raise ValueError(f"alpha must be one of {sorted(_Z)}")
    if power not in _Z_POWER:
        raise ValueError(f"power must be one of {sorted(_Z_POWER)}")
    n = 2 * (_Z[alpha] + _Z_POWER[power]) ** 2 / effect_size ** 2
    return math.ceil(n) + 1  # noncentral-t correction; see the docstring


@dataclass
class StudyDesign:
    """A pre-registerable design. Missing fields are the point — they cause refusal."""
    name: str
    primary_metric: str | None = None          # exactly ONE, named in advance
    effect_size: float | None = None           # the smallest effect worth detecting
    planned_n_per_arm: int | None = None
    arms: int = 2
    alpha: float = 0.05
    power: float = 0.80
    within_subjects: bool = False
    condition_orders: list[tuple[str, ...]] = field(default_factory=list)
    secondary_metrics: list[str] = field(default_factory=list)


def counterbalance_ok(design: StudyDesign) -> tuple[bool, str]:
    """Within-subjects designs must balance condition ORDER, or order confounds it.

    Balanced = every condition appears in every position equally often across the
    declared orders (a Latin square satisfies this; 'everyone sees A then B' does not).
    """
    if not design.within_subjects:
        return True, "between-subjects — order effects not applicable"
    orders = design.condition_orders
    if not orders:
        return False, "within-subjects but no condition_orders declared"
    k = len(orders[0])
    if any(len(o) != k for o in orders):
        return False, "condition_orders have inconsistent lengths"
    conditions = set(orders[0])
    if any(set(o) != conditions for o in orders):
        return False, "condition_orders do not all cover the same conditions"
    # position → Counter of conditions
    for pos in range(k):
        seen: dict[str, int] = {}
        for o in orders:
            seen[o[pos]] = seen.get(o[pos], 0) + 1
        if len(set(seen.values())) != 1 or len(seen) != len(conditions):
            worst = ", ".join(f"{c}×{n}" for c, n in sorted(seen.items()))
            return False, f"position {pos + 1} is imbalanced ({worst})"
    return True, f"balanced across {len(orders)} orders of {k} conditions"


def gate(design: StudyDesign) -> dict:
    """Return the verdict plus the arithmetic, so a reviewer can check it by hand."""
    reasons: list[str] = []

    # 1. Is this even a design? Refuse rather than guess a default.
    missing = [f for f, v in (("primary_metric", design.primary_metric),
                              ("effect_size", design.effect_size),
                              ("planned_n_per_arm", design.planned_n_per_arm)) if not v]
    if missing:
        return {"verdict": NOT_MEASURED, "required_n_per_arm": None,
                "reasons": [f"design is incomplete: missing {', '.join(missing)}"
                            " — a study cannot be gated on intentions"],
                "counterbalance": counterbalance_ok(design)[1],
                "exploratory": design.secondary_metrics}

    need = required_n_per_arm(design.effect_size, design.alpha, design.power)

    # 2. Order effects void the comparison regardless of N — check before power.
    cb_ok, cb_note = counterbalance_ok(design)
    if not cb_ok:
        reasons.append(f"order confound: {cb_note}")

    # 3. Power.
    if design.planned_n_per_arm < need:
        reasons.append(
            f"underpowered: {design.planned_n_per_arm}/arm planned, {need}/arm needed to "
            f"detect d={design.effect_size} at alpha={design.alpha}, power={design.power}")

    verdict = (CONFOUNDED if not cb_ok
               else UNDERPOWERED if design.planned_n_per_arm < need
               else SUPPORTED)
    if verdict == SUPPORTED:
        reasons.append(f"{design.planned_n_per_arm}/arm ≥ {need}/arm required; {cb_note}")
    return {"verdict": verdict, "required_n_per_arm": need, "reasons": reasons,
            "counterbalance": cb_note, "exploratory": design.secondary_metrics}


def latin_square(conditions: list[str]) -> list[tuple[str, ...]]:
    """A balanced order set for within-subjects designs (cyclic Latin square)."""
    k = len(conditions)
    return [tuple(conditions[(i + j) % k] for j in range(k)) for i in range(k)]


def report(design: StudyDesign, result: dict) -> str:
    lines = [f"── {design.name} ──",
             f"  primary metric : {design.primary_metric or '(none declared)'}",
             f"  effect size    : d={design.effect_size}" if design.effect_size else
             "  effect size    : (none declared)",
             f"  N per arm      : planned {design.planned_n_per_arm} · "
             f"required {result['required_n_per_arm']}",
             f"  counterbalance : {result['counterbalance']}"]
    if design.secondary_metrics:
        lines.append(f"  exploratory    : {', '.join(design.secondary_metrics)}"
                     "  (cannot carry the headline)")
    lines.append(f"  VERDICT        : {result['verdict']}")
    for r in result["reasons"]:
        lines.append(f"    - {r}")
    return "\n".join(lines)


if __name__ == "__main__":
    # A well-powered, counterbalanced design passes.
    good = StudyDesign(name="agent-vs-baseline (well-powered)",
                       primary_metric="task_success_rate", effect_size=0.5,
                       planned_n_per_arm=64, within_subjects=True,
                       condition_orders=latin_square(["agent", "baseline"]),
                       secondary_metrics=["trust_rating", "time_on_task"])
    # The classic: n=12 per arm, reported as a finding.
    small = StudyDesign(name="agent-vs-baseline (n=12, the classic)",
                        primary_metric="task_success_rate", effect_size=0.5,
                        planned_n_per_arm=12)
    # Everyone sees the AI second: practice and fatigue, not the AI.
    confounded = StudyDesign(name="agent-vs-baseline (fixed order)",
                             primary_metric="task_success_rate", effect_size=0.5,
                             planned_n_per_arm=64, within_subjects=True,
                             condition_orders=[("baseline", "agent")])
    # No pre-registered metric at all.
    vague = StudyDesign(name="we'll see what's significant")

    results = [(d, gate(d)) for d in (good, small, confounded, vague)]
    for d, r in results:
        print(report(d, r))
        print()
    expected = [SUPPORTED, UNDERPOWERED, CONFOUNDED, NOT_MEASURED]
    got = [r["verdict"] for _, r in results]
    if got != expected:
        print(f"✗ gate misbehaved: expected {expected}, got {got}")
        sys.exit(1)
    print("✓ the gate passes a sound design and refuses underpowered, confounded, "
          "and unpre-registered ones")
