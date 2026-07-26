"""The BARE thesis, falsifiable: only base+refine passes BOTH gates, the
refiner never invents facts, and runs are deterministic. The skill's teeth."""

import random

from bare_loop import (
    IMAGES,
    alignment,
    base_model,
    refine,
    run_pipeline,
)


def test_base_only_fails_alignment_but_is_diverse():
    r = run_pipeline("base_only")
    assert not r["gate_pass"]
    assert any("alignment" in reason for reason in r["gate_reasons"])
    assert not any("diversity" in reason for reason in r["gate_reasons"])
    assert r["yield"] < 1.0  # the CLIP-filter analog would throw data away


def test_instruct_only_fails_diversity_but_is_grounded():
    r = run_pipeline("instruct_only")
    assert not r["gate_pass"]
    assert any("diversity" in reason for reason in r["gate_reasons"])
    assert r["alignment"] == 1.0  # correct, just mode-collapsed


def test_bare_passes_both_gates_at_full_yield():
    r = run_pipeline("bare")
    assert r["gate_pass"], r["gate_reasons"]
    assert r["yield"] == 1.0  # refinement repairs instead of discarding


def test_refiner_never_invents_ungrounded_facts():
    rng = random.Random(7)
    glue = {"a", "the", "with", "and", "near", "beside", "by", "under", "scene",
            "showing", "close", "view", "of", "photo"}
    for image in IMAGES:
        for _ in range(20):
            refined = refine(image, base_model(image, rng))
            grounded = image["objects"] | {image["attr"], image["main"]}
            assert all(t in grounded or t in glue for t in refined.split())
            assert alignment(image, refined) == 1.0


def test_deterministic_given_seed():
    assert run_pipeline("bare", seed=3) == run_pipeline("bare", seed=3)
