#!/usr/bin/env python3
"""Gates for tinker_local.py — runnable standalone (python test_tinker_local.py)
or via pytest. Verifies the Tinker contract (frozen base, adapter-only training,
state roundtrip, greedy determinism) and that the eval gates have teeth both ways.
"""
from __future__ import annotations

import os
import sys
import tempfile

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tinker_local as tl  # noqa: E402


def test_base_stays_frozen():
    """Tinker's core contract: training touches ONLY the LoRA adapters."""
    rng = np.random.default_rng(0)
    base = tl._pretrain_base()
    snapshot = base.copy()
    client = tl.LocalTrainingClient(base, rng)
    for _ in range(5):
        client.forward_backward(tl.DOMAIN_TRAIN, loss_fn="cross_entropy")
        client.optim_step()
    assert np.array_equal(client.base, snapshot), "base weights must never change"
    assert not np.allclose(client.A @ client.B, 0.0), "adapters must have trained"


def test_lora_delta_starts_at_zero():
    client = tl.LocalTrainingClient(tl._pretrain_base(), np.random.default_rng(0))
    assert np.allclose(client.logits(), client.base), "B=0 init => delta starts at 0"


def test_forward_backward_reduces_loss():
    client = tl.LocalTrainingClient(tl._pretrain_base(), np.random.default_rng(0))
    first = client.forward_backward(tl.DOMAIN_TRAIN)["loss"]
    for _ in range(50):
        client.optim_step(lr=0.05)
        last = client.forward_backward(tl.DOMAIN_TRAIN)["loss"]
    assert last < first, "SFT loop must reduce training loss"


def test_dpo_loss_fn_runs_and_improves_margin():
    client = tl.LocalTrainingClient(tl._pretrain_base(), np.random.default_rng(0))
    before = tl.pref_margin(client.logits(), tl.PREF_HELDOUT)
    for _ in range(30):
        client.forward_backward(tl.PREF_TRAIN, loss_fn="dpo")
        client.optim_step(lr=0.01)
    after = tl.pref_margin(client.logits(), tl.PREF_HELDOUT)
    assert after > before, "DPO must raise the held-out preference margin"


def test_save_state_roundtrip():
    client = tl.LocalTrainingClient(tl._pretrain_base(), np.random.default_rng(0))
    client.forward_backward(tl.DOMAIN_TRAIN)
    client.optim_step()
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "ckpt")
        client.save_state(path)
        other = tl.LocalTrainingClient(tl._pretrain_base(), np.random.default_rng(1))
        other.load_state(path)
        assert np.array_equal(other.A, client.A) and np.array_equal(other.B, client.B)


def test_greedy_sampling_is_deterministic():
    client = tl.LocalTrainingClient(tl._pretrain_base(), np.random.default_rng(0))
    sampler = client.save_weights_and_get_sampling_client()
    assert sampler.sample("the ", 20, 0.0) == sampler.sample("the ", 20, 0.0)


def test_gates_have_teeth_both_ways():
    """The demo's promise: naive recipe ROLLBACK, replay recipe SHIP."""
    naive = tl.run_demo("naive")
    replay = tl.run_demo("replay")
    assert not naive["ship"], "naive domain-only SFT must be caught by the forgetting gate"
    assert not naive["gates"]["G2_no_forgetting"]
    assert replay["ship"], "replay recipe must pass all three gates"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    for fn in fns:
        fn()
        print(f"✅ {fn.__name__}")
    print(f"{len(fns)}/{len(fns)} gates green")
    sys.exit(0)
