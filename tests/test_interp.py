"""Gate tests for the interpretability & alignment claim ledger.

The rules under test all defend one property: you cannot tell a checked claim
from an unchecked one by reading it, so the ledger has to make the difference
structural. Every test below is a way the difference could be erased quietly —
a correction that corrects nothing, an "unverified" that smuggles a source, a
wrong correction deleted after the fact, a claim that was true when someone
last looked and has not been looked at since.
"""
from __future__ import annotations

import copy
import datetime as dt

import interp
from fmos import load

DOC = load("interp_ledger")
CLAIMS = DOC["claims"]
TODAY = dt.date(2026, 8, 27)


def mutate(**patch) -> dict:
    """A copy of the shipped ledger with one claim altered — mutation testing:
    a gate that never fails is indistinguishable from no gate."""
    doc = copy.deepcopy(DOC)
    doc["claims"][0].update(patch)
    return doc


# ── the shipped ledger passes its own gate ───────────────────────────────────


def test_shipped_ledger_validates():
    assert not interp.validate(DOC), "\n".join(interp.validate(DOC))


def test_every_checked_claim_cites_a_primary_source():
    for c in CLAIMS:
        if c["status"] in interp.CHECKED:
            assert str(c.get("source", "")).startswith("http"), c["id"]


def test_every_claim_records_when_it_was_checked():
    for c in CLAIMS:
        assert interp._date(c["checked"]) is not None, c["id"]


# ── fail-closed: each rule actually fails ────────────────────────────────────


def test_a_checked_claim_without_a_source_is_rejected():
    doc = mutate(status="verified", source=None)
    assert any("requires a primary-source URL" in e for e in interp.validate(doc))


def test_a_correction_that_changes_nothing_is_rejected():
    """'Corrected' with an identical replacement claims work that never happened."""
    same = DOC["claims"][0]["as_transcribed"]
    doc = mutate(status="corrected", verified_as=same)
    assert any("that is not a correction" in e for e in interp.validate(doc))


def test_a_refuted_correction_must_keep_the_wrong_correction():
    doc = mutate(status="refuted_correction", proposed=None)
    assert any("must stay on the record" in e for e in interp.validate(doc))


def test_unverified_must_say_what_stopped_the_check():
    doc = mutate(status="unverified", source=None, why=None, verified_as=None)
    assert any("requires 'why'" in e for e in interp.validate(doc))


def test_unverified_may_not_carry_a_source_url():
    """A source that was read is a check that happened — the two cannot coexist."""
    doc = mutate(status="unverified", why="could not reach it",
                 source="https://example.com/")
    assert any("must not carry a source URL" in e for e in interp.validate(doc))


def test_an_unknown_status_is_rejected():
    doc = mutate(status="probably-fine")
    assert any("status must be one of" in e for e in interp.validate(doc))


def test_duplicate_ids_are_rejected():
    doc = copy.deepcopy(DOC)
    doc["claims"].append(copy.deepcopy(doc["claims"][0]))
    assert any("duplicate claim id" in e for e in interp.validate(doc))


# ── staleness: true-when-I-looked is not true ────────────────────────────────


def test_a_claim_past_its_half_life_stops_being_citable():
    doc = copy.deepcopy(DOC)
    row = next(c for c in doc["claims"] if c["kind"] == "org")   # 365-day half-life
    row["checked"] = "2024-01-01"
    assert not interp.citable(row, doc["half_life_days"], TODAY)
    assert interp.stale(row, doc["half_life_days"], TODAY) > 0


def test_a_fresh_claim_is_citable():
    row = next(c for c in CLAIMS if c["id"] == "jspace")
    assert interp.citable(row, DOC["half_life_days"], TODAY)


# ── the refusal is the product ───────────────────────────────────────────────


def test_cite_emits_a_verified_claim():
    assert interp.cite(DOC, "jspace", TODAY) == 0


def test_cite_refuses_an_unverified_claim():
    """The whole section exists so that this returns non-zero."""
    assert interp.cite(DOC, "sushi_japanese", TODAY) == 1


def test_cite_refuses_an_id_that_does_not_exist():
    assert interp.cite(DOC, "not_a_claim", TODAY) == 1


# ── the scoreboard tells on itself ───────────────────────────────────────────


def test_corrector_accuracy_counts_our_own_wrong_correction():
    """8 corrections held, 1 was refuted — 89%, not 100%. A corrector that
    reports 100% has simply deleted its misses."""
    s = interp.score(DOC, TODAY)
    assert s["counts"]["refuted_correction"] >= 1
    assert s["corrector_accuracy"] < 100.0
    assert s["proposed"] == s["corrections_held"] + s["counts"]["refuted_correction"]


def test_source_error_rate_excludes_claims_the_source_never_made():
    """`omitted` rows have no as_transcribed assertion, so grading the source
    on them would invent an error it did not commit."""
    s = interp.score(DOC, TODAY)
    assert s["asserted"] == sum(1 for c in CLAIMS if c["status"] in interp.ASSERTED)
    assert s["gaps"] == sum(1 for c in CLAIMS if c["status"] == "omitted")
    assert s["source_error_rate"] > 0


def test_coverage_never_counts_an_unverified_claim():
    s = interp.score(DOC, TODAY)
    assert s["citable"] == s["total"] - s["counts"]["unverified"]
    assert s["coverage"] < 100.0, "a 100% ledger means nothing was left unchecked"


def test_the_ledger_keeps_at_least_one_thing_it_could_not_verify():
    """A ledger with no unknowns is a ledger that stopped looking."""
    assert any(c["status"] == "unverified" for c in CLAIMS)
