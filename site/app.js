/* FM-os Copilot — agentic webapp over a verified SLM knowledge base.
 * Deterministic actions run with no key; open-ended answers/drafts use a
 * bring-your-own Anthropic key stored in localStorage. Grounded in data.json,
 * which is compiled from the same data/*.yml source of truth as the README. */

let DB = { repos: [], courses: [], papers: [], jobs: [], models: [], counts: {} };
const $ = (s, r = document) => r.querySelector(s);
const el = (t, c, h) => { const e = document.createElement(t); if (c) e.className = c; if (h != null) e.innerHTML = h; return e; };
const esc = s => String(s == null ? "" : s).replace(/[&<>]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c]));
const byTopic = (arr, t) => arr.filter(x => x.topic === t);
const byCat = (arr, c) => arr.filter(x => x.category === c);

/* ---------- LLM (BYOK) ---------- */
const KEY = "fmos_anthropic_key";
const getKey = () => localStorage.getItem(KEY) || "";
function keyState() {
  $("#keyState").textContent = getKey() ? "✓ key set" : "";
}
async function llm(system, user) {
  const key = getKey();
  if (!key) throw new Error("no-key");
  const r = await fetch("https://api.anthropic.com/v1/messages", {
    method: "POST",
    headers: {
      "content-type": "application/json",
      "x-api-key": key,
      "anthropic-version": "2023-06-01",
      "anthropic-dangerous-direct-browser-access": "true",
    },
    body: JSON.stringify({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 900,
      system,
      messages: [{ role: "user", content: user }],
    }),
  });
  if (!r.ok) throw new Error("HTTP " + r.status + " — " + (await r.text()).slice(0, 200));
  const j = await r.json();
  return (j.content || []).map(b => b.text || "").join("");
}
/* Compact grounded index for the LLM system prompt. */
function groundingIndex() {
  const line = x => `- ${x.name || x.title} <${x.url}>${x.blurb ? ": " + x.blurb : x.focus ? ": " + x.focus : ""}`;
  return [
    "# FM-os knowledge base (only cite from here; if not present, say so).",
    "## Repos", ...DB.repos.map(line),
    "## Courses", ...DB.courses.map(line),
    "## Papers", ...DB.papers.map(line),
    "## Jobs/People/Orgs", ...DB.jobs.map(line),
  ].join("\n").slice(0, 14000);
}

/* ---------- modal ---------- */
function open(title, sub, build) {
  const m = $("#modal");
  m.innerHTML = "";
  m.appendChild(el("button", "close", "&times;")).onclick = close;
  m.appendChild(el("h2", null, esc(title)));
  m.appendChild(el("div", "sub", sub));
  const body = m.appendChild(el("div"));
  build(body);
  $("#overlay").classList.add("open");
}
function close() { $("#overlay").classList.remove("open"); }
$("#overlay").addEventListener("click", e => { if (e.target.id === "overlay") close(); });

/* ---------- helpers ---------- */
const isNC = m => !!m.nc || /NC|non-?commercial/i.test(m.license || "");
const parseB = p => { const m = /([\d.]+)\s*B/i.exec(p || ""); return m ? parseFloat(m[1]) : (/(\d+)\s*M/i.exec(p || "") ? parseFloat(RegExp.$1) / 1000 : null); };
function linkList(items, fmt) {
  const ul = el("ul");
  items.forEach(x => { const li = el("li"); li.innerHTML = fmt(x); ul.appendChild(li); });
  return ul;
}
function copy(text, btn) {
  navigator.clipboard.writeText(text).then(() => { const t = btn.textContent; btn.textContent = "✓ copied"; setTimeout(() => btn.textContent = t, 1500); });
}

/* ======================= THE 10 ACTIONS ======================= */
const ACTIONS = [
  /* ---- KNOWLEDGE ---- */
  {
    id: "path", pillar: "Knowledge", ic: "🗺️", title: "Build my learning path",
    desc: "An ordered plan across courses, repos & papers for your goal + level.",
    run(b) {
      const goals = {
        "train": "Train a small model from scratch",
        "finetune": "Fine-tune an open SLM on my data",
        "align": "Post-train / align (SFT → DPO → RL)",
        "deploy": "Quantize & deploy on-device",
      };
      b.innerHTML = `<div class="field"><label>Your goal</label><select id="g">${Object.entries(goals).map(([k, v]) => `<option value="${k}">${v}</option>`).join("")}</select></div>
        <div class="field"><label>Your level</label><select id="lv"><option value="beg">Beginner</option><option value="int">Intermediate</option></select></div>
        <button class="btn" id="go">Generate path</button><div class="result" id="out"></div>`;
      $("#go", b).onclick = () => {
        const g = $("#g", b).value, out = $("#out", b); out.innerHTML = "";
        const steps = [];
        const course = t => byTopic(DB.courses, t)[0];
        const repo = c => byCat(DB.repos, c).find(r => r.slm) || byCat(DB.repos, c)[0];
        const paper = t => byTopic(DB.papers, t)[0];
        steps.push(["Foundations", course("foundations") || course("pretraining")]);
        if (g === "train") { steps.push(["From-scratch course", course("pretraining")], ["Training framework", repo("frameworks")], ["Scaling law", paper("scaling")], ["Data recipe", paper("pretraining")]); }
        if (g === "finetune") { steps.push(["Fine-tuning course", byTopic(DB.courses, "finetuning")[0]], ["PEFT toolkit", repo("finetuning")], ["LoRA paper", DB.papers.find(p => /LoRA/.test(p.title))], ["Evaluate", repo("eval")]); }
        if (g === "align") { steps.push(["Post-training course", byTopic(DB.courses, "posttraining")[0]], ["RL toolkit", repo("rl")], ["DPO paper", DB.papers.find(p => /Direct Preference/.test(p.title))], ["GRPO paper", DB.papers.find(p => /DeepSeekMath|R1/.test(p.title))]); }
        if (g === "deploy") { steps.push(["Serving engine", repo("serving")], ["Quantization", repo("compression")], ["AWQ paper", DB.papers.find(p => /AWQ/.test(p.title))], ["Pick a model", null]); }
        const ol = el("ol");
        steps.filter(s => s[1]).forEach(([label, x]) => {
          ol.appendChild(el("li", null, `<strong>${esc(label)}:</strong> <a href="${x.url}" target="_blank">${esc(x.name || x.title)}</a>${x.blurb ? " — " + esc(x.blurb) : ""}`));
        });
        out.appendChild(el("p", null, "Follow these in order 👇"));
        out.appendChild(ol);
        const md = "# My FM-os path\n" + steps.filter(s => s[1]).map(([l, x], i) => `${i + 1}. ${l}: ${x.name || x.title} — ${x.url}`).join("\n");
        const dl = el("button", "btn ghost", "⬇ Export as checklist");
        dl.onclick = () => { const a = el("a"); a.href = "data:text/markdown," + encodeURIComponent(md); a.download = "fm-os-path.md"; a.click(); };
        out.appendChild(dl);
      };
    },
  },
  {
    id: "ask", pillar: "Knowledge", ic: "💬", title: "Ask & get next steps", byok: true,
    desc: "Open-ended Q&A grounded in the knowledge base, with what to read next.",
    run(b) { chatUI(b, "You are the FM-os copilot. Answer ONLY from the provided knowledge base, cite entries as [name](url), and end with a 'Next steps' list. If the KB lacks it, say so plainly.", "Ask about small language models, training, RL, deployment…"); },
  },
  {
    id: "choose", pillar: "Knowledge", ic: "⚖️", title: "Choose a model",
    desc: "Filter the SLM model zoo by size, license & on-device to a ranked table.",
    run(b) {
      if (!DB.models.length) { b.innerHTML = "<p>Model zoo loads with the next data build.</p>"; return; }
      b.innerHTML = `<div class="row">
        <div class="field"><label>Max params (B)</label><input id="mp" type="number" value="4" step="0.5" style="width:90px"></div>
        <div class="field"><label>License</label><select id="lic"><option value="any">Any</option><option value="comm">Commercial-friendly only</option></select></div>
        <div class="field"><label><input type="checkbox" id="od" checked> On-device capable</label></div>
      </div><button class="btn" id="go">Filter</button><div class="result" id="out"></div>`;
      const render = () => {
        const mp = parseFloat($("#mp", b).value) || 99, comm = $("#lic", b).value === "comm", od = $("#od", b).checked;
        let rows = DB.models.filter(m => (parseB(m.params) || 99) <= mp);
        if (od) rows = rows.filter(m => m.ondevice);
        if (comm) rows = rows.filter(m => !isNC(m));
        rows.sort((a, b) => (parseB(a.params) || 0) - (parseB(b.params) || 0));
        const out = $("#out", b);
        out.innerHTML = rows.length ? `<table><thead><tr><th>Model</th><th>Params</th><th>License</th><th>Context</th><th>On-device</th></tr></thead><tbody>${rows.map(m => `<tr><td><a href="${m.url}" target="_blank">${esc(m.name)}</a></td><td>${esc(m.params)}</td><td><span class="chip ${isNC(m) ? "nc" : "ok"}">${esc(m.license)}</span></td><td>${esc(m.context || "—")}</td><td>${m.ondevice ? "✅" : "—"}</td></tr>`).join("")}</tbody></table>` : "<p>No models match — loosen the filters.</p>";
      };
      $("#go", b).onclick = render; render();
    },
  },
  {
    id: "hw", pillar: "Knowledge", ic: "🖥️", title: "Can I run this?",
    desc: "Enter your VRAM/RAM → which models fit at fp16 / 8-bit / 4-bit.",
    run(b) {
      if (!DB.models.length) { b.innerHTML = "<p>Model zoo loads with the next data build.</p>"; return; }
      b.innerHTML = `<div class="field"><label>Available memory for weights (GB)</label><input id="gb" type="number" value="8" step="1"></div>
        <p class="sub">Rule of thumb: fp16 ≈ 2 GB/B, 8-bit ≈ 1 GB/B, 4-bit ≈ 0.6 GB/B (plus KV cache).</p>
        <button class="btn" id="go">Check fit</button><div class="result" id="out"></div>`;
      $("#go", b).onclick = () => {
        const gb = parseFloat($("#gb", b).value) || 8;
        const rows = DB.models.map(m => { const p = parseB(m.params) || 99; return { m, fp16: p * 2, i8: p * 1, i4: p * 0.6 }; })
          .sort((a, c) => a.i4 - c.i4);
        const fit = (v) => v <= gb ? "✅" : "—";
        $("#out", b).innerHTML = `<table><thead><tr><th>Model</th><th>fp16</th><th>8-bit</th><th>4-bit</th></tr></thead><tbody>${rows.map(r => `<tr><td><a href="${r.m.url}" target="_blank">${esc(r.m.name)}</a> <span class="sub">${esc(r.m.params)}</span></td><td>${fit(r.fp16)} ${r.fp16.toFixed(1)}GB</td><td>${fit(r.i8)} ${r.i8.toFixed(1)}GB</td><td>${fit(r.i4)} ${r.i4.toFixed(1)}GB</td></tr>`).join("")}</tbody></table><p class="sub">✅ = fits in ${gb} GB. Use llama.cpp/AWQ for 4-bit.</p>`;
      };
    },
  },
  /* ---- SKILLS-TOOLING ---- */
  {
    id: "recipe", pillar: "Skills · Tooling", ic: "🍳", title: "Generate a recipe",
    desc: "Pick a task → a runnable starter command using the right tool + docs.",
    run(b) {
      const R = {
        lora: { title: "LoRA fine-tune (Unsloth)", repo: "unslothai/unsloth", code: `pip install unsloth\n\nfrom unsloth import FastLanguageModel\nmodel, tok = FastLanguageModel.from_pretrained("unsloth/SmolLM2-1.7B", load_in_4bit=True)\nmodel = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=16)\n# ...then train with trl SFTTrainer on your dataset` },
        dpo: { title: "DPO alignment (TRL)", repo: "huggingface/trl", code: `pip install trl\n\nfrom trl import DPOTrainer, DPOConfig\ntrainer = DPOTrainer(model, args=DPOConfig(beta=0.1),\n                     train_dataset=prefs)  # cols: prompt, chosen, rejected\ntrainer.train()` },
        grpo: { title: "GRPO reasoning RL (TRL)", repo: "huggingface/trl", code: `pip install trl\n\nfrom trl import GRPOTrainer, GRPOConfig\ndef reward(completions, **kw):  # e.g. reward correct answers\n    return [1.0 if is_correct(c) else 0.0 for c in completions]\nGRPOTrainer(model="Qwen/Qwen2.5-1.5B", reward_funcs=reward,\n            args=GRPOConfig(), train_dataset=ds).train()` },
        quant: { title: "Quantize to GGUF (llama.cpp)", repo: "ggml-org/llama.cpp", code: `# convert HF model -> GGUF, then quantize to 4-bit\npython convert_hf_to_gguf.py ./my-model --outfile model.gguf\n./llama-quantize model.gguf model-q4.gguf Q4_K_M` },
        serve: { title: "Serve locally (Ollama)", repo: "ollama/ollama", code: `# run any small model in one command\nollama run smollm2:1.7b\n# or serve an OpenAI-compatible endpoint:\nollama serve  # -> http://localhost:11434` },
      };
      b.innerHTML = `<div class="field"><label>Task</label><select id="t">${Object.entries(R).map(([k, v]) => `<option value="${k}">${v.title}</option>`).join("")}</select></div><div class="result" id="out"></div>`;
      const render = () => {
        const r = R[$("#t", b).value], repo = DB.repos.find(x => x.repo === r.repo);
        const out = $("#out", b);
        out.innerHTML = `<p>${esc(r.title)} — via ${repo ? `<a href="${repo.url}" target="_blank">${esc(repo.name)}</a>` : esc(r.repo)}</p>`;
        const pre = el("pre", null, esc(r.code)); out.appendChild(pre);
        const cp = el("button", "btn ghost", "Copy"); cp.onclick = () => copy(r.code, cp); out.appendChild(cp);
      };
      $("#t", b).onchange = render; render();
    },
  },
  {
    id: "scaffold", pillar: "Skills · Tooling", ic: "📦", title: "Scaffold a project",
    desc: "Download a starter setup script wiring model + fine-tune + eval + serve.",
    run(b) {
      b.innerHTML = `<div class="field"><label>Base model (small)</label><input id="mdl" type="text" value="unsloth/SmolLM2-1.7B"></div>
        <button class="btn" id="go">Generate setup.sh</button><div class="result" id="out"></div>`;
      $("#go", b).onclick = () => {
        const mdl = $("#mdl", b).value.trim() || "unsloth/SmolLM2-1.7B";
        const sh = `#!/usr/bin/env bash\nset -euo pipefail\n# FM-os SLM starter — model: ${mdl}\npython -m venv .venv && source .venv/bin/activate\npip install -U unsloth trl peft datasets lm-eval\n\n# 1) fine-tune (edit train.py): LoRA over ${mdl}\n# 2) evaluate:  lm_eval --model hf --model_args pretrained=${mdl} --tasks hellaswag,arc_easy\n# 3) quantize:  see ggml-org/llama.cpp convert_hf_to_gguf.py\n# 4) serve:     ollama create my-slm -f Modelfile && ollama run my-slm\necho "FM-os starter ready. See https://github.com/wjlgatech/FM-os"`;
        const out = $("#out", b); out.innerHTML = "";
        out.appendChild(el("pre", null, esc(sh)));
        const dl = el("button", "btn", "⬇ Download setup.sh");
        dl.onclick = () => { const a = el("a"); a.href = "data:text/x-sh," + encodeURIComponent(sh); a.download = "setup.sh"; a.click(); };
        out.appendChild(dl);
      };
    },
  },
  {
    id: "install", pillar: "Skills · Tooling", ic: "🔌", title: "Get the tooling",
    desc: "Clone the hub or install it as a Claude Code plugin/skill.",
    run(b) {
      const cmds = `# Clone the knowledge base\ngit clone https://github.com/wjlgatech/FM-os && cd FM-os\nmake help          # data-driven: edit data/*.yml, README regenerates\nmake check         # validate + rebuild + drift-gate\nmake sync          # refresh live repo stars`;
      b.innerHTML = "";
      b.appendChild(el("p", null, "FM-os is data-driven and forkable. Grab it:"));
      b.appendChild(el("pre", null, esc(cmds)));
      const cp = el("button", "btn ghost", "Copy"); cp.onclick = () => copy(cmds, cp); b.appendChild(cp);
      b.appendChild(el("p", "sub", 'A Claude Code plugin (skills + a "sync" workflow) is on the roadmap — see docs/GROWTH.md.'));
    },
  },
  /* ---- CONNECTION ---- */
  {
    id: "people", pillar: "Connection", ic: "🌐", title: "People & orgs to know",
    desc: "The high-impact labs, authors & hiring sources behind the work — linked.",
    run(b) {
      const orgs = {};
      DB.papers.forEach(p => { if (p.org) (orgs[p.org] = orgs[p.org] || []).push(p.title); });
      const labs = DB.jobs.filter(j => j.type === "company");
      const feeds = DB.jobs.filter(j => j.type === "newsletter");
      b.innerHTML = "";
      b.appendChild(el("h3", null, "🏛️ Frontier labs (careers + work)"));
      b.appendChild(linkList(labs, j => `<a href="${j.url}" target="_blank">${esc(j.name)}</a> — ${esc(j.focus)}`));
      b.appendChild(el("h3", null, "📚 Most-cited orgs in the KB"));
      b.appendChild(linkList(Object.entries(orgs).sort((a, c) => c[1].length - a[1].length).slice(0, 8),
        ([o, ps]) => `<strong>${esc(o)}</strong> — ${ps.length} paper${ps.length > 1 ? "s" : ""} here (e.g. ${esc(ps[0])})`));
      b.appendChild(el("h3", null, "📡 Follow the signal"));
      b.appendChild(linkList(feeds, j => `<a href="${j.url}" target="_blank">${esc(j.name)}</a> — ${esc(j.focus)}`));
    },
  },
  {
    id: "outreach", pillar: "Connection", ic: "✉️", title: "Draft an outreach note", byok: true,
    desc: "A tailored, non-cringe intro to a lab/author, grounded in their work.",
    run(b) {
      b.innerHTML = `<div class="field"><label>Who (org or author in the KB)</label><input id="who" type="text" placeholder="e.g. Hugging Face, or the SmolLM2 authors"></div>
        <div class="field"><label>Your goal</label><input id="goal" type="text" placeholder="e.g. contribute to open SLM training / apply for a role"></div>
        <div class="field"><label>About you (1 line)</label><input id="me" type="text" placeholder="e.g. engineer shipping on-device models"></div>
        <button class="btn" id="go">Draft it</button><div class="result" id="out"></div>`;
      $("#go", b).onclick = async () => {
        const out = $("#out", b); out.textContent = "Drafting…";
        try {
          const txt = await llm(
            "You write short, specific, non-sycophantic outreach notes. 120 words max. Reference the recipient's ACTUAL work from the knowledge base; no flattery, no buzzwords. Output just the message.",
            `Knowledge base:\n${groundingIndex()}\n\nWrite an outreach note to: ${$("#who", b).value}\nMy goal: ${$("#goal", b).value}\nAbout me: ${$("#me", b).value}`);
          out.innerHTML = ""; out.appendChild(el("pre", null, esc(txt)));
          const cp = el("button", "btn ghost", "Copy"); cp.onclick = () => copy(txt, cp); out.appendChild(cp);
        } catch (e) { out.innerHTML = needKey(e); }
      };
    },
  },
  {
    id: "contribute", pillar: "Connection", ic: "➕", title: "Contribute a resource",
    desc: "Turn a link into a valid YAML entry + open a prefilled GitHub edit.",
    run(b) {
      b.innerHTML = `<div class="field"><label>Type</label><select id="ty"><option value="repos">Repo</option><option value="courses">Course</option><option value="papers">Paper</option><option value="jobs">Job source</option></select></div>
        <div class="field"><label>Name / title</label><input id="nm" type="text"></div>
        <div class="field"><label>URL</label><input id="url" type="text" placeholder="https://…"></div>
        <div class="field"><label>One-sentence blurb</label><input id="bl" type="text"></div>
        <button class="btn" id="go">Generate entry</button><div class="result" id="out"></div>`;
      $("#go", b).onclick = () => {
        const ty = $("#ty", b).value, nm = $("#nm", b).value.trim(), url = $("#url", b).value.trim(), bl = $("#bl", b).value.trim();
        if (!nm || !url) { $("#out", b).innerHTML = "<p class='sub'>Name and URL are required.</p>"; return; }
        let y;
        if (ty === "repos") y = `- name: ${nm}\n  repo: OWNER/REPO   # fill for star-sync\n  url: ${url}\n  category: models   # models|frameworks|finetuning|rl|eval|serving|compression\n  slm: true\n  blurb: "${bl}"`;
        else if (ty === "courses") y = `- title: "${nm}"\n  org: ORG\n  url: ${url}\n  free: true\n  topic: foundations   # foundations|pretraining|posttraining|finetuning|rl|agents\n  blurb: "${bl}"`;
        else if (ty === "papers") y = `- title: "${nm}"\n  org: ORG\n  year: 2025\n  venue: "arXiv:XXXX"\n  url: ${url}\n  topic: slm   # slm|pretraining|scaling|posttraining|rl|peft|distillation|compression\n  blurb: "${bl}"`;
        else y = `- name: "${nm}"\n  type: board   # company|board|aggregator|newsletter\n  url: ${url}\n  focus: "${bl}"`;
        const out = $("#out", b); out.innerHTML = "";
        out.appendChild(el("p", null, `Append this to <code>data/${ty}.yml</code>:`));
        out.appendChild(el("pre", null, esc(y)));
        const cp = el("button", "btn ghost", "Copy YAML"); cp.onclick = () => copy(y, cp); out.appendChild(cp);
        const edit = el("a", "btn", "✏️ Open GitHub editor");
        edit.href = `https://github.com/wjlgatech/FM-os/edit/main/data/${ty}.yml`; edit.target = "_blank";
        edit.style.marginLeft = "8px"; out.appendChild(edit);
        out.appendChild(el("p", "sub", "Paste the YAML at the end of the file, then commit as a PR. CI runs make check + link-check."));
      };
    },
  },
];

/* ---------- shared chat UI (BYOK actions) ---------- */
function needKey(e) {
  return e.message === "no-key"
    ? `<p>This action needs an Anthropic API key. <a href="#" onclick="promptKey();return false">Add one</a> (stored only in your browser) — deterministic actions work without it.</p>`
    : `<p class="sub">Error: ${esc(e.message)}</p>`;
}
function chatUI(b, system, placeholder) {
  b.innerHTML = `<div id="log"></div><div class="row"><input id="q" type="text" placeholder="${placeholder}" style="flex:1"><button class="btn" id="send">Send</button></div>`;
  const log = $("#log", b), q = $("#q", b);
  const send = async () => {
    const text = q.value.trim(); if (!text) return; q.value = "";
    log.appendChild(el("div", "msg user", esc(text)));
    const bot = log.appendChild(el("div", "msg bot", "…"));
    try { bot.innerHTML = mdLinks(await llm(system + "\n\n" + groundingIndex(), text)); }
    catch (e) { bot.innerHTML = needKey(e); }
  };
  $("#send", b).onclick = send;
  q.addEventListener("keydown", e => { if (e.key === "Enter") send(); });
}
const mdLinks = s => esc(s).replace(/\[([^\]]+)\]\((https?:[^)]+)\)/g, '<a href="$2" target="_blank">$1</a>').replace(/\n/g, "<br>");

/* ---------- key prompt ---------- */
window.promptKey = function () {
  const k = prompt("Paste your Anthropic API key (stored only in this browser's localStorage; never sent anywhere but api.anthropic.com):", getKey());
  if (k !== null) { localStorage.setItem(KEY, k.trim()); keyState(); }
};
$("#setKey").onclick = window.promptKey;

/* ---------- copilot router ---------- */
async function route(text) {
  const t = text.toLowerCase();
  const map = [
    [/(path|plan|learn|roadmap|start|beginner)/, "path"],
    [/(run|vram|ram|gb|fit|memory|hardware|gpu|phone)/, "hw"],
    [/(choose|which model|pick|compare|smallest|license)/, "choose"],
    [/(recipe|lora|dpo|grpo|quantize|serve|fine-?tune|command|snippet)/, "recipe"],
    [/(scaffold|starter|project|template|boilerplate)/, "scaffold"],
    [/(install|clone|plugin|tooling|fork)/, "install"],
    [/(who|people|org|lab|follow|hire|job|career)/, "people"],
    [/(outreach|email|message|intro|dm|reach out)/, "outreach"],
    [/(contribute|add|suggest|submit|entry)/, "contribute"],
  ];
  for (const [re, id] of map) if (re.test(t)) { const a = ACTIONS.find(x => x.id === id); openAction(a, text); return; }
  // fallback: grounded answer
  const a = ACTIONS.find(x => x.id === "ask"); openAction(a);
  const q = $("#q", $("#modal")); if (q) { q.value = text; $("#send", $("#modal")).click(); }
}
function openAction(a, prefill) { open(a.title + (a.byok ? "  ·  needs API key" : ""), esc(a.desc), b => a.run(b)); }

$("#askBtn").onclick = () => { const v = $("#ask").value.trim(); if (v) route(v); };
$("#ask").addEventListener("keydown", e => { if (e.key === "Enter") { const v = $("#ask").value.trim(); if (v) route(v); } });

/* ---------- render ---------- */
function render() {
  $("#counts").innerHTML = [
    ["repos", "repos"], ["courses", "courses"], ["papers", "papers"], ["models", "models"], ["jobs", "job sources"],
  ].filter(([k]) => DB.counts[k]).map(([k, label]) => `<span class="pill">${DB.counts[k]} ${label}</span>`).join("");
  const host = $("#actions");
  const pillars = ["Knowledge", "Skills · Tooling", "Connection"];
  pillars.forEach(p => {
    host.appendChild(el("div", "pillar-label", esc(p)));
    const grid = host.appendChild(el("div", "grid"));
    ACTIONS.filter(a => a.pillar === p).forEach(a => {
      const c = el("div", "card", `<div class="ic">${a.ic}</div><h3>${esc(a.title)}</h3><p>${esc(a.desc)}</p><span class="tag${a.byok ? " byok" : ""}">${a.byok ? "needs key" : "no key needed"}</span>`);
      c.onclick = () => openAction(a);
      grid.appendChild(c);
    });
  });
  keyState();
}

fetch("data.json").then(r => r.json()).then(d => { DB = d; render(); }).catch(() => {
  DB.counts = {}; render();
  $("#actions").prepend(el("p", "hint", "Could not load data.json (open via the deployed site, not file://)."));
});
