#!/usr/bin/env python3
"""Gate for the Thomson-1 stack reconstruction + its pre-registered predictions.

Two files, one discipline:

  data/thomson_stack.yml  — the reverse-engineered pipeline, every stage tagged
                            published | stated | inferred.
  data/predictions.yml    — falsifiable claims registered BEFORE the technical
                            report exists, scored by Brier once it does.

The rule that makes the reconstruction honest: **an `inferred` stage must carry
a matching prediction id.** Anything we made up has to be written down as a
checkable bet. A guess with no bet attached fails this gate.

Scoring is equally strict: an UNRESOLVED prediction is excluded from the Brier
score and reported as unresolved — it is never quietly counted as a win.

  python3 scripts/thomson.py            # validate + report coverage
  python3 scripts/thomson.py --score    # also compute the Brier score
"""
from __future__ import annotations

import argparse
import sys

from fmos import load

TIERS = ("published", "stated", "inferred")
STACK_REQUIRED = ("id", "stage", "mechanism", "evidence", "owner", "source", "detail")
PRED_REQUIRED = (
    "id", "claim", "probability", "rationale",
    "resolution_criteria", "resolves_by", "resolver", "stage",
)


def check_stack(stack: list) -> tuple[list[str], set[str]]:
    """Validate every stage row; return (errors, stage ids)."""
    errors: list[str] = []
    ids: set[str] = set()
    if not isinstance(stack, list) or not stack:
        return ["thomson_stack.yml: expected a non-empty list"], ids

    for i, row in enumerate(stack):
        where = f"thomson_stack.yml[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{where}: entry must be a mapping")
            continue
        for field in STACK_REQUIRED:
            if not row.get(field):
                errors.append(f"{where}: missing required field '{field}'")
        sid = str(row.get("id", ""))
        if sid in ids:
            errors.append(f"{where}: duplicate stage id {sid!r}")
        ids.add(sid)

        tier = row.get("evidence")
        if tier not in TIERS:
            errors.append(f"{where}: evidence must be one of {TIERS}, got {tier!r}")

        src = str(row.get("source", ""))
        if src and not src.startswith(("http://", "https://")):
            errors.append(f"{where}: source must be a URL — got {src!r}")

    return errors, ids


def check_predictions(doc: dict, stage_ids: set[str]) -> tuple[list[str], list[dict]]:
    """Validate the prediction ledger; return (errors, prediction rows)."""
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["predictions.yml: top level must be a mapping"], []
    if not doc.get("registered"):
        errors.append("predictions.yml: missing 'registered' date")

    preds = doc.get("predictions") or []
    if not isinstance(preds, list) or not preds:
        return errors + ["predictions.yml: expected a non-empty 'predictions' list"], []

    seen: set[str] = set()
    for i, row in enumerate(preds):
        where = f"predictions.yml[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{where}: entry must be a mapping")
            continue
        for field in PRED_REQUIRED:
            if row.get(field) in (None, "", []):
                errors.append(f"{where}: missing required field '{field}'")

        pid = str(row.get("id", ""))
        if pid in seen:
            errors.append(f"{where}: duplicate prediction id {pid!r}")
        seen.add(pid)

        prob = row.get("probability")
        if not isinstance(prob, (int, float)) or isinstance(prob, bool):
            errors.append(f"{where}: probability must be a number, got {prob!r}")
        elif not 0.0 < float(prob) < 1.0:
            # 0 and 1 are not forecasts — they are claims of certainty, and they
            # make the Brier score degenerate. Refuse them.
            errors.append(f"{where}: probability must be strictly between 0 and 1, got {prob}")

        stage = row.get("stage")
        if stage and stage not in stage_ids:
            errors.append(f"{where}: stage {stage!r} is not a stage in thomson_stack.yml")

        outcome = row.get("outcome", None)
        if outcome not in (None, True, False):
            errors.append(f"{where}: outcome must be null, true, or false — got {outcome!r}")
        if outcome in (True, False) and not row.get("resolved_by"):
            # No citation, no resolution. This is the whole point of the ledger.
            errors.append(f"{where}: outcome is set but 'resolved_by' citation is missing")

    return errors, preds


def check_inferred_have_bets(stack: list, preds: list) -> list[str]:
    """Every `inferred` stage must name a prediction, and that id must exist."""
    pred_ids = {str(p.get("id")) for p in preds if isinstance(p, dict)}
    errors: list[str] = []
    for row in stack:
        if not isinstance(row, dict):
            continue
        named = row.get("prediction")
        if row.get("evidence") == "inferred" and not named:
            errors.append(
                f"thomson_stack.yml[{row.get('id')}]: evidence is 'inferred' but no "
                "prediction id is attached — a guess must be a registered bet"
            )
        if named and str(named) not in pred_ids:
            errors.append(
                f"thomson_stack.yml[{row.get('id')}]: prediction {named!r} not found "
                "in predictions.yml"
            )
    return errors


def brier(preds: list) -> tuple[float | None, int, int]:
    """Brier score over RESOLVED predictions only.

    Returns (score, n_resolved, n_unresolved). Score is None when nothing has
    resolved yet — an empty ledger scores nothing, it does not score perfectly.
    """
    resolved = [p for p in preds if p.get("outcome") in (True, False)]
    unresolved = len(preds) - len(resolved)
    if not resolved:
        return None, 0, unresolved
    total = sum((float(p["probability"]) - (1.0 if p["outcome"] else 0.0)) ** 2 for p in resolved)
    return total / len(resolved), len(resolved), unresolved


def report(stack: list, preds: list, show_score: bool) -> None:
    """Print the coverage table and, optionally, the Brier score."""
    counts = {t: sum(1 for r in stack if r.get("evidence") == t) for t in TIERS}
    total = len(stack)
    print(f"Thomson-1 stack reconstruction — {total} stages")
    for tier in TIERS:
        pct = 100.0 * counts[tier] / total if total else 0.0
        print(f"  {tier:<10} {counts[tier]:>2}  ({pct:.0f}%)")
    grounded = counts["published"] + counts["stated"]
    print(f"  → {grounded}/{total} stages rest on a primary source, not on our reading.")

    print(f"\nPrediction ledger — {len(preds)} registered claims")
    score, n_res, n_unres = brier(preds)
    if show_score:
        if score is None:
            print(f"  Brier: UNSCORED — 0 resolved, {n_unres} awaiting the technical report.")
            print("  (An unresolved ledger is not a perfect ledger.)")
        else:
            print(f"  Brier: {score:.4f} over {n_res} resolved ({n_unres} unresolved, excluded)")
            print("  Reference: 0.25 = always guessing 0.5. Lower is better.")
    else:
        print(f"  {n_res} resolved · {n_unres} awaiting resolution")


def main() -> int:
    """Validate both files, enforce the inferred-needs-a-bet rule, report."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--score", action="store_true", help="compute the Brier score")
    args = ap.parse_args()

    stack = load("thomson_stack")
    doc = load("predictions")

    errors, stage_ids = check_stack(stack)
    pred_errors, preds = check_predictions(doc if isinstance(doc, dict) else {}, stage_ids)
    errors += pred_errors
    if stack and preds:
        errors += check_inferred_have_bets(stack, preds)

    if errors:
        print("Thomson stack gate FAILED:", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1

    report(stack, preds, args.score)
    print("\nThomson stack gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
