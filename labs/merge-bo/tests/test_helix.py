"""Helix product layer: spec compiler, persistent campaign, and MCP tools."""
import numpy as np

from helix.campaign import Campaign
from helix.spec import Objective, compile_spec
from merge_bo.objectives import MolecularLibrary


# ── spec compiler ─────────────────────────────────────────────────────────────
def test_brief_compiles_objectives_constraints_budget():
    s = compile_spec("Optimize a peptide for binding affinity. 6 a week, ~30 total. "
                     "Keep cost under 0.7 and also maximize stability.", title="p1")
    names = {o.name: o.direction for o in s.objectives}
    assert names.get("affinity") == "max"
    assert names.get("stability") == "max"       # nearest cue is 'maximize', not distant 'under'
    assert "binding" not in names                 # collapsed into 'binding affinity'
    assert any(c.name == "cost" and c.threshold == 0.7 for c in s.constraints)
    assert s.batch_size == 6 and s.total_budget == 30
    assert s.validate() == []


def test_brief_records_open_questions_not_guesses():
    s = compile_spec("I want to reduce toxicity somehow.", title="p2")
    # a constraint noun without a threshold becomes an open question, never a fabricated number
    assert any("toxicity" in q for q in s.open_questions)


def test_min_direction_detected():
    s = compile_spec(parsed={"objectives": [{"name": "cost", "direction": "min"}]}, title="p3")
    assert s.objectives[0].direction == "min"


# ── campaign engine ───────────────────────────────────────────────────────────
def _spec(**kw):
    base = {"objectives": [{"name": "potency", "direction": "max"}],
            "batch_size": 3, "total_budget": 24, "dim": 6}
    base.update(kw)
    return compile_spec(parsed=base, title="c")


def test_cold_start_then_model_proposes():
    lib = MolecularLibrary(seed=1)
    camp = Campaign(_spec(), candidates=lib.X, seed=1)
    cold = camp.propose()
    assert len(cold) == 3 and "cold start" in cold[0].rationale
    camp.ingest([{"candidate_id": c.candidate_id, "potency": lib.assay_potency(c.candidate_id)}
                 for c in cold])
    warm = camp.propose()
    assert warm and "expected improvement" in warm[0].rationale


def test_simulate_beats_random_on_average():
    # BO beats random *on average* (not on every seed) — the honest, multi-seed claim.
    bo, rnd = [], []
    for s in range(6):
        lib = MolecularLibrary(seed=s)
        camp = Campaign(_spec(total_budget=27), candidates=lib.X, seed=s)
        res = camp.simulate(
            lambda f, lib=lib: {"potency": lib.assay_potency(int(np.argmin(((lib.X - f) ** 2).sum(1))))})
        bo.append(res["status"]["best"])
        g = np.random.default_rng(s + 999)
        rnd.append(max(lib.assay_potency(int(i)) for i in g.permutation(lib.n)[:len(camp.observations)]))
    assert np.mean(bo) > np.mean(rnd)


def test_persistence_roundtrip(tmp_path):
    lib = MolecularLibrary(seed=3)
    camp = Campaign(_spec(), candidates=lib.X, seed=3)
    camp.ingest([{"candidate_id": 0, "potency": 0.5}])
    p = tmp_path / "camp.json"
    camp.save(p)
    back = Campaign.load(p)
    assert back.observations == camp.observations
    assert back.spec.title == camp.spec.title


def test_constraint_feasibility_weighting_runs():
    lib = MolecularLibrary(seed=4)
    spec = compile_spec(parsed={"objectives": [{"name": "potency", "direction": "max"}],
                                "constraints": [{"name": "cost", "op": "<=", "threshold": 0.8}],
                                "batch_size": 3, "total_budget": 21, "dim": 6}, title="con")
    camp = Campaign(spec, candidates=lib.X, seed=4)
    camp.ingest([{"candidate_id": i, "potency": lib.assay_potency(i), "cost": lib.assay_sa(i)}
                 for i in range(4)])
    cards = camp.propose()
    assert cards and "feasibility-weighted" in cards[0].rationale


# ── MCP server ────────────────────────────────────────────────────────────────
def test_mcp_lists_four_tools():
    from helix.mcp_server import handle
    tools = handle({"jsonrpc": "2.0", "id": 1, "method": "tools/list"})["result"]["tools"]
    assert {t["name"] for t in tools} == {
        "define_campaign", "propose_experiments", "ingest_results", "campaign_status"}


def test_mcp_full_cycle(tmp_path, monkeypatch):
    import helix.mcp_server as srv
    monkeypatch.setattr(srv, "STORE", tmp_path)
    def call(name, args):
        r = srv.handle({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                        "params": {"name": name, "arguments": args}})
        return r["result"]
    d = call("define_campaign", {"title": "t", "brief": "maximize potency, 3 a week, 15 total"})
    assert not d.get("isError")
    prop = call("propose_experiments", {"campaign": "t", "batch": 3})
    assert not prop.get("isError")
    ing = call("ingest_results", {"campaign": "t",
                                  "results": [{"candidate_id": 0, "potency": 0.4}]})
    assert not ing.get("isError")
    st = call("campaign_status", {"campaign": "t"})
    assert not st.get("isError")
