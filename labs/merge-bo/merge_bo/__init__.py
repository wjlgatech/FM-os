"""merge-bo — a from-scratch, dependency-light closed-loop Bayesian optimization lab.

Mirrors the Merge Labs 'closed-loop optimization backbone': a GP surrogate, standard
acquisition functions, and a Design-Build-Test-Learn loop over a molecular library,
with constrained and multi-objective variants. Numpy-only core so it runs anywhere;
an optional BoTorch adapter shows the same loop on the production stack.
"""
from .gp import GaussianProcess
from .objectives import MolecularLibrary

__all__ = ["GaussianProcess", "MolecularLibrary"]
