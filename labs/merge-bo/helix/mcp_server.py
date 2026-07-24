"""Helix MCP server — the closed-loop optimizer as tools any agent can call.

This is "serve to non-domain experts for model democratization" made literal: a wet-lab
scientist talks to Claude Desktop, and Claude drives the DBTL loop through four tools:

    define_campaign(title, brief|spec)   -> compile a brief to a typed spec, start a campaign
    propose_experiments(campaign, batch) -> the next batch to run, with uncertainty + rationale
    ingest_results(campaign, results)    -> record assay readouts, refit
    campaign_status(campaign)            -> best-so-far, budget left, Pareto (if multi-objective)

Implemented as minimal stdio JSON-RPC (MCP 2024-11-05) with NO third-party deps, so it runs
anywhere python runs and is unit-testable: `handle(request_dict)` returns the response dict.
Wire into Claude Desktop / Code via examples in the plugin's mcp.json.

Campaign state persists under helix/campaigns/<name>.json, so a campaign survives across the
days/weeks between proposing a batch and getting wet-lab results back.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from .campaign import Campaign
from .spec import compile_spec

STORE = Path(__file__).parent / "campaigns"
STORE.mkdir(exist_ok=True)

TOOLS = [
    {
        "name": "define_campaign",
        "description": "Compile a plain-language brief (or an explicit spec dict) into a typed "
                       "optimization campaign and start it. Returns the compiled spec + any open questions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "brief": {"type": "string", "description": "plain-language description of the campaign"},
                "spec": {"type": "object", "description": "optional explicit spec (objectives/constraints/budget)"},
            },
            "required": ["title"],
        },
    },
    {
        "name": "propose_experiments",
        "description": "Return the next batch of experiments to run for a campaign, each with a "
                       "predicted value, uncertainty, and a plain-language rationale.",
        "inputSchema": {
            "type": "object",
            "properties": {"campaign": {"type": "string"}, "batch": {"type": "integer"}},
            "required": ["campaign"],
        },
    },
    {
        "name": "ingest_results",
        "description": "Record assay readouts for proposed candidates and refit the model. "
                       "results is a list of {candidate_id, <objective/constraint>: value}.",
        "inputSchema": {
            "type": "object",
            "properties": {"campaign": {"type": "string"}, "results": {"type": "array", "items": {"type": "object"}}},
            "required": ["campaign", "results"],
        },
    },
    {
        "name": "campaign_status",
        "description": "Progress report for a campaign: best-so-far, budget remaining, cycles, and "
                       "Pareto-front size/hypervolume for multi-objective campaigns.",
        "inputSchema": {
            "type": "object",
            "properties": {"campaign": {"type": "string"}},
            "required": ["campaign"],
        },
    },
]


def _path(name: str) -> Path:
    safe = "".join(c for c in name if c.isalnum() or c in "-_")
    return STORE / f"{safe}.json"


# ── tool implementations ──────────────────────────────────────────────────────
def _define(args: dict) -> dict:
    title = args["title"]
    spec = compile_spec(args.get("brief", ""), title=title, parsed=args.get("spec"))
    camp = Campaign(spec, seed=0)
    camp.save(_path(title))
    return {"campaign": title, "spec": spec.to_dict(), "ready": not spec.validate(),
            "issues": spec.validate(), "open_questions": spec.open_questions}


def _propose(args: dict) -> dict:
    camp = Campaign.load(_path(args["campaign"]))
    cards = camp.propose(args.get("batch"))
    camp.save(_path(args["campaign"]))
    return {"campaign": args["campaign"], "experiments": [c.to_dict() for c in cards]}


def _ingest(args: dict) -> dict:
    camp = Campaign.load(_path(args["campaign"]))
    n = camp.ingest(args["results"])
    camp.save(_path(args["campaign"]))
    return {"campaign": args["campaign"], "ingested": n, "status": camp.status()}


def _status(args: dict) -> dict:
    return Campaign.load(_path(args["campaign"])).status()


DISPATCH = {"define_campaign": _define, "propose_experiments": _propose,
            "ingest_results": _ingest, "campaign_status": _status}


# ── JSON-RPC / MCP plumbing ────────────────────────────────────────────────────
def handle(req: dict) -> dict | None:
    """Handle one JSON-RPC request; return the response (or None for a notification)."""
    method, rid = req.get("method"), req.get("id")
    if method == "initialize":
        return _ok(rid, {"protocolVersion": "2024-11-05",
                         "capabilities": {"tools": {}},
                         "serverInfo": {"name": "helix", "version": "0.1.0"}})
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return _ok(rid, {"tools": TOOLS})
    if method == "tools/call":
        params = req.get("params", {})
        name, args = params.get("name"), params.get("arguments", {})
        fn = DISPATCH.get(name)
        if not fn:
            return _err(rid, -32601, f"unknown tool {name!r}")
        try:
            result = fn(args)
        except Exception as exc:  # surface the error as tool content, not a transport crash
            return _ok(rid, {"content": [{"type": "text", "text": f"error: {exc}"}], "isError": True})
        return _ok(rid, {"content": [{"type": "text", "text": json.dumps(result, indent=2)}]})
    return _err(rid, -32601, f"unknown method {method!r}")


def _ok(rid, result):
    return {"jsonrpc": "2.0", "id": rid, "result": result}


def _err(rid, code, msg):
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": code, "message": msg}}


def main() -> int:
    """stdio loop: one JSON-RPC message per line in, one per line out."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            resp = handle(json.loads(line))
        except json.JSONDecodeError:
            continue
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
