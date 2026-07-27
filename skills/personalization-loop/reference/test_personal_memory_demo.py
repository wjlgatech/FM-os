"""The personalization loop's teeth: memory must pay rent under four gates —
lift, cold-start parity, bit-level user isolation, and wrong-memory-harms."""

import numpy as np

from personal_memory_demo import gate_cohort, leakage, run_cohort


def test_all_four_gates_pass():
    for seed in (0, 1, 2):
        r = run_cohort(seed)
        ok, reasons = gate_cohort(r, leakage(seed))
        assert ok, reasons


def test_memory_pays_rent_wrong_user_memory_hurts():
    r = run_cohort(0)
    assert r["lift"] > 0.3                 # real personalization lift
    assert r["wrong_memory_delta"] < 0     # the CONTENT drives it, not adaptivity


def test_cold_start_never_worse_than_baseline():
    r = run_cohort(0)
    assert r["cold_start_deficit"] <= 0.0  # memory starts at the global prior


def test_isolation_is_bit_exact():
    assert leakage(0) == 0.0


def test_gate_flags_a_rent_free_memory():
    r = run_cohort(0)
    r = dict(r, wrong_memory_delta=+0.05)  # a memory that helps even when wrong = suspicious
    ok, reasons = gate_cohort(r, 0.0)
    assert not ok and any("rent" in x for x in reasons)


def test_deterministic():
    a, b = run_cohort(3), run_cohort(3)
    assert a["lift"] == b["lift"] and np.allclose(a["personal"], b["personal"])
