"""Gate tests for the Thomson-1 stack reconstruction + prediction ledger.

The rules under test are the ones that stop a reverse-engineering from quietly
becoming fan fiction: every stage carries an evidence tier, every guess carries
a registered bet, every resolved prediction carries a citation, and an
unresolved ledger scores nothing rather than scoring perfectly.
"""
from __future__ import annotations

import pytest

import thomson as th
from fmos import load

STACK = load("thomson_stack")
LEDGER = load("predictions")
PREDS = LEDGER["predictions"]


# ── the shipped data must pass its own gate ──────────────────────────────────


def test_shipped_stack_and_ledger_validate():
    """The committed files pass every check the gate makes."""
    errors, stage_ids = th.check_stack(STACK)
    pred_errors, preds = th.check_predictions(LEDGER, stage_ids)
    errors += pred_errors
    errors += th.check_inferred_have_bets(STACK, preds)
    assert not errors, "\n".join(errors)


def test_every_stage_has_a_recognized_evidence_tier():
    """No stage may ship without declaring how well it is evidenced."""
    for row in STACK:
        assert row["evidence"] in th.TIERS, f"{row['id']}: {row['evidence']!r}"


def test_every_stage_cites_a_url():
    """A tier is a claim about a source, so the source must be reachable."""
    for row in STACK:
        assert str(row["source"]).startswith("https://"), row["id"]


def test_no_unresolved_prediction_is_treated_as_correct():
    """Nothing is resolved yet, so the Brier score must be None — not 0.0."""
    score, n_resolved, n_unresolved = th.brier(PREDS)
    assert score is None
    assert n_resolved == 0
    assert n_unresolved == len(PREDS)


def test_ledger_contains_genuine_uncertainty():
    """A ledger with no coin-flips is one that was tuned after the fact."""
    probs = [p["probability"] for p in PREDS]
    assert min(probs) < 0.5 < max(probs)
    assert any(0.4 <= p <= 0.6 for p in probs), "no genuinely uncertain claim registered"


# ── the rules, exercised against synthetic violations ────────────────────────


def test_inferred_stage_without_a_bet_is_rejected():
    """THE CORE RULE: a guess with no registered prediction fails the gate."""
    bad = [{"id": "made-up", "evidence": "inferred", "stage": "s",
            "mechanism": "m", "owner": "o", "source": "https://x", "detail": "d"}]
    errors = th.check_inferred_have_bets(bad, PREDS)
    assert any("no prediction id is attached" in e for e in errors)


def test_stage_naming_a_missing_prediction_is_rejected():
    """A stage may not point at a bet that was never registered."""
    bad = [{"id": "s1", "evidence": "published", "prediction": "P99-nonexistent",
            "stage": "s", "mechanism": "m", "owner": "o",
            "source": "https://x", "detail": "d"}]
    errors = th.check_inferred_have_bets(bad, PREDS)
    assert any("not found" in e for e in errors)


@pytest.mark.parametrize("prob", [0.0, 1.0, 1.5, -0.2, "high", True])
def test_certainty_is_not_a_forecast(prob):
    """Probabilities of exactly 0 or 1 (or non-numbers) are refused."""
    doc = {"registered": "2026-08-13", "predictions": [dict(
        id="X", claim="c", probability=prob, rationale="r",
        resolution_criteria="rc", resolves_by="2026-12-31",
        resolver="report", stage="base-selection", outcome=None)]}
    errors, _ = th.check_predictions(doc, {"base-selection"})
    assert any("probability" in e for e in errors)


def test_resolved_outcome_requires_a_citation():
    """An outcome may only be set from a cited source, never from memory."""
    doc = {"registered": "2026-08-13", "predictions": [dict(
        id="X", claim="c", probability=0.6, rationale="r",
        resolution_criteria="rc", resolves_by="2026-12-31",
        resolver="report", stage="base-selection",
        outcome=True, resolved_by=None)]}
    errors, _ = th.check_predictions(doc, {"base-selection"})
    assert any("resolved_by" in e for e in errors)


def test_prediction_must_point_at_a_real_stage():
    """Predictions are anchored to the stack, so orphans are rejected."""
    doc = {"registered": "2026-08-13", "predictions": [dict(
        id="X", claim="c", probability=0.6, rationale="r",
        resolution_criteria="rc", resolves_by="2026-12-31",
        resolver="report", stage="not-a-stage", outcome=None)]}
    errors, _ = th.check_predictions(doc, {"base-selection"})
    assert any("not a stage" in e for e in errors)


def test_duplicate_prediction_ids_are_rejected():
    """Two bets under one id would make the Brier score ambiguous."""
    row = dict(id="X", claim="c", probability=0.6, rationale="r",
               resolution_criteria="rc", resolves_by="2026-12-31",
               resolver="report", stage="base-selection", outcome=None)
    doc = {"registered": "2026-08-13", "predictions": [row, dict(row)]}
    errors, _ = th.check_predictions(doc, {"base-selection"})
    assert any("duplicate prediction id" in e for e in errors)


# ── the scorer ───────────────────────────────────────────────────────────────


def test_brier_arithmetic_is_pinned_by_hand():
    """Hand-computed: (0.8-1)^2 + (0.3-0)^2 = 0.04 + 0.09 = 0.13; /2 = 0.065."""
    preds = [
        {"probability": 0.8, "outcome": True},
        {"probability": 0.3, "outcome": False},
    ]
    score, n_res, n_unres = th.brier(preds)
    assert score == pytest.approx(0.065)
    assert (n_res, n_unres) == (2, 0)


def test_brier_excludes_unresolved_rather_than_crediting_them():
    """An unresolved claim must not move the score in either direction."""
    preds = [
        {"probability": 0.8, "outcome": True},
        {"probability": 0.3, "outcome": False},
        {"probability": 0.99, "outcome": None},
    ]
    score, n_res, n_unres = th.brier(preds)
    assert score == pytest.approx(0.065)
    assert (n_res, n_unres) == (2, 1)


def test_perfect_and_worst_case_scores():
    """Sanity bounds: a perfect ledger approaches 0, an inverted one approaches 1."""
    good, _, _ = th.brier([{"probability": 0.99, "outcome": True}])
    bad, _, _ = th.brier([{"probability": 0.99, "outcome": False}])
    assert good < 0.001 < 0.9 < bad
