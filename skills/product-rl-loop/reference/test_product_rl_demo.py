"""The product-RL loop's teeth: the held-out gate must catch reward hacking
from biased product signal, pass the bias-blind update, and never regress
safety — across seeds, deterministically."""

import numpy as np

from product_rl_demo import GATES, dpo_fit, gate, make_world, product_preferences, run_arm


def test_raw_product_signal_is_reward_hacked_and_rolled_back():
    for seed in (0, 1, 2):
        r = run_arm(debias=False, seed=seed)
        assert r["w"][2] > 1.0          # verbosity (true worth 0) got learned — the hack
        assert not r["ship"]            # the held-out gate rolls it back
        assert any("win_rate" in reason for reason in r["reasons"])


def test_bias_projected_update_ships():
    for seed in (0, 1, 2):
        r = run_arm(debias=True, seed=seed)
        assert r["ship"], r["reasons"]
        assert r["win_rate"] >= GATES["min_win_rate"]
        assert abs(r["w"][2] - 0.3) < 1e-9  # bias direction frozen at baseline


def test_safety_gate_blocks_unsafe_regression():
    ok, reasons = gate(win_rate=0.9, unsafe_policy=0.10, unsafe_base=0.05)
    assert not ok and any("unsafe" in r for r in reasons)


def test_projection_learns_quality_and_safety_not_bias():
    feats, quality, rng = make_world(seed=5)
    pairs = product_preferences(feats, quality, rng)
    w0 = np.array([0.9, 0.7, 0.3, -0.5])
    w = dpo_fit(pairs, w0, project_out=2)
    assert w[0] > w0[0] and w[3] < w0[3]  # quality up-weighted, unsafe punished harder
    assert w[2] == w0[2]


def test_deterministic_given_seed():
    a, b = run_arm(debias=True, seed=7), run_arm(debias=True, seed=7)
    assert a["win_rate"] == b["win_rate"] and np.allclose(a["w"], b["w"])
