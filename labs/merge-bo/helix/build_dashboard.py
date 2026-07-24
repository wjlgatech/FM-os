#!/usr/bin/env python3
"""Generate the Helix dashboard — a self-contained, Anthropic-brand HTML wow surface.

Runs a real campaign (BO closed loop) and a random-search baseline against a known oracle,
then renders best-so-far curves, the experiments-saved hero metric, a multi-objective Pareto
front, and the next proposed batch — all as inline SVG/HTML with zero external dependencies.
Every number on the page is produced live here; nothing is hand-entered.

    python -m helix.build_dashboard   ->   out/helix-dashboard.html
"""
from __future__ import annotations

import statistics as stats
from pathlib import Path

import numpy as np

from merge_bo.acquisition import _hypervolume_2d, _pareto_front
from merge_bo.objectives import MolecularLibrary

from .campaign import Campaign
from .spec import compile_spec

OUT = Path(__file__).parent.parent / "out"

# brand tokens (anyagent brand as code)
IVORY, CARD, INK = "#faf9f5", "#ffffff", "#141413"
BORDER, MUTED, ORANGE = "#e3e0d6", "#6b6a63", "#d97757"
BLUE, GREEN = "#6a9bcc", "#788c5d"


def _single_objective(seeds):
    """BO vs random on a molecular potency landscape; return trajectories + experiments-saved."""
    bo_traj, rand_traj, saved = [], [], []
    target_frac = 0.90
    for s in seeds:
        lib = MolecularLibrary(seed=s)
        opt = lib.best_potency()
        target = target_frac * opt
        sp = compile_spec(parsed={"objectives": [{"name": "potency", "direction": "max"}],
                                  "batch_size": 3, "total_budget": 30, "dim": 6}, title=f"sim{s}")
        camp = Campaign(sp, candidates=lib.X, seed=s)

        def oracle(feat, lib=lib):
            i = int(np.argmin(((lib.X - feat) ** 2).sum(1)))
            return {"potency": lib.assay_potency(i)}

        res = camp.simulate(oracle)
        bo_best = res["best_trajectory"]
        bo_traj.append(bo_best)
        # random baseline over the same budget
        rng = np.random.default_rng(s + 500)
        order = rng.permutation(lib.n)[:len(camp.observations)]
        rbest, rb = [], float("-inf")
        for k, idx in enumerate(order):
            rb = max(rb, lib.assay_potency(int(idx)))
            if (k + 1) % 3 == 0:
                rbest.append(rb)
        rand_traj.append(rbest)
        # experiments to reach the target
        def first_hit(vals, per=3):
            for k, v in enumerate(vals):
                if v >= target:
                    return (k + 1) * per
            return None
        bo_hit = first_hit(bo_best)
        rand_flat, rf = [], float("-inf")
        for k, idx in enumerate(rng.permutation(lib.n)):
            rf = max(rf, lib.assay_potency(int(idx)))
            rand_flat.append(rf)
        rand_hit = next((k + 1 for k, v in enumerate(rand_flat) if v >= target), None)
        if bo_hit and rand_hit:
            saved.append(rand_hit - bo_hit)
    return bo_traj, rand_traj, saved


def _multi_objective(seed=2):
    """A 2-objective campaign; return the observed points and the Pareto front."""
    lib = MolecularLibrary(seed=seed)
    sp = compile_spec(parsed={"objectives": [{"name": "potency", "direction": "max"},
                                             {"name": "selectivity", "direction": "max"}],
                              "batch_size": 4, "total_budget": 32, "dim": 6}, title="mo")
    camp = Campaign(sp, candidates=lib.X, seed=seed)

    def oracle(feat):
        i = int(np.argmin(((lib.X - feat) ** 2).sum(1)))
        return {"potency": lib.assay_potency(i), "selectivity": lib.assay_selectivity(i)}

    camp.simulate(oracle)
    pts = np.array([[o["potency"], o["selectivity"]] for o in camp.observations.values()
                    if "potency" in o and "selectivity" in o])
    front = _pareto_front(pts)
    return pts, front, camp


def _mean_curve(trajs):
    n = min(len(t) for t in trajs)
    return [stats.mean(t[i] for t in trajs) for i in range(n)]


# ── tiny inline-SVG charting (no deps) ────────────────────────────────────────
def _line_chart(series, w=520, h=240, pad=38):
    ymin = min(min(s["data"]) for s in series)
    ymax = max(max(s["data"]) for s in series)
    xmax = max(len(s["data"]) for s in series) - 1
    def X(i): return pad + i * (w - 2 * pad) / max(1, xmax)
    def Y(v): return h - pad - (v - ymin) * (h - 2 * pad) / (ymax - ymin or 1)
    parts = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px">']
    parts.append(f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="{BORDER}"/>')
    parts.append(f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h-pad}" stroke="{BORDER}"/>')
    for s in series:
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(s["data"]))
        parts.append(f'<polyline fill="none" stroke="{s["color"]}" stroke-width="2.5" points="{pts}"/>')
        cx, cy = X(len(s["data"]) - 1), Y(s["data"][-1])
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="{s["color"]}"/>')
    parts.append(f'<text x="{pad}" y="{h-8}" font-size="11" fill="{MUTED}">experiments →</text>')
    parts.append(f'<text x="8" y="{pad-8}" font-size="11" fill="{MUTED}">best objective</text>')
    parts.append("</svg>")
    return "".join(parts)


def _scatter(pts, front, w=520, h=240, pad=38):
    xs, ys = pts[:, 0], pts[:, 1]
    def X(v): return pad + (v - xs.min()) * (w - 2 * pad) / (np.ptp(xs) or 1)
    def Y(v): return h - pad - (v - ys.min()) * (h - 2 * pad) / (np.ptp(ys) or 1)
    parts = [f'<svg viewBox="0 0 {w} {h}" width="100%" style="max-width:{w}px">']
    parts.append(f'<line x1="{pad}" y1="{h-pad}" x2="{w-pad}" y2="{h-pad}" stroke="{BORDER}"/>')
    parts.append(f'<line x1="{pad}" y1="{pad}" x2="{pad}" y2="{h-pad}" stroke="{BORDER}"/>')
    for x, y in pts:
        parts.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="3" fill="{BLUE}" opacity="0.5"/>')
    fr = front[np.argsort(front[:, 0])]
    line = " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in fr)
    parts.append(f'<polyline fill="none" stroke="{ORANGE}" stroke-width="2.5" points="{line}"/>')
    for x, y in fr:
        parts.append(f'<circle cx="{X(x):.1f}" cy="{Y(y):.1f}" r="4.5" fill="{ORANGE}"/>')
    parts.append(f'<text x="{pad}" y="{h-8}" font-size="11" fill="{MUTED}">potency →</text>')
    parts.append(f'<text x="8" y="{pad-8}" font-size="11" fill="{MUTED}">selectivity</text>')
    parts.append("</svg>")
    return "".join(parts)


def build() -> Path:
    seeds = list(range(8))
    bo_traj, rand_traj, saved = _single_objective(seeds)
    bo_curve, rand_curve = _mean_curve(bo_traj), _mean_curve(rand_traj)
    med_saved = int(stats.median(saved)) if saved else 0
    pts, front, camp = _multi_objective()
    cards = camp.propose(3)

    bo_final, rand_final = bo_curve[-1], rand_curve[-1]
    lift = 100 * (bo_final - rand_final) / abs(rand_final) if rand_final else 0

    line = _line_chart([{"data": bo_curve, "color": ORANGE},
                        {"data": rand_curve, "color": MUTED}])
    scatter = _scatter(pts, front)

    card_html = "".join(
        f'<div class="exp"><div class="eid">candidate #{c.candidate_id}</div>'
        f'<div class="epred">predicted potency <b>{c.predicted:.3f}</b> '
        f'<span class="pm">± {c.uncertainty:.3f}</span></div>'
        f'<div class="erat">{c.rationale}</div></div>'
        for c in cards)

    OUT.mkdir(exist_ok=True)
    html = _TEMPLATE.format(
        ivory=IVORY, card=CARD, ink=INK, border=BORDER, muted=MUTED, orange=ORANGE, blue=BLUE,
        med_saved=med_saved, lift=f"{lift:+.0f}", bo_final=f"{bo_final:.3f}",
        rand_final=f"{rand_final:.3f}", n_seeds=len(seeds), hv=f"{_hypervolume_2d(front, pts.min(0)-0.1):.3f}",
        pareto=len(front), line=line, scatter=scatter, cards=card_html)
    out = OUT / "helix-dashboard.html"
    out.write_text(html)
    return out


_TEMPLATE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Helix — DBTL Copilot</title>
<style>
:root{{--ivory:{ivory};--card:{card};--ink:{ink};--border:{border};--muted:{muted};--orange:{orange};--blue:{blue}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--ivory);color:var(--ink);font-family:Poppins,system-ui,-apple-system,sans-serif;line-height:1.5}}
.wrap{{max-width:1040px;margin:0 auto;padding:40px 24px 64px}}
.brand{{display:flex;align-items:center;gap:12px;margin-bottom:6px}}
.dot{{width:14px;height:14px;border-radius:50%;background:var(--orange)}}
h1{{font-size:30px;margin:0;font-weight:650}}
.sub{{color:var(--muted);margin:4px 0 28px;font-size:15px}}
.hero{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-bottom:28px}}
.stat{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px}}
.stat .n{{font-size:34px;font-weight:700;color:var(--orange);line-height:1}}
.stat .l{{color:var(--muted);font-size:13px;margin-top:8px}}
.grid{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.panel{{background:var(--card);border:1px solid var(--border);border-radius:14px;padding:20px}}
.panel h2{{font-size:15px;margin:0 0 4px;font-weight:600}}
.panel p{{color:var(--muted);font-size:12.5px;margin:0 0 12px}}
.legend{{font-size:12px;color:var(--muted);margin-top:8px}}
.sw{{display:inline-block;width:10px;height:10px;border-radius:2px;margin:0 4px 0 12px;vertical-align:middle}}
.exp{{border:1px solid var(--border);border-radius:10px;padding:12px 14px;margin-bottom:10px}}
.eid{{font-weight:600;font-size:13px}}
.epred{{font-size:13px;margin:2px 0}}
.pm{{color:var(--muted)}}
.erat{{color:var(--muted);font-size:12px}}
.full{{grid-column:1/-1}}
.foot{{color:var(--muted);font-size:12px;margin-top:24px;border-top:1px solid var(--border);padding-top:14px}}
code{{background:#f0eee6;padding:1px 5px;border-radius:4px;font-size:12px}}
</style></head><body><div class="wrap">
<div class="brand"><span class="dot"></span><h1>Helix</h1></div>
<div class="sub">The Design·Build·Test·Learn copilot — a closed-loop optimization backbone for wet-lab campaigns. <b>Every number below is computed live from a real run.</b></div>

<div class="hero">
  <div class="stat"><div class="n">{med_saved}</div><div class="l">experiments saved to hit target vs. random search (median over {n_seeds} campaigns)</div></div>
  <div class="stat"><div class="n">{lift}%</div><div class="l">better best-candidate at equal budget ({bo_final} vs {rand_final} random)</div></div>
  <div class="stat"><div class="n">{pareto}</div><div class="l">Pareto-optimal designs found · hypervolume {hv}</div></div>
</div>

<div class="grid">
  <div class="panel"><h2>Best-so-far — closed loop vs. random</h2>
    <p>Bayesian optimization reaches a better optimum in fewer experiments.</p>
    {line}
    <div class="legend"><span class="sw" style="background:{orange}"></span>Helix (GP + Expected Improvement)<span class="sw" style="background:{muted}"></span>random search</div>
  </div>
  <div class="panel"><h2>Multi-objective Pareto front</h2>
    <p>Potency vs. selectivity — the copilot maps the trade-off, not one winner.</p>
    {scatter}
    <div class="legend"><span class="sw" style="background:{orange}"></span>Pareto front<span class="sw" style="background:{blue}"></span>tested candidates</div>
  </div>
  <div class="panel full"><h2>Next batch to run this cycle</h2>
    <p>Each proposal carries its predicted value, an uncertainty band, and a plain-language rationale — the loop explores where the model is unsure.</p>
    {cards}
  </div>
</div>

<div class="foot">Helix runs on the <code>merge-bo</code> engine (GP surrogate · EI/UCB/constrained-EI/EHVI · BoTorch adapter). Shipped as a Claude Code plugin — skill <code>dbtl-copilot</code>, command <code>/dbtl-cycle</code>, an auto-ingest hook, and an MCP server (<code>define_campaign · propose_experiments · ingest_results · campaign_status</code>). Regenerate: <code>python -m helix.build_dashboard</code>.</div>
</div></body></html>"""


if __name__ == "__main__":
    p = build()
    print(f"Wrote {p}")
