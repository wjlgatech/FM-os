"""Optional: the SAME closed loop on the production stack (BoTorch + GPyTorch).

This is what ships in the role — BoTorch's SingleTaskGP + qLogExpectedImprovement.
It is import-guarded so the offline lab never depends on it; run it only when
`torch`, `gpytorch`, and `botorch` are installed:

    pip install botorch    # pulls torch + gpytorch
    python -m merge_bo.botorch_adapter

Keeping the numpy loop and this adapter side by side makes the point the JD asks
for: 'translate prototypes into production pipelines' — same interface, same DBTL
structure, swap the surrogate/acquisition implementation.
"""
from __future__ import annotations

import numpy as np

from .objectives import MolecularLibrary


def available() -> bool:
    try:
        import botorch  # noqa: F401
        import gpytorch  # noqa: F401
        import torch  # noqa: F401
        return True
    except Exception:
        return False


def bo_loop_botorch(lib: MolecularLibrary, n_init: int = 5, n_iters: int = 25, seed: int = 0):
    """Run single-objective BO over the library pool using BoTorch. Requires botorch."""
    import torch
    from botorch.acquisition import qLogExpectedImprovement
    from botorch.fit import fit_gpytorch_mll
    from botorch.models import SingleTaskGP
    from botorch.sampling.normal import SobolQMCNormalSampler
    from gpytorch.mlls import ExactMarginalLogLikelihood

    rng = np.random.default_rng(seed)
    tested = list(rng.choice(lib.n, size=n_init, replace=False))
    ys = [lib.assay_potency(i) for i in tested]
    best = max(ys)
    traj = [best]

    for _ in range(n_iters):
        untested = [i for i in range(lib.n) if i not in set(tested)]
        if not untested:
            break
        train_x = torch.tensor(lib.X[tested], dtype=torch.double)
        train_y = torch.tensor(np.array(ys)[:, None], dtype=torch.double)
        model = SingleTaskGP(train_x, train_y)
        mll = ExactMarginalLogLikelihood(model.likelihood, model)
        fit_gpytorch_mll(mll)
        sampler = SobolQMCNormalSampler(torch.Size([64]))
        acqf = qLogExpectedImprovement(model, best_f=best, sampler=sampler)
        cand = torch.tensor(lib.X[untested], dtype=torch.double).unsqueeze(1)
        with torch.no_grad():
            scores = acqf(cand)
        idx = untested[int(torch.argmax(scores))]
        y = lib.assay_potency(idx)
        tested.append(idx)
        ys.append(y)
        best = max(best, y)
        traj.append(best)
    return traj


if __name__ == "__main__":
    if not available():
        print("botorch/gpytorch/torch not installed — skipping (offline lab uses the numpy loop).")
        raise SystemExit(0)
    lib = MolecularLibrary(seed=0)
    traj = bo_loop_botorch(lib)
    print(f"BoTorch loop best potency: {traj[-1]:.3f} (true optimum {lib.best_potency():.3f})")
