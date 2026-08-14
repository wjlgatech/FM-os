#!/usr/bin/env python3
"""Live proof: run the BARE pipeline against REAL vision models and write the
evidence artifacts — out/RESULTS.md, out/bare_results_table.tex (paste-ready for
the BARE paper) and out/raw_captions.json.

    ANTHROPIC_API_KEY=… python run_real.py [--repeat 3]

The counterpart of vlm-failure-probe/reference/run_real.py, which is the only
reason the VSS paper carries measurements and the BARE paper does not.

Three pipelines run over identical scenes at matched budget:

  base_only      the base role alone   → expected to hallucinate
  instruct_only  the instruct role     → expected to mode-collapse
  bare           base drafts, instruct refines → expected to pass both gates

WHAT THIS CAN AND CANNOT SUBSTANTIATE
-------------------------------------
Two different claims are at stake and the runner scores them separately:

  pipeline claim — draft-then-refine beats either single stage at matched
                   budget. Measurable with any two models.
  paper claim    — a BASE checkpoint supplies diversity that an instruction-
                   tuned checkpoint cannot. Measurable only when the base role
                   is filled by a real base checkpoint (`vlm_roles`).

Filling the base role with an instruction-tuned model at temperature 1.0 is a
proxy. It can support the pipeline claim; it can NEVER support the paper claim,
and this runner will not stamp it as such. That is the difference between the
0.92 already in the draft and a number worth printing.
"""
from __future__ import annotations

import argparse
import datetime
import itertools
import json
import re
import statistics
import sys
from pathlib import Path

import bare_stimuli
from vlm_roles import (BASE_PROMPT, INSTRUCT_PROMPT, REFINE_PROMPT, get_role,
                       is_true_base)

OUT = Path(__file__).parent / "out"
PIPELINES = ("base_only", "instruct_only", "bare")
GATES = {"alignment_floor": 0.95, "diversity_floor": 0.25}


# ── metrics ──────────────────────────────────────────────────────────────────
def _words(caption: str) -> set[str]:
    toks = re.findall(r"[a-z]+", caption.lower())
    # check singular and plural forms against the closed vocabulary; anything
    # outside that vocabulary is never scored in either direction
    return set(toks) | {t[:-1] for t in toks if t.endswith("s")}


def hallucinations(caption: str, facts: dict) -> set[str]:
    """Colour/shape terms named by the caption that are definitionally ABSENT.

    Only closed-vocabulary decoys count. An unrecognised word is unscored — the
    synonym trap ("box" for "square") would otherwise manufacture failures.
    """
    return _words(caption) & (facts["decoy_colors"] | facts["decoy_shapes"])


def diversity(captions: list[str]) -> float:
    """Mean pairwise Jaccard DISTANCE between caption token sets (0 = collapse)."""
    real = [c for c in captions if c]
    if len(real) < 2:
        return 0.0
    dists = []
    for a, b in itertools.combinations(real, 2):
        ta, tb = set(re.findall(r"[a-z]+", a.lower())), set(re.findall(r"[a-z]+", b.lower()))
        dists.append(1.0 - len(ta & tb) / len(ta | tb) if (ta | tb) else 0.0)
    return sum(dists) / len(dists)


def score(per_scene: dict[str, list[str | None]]) -> dict:
    """Aggregate one pipeline's captions. Unmeasured captions are EXCLUDED from
    every aggregate — never counted as a hallucination, never as a pass."""
    measured, clean = 0, 0
    divs = []
    for scene_id, caps in per_scene.items():
        facts = bare_stimuli.facts(bare_stimuli.by_id(scene_id))
        got = [c for c in caps if c is not None]
        measured += len(got)
        clean += sum(1 for c in got if not hallucinations(c, facts))
        if len(got) >= 2:
            divs.append(diversity(got))
    if not measured:
        return {"measured": 0, "alignment": None, "diversity": None, "yield": None,
                "gate_pass": None, "gate_reasons": ["nothing measured"]}
    alignment = clean / measured
    div = sum(divs) / len(divs) if divs else 0.0
    reasons = []
    if alignment < GATES["alignment_floor"]:
        reasons.append(f"alignment {alignment:.2f} < {GATES['alignment_floor']}")
    if div < GATES["diversity_floor"]:
        reasons.append(f"diversity {div:.2f} < {GATES['diversity_floor']}")
    return {"measured": measured, "alignment": alignment, "diversity": div,
            "yield": clean / measured, "gate_pass": not reasons, "gate_reasons": reasons}


# ── the loop ─────────────────────────────────────────────────────────────────
def run_pipeline(mode: str, base, instruct, n_per_scene: int) -> dict[str, list[str | None]]:
    out: dict[str, list[str | None]] = {}
    for scene in bare_stimuli.SCENES:
        caps: list[str | None] = []
        for _ in range(n_per_scene):
            if mode == "base_only":
                caps.append(base.caption(scene, BASE_PROMPT))
            elif mode == "instruct_only":
                caps.append(instruct.caption(scene, INSTRUCT_PROMPT))
            elif mode == "bare":
                draft = base.caption(scene, BASE_PROMPT)
                caps.append(None if draft is None
                            else instruct.caption(scene, REFINE_PROMPT.format(draft=draft)))
            else:  # pragma: no cover
                raise ValueError(mode)
        out[scene["id"]] = caps
    return out


def verdicts(scored: dict[str, dict], fidelity: str) -> dict:
    """The two claims, scored separately and never conflated."""
    bare, base, instr = scored["bare"], scored["base_only"], scored["instruct_only"]
    if any(s["gate_pass"] is None for s in scored.values()):
        return {"pipeline_claim": None, "paper_claim": None,
                "why": "at least one pipeline measured nothing"}
    pipeline = (bare["gate_pass"]
                and not base["gate_pass"]
                and not instr["gate_pass"])
    why = []
    if not bare["gate_pass"]:
        why.append("bare failed its own gates: " + "; ".join(bare["gate_reasons"]))
    if base["gate_pass"]:
        why.append("base_only passed — no hallucination for refinement to fix")
    if instr["gate_pass"]:
        why.append("instruct_only passed — no mode collapse for diversity to beat")
    return {
        "pipeline_claim": pipeline,
        "paper_claim": bool(pipeline) if fidelity == "true_base" else False,
        "why": "; ".join(why) if why else "all three gates behaved as the thesis predicts",
        "paper_claim_blocked_by_proxy": fidelity != "true_base",
    }


# ── artifacts ────────────────────────────────────────────────────────────────
def _cell(v) -> str:
    return "n.m." if v is None else f"{v:.2f}"


def latex_table(scored: dict[str, dict], meta: dict) -> str:
    rows = []
    for mode in PIPELINES:
        s = scored[mode]
        gate = ("n.m." if s["gate_pass"] is None else ("PASS" if s["gate_pass"] else "FAIL"))
        rows.append("    " + " & ".join([
            mode.replace("_", r"\_"), _cell(s["alignment"]), _cell(s["diversity"]),
            _cell(s["yield"]), str(s["measured"]), gate]) + r" \\")
    fidelity_note = (
        "The base role is filled by a genuine base checkpoint."
        if meta["role_fidelity"] == "true_base" else
        "\\textbf{The base role is filled by an instruction-tuned model at "
        "temperature 1.0, not a base checkpoint.} These figures therefore support "
        "the draft-then-refine pipeline claim only; they do not substantiate "
        "BARE's base-vs-instruct claim."
    )
    return (
        "% Auto-generated by FM-os skills/syndata-bare/reference/run_real.py\n"
        f"% base={meta['base_model']} instruct={meta['instruct_model']} "
        f"fidelity={meta['role_fidelity']} date={meta['date']}\n"
        "% n.m. = not measured — excluded from every aggregate, never a fake pass.\n"
        "\\begin{table}[t]\n  \\centering\n"
        "  \\caption{BARE pipeline under matched budget: grounding alignment, caption "
        f"diversity and yield across {meta['n_scenes']} synthetic scenes. {fidelity_note}}}\n"
        "  \\label{tab:bare-results}\n"
        "  \\begin{tabular}{lccccc}\n    \\hline\n"
        "    Pipeline & Align. & Divers. & Yield & $n$ & Gate \\\\\n    \\hline\n"
        + "\n".join(rows) +
        "\n    \\hline\n  \\end{tabular}\n\\end{table}\n"
    )


def results_md(scored, raw, meta, verd, var) -> str:
    L = [
        "# syndata-bare — live run against real vision models",
        "",
        f"- **base role**: `{meta['base_model']}` @ T={meta['base_temp']}"
        f"{'' if meta.get('base_temp_applied', True) else ' **(REJECTED by the API — model default used)**'}"
        f" (`{meta['role_fidelity']}`)",
        f"- **instruct role**: `{meta['instruct_model']}` @ T={meta['instruct_temp']}"
        f"{'' if meta.get('instruct_temp_applied', True) else ' **(REJECTED by the API — model default used)**'}",
        f"- **scenes**: {meta['n_scenes']} deterministic synthetic compositions "
        f"(`bare_stimuli.py`), {meta['n_per_scene']} caption(s) per scene per pipeline",
        f"- **date**: {meta['date']} · **repeats**: {meta['repeat']}",
        "- alignment = 1 − (captions naming an absent colour/shape) / (captions measured)",
        "- an unmeasured caption is excluded from every aggregate — never scored 0",
        "",
        "| pipeline | alignment | diversity | yield | measured | gate |",
        "|---|---|---|---|---|---|",
    ]
    for mode in PIPELINES:
        s = scored[mode]
        g = ("n.m." if s["gate_pass"] is None
             else ("PASS" if s["gate_pass"] else "FAIL — " + "; ".join(s["gate_reasons"])))
        L.append(f"| {mode} | {_cell(s['alignment'])} | {_cell(s['diversity'])} | "
                 f"{_cell(s['yield'])} | {s['measured']} | {g} |")
    L += [
        "",
        "## The two claims, scored separately",
        "",
        f"- **pipeline claim** (draft-then-refine beats either single stage): "
        f"**{ {True: 'SUBSTANTIATED', False: 'NOT SUBSTANTIATED', None: 'UNMEASURED'}[verd['pipeline_claim']] }**",
        f"- **paper claim** (a BASE checkpoint supplies diversity an instruct model cannot): "
        f"**{ {True: 'SUBSTANTIATED', False: 'NOT SUBSTANTIATED', None: 'UNMEASURED'}[verd['paper_claim']] }**",
        "",
        f"  {verd['why']}",
    ]
    if verd.get("paper_claim_blocked_by_proxy"):
        L += [
            "",
            "  The paper claim is blocked by role fidelity, not by the numbers: the base",
            f"  role is filled by `{meta['base_model']}`, which is instruction-tuned. Point",
            "  `--base-model` at a real base checkpoint over an OpenAI-compatible endpoint",
            "  to make this claim measurable at all.",
        ]
    L += [
        "",
        "## Known limits of this measurement",
        "",
        "1. **Alignment is an upper bound.** Only closed-vocabulary decoys "
        f"({', '.join(sorted(bare_stimuli.ALL_COLORS))} / "
        f"{', '.join(sorted(bare_stimuli.ALL_SHAPES))}) can be scored wrong. Any other "
        "word is unscored, so a hallucination we did not enumerate is invisible.",
        "2. **High-entropy captions route around the vocabulary.** Observed live: the "
        "base role says \"crimson\", \"cobalt\", \"emerald\", \"golden\", \"orbs\" rather "
        "than the plain colour and shape words. The freer the phrasing, the less surface "
        "the detector has — so alignment is a *weaker* bound for the base role than for "
        "the instruct role, in the direction that flatters the base role.",
        "3. **Primitive attributes only.** Colour and shape are checkable without a judge; "
        "that is why this can run at all. It is a weaker proxy than natural-image "
        "captioning, and a result here does not transfer to one without being re-run.",
        "",
        "## Variance",
        "",
    ]
    L.append(var)
    L += ["", "## Raw captions (evidence)", ""]
    for mode in PIPELINES:
        L.append(f"### {mode}")
        for scene_id, caps in raw[mode].items():
            facts = bare_stimuli.facts(bare_stimuli.by_id(scene_id))
            L.append(f"- **{scene_id}** — true: "
                     f"{sorted(facts['colors'])} {sorted(facts['shapes'])}")
            for c in caps:
                if c is None:
                    L.append("  - *(not measured)*")
                else:
                    h = hallucinations(c, facts)
                    tag = f" ⚠ hallucinated: {sorted(h)}" if h else ""
                    L.append(f"  - {c}{tag}")
        L.append("")
    return "\n".join(L)


def variance_report(reps: list[dict[str, dict]], repeat: int) -> str:
    if repeat < 2:
        return ("**UNMEASURED** — a single run. The base role samples at temperature 1.0, so "
                "these figures have unknown spread; `--repeat N` reports it. A single-run "
                "score is not yet a measurement (the lesson vlm-failure-probe learned live).")
    lines = ["| pipeline | metric | values | mean | sd |", "|---|---|---|---|---|"]
    for mode in PIPELINES:
        for metric in ("alignment", "diversity"):
            vals = [r[mode][metric] for r in reps if r[mode][metric] is not None]
            if len(vals) < 2:
                continue
            lines.append(f"| {mode} | {metric} | {', '.join(f'{v:.2f}' for v in vals)} | "
                         f"{statistics.mean(vals):.2f} | {statistics.pstdev(vals):.3f} |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-model", default="claude-haiku-4-5-20251001")
    ap.add_argument("--instruct-model", default="claude-sonnet-5")
    ap.add_argument("--base-temp", type=float, default=1.0)
    ap.add_argument("--instruct-temp", type=float, default=0.0)
    ap.add_argument("--per-scene", type=int, default=3,
                    help="captions per scene per pipeline (diversity needs >= 2)")
    ap.add_argument("--repeat", type=int, default=1,
                    help="repeat the whole run N times and report spread")
    args = ap.parse_args()

    fidelity = "true_base" if is_true_base(args.base_model) else "proxy"
    base = get_role(args.base_model, args.base_temp, "base")
    instruct = get_role(args.instruct_model, args.instruct_temp, "instruct")

    print(f"base role     : {args.base_model} @ T={args.base_temp}  [{fidelity}]")
    print(f"instruct role : {args.instruct_model} @ T={args.instruct_temp}")
    if fidelity == "proxy":
        print("  ! base role is instruction-tuned — the paper's base-vs-instruct claim "
              "cannot be substantiated by this run", file=sys.stderr)

    all_reps, raw_last = [], {}
    for i in range(max(1, args.repeat)):
        raw = {}
        for mode in PIPELINES:
            print(f"run {i + 1}/{args.repeat}: {mode} over "
                  f"{len(bare_stimuli.SCENES)} scenes × {args.per_scene}…")
            raw[mode] = run_pipeline(mode, base, instruct, args.per_scene)
        all_reps.append({m: score(raw[m]) for m in PIPELINES})
        raw_last = raw

    scored = all_reps[0]
    if all(s["measured"] == 0 for s in scored.values()):
        print("nothing measured (no key?) — no artifacts written", file=sys.stderr)
        return 1

    meta = {
        "base_model": args.base_model, "instruct_model": args.instruct_model,
        "base_temp": args.base_temp, "instruct_temp": args.instruct_temp,
        "role_fidelity": fidelity, "n_scenes": len(bare_stimuli.SCENES),
        "n_per_scene": args.per_scene, "repeat": args.repeat,
        "date": datetime.date.today().isoformat(),
        # A requested temperature that the API refused is not the regime that ran.
        "base_temp_applied": getattr(base, "temperature_applied", True),
        "instruct_temp_applied": getattr(instruct, "temperature_applied", True),
    }
    verd = verdicts(scored, fidelity)
    var = variance_report(all_reps, args.repeat)

    OUT.mkdir(exist_ok=True)
    (OUT / "RESULTS.md").write_text(results_md(scored, raw_last, meta, verd, var))
    (OUT / "bare_results_table.tex").write_text(latex_table(scored, meta))
    (OUT / "raw_captions.json").write_text(json.dumps(
        {"meta": meta, "verdicts": verd, "scored": all_reps, "captions": raw_last}, indent=1))

    for mode in PIPELINES:
        s = scored[mode]
        print(f"  {mode:<14} align={_cell(s['alignment'])} div={_cell(s['diversity'])} "
              f"yield={_cell(s['yield'])} n={s['measured']} "
              f"gate={'PASS' if s['gate_pass'] else 'FAIL'}")
    print(f"pipeline claim : {verd['pipeline_claim']}")
    print(f"paper claim    : {verd['paper_claim']}"
          + ("  (blocked: base role is a proxy)" if verd.get("paper_claim_blocked_by_proxy") else ""))
    print(f"wrote {OUT}/RESULTS.md, bare_results_table.tex, raw_captions.json")
    # Exit non-zero when the pipeline claim does not hold: the artifact is still
    # written (an honest negative is evidence), but CI must not read it as green.
    return 0 if verd["pipeline_claim"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
