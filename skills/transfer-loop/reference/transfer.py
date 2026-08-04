#!/usr/bin/env python3
"""Score whether a lesson learned at one engagement actually transfers to others.

The failure this exists to prevent: a lesson is extracted from the same data that
motivated it, so it always looks true. That is overfitting wearing project-management
vocabulary. The fix is not more care — it is holding out *engagements* (never rows) and
requiring a directional prediction registered before the test.

Verdicts, and why each is separate:
    TRANSFERS         helped the held-out engagements by at least the predicted effect
    LOCAL-ONLY        helped the source and not elsewhere — keep it as a note on that
                      engagement, never promote it to a default
    NEGATIVE-TRANSFER hurt the held-out engagements. Worth more than a pass, because a
                      default would have quietly cost you everywhere else.
    NOT-MEASURED      no prediction, or too few held-out engagements. Never a pass.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass

TRANSFERS = "TRANSFERS"
LOCAL_ONLY = "LOCAL-ONLY"
NEGATIVE = "NEGATIVE-TRANSFER"
NOT_MEASURED = "NOT-MEASURED"

MIN_HELD_OUT = 2


@dataclass
class Lesson:
    """A candidate default. The fields are the pre-registration."""
    name: str
    source: str                  # the engagement it was found in
    metric: str
    direction: str               # "up" or "down" — which way is better
    min_effect: float            # smallest change worth promoting a default for
    predicted_before: bool       # was this registered BEFORE the held-out test?

    def signed(self, delta: float) -> float:
        """Improvement as a positive number, whichever way the metric is good."""
        if self.direction not in ("up", "down"):
            raise ValueError("direction must be 'up' or 'down'")
        return delta if self.direction == "up" else -delta


def evaluate(lesson: Lesson, baseline: dict[str, float],
             treatment: dict[str, float]) -> dict:
    """baseline/treatment: {engagement_id: metric_value}. Held-out = every engagement
    that is NOT the source, so the split is by engagement rather than by row."""
    shared = set(baseline) & set(treatment)
    held_out = sorted(shared - {lesson.source})
    reasons: list[str] = []

    def improvement(eid: str) -> float:
        return lesson.signed(treatment[eid] - baseline[eid])

    source_lift = improvement(lesson.source) if lesson.source in shared else None
    lifts = {e: improvement(e) for e in held_out}
    mean_lift = sum(lifts.values()) / len(lifts) if lifts else None

    # 1. A prediction made after seeing the result is not a prediction.
    if not lesson.predicted_before:
        return _out(NOT_MEASURED, lesson, source_lift, lifts, mean_lift,
                    ["the prediction was not registered before the test — a lesson "
                     "scored against the data that produced it cannot fail"])

    # 2. Nowhere else to test it is not evidence of generality.
    if len(held_out) < MIN_HELD_OUT:
        return _out(NOT_MEASURED, lesson, source_lift, lifts, mean_lift,
                    [f"only {len(held_out)} held-out engagement(s); {MIN_HELD_OUT} "
                     f"required. Source-side improvement cannot substitute."])

    # 3. Negative transfer outranks everything: a harmful default is the finding.
    if mean_lift is not None and mean_lift < -1e-12:
        hurt = [e for e, v in lifts.items() if v < 0]
        return _out(NEGATIVE, lesson, source_lift, lifts, mean_lift,
                    [f"held-out mean {mean_lift:+.3f} on {lesson.metric}; hurt "
                     f"{len(hurt)}/{len(lifts)} engagement(s): {', '.join(hurt)}"])

    if mean_lift is not None and mean_lift >= lesson.min_effect:
        return _out(TRANSFERS, lesson, source_lift, lifts, mean_lift,
                    [f"held-out mean {mean_lift:+.3f} >= predicted {lesson.min_effect:+.3f}"])

    detail = (f"held-out mean {mean_lift:+.3f} < predicted {lesson.min_effect:+.3f}")
    if source_lift is not None and source_lift >= lesson.min_effect:
        detail += (f", while the source gained {source_lift:+.3f} — the signature of a "
                   f"lesson fitted to where it was found")
    return _out(LOCAL_ONLY, lesson, source_lift, lifts, mean_lift, [detail])


def _out(verdict, lesson, source_lift, lifts, mean_lift, reasons) -> dict:
    return {"verdict": verdict, "lesson": lesson.name, "metric": lesson.metric,
            "source": lesson.source, "source_lift": source_lift,
            "held_out_lifts": lifts, "held_out_mean": mean_lift,
            "promote": verdict == TRANSFERS, "reasons": reasons}


def report(r: dict) -> str:
    lines = [f"── {r['lesson']} ({r['metric']}) ──"]
    src = "n/a" if r["source_lift"] is None else f"{r['source_lift']:+.3f}"
    lines.append(f"  source ({r['source']}): {src}   [reported, never decisive]")
    for e, v in sorted(r["held_out_lifts"].items()):
        lines.append(f"  held out {e:<18} {v:+.3f}")
    mean = "n/a" if r["held_out_mean"] is None else f"{r['held_out_mean']:+.3f}"
    lines.append(f"  held-out mean: {mean}")
    lines.append(f"  VERDICT: {r['verdict']}   promote={r['promote']}")
    for x in r["reasons"]:
        lines.append(f"    - {x}")
    return "\n".join(lines)


if __name__ == "__main__":
    base = {"eng-a": 0.60, "eng-b": 0.55, "eng-c": 0.58, "eng-d": 0.62}

    real = Lesson("retry-429-with-jitter", "eng-a", "task_success", "up", 0.05, True)
    good = {"eng-a": 0.72, "eng-b": 0.64, "eng-c": 0.66, "eng-d": 0.70}

    local = Lesson("hardcode-eng-a-schema", "eng-a", "task_success", "up", 0.05, True)
    local_t = {"eng-a": 0.78, "eng-b": 0.555, "eng-c": 0.585, "eng-d": 0.625}

    harmful = Lesson("always-retry-3x", "eng-a", "task_success", "up", 0.05, True)
    harmful_t = {"eng-a": 0.70, "eng-b": 0.48, "eng-c": 0.50, "eng-d": 0.54}

    posthoc = Lesson("communicate-more-clearly", "eng-a", "task_success", "up", 0.05, False)

    cases = [(real, good), (local, local_t), (harmful, harmful_t), (posthoc, good)]
    results = [evaluate(l, base, t) for l, t in cases]
    for r in results:
        print(report(r))
        print()

    expected = [TRANSFERS, LOCAL_ONLY, NEGATIVE, NOT_MEASURED]
    got = [r["verdict"] for r in results]
    if got != expected:
        print(f"✗ gate misbehaved: expected {expected}, got {got}")
        sys.exit(1)
    print("✓ promotes a real transfer; refuses a source-only win, a harmful default, "
          "and a lesson registered after the fact")
