"""The Campaign — a persistent, resumable DBTL loop over the merge_bo engine.

Real design-build-test-learn runs asynchronously over weeks: you propose a batch on
Monday, the wet lab reports results the following week, you refit and propose again. So
the campaign persists to JSON and is fully resumable — the "translate prototypes into
production pipelines" half of the JD.

Each cycle:
  propose(batch)  -> experiment cards {candidate, predicted mean, uncertainty, rationale}
  ingest(results) -> record assay readouts for the proposed candidates
  status()        -> best-so-far, predicted headroom, and (in simulation) experiments saved

The optimizer under the hood is the same GP surrogate + acquisition from merge_bo. A
`simulate()` helper runs the whole loop against a known oracle so the product can show a
measured "experiments saved vs. random" number — the evidence artifact.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

import numpy as np

from merge_bo.acquisition import _hypervolume_2d, _pareto_front, constrained_ei, ei
from merge_bo.gp import GaussianProcess

from .spec import OptimizationSpec


@dataclass
class ExperimentCard:
    """A single proposed experiment, in language a wet-lab scientist can act on."""
    candidate_id: int
    features: list[float]
    predicted: float
    uncertainty: float
    acquisition: float
    rationale: str

    def to_dict(self) -> dict:
        return asdict(self)


class Campaign:
    """A resumable closed-loop optimization campaign bound to an OptimizationSpec."""

    def __init__(self, spec: OptimizationSpec, pool_size: int = 400, seed: int = 0,
                 candidates: np.ndarray | None = None) -> None:
        self.spec = spec
        self.seed = seed
        self.rng = np.random.default_rng(seed)
        # The candidate library: a discrete pool of featurized designs. In production
        # this is your enumerated/generated library; here we sample one if not given.
        if candidates is None:
            candidates = self.rng.uniform(0.0, 1.0, size=(pool_size, spec.dim))
        self.candidates = np.asarray(candidates, float)
        # observations: candidate_id -> {objective_name: value, constraint_name: value}
        self.observations: dict[int, dict[str, float]] = {}
        self.history: list[dict] = []   # per-cycle log for the timeline

    # ── the primary objective as a signed array the GP maximizes ──────────────
    def _obj_name(self) -> str:
        return self.spec.objectives[0].name if self.spec.objectives else "objective"

    def _y(self, name: str, sign: float = 1.0) -> tuple[np.ndarray, np.ndarray]:
        """Return (candidate_ids, values) observed for a measured field."""
        ids = [i for i, o in self.observations.items() if name in o]
        vals = np.array([sign * self.observations[i][name] for i in ids], float)
        return np.array(ids, int), vals

    def _fit(self, name: str, sign: float = 1.0) -> GaussianProcess | None:
        ids, vals = self._y(name, sign)
        if len(ids) < 2:
            return None
        return GaussianProcess(seed=self.seed).fit(self.candidates[ids], vals)

    # ── propose ───────────────────────────────────────────────────────────────
    def propose(self, batch: int | None = None) -> list[ExperimentCard]:
        """Score the untested pool and return the next batch of experiments to run."""
        batch = batch or self.spec.batch_size
        untested = np.array([i for i in range(len(self.candidates)) if i not in self.observations])
        if len(untested) == 0:
            return []

        primary = self.spec.objectives[0] if self.spec.objectives else None
        sign = -1.0 if (primary and primary.direction == "min") else 1.0
        gp = self._fit(self._obj_name(), sign) if primary else None

        if gp is None:
            # Cold start: no model yet — propose a space-filling random batch, said plainly.
            pick = self.rng.choice(untested, size=min(batch, len(untested)), replace=False)
            return [ExperimentCard(int(i), self.candidates[i].round(3).tolist(), float("nan"),
                                   float("nan"), float("nan"),
                                   "cold start — no data yet; exploring the design space")
                    for i in pick]

        mu, var = gp.predict(self.candidates[untested])
        sigma = np.sqrt(var)
        _, yvals = self._y(self._obj_name(), sign)
        best = float(yvals.max())

        # constraint handling: feasibility-weight the acquisition by every constraint GP
        acq = ei(mu, var, best_f=best)
        con_note = ""
        for c in self.spec.constraints:
            cgp = self._fit(c.name, 1.0)
            if cgp is None:
                continue
            cmu, cvar = cgp.predict(self.candidates[untested])
            thr = c.threshold if c.op == "<=" else -c.threshold
            csign_mu = cmu if c.op == "<=" else -cmu
            acq = constrained_ei(mu, var, best, csign_mu, cvar, c_threshold=thr)
            con_note = f"; feasibility-weighted for {c.name} {c.op} {c.threshold}"

        order = np.argsort(-acq)[:batch]
        cards = []
        for k in order:
            i = int(untested[k])
            disp_mu = sign * mu[k]  # de-sign for display so "predicted" reads in real units
            rank = "highest expected improvement" if k == order[0] else "strong expected improvement"
            rationale = (f"{rank}: predicted {self._obj_name()} ≈ {disp_mu:.3f} "
                         f"± {sigma[k]:.3f} (model {'confident' if sigma[k] < 0.15 else 'uncertain → explores'})"
                         + con_note)
            cards.append(ExperimentCard(i, self.candidates[i].round(3).tolist(),
                                        float(disp_mu), float(sigma[k]), float(acq[k]), rationale))
        return cards

    # ── ingest ──────────────────────────────────────────────────────────────
    def ingest(self, results: list[dict]) -> int:
        """Record assay readouts. Each result: {candidate_id, <objective/constraint>: value}."""
        n = 0
        for r in results:
            cid = int(r["candidate_id"])
            fields = {k: float(v) for k, v in r.items() if k != "candidate_id"}
            self.observations.setdefault(cid, {}).update(fields)
            n += 1
        self.history.append({"cycle": len(self.history) + 1, "ingested": n,
                             "total_observed": len(self.observations)})
        return n

    # ── status ────────────────────────────────────────────────────────────────
    def status(self) -> dict:
        """A human-facing progress report — best so far, headroom, and Pareto (if MO)."""
        primary = self.spec.objectives[0] if self.spec.objectives else None
        out: dict = {
            "title": self.spec.title, "observed": len(self.observations),
            "budget": self.spec.total_budget,
            "budget_remaining": max(0, self.spec.total_budget - len(self.observations)),
            "cycles": len(self.history),
        }
        if primary and any(primary.name in o for o in self.observations.values()):
            vals = [o[primary.name] for o in self.observations.values() if primary.name in o]
            out["objective"] = primary.name
            out["best"] = (max(vals) if primary.direction == "max" else min(vals))
        if self.spec.is_multi_objective:
            names = [ob.name for ob in self.spec.objectives[:2]]
            pts = np.array([[o[n] for n in names] for o in self.observations.values()
                            if all(n in o for n in names)])
            if len(pts):
                ref = pts.min(0) - 0.1
                out["hypervolume"] = float(_hypervolume_2d(_pareto_front(pts), ref))
                out["pareto_size"] = int(len(_pareto_front(pts)))
        return out

    # ── persistence ────────────────────────────────────────────────────────────
    def save(self, path: str | Path) -> None:
        path = Path(path)
        path.write_text(json.dumps({
            "spec": self.spec.to_dict(), "seed": self.seed,
            "candidates": self.candidates.tolist(),
            "observations": {str(k): v for k, v in self.observations.items()},
            "history": self.history,
        }, indent=2))

    @classmethod
    def load(cls, path: str | Path) -> "Campaign":
        d = json.loads(Path(path).read_text())
        c = cls(OptimizationSpec.from_dict(d["spec"]), seed=d.get("seed", 0),
                candidates=np.array(d["candidates"], float))
        c.observations = {int(k): v for k, v in d["observations"].items()}
        c.history = d.get("history", [])
        return c

    # ── simulation (evidence artifact) ──────────────────────────────────────────
    def simulate(self, oracle, cycles: int | None = None) -> dict:
        """Run the full loop against a known oracle; measure experiments saved vs random.

        `oracle(features) -> dict(objective/constraint values)`. Only for demo/validation —
        production campaigns get their readouts from real assays via ingest().
        """
        cycles = cycles or (self.spec.total_budget // self.spec.batch_size)
        best_traj = []
        for _ in range(cycles):
            cards = self.propose()
            if not cards:
                break
            self.ingest([{"candidate_id": c.candidate_id, **oracle(np.array(c.features))}
                         for c in cards])
            best_traj.append(self.status().get("best", float("nan")))
        return {"best_trajectory": best_traj, "status": self.status()}
