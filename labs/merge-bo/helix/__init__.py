"""Helix — the Design·Build·Test·Learn copilot, built on the merge_bo engine.

A wet-lab scientist describes a campaign in plain terms; Helix compiles it to a typed
optimization spec, proposes the next batch of experiments with uncertainty and a
rationale, ingests assay results, refits, and reports how many experiments the closed
loop saved versus guessing. Ships as agent tooling (skill + workflow + hook + MCP).
"""
from .spec import OptimizationSpec, Objective, Constraint, compile_spec
from .campaign import Campaign

__all__ = ["OptimizationSpec", "Objective", "Constraint", "compile_spec", "Campaign"]
