#!/usr/bin/env python3
"""What can a study of this size actually see? — confidence intervals and MDE.

Written 2026-08-14, the day this repo caught itself publishing an unsupported
NEGATIVE (`syndata-bare` called a claim refuted on 0 events in 18 trials). The
standing rule that came out of it — *a rate without its n is an opinion* — needs
a tool, or it stays a slogan.

Three functions, one job each:

  rule_of_three(n)          the zero-event case: 0 in n ⇒ 95% CI [0, 3/n]
  wilson(k, n)              a proportion's 95% CI, correct near 0 and 1 where the
                            normal approximation quietly fails
  mde_two_proportions(...)  the smallest DIFFERENCE two arms of size n could
                            detect — the number that decides whether "A is more
                            susceptible than B" is a finding or a coin flip

Wilson rather than the textbook normal interval on purpose: at k=0 or k=n the
normal interval has zero width, which reports perfect certainty exactly where
there is least evidence.

  python3 scripts/power.py --rate 196 1152 --label "runs that skipped the tool"
  python3 scripts/power.py --mde 288 --baseline 0.5
  python3 scripts/power.py --intern-report
"""
from __future__ import annotations

import argparse
import math

Z95 = 1.959963984540054   # two-sided alpha = 0.05
Z80 = 0.8416212335729143  # power = 0.80


def rule_of_three(n: int) -> float | None:
    """95% upper bound on a rate after ZERO observed events (Hanley 1983)."""
    return None if n <= 0 else 3.0 / n


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    """95% Wilson score interval for k successes in n trials."""
    if n <= 0:
        raise ValueError("n must be positive")
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z / denom * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return max(0.0, centre - half), min(1.0, centre + half)


def mde_two_proportions(n_per_arm: int, baseline: float = 0.5,
                        z_alpha: float = Z95, z_beta: float = Z80) -> float:
    """Smallest difference in proportions two arms of `n_per_arm` can detect.

    delta = (z_alpha + z_beta) * sqrt(2 * p(1-p) / n)

    The pooled approximation, which is the right level of precision for a design
    question: whether a study needed 10 points or 30 points of separation is the
    decision, and no second decimal changes it.
    """
    if n_per_arm <= 0:
        raise ValueError("n_per_arm must be positive")
    return (z_alpha + z_beta) * math.sqrt(2 * baseline * (1 - baseline) / n_per_arm)


def n_for_mde(delta: float, baseline: float = 0.5,
              z_alpha: float = Z95, z_beta: float = Z80) -> int:
    """Runs per arm needed to detect a difference of `delta`."""
    if not 0 < delta < 1:
        raise ValueError("delta must be in (0, 1)")
    return math.ceil((z_alpha + z_beta) ** 2 * 2 * baseline * (1 - baseline) / delta ** 2)


def describe_rate(k: int, n: int, label: str = "") -> str:
    lo, hi = wilson(k, n)
    width = (hi - lo) * 100
    head = f"{label}: " if label else ""
    if k == 0:
        r3 = rule_of_three(n)
        return (f"{head}0/{n} — 95% CI [0, {r3:.1%}] (rule of three). "
                f"Zero events is not a zero rate.")
    return (f"{head}{k}/{n} = {k / n:.1%} — 95% CI [{lo:.1%}, {hi:.1%}], "
            f"width {width:.1f} points")


# ── the intern report, scored ────────────────────────────────────────────────
def intern_report() -> int:
    """Apply the above to the 2026-08-14 Agent Assurance intern study.

    Design as reported: 2 architectures x 2 models x 24 tasks x 4 prompting
    strategies x 3 repetitions = 1,152 runs (arithmetic checks out exactly).

    The aggregate rates are well supported. The claim that needs the most care is
    the strategic one — that architectures differ in attack susceptibility —
    because it is a DIFFERENCE, and differences need far more n than rates.
    """
    print("Agent Assurance intern study — what the reported n supports")
    print("=" * 74)
    print("Design: 2 arch x 2 models x 24 tasks x 4 prompts x 3 reps = "
          f"{2 * 2 * 24 * 4 * 3} runs\n")

    print("Reported rates, with the interval the design earns:")
    print("  " + describe_rate(196, 1152, "~17% never invoked the expected tool"))
    print("  " + describe_rate(45, 196, "~23% of those still correct"))
    print("  (both recomputed from the reported percentages; exact counts were "
          "not in the report)\n")

    print("The claim that needs more n — 'architectures differ in susceptibility':")
    print("  A difference needs roughly 4x the sample a rate does. Because the")
    print("  adversarial subset size was not reported, here is the whole curve.\n")
    print(f"  {'runs per arm':>14} {'smallest detectable difference':>34}")
    for n in (36, 72, 144, 288, 576):
        print(f"  {n:>14} {mde_two_proportions(n):>33.1%}")
    print()
    print(f"  To resolve a 10-point difference: {n_for_mde(0.10)} runs per arm.")
    print(f"  To resolve a  5-point difference: {n_for_mde(0.05)} runs per arm.")
    print()
    print("  Read this as a design note, not a correction: nothing above says the")
    print("  architectures do NOT differ. It says a difference smaller than the")
    print("  detectable threshold cannot be told from noise by this design — and")
    print("  the report's own framing (susceptibility 'cannot be generalized')")
    print("  is the claim most worth protecting with the extra runs.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rate", nargs=2, type=int, metavar=("K", "N"),
                    help="k successes in n trials -> 95%% CI")
    ap.add_argument("--label", default="", help="label for --rate")
    ap.add_argument("--mde", type=int, metavar="N_PER_ARM",
                    help="smallest detectable difference at this arm size")
    ap.add_argument("--baseline", type=float, default=0.5,
                    help="assumed baseline proportion for --mde (default 0.5, the worst case)")
    ap.add_argument("--intern-report", action="store_true",
                    help="score the 2026-08-14 Agent Assurance intern study")
    args = ap.parse_args()

    if args.intern_report:
        return intern_report()
    if args.rate:
        print(describe_rate(args.rate[0], args.rate[1], args.label))
        return 0
    if args.mde:
        d = mde_two_proportions(args.mde, args.baseline)
        print(f"{args.mde} per arm at baseline {args.baseline:.0%}: "
              f"smallest detectable difference {d:.1%}")
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
