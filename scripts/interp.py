#!/usr/bin/env python3
"""Gate for the AI Interpretability & Alignment claim ledger.

WHAT THIS IS FOR. The section's seed artifact was an AI-generated summary of a
podcast: fluent, well-structured, and wrong about roughly a third of the proper
nouns it asserted. Reading it more carefully would not have helped — the wrong
entries read exactly like the right ones. The only thing that separates them is
a check against a source outside the artifact, and the only way a check stays
honest is if its misses are recorded next to its hits.

So this script does three things, in increasing order of how much they matter:

  1. it validates the ledger's shape (fail-closed: no source URL, no claim)
  2. it reports how much of the ledger is CITABLE, and never rounds up
  3. `--cite <id>` REFUSES to emit anything that is not — that refusal is the
     product; the table is just how you read it

THE RULE THAT DOES THE REAL WORK is `refuted_correction`: an entry where WE
proposed a correction and the primary source proved US wrong. Recording those
is not humility theatre. A corrector that keeps only the corrections that held
reports 100% accuracy by construction, which is the exact failure mode — false
confidence with no internal signal — that this section exists to study.

STALENESS. A claim checked long enough ago is not a checked claim. Each kind
carries a half-life; past it, an entry stops being citable and says so. "It was
true when I looked" is how a live registry rots quietly.

  python3 scripts/interp.py                 # validate + report
  python3 scripts/interp.py --gate 85       # exit 1 below 85% citable
  python3 scripts/interp.py --cite jspace   # emit one claim, or refuse
  python3 scripts/interp.py --errors        # only what the source got wrong
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys

from fmos import load

# Statuses that represent a completed check against a primary source.
CHECKED = ("verified", "corrected", "refuted_correction", "omitted")
STATUSES = CHECKED + ("unverified",)

# Statuses where the SOURCE made an assertion we can score. `omitted` is
# excluded on purpose: the source said nothing, so it cannot be graded wrong —
# it is a gap, which is tracked separately and is arguably worse.
ASSERTED = ("verified", "corrected", "refuted_correction")

REQUIRED = ("id", "kind", "as_transcribed", "status", "checked", "source_id")
DEFAULT_HALF_LIFE = 365


def _date(value: object) -> dt.date | None:
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def validate(doc: dict) -> list[str]:
    """Fail-closed shape check. Every rule here exists because its absence
    would let an unchecked claim pass as a checked one."""
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["interp_ledger.yml: top level must be a mapping"]

    sources = doc.get("sources") or []
    if not isinstance(sources, list) or not sources:
        return errors + ["interp_ledger.yml: expected a non-empty 'sources' list"]
    ids = set()
    for i, src in enumerate(sources):
        where = f"sources[{src.get('id', i)}]"
        for field in ("id", "kind", "title", "url", "received"):
            if not src.get(field):
                errors.append(f"{where}: missing '{field}'")
        if src.get("id") in ids:
            errors.append(f"{where}: duplicate source id")
        ids.add(src.get("id"))

    claims = doc.get("claims") or []
    if not isinstance(claims, list) or not claims:
        return errors + ["interp_ledger.yml: expected a non-empty 'claims' list"]

    seen: set[str] = set()
    for i, row in enumerate(claims):
        where = f"claims[{i}]"
        if not isinstance(row, dict):
            errors.append(f"{where}: entry must be a mapping")
            continue
        where = f"claims[{row.get('id', i)}]"

        for field in REQUIRED:
            if not row.get(field):
                errors.append(f"{where}: missing required field '{field}'")

        cid = str(row.get("id", ""))
        if cid in seen:
            errors.append(f"{where}: duplicate claim id {cid!r}")
        seen.add(cid)

        # A claim naming no source, or a source that does not exist, would vanish
        # from every per-source rate while still counting in the total — a
        # denominator that quietly disagrees with its own numerators.
        if not row.get("source_id"):
            errors.append(f"{where}: missing 'source_id' — which source asserted this?")
        elif row["source_id"] not in ids:
            errors.append(f"{where}: source_id {row['source_id']!r} is not in 'sources'")

        status = row.get("status")
        if status not in STATUSES:
            errors.append(f"{where}: status must be one of {STATUSES}, got {status!r}")

        # `or ""` not a default: YAML `source:` yields None, and str(None) is truthy.
        url = str(row.get("source") or "")
        if status in CHECKED and not url:
            errors.append(f"{where}: status '{status}' requires a primary-source URL")
        if url and not url.startswith(("http://", "https://")):
            errors.append(f"{where}: source must be a URL — got {url!r}")

        # A "correction" that does not change anything is a claim of work not done.
        if status == "corrected":
            if not row.get("verified_as"):
                errors.append(f"{where}: 'corrected' requires 'verified_as'")
            elif str(row["verified_as"]).strip() == str(row.get("as_transcribed", "")).strip():
                errors.append(f"{where}: 'corrected' but verified_as is identical to "
                              f"as_transcribed — that is not a correction")

        # The self-scoring rule: keep the wrong correction itself, or the
        # corrector's accuracy is unmeasurable and reads as perfect.
        if status == "refuted_correction" and not row.get("proposed"):
            errors.append(f"{where}: 'refuted_correction' requires 'proposed' — the "
                          f"correction that was itself wrong must stay on the record")

        # "Could not look" has to say what stopped it, or it is just silence.
        if status == "unverified":
            if not row.get("why"):
                errors.append(f"{where}: 'unverified' requires 'why' — what specifically "
                              f"stopped the check")
            if row.get("source"):
                errors.append(f"{where}: 'unverified' must not carry a source URL — a "
                              f"source that was read is a check that happened")

        if row.get("checked") and _date(row["checked"]) is None:
            errors.append(f"{where}: 'checked' must be an ISO date — got {row['checked']!r}")

    return errors


def stale(row: dict, half_lives: dict, today: dt.date) -> int | None:
    """Days past this claim's half-life, or None if fresh / undatable."""
    when = _date(row.get("checked"))
    if when is None:
        return None
    limit = int(half_lives.get(row.get("kind"), DEFAULT_HALF_LIFE))
    over = (today - when).days - limit
    return over if over > 0 else None


def citable(row: dict, half_lives: dict, today: dt.date) -> bool:
    return row.get("status") in CHECKED and stale(row, half_lives, today) is None


def score(doc: dict, today: dt.date) -> dict:
    claims = doc.get("claims") or []
    half_lives = doc.get("half_life_days") or {}
    counts = {s: sum(1 for c in claims if c.get("status") == s) for s in STATUSES}
    ok = [c for c in claims if citable(c, half_lives, today)]
    stales = [c for c in claims if c.get("status") in CHECKED
              and stale(c, half_lives, today) is not None]

    asserted = [c for c in claims if c.get("status") in ASSERTED]
    wrong = [c for c in asserted if c.get("status") == "corrected"]
    per_source = {}
    for src in doc.get("sources") or []:
        sid = src.get("id")
        a = [c for c in asserted if c.get("source_id") == sid]
        w = [c for c in a if c.get("status") == "corrected"]
        g = [c for c in claims if c.get("source_id") == sid and c.get("status") == "omitted"]
        per_source[sid] = {"asserted": len(a), "wrong": len(w), "gaps": len(g),
                           "rate": 100.0 * len(w) / len(a) if a else None}
    proposed = [c for c in claims if c.get("status") in ("corrected", "refuted_correction")]
    held = [c for c in proposed if c.get("status") == "corrected"]

    return {
        "total": len(claims),
        "counts": counts,
        "citable": len(ok),
        "coverage": 100.0 * len(ok) / len(claims) if claims else 0.0,
        "stale": stales,
        # How wrong was the source, on the claims it actually made?
        "asserted": len(asserted),
        "source_wrong": len(wrong),
        "source_error_rate": 100.0 * len(wrong) / len(asserted) if asserted else 0.0,
        # How wrong were WE, on the corrections we proposed?
        "proposed": len(proposed),
        "corrections_held": len(held),
        "corrector_accuracy": 100.0 * len(held) / len(proposed) if proposed else 0.0,
        "gaps": counts["omitted"],
        "per_source": per_source,
    }


def report(doc: dict, s: dict, errors_only: bool = False) -> None:
    claims = doc.get("claims") or []
    mark = {"verified": "✓", "corrected": "✗→", "refuted_correction": "!!",
            "omitted": "▽", "unverified": "?"}

    print(f"\n═══ Interpretability & Alignment — claim ledger")
    for src in doc.get("sources") or []:
        print(f"    [{src.get('id')}] {str(src.get('title','?'))[:62]}")
        print(f"          {src.get('pipeline','?')}")
    print()

    rows = [c for c in claims
            if not errors_only or c.get("status") in ("corrected", "refuted_correction", "omitted")]
    print(f"  {'':<3}{'id':<22}{'kind':<10}claim")
    for c in rows:
        m = mark.get(c.get("status"), "?")
        head = str(c.get("verified_as") or c.get("as_transcribed") or "").split("\n")[0]
        print(f"  {m:<3}{str(c.get('id'))[:21]:<22}{str(c.get('kind'))[:9]:<10}{head[:78]}")

    print(f"\n  ── the sources ─────────────────────────────────────────────")
    print(f"  {'source':<12}{'asserted':>10}{'wrong':>8}{'rate':>8}{'gaps':>7}")
    for sid, v in s["per_source"].items():
        rate = f"{v['rate']:.0f}%" if v["rate"] is not None else "n/a"
        print(f"  {sid:<12}{v['asserted']:>10}{v['wrong']:>8}{rate:>8}{v['gaps']:>7}")
    print(f"  {'ALL':<12}{s['asserted']:>10}{s['source_wrong']:>8}"
          f"{s['source_error_rate']:>7.0f}%{s['gaps']:>7}")
    print("  (gaps = a caveat the PRIMARY source states and this source dropped)")

    print(f"\n  ── this ledger ─────────────────────────────────────────────")
    for st in STATUSES:
        print(f"  {st:<30} {s['counts'][st]}")
    if s["stale"]:
        for c in s["stale"]:
            print(f"  ⚠ STALE — {c['id']} (past its half-life; not citable until re-checked)")

    print(f"\n  ── us ──────────────────────────────────────────────────────")
    print(f"  corrections proposed           {s['proposed']}")
    print(f"  survived the primary source    {s['corrections_held']}  "
          f"({s['corrector_accuracy']:.0f}% corrector accuracy)")
    if s["counts"]["refuted_correction"]:
        for c in claims:
            if c.get("status") == "refuted_correction":
                print(f"  !! we were wrong about '{c['id']}': proposed "
                      f"{str(c.get('proposed'))[:60]}…")

    print(f"\n  NORTH STAR — Verified Claim Coverage: "
          f"{s['citable']}/{s['total']} ({s['coverage']:.1f}%) citable")
    if s["counts"]["unverified"]:
        print(f"  {s['counts']['unverified']} claim(s) UNVERIFIED and therefore not citable. "
              f"Could not look is not all clear.")


def cite(doc: dict, cid: str, today: dt.date) -> int:
    """Emit one claim in citable form, or refuse. This refusal IS the gate."""
    claims = doc.get("claims") or []
    half_lives = doc.get("half_life_days") or {}
    row = next((c for c in claims if str(c.get("id")) == cid), None)
    if row is None:
        print(f"REFUSED — no claim with id {cid!r} in the ledger", file=sys.stderr)
        return 1
    if not citable(row, half_lives, today):
        over = stale(row, half_lives, today)
        why = (f"{over} days past its half-life — re-check before citing" if over
               else f"status is '{row.get('status')}': {row.get('why') or 'not checked'}")
        print(f"REFUSED — {cid} is not citable. {why}", file=sys.stderr)
        return 1
    print(f"{row.get('verified_as') or row.get('as_transcribed')}")
    print(f"  — source: {row.get('source')}  (checked {row.get('checked')})")
    if row.get("status") == "corrected":
        print(f"  — NOTE: the summary said: {row.get('as_transcribed')}")
    if row.get("status") == "refuted_correction":
        print(f"  — NOTE: our proposed correction was WRONG: {row.get('proposed')}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--gate", type=float, metavar="PCT",
                    help="exit 1 if citable coverage is below PCT")
    ap.add_argument("--cite", metavar="ID", help="emit one claim, or refuse")
    ap.add_argument("--errors", action="store_true",
                    help="show only what the source got wrong or dropped")
    ap.add_argument("--today", help="ISO date override (for tests)")
    args = ap.parse_args()

    doc = load("interp_ledger")
    today = _date(args.today) or dt.date.today()

    errors = validate(doc)
    if errors:
        print("Interpretability ledger FAILED validation:", file=sys.stderr)
        for e in errors:
            print(f"  ✗ {e}", file=sys.stderr)
        return 1

    if args.cite:
        return cite(doc, args.cite, today)

    s = score(doc, today)
    report(doc, s, errors_only=args.errors)

    if args.gate is not None and s["coverage"] < args.gate:
        print(f"\nGATE FAILED — {s['coverage']:.1f}% citable, floor is {args.gate:.1f}%",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
