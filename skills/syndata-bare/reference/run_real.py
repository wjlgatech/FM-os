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

# The smallest base-role hallucination rate this suite must be able to SEE.
# Anchored to a published figure rather than taste: independent 2026 frontier
# benchmarking puts Claude Haiku 4.5 — the default base role here — at a 4.62%
# hallucination rate. A run that cannot resolve a rate that size cannot claim
# the base role "does not hallucinate".
MIN_DETECTABLE_RATE = 0.0462


def rule_of_three(n: int) -> float | None:
    """95% upper confidence bound on an event rate after ZERO observed events.

    Hanley & Lippman-Hand, "If nothing goes wrong, is everything all right?
    Interpreting zero numerators" (JAMA 1983): with 0 events in n trials, the
    95% CI for the true rate is [0, 3/n]. It falls straight out of the binomial
    — (1−p)^n = 0.05 — and it is the oldest, plainest correction to the mistake
    this runner made on its first live run: reading 0/18 as "does not happen".
    """
    return None if n <= 0 else 3.0 / n


def power_check(hallucinated: int, measured: int,
                mde: float = MIN_DETECTABLE_RATE) -> dict:
    """Could this run have DETECTED a base-role hallucination rate of `mde`?

    Only meaningful for the zero-event case, which is exactly the case that
    misleads. With events observed, the rate is estimated directly and the
    question does not arise.
    """
    if measured == 0:
        return {"powered": None, "n": 0, "upper95": None, "n_required": None,
                "why": "nothing measured"}
    if hallucinated > 0:
        return {"powered": True, "n": measured, "upper95": None,
                "n_required": None,
                "why": f"{hallucinated} hallucination(s) observed — rate estimated directly"}
    upper = rule_of_three(measured)
    n_req = int(3.0 / mde) + 1
    return {
        "powered": upper <= mde, "n": measured, "upper95": upper,
        "n_required": n_req,
        "why": (f"0 hallucinations in {measured}; 95% CI for the true rate is "
                f"[0, {upper:.3f}]. "
                + (f"That resolves the {mde:.2%} reference rate."
                   if upper <= mde else
                   f"That CANNOT exclude the {mde:.2%} reference rate — "
                   f"n≥{n_req} is needed. The zero is uninformative.")),
    }


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
            "yield": clean / measured, "hallucinated": measured - clean,
            "gate_pass": not reasons, "gate_reasons": reasons}


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


def score_interference(answers: dict[str, list[str | None]]) -> dict:
    """The precondition probe: does the base role hallucinate AT ALL, when a
    published mechanism is used to induce it?

    BARE's pipeline claim presupposes a base role that produces ungrounded
    content for refinement to repair. On plain geometry that presupposition
    could not be resolved. Here a conflicting colour word is printed on the
    shape (arXiv:2511.13400) and the model is asked the shape's colour; naming
    the printed word instead of the actual colour is unambiguous hallucination.
    """
    measured, wrong, detail = 0, 0, []
    for scene_id, got in answers.items():
        scene = bare_stimuli.by_id(scene_id)
        printed = scene["label"].lower()
        true_color = scene["objects"][0][0]
        for a in got:
            if a is None:
                continue
            measured += 1
            words = _words(a)
            hit = printed in words and true_color not in words
            wrong += hit
            detail.append({"scene": scene_id, "answer": a, "true": true_color,
                           "printed": printed, "hallucinated": hit})
    return {"measured": measured, "hallucinated": wrong,
            "rate": (wrong / measured) if measured else None,
            "power": power_check(wrong, measured), "detail": detail}


def verdicts(scored: dict[str, dict], fidelity: str) -> dict:
    """The two claims, scored separately, and never conflated with each other or
    with an absence of evidence.

    THE CORRECTION THIS FUNCTION EXISTS TO CARRY. The first live run reported
    `pipeline_claim: False` because the base role hallucinated 0 times in 18
    captions. That was wrong — not the arithmetic, the LOGIC. By the rule of
    three, 0/18 puts the 95% CI for the true rate at [0, 16.7%], which cannot
    exclude the ~4.6% rate independently published for that very model. The
    honest verdict was never "false"; it was UNDERPOWERED. A claim can only be
    refuted by a run that could have detected it.
    """
    bare, base, instr = scored["bare"], scored["base_only"], scored["instruct_only"]
    if any(s["gate_pass"] is None for s in scored.values()):
        return {"pipeline_claim": None, "paper_claim": None,
                "power": {"powered": None, "why": "nothing measured"},
                "why": "at least one pipeline measured nothing"}

    power = power_check(base.get("hallucinated", 0), base["measured"])

    # The pipeline claim PRESUPPOSES a base role that hallucinates. If the run
    # could not have seen hallucination at the reference rate, the claim was not
    # tested — it is neither supported nor refuted.
    if base["gate_pass"] and power["powered"] is False:
        return {
            "pipeline_claim": None, "paper_claim": None, "power": power,
            "underpowered": True,
            "paper_claim_blocked_by_proxy": fidelity != "true_base",
            "why": ("base_only showed no hallucination, but the run lacked the power to "
                    "detect it: " + power["why"]),
        }

    pipeline = (bare["gate_pass"]
                and not base["gate_pass"]
                and not instr["gate_pass"])
    why = []
    if not bare["gate_pass"]:
        why.append("bare failed its own gates: " + "; ".join(bare["gate_reasons"]))
    if base["gate_pass"]:
        why.append("base_only passed with adequate power — this base role genuinely "
                   "does not hallucinate here, so there is nothing for refinement to fix")
    if instr["gate_pass"]:
        why.append("instruct_only passed — no mode collapse for diversity to beat")
    return {
        "pipeline_claim": pipeline,
        "paper_claim": bool(pipeline) if fidelity == "true_base" else False,
        "power": power,
        "underpowered": False,
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
        "",
        "### Statistical power — could this run have seen what it looked for?",
        "",
        f"  {verd['power']['why']}",
        "",
        "  Rule of three (Hanley & Lippman-Hand, *JAMA* 1983): with 0 events in *n*",
        "  trials the 95% CI for the true rate is [0, 3/n]. Reference rate: "
        f"{MIN_DETECTABLE_RATE:.2%}, the independently published 2026 hallucination rate for",
        "  the default base role. Observing zero does not make the rate zero.",
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


def interference_md(res: dict) -> str:
    p = res["power"]
    powered = {True: "ADEQUATE", False: "UNDERPOWERED", None: "UNMEASURED"}[p["powered"]]
    lines = [
        "## Precondition probe — does the base role hallucinate at all?",
        "",
        "Text-interference in colour perception, after *What Color Is It?* "
        "(arXiv:2511.13400): a conflicting colour word is printed on the shape and the "
        "model is asked the shape's colour. Naming the printed word is unambiguous "
        "hallucination — no caption parsing, no synonym trap.",
        "",
        "This is a SECOND declared condition, not the plain condition retuned. Both are "
        "reported; neither replaces the other.",
        "",
        f"- **measured**: {res['measured']} answers",
        f"- **hallucinated**: {res['hallucinated']}",
        f"- **rate**: {_cell(res['rate'])}",
        f"- **power**: {powered} — {p['why']}",
        "",
    ]
    if res["detail"]:
        lines += ["| scene | true | printed | answer | hallucinated |", "|---|---|---|---|---|"]
        for d in res["detail"][:24]:
            lines.append(f"| {d['scene']} | {d['true']} | {d['printed']} | "
                         f"{d['answer'][:60]} | {'YES' if d['hallucinated'] else 'no'} |")
        if len(res["detail"]) > 24:
            lines.append(f"| … | | | *{len(res['detail']) - 24} more in raw_captions.json* | |")
        lines.append("")
    return "\n".join(lines) + "\n"


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
    ap.add_argument("--interference-n", type=int, default=12,
                    help="answers per interference scene for the precondition probe "
                         "(6 scenes x N; N=12 gives n=72, enough to resolve a 4.62%% rate)")
    ap.add_argument("--skip-interference", action="store_true",
                    help="skip the precondition probe (the plain condition alone "
                         "could not resolve it — you will get an UNDERPOWERED verdict)")
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

    interference = None
    if not args.skip_interference:
        print(f"precondition probe: {len(bare_stimuli.INTERFERENCE_SCENES)} interference "
              f"scenes × {args.interference_n} (text-interference, arXiv:2511.13400)…")
        answers = {
            s["id"]: [base.caption(s, bare_stimuli.INTERFERENCE_QUESTION,
                                   renderer=bare_stimuli.render_interference)
                      for _ in range(args.interference_n)]
            for s in bare_stimuli.INTERFERENCE_SCENES
        }
        interference = score_interference(answers)
        meta["interference_n"] = args.interference_n

    OUT.mkdir(exist_ok=True)
    body = results_md(scored, raw_last, meta, verd, var)
    if interference is not None:
        body = body.replace("## Raw captions (evidence)",
                            interference_md(interference) + "## Raw captions (evidence)", 1)
    (OUT / "RESULTS.md").write_text(body)
    (OUT / "bare_results_table.tex").write_text(latex_table(scored, meta))
    (OUT / "raw_captions.json").write_text(json.dumps(
        {"meta": meta, "verdicts": verd, "scored": all_reps, "captions": raw_last,
         "interference": interference}, indent=1))

    for mode in PIPELINES:
        s = scored[mode]
        print(f"  {mode:<14} align={_cell(s['alignment'])} div={_cell(s['diversity'])} "
              f"yield={_cell(s['yield'])} n={s['measured']} "
              f"gate={'PASS' if s['gate_pass'] else 'FAIL'}")
    POWER_LABEL = {True: "ADEQUATE", False: "UNDERPOWERED", None: "n.m."}
    if interference is not None:
        print(f"  precondition   hallucinated={interference['hallucinated']}"
              f"/{interference['measured']} rate={_cell(interference['rate'])} "
              f"power={POWER_LABEL[interference['power']['powered']]}")
    label = {True: "SUBSTANTIATED", False: "NOT SUBSTANTIATED", None: "INCONCLUSIVE"}
    print(f"pipeline claim : {label[verd['pipeline_claim']]}"
          + ("  (UNDERPOWERED — see the power section)" if verd.get("underpowered") else ""))
    print(f"paper claim    : {label[verd['paper_claim']]}"
          + ("  (blocked: base role is a proxy)" if verd.get("paper_claim_blocked_by_proxy") else ""))
    print(f"wrote {OUT}/RESULTS.md, bare_results_table.tex, raw_captions.json")
    # Exit codes distinguish the three outcomes, because "we could not tell" must
    # never be filed under the same code as "we tested it and it failed":
    #   0 = substantiated · 2 = inconclusive/underpowered · 1 = refuted
    if verd["pipeline_claim"] is True:
        return 0
    return 2 if verd["pipeline_claim"] is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
