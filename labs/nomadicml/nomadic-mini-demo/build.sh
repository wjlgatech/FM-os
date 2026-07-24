#!/usr/bin/env bash
# Regenerate the deploy artifacts from the lab's source of truth, then (optionally) deploy.
# The webapp is DATA, not a second copy of truth: _knowledge.txt and results.json are built
# from the lab docs/source and out/*.json so they can never drift.
set -euo pipefail
cd "$(dirname "$0")"

# 1) bundle the copilot knowledge pack + the results payload from the lab (reuses webapp/server.py)
python3 - <<'PY'
import sys, json
from pathlib import Path
sys.path.insert(0, "../webapp")
import server
Path("api/_knowledge.txt").write_text(server.SYSTEM_PROMPT)
docs = []
for f in sorted((server.LAB / "out").glob("*.json")):
    d = json.loads(f.read_text()); clip, _, ex = f.stem.partition("__")
    d["_clip"], d["_example"] = f"{clip}.mp4", ex; docs.append(d)
Path("public/results.json").write_text(json.dumps({"documents": docs}))
print(f"built _knowledge.txt ({len(server.SYSTEM_PROMPT):,} chars) + results.json ({len(docs)} docs)")
PY

# 2) copy the demo clips (gitignored here; canonical copies live in ../data)
mkdir -p public/data && cp ../data/*.mp4 public/data/
echo "copied $(ls public/data/*.mp4 | wc -l | tr -d ' ') clips"

# 3) interview lane-change results — merge every banked live run (Gemini partial + Claude full)
python3 - <<'PY'
import json
from pathlib import Path

RUNS = [  # (file, note shown next to the model name)
    ("../interview/live_results_gemini_partial.json", "partial: free tier is 20 req/day"),
    ("../interview/live_results.json", "full run, frames backend"),
]
stages, models, meta = [], [], {}
for path, note in RUNS:
    f = Path(path)
    if not f.exists():
        continue
    d = json.loads(f.read_text())
    models.append(f"{d['model']} ({note})")
    meta.setdefault("duration_s", d["duration_s"])
    meta.setdefault("ground_truth", d["ground_truth"])
    for s in d["stages"]:
        stages.append({**s, "title": f"{d['model']} · {s['title']}"})
if stages:
    out = {"model": "  +  ".join(models), **meta, "stages": stages}
    Path("public/interview.json").write_text(json.dumps(out, indent=2))
    print(f"built interview.json ({len(models)} run(s), {len(stages)} stages)")
else:
    print("no banked interview runs yet — interview section will show 'pending'")
PY

echo
echo "Deploy:   vercel deploy --prod --yes"
echo "Env vars (set once, Production):  ANTHROPIC_API_KEY  ·  APP_PASSWORD"
