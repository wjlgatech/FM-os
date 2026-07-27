"""Offline gates (no model, no network): pair provenance + no leakage,
DPO loss math against hand-computed values, and gate math incl. rollback."""

import math
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from rewardforge import gates, pairs
from rewardforge.dpo import dpo_loss


# ── pairs ────────────────────────────────────────────────────────────────────
def test_every_pair_has_provenance_and_real_difference():
    train = pairs.training_pairs()
    assert len(train) >= 150
    for p in train:
        assert p["provenance"] and p["chosen"] != p["rejected"]


def test_rejected_bare_drafts_actually_hallucinate():
    import bare_loop

    for p in pairs.bare_pairs(n_per_image=5):
        image = next(im for im in bare_loop.IMAGES if im["id"] in p["provenance"])
        assert bare_loop.alignment(image, p["rejected"].strip(" .")) < 1.0
        assert bare_loop.alignment(image, p["chosen"].strip(" .")) == 1.0


def test_heldout_worlds_share_no_content_words_with_training():
    train_vocab = pairs.train_vocabulary()
    for h in pairs.heldout_prompts():
        im = h["image"]
        held_vocab = im["objects"] | {im["attr"], im["main"]}
        assert not (held_vocab & train_vocab), (im["id"], held_vocab & train_vocab)


def test_pairs_deterministic():
    a, b = pairs.training_pairs(seed=1), pairs.training_pairs(seed=1)
    assert a == b


# ── DPO loss math ────────────────────────────────────────────────────────────
def test_dpo_loss_matches_hand_computation():
    # margin = beta*((pi_w-ref_w)-(pi_l-ref_l)) = 0.1*((-1+2)-(-3+1)) = 0.3
    loss = dpo_loss(torch.tensor(-1.0), torch.tensor(-3.0), -2.0, -1.0, beta=0.1)
    assert math.isclose(loss.item(), -math.log(1 / (1 + math.exp(-0.3))), rel_tol=1e-6)


def test_dpo_loss_decreases_as_chosen_gains_margin():
    base = dpo_loss(torch.tensor(-2.0), torch.tensor(-2.0), -2.0, -2.0)
    better = dpo_loss(torch.tensor(-1.0), torch.tensor(-3.0), -2.0, -2.0)
    assert better.item() < base.item()


# ── gate math ────────────────────────────────────────────────────────────────
def test_hallucination_rate_grounds_correctly():
    im = {"main": "horse", "attr": "brown", "objects": {"horse", "meadow", "fence"}}
    assert gates.hallucination_rate("a brown horse in the meadow", im) == 0.0
    assert gates.hallucination_rate("a purple dragon in the meadow", im) > 0.5
    assert gates.hallucination_rate("", im) == 1.0  # degenerate = fully ungrounded


def test_gate_ships_on_real_drop_and_rolls_back_otherwise():
    before = {"halluc_rate": 0.40, "avg_words": 8.0}
    ok, _ = gates.gate(before, {"halluc_rate": 0.25, "avg_words": 7.0})
    assert ok
    ok, reasons = gates.gate(before, {"halluc_rate": 0.39, "avg_words": 7.0})
    assert not ok and "drop" in reasons[0]
    ok, reasons = gates.gate(before, {"halluc_rate": 0.10, "avg_words": 1.0})
    assert not ok and any("degeneration" in r for r in reasons)
