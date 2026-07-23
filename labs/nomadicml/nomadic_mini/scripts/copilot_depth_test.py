"""Depth test against the LIVE deployed copilot (/api/chat) — the real thing, not a proxy.

Sends the 10 cofounder questions to the deployed endpoint (which is grounded in the bundled
_knowledge.txt incl. KNOWLEDGE-BASE.md), collects each answer over SSE, then a strict
cofounder-persona judge scores depth + the 15-yo mental model + whether numbers are given.

Run:  APP_PW=... python3 copilot_depth_test.py
"""
import json, os, re, urllib.request
import anthropic

URL = os.environ.get("COPILOT_URL", "https://nomadic-mini-demo.vercel.app/api/chat")
PW = os.environ["APP_PW"]
JUDGE_MODEL = "claude-sonnet-5"
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "out", "copilot-depth-test.md")

QUESTIONS = [
    ("VLM fine-tuning for motion", "To make a VLM reason about motion (turns, lane changes) in driving video, what exactly would you fine-tune vs freeze, and why?"),
    ("Spatiotemporal localization eval", "How would you measure whether the model puts an event at the RIGHT time in the clip — design the metric, not just 'accuracy'?"),
    ("DeepSpeed ZeRO stages", "Walk me through ZeRO stages 1/2/3 — what each shards, the memory math, and how you choose one for a large VLM."),
    ("Video token explosion", "A minute of video is a huge number of tokens. How do you fit video into a VLM's context without blowing up cost or losing motion?"),
    ("Curation loop / collapse", "In an 'AI-training-AI' curation loop, how do you stop the model from collapsing or drifting as it labels its own data?"),
    ("Retrieval over millions of frames", "How would you build search over events across millions of frames — embeddings, index choice, recall at scale?"),
    ("VLM inference optimization", "How do you make VLM inference cheap and fast for enterprise fleets — quantization, KV cache, batching, TensorRT?"),
    ("Narrative consistency", "How do you measure whether the model's DESCRIPTION of a scene is faithful and not hallucinated?"),
    ("Multi-modal fusion", "How do you fuse video with language and sensor metadata (GPS, IMU, lidar) — early/late/cross-attention, and why?"),
    ("Petabyte data pipeline", "At petabyte scale, how do you feed GPUs fast enough that they're not starved?"),
]


def ask_copilot(q):
    body = json.dumps({"messages": [{"role": "user", "content": q}]}).encode()
    req = urllib.request.Request(URL, data=body, method="POST",
                                 headers={"Content-Type": "application/json", "X-App-Password": PW})
    out = ""
    with urllib.request.urlopen(req, timeout=90) as r:
        for raw in r:
            line = raw.decode().strip()
            if line.startswith("data:"):
                j = json.loads(line[5:])
                out += j.get("delta", "")
                if j.get("error"):
                    return f"[ERROR] {j['error']}"
    return out.strip()


def main():
    client = anthropic.Anthropic()
    rows = []
    for i, (topic, q) in enumerate(QUESTIONS, 1):
        print(f"[{i}/10] {topic} …")
        ans = ""
        for _ in range(3):  # retry transient short/empty responses
            ans = ask_copilot(q)
            if len(ans) > 300 and not ans.startswith("[ERROR]"):
                break
        schema = ('Return ONLY compact JSON {"depth":0-5,"has_numbers":true/false,'
                  '"mental_model":true/false,"grade_reason":"20-30 words"}')
        v = {}
        for _ in range(3):
            jr = client.messages.create(model=JUDGE_MODEL, max_tokens=400,
                system="You are a demanding NomadicML technical cofounder grading an answer for DEPTH, concrete NUMBERS, and a 15-yo mental model. Be strict.",
                messages=[{"role": "user", "content": f"Q: {q}\n\nA:\n{ans}\n\n{schema}"}])
            t = "".join(b.text for b in jr.content if b.type == "text")
            for m in re.findall(r"\{[^{}]*\}", t, re.DOTALL):
                try:
                    c = json.loads(m)
                    if "depth" in c:
                        v = c; break
                except json.JSONDecodeError:
                    continue
            if v:
                break
        rows.append({"i": i, "topic": topic, "q": q, "ans": ans, **v})

    passed = [r for r in rows if r.get("depth", 0) >= 4 and r.get("mental_model")]
    avg = sum(r.get("depth", 0) for r in rows) / len(rows)
    L = ["# Live copilot depth test — deployed /api/chat\n",
         f"**{len(passed)}/10 answered at depth ≥4 with a 15-yo mental model. Avg depth {avg:.1f}/5.**\n",
         "> The REAL deployed copilot (grounded in bundled _knowledge.txt incl. KNOWLEDGE-BASE.md), "
         "graded by a strict cofounder-persona judge.\n",
         "| # | Topic | Depth | Numbers | 15-yo | Grade reasoning |", "|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['i']} | {r['topic']} | {r.get('depth','?')} | "
                 f"{'✅' if r.get('has_numbers') else '—'} | {'✅' if r.get('mental_model') else '❌'} | "
                 f"{r.get('grade_reason','')} |")
    L.append("\n---\n")
    for r in rows:
        L.append(f"## {r['i']}. {r['topic']} · depth {r.get('depth','?')}/5\n\n**Q:** {r['q']}\n\n"
                 f"**Copilot:**\n\n{r['ans']}\n")
    open(os.path.normpath(OUT), "w").write("\n".join(L))
    print(f"\n{len(passed)}/10 passed, avg depth {avg:.1f} → wrote out/copilot-depth-test.md")


if __name__ == "__main__":
    main()
