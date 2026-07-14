# FM-os Certified

Most directories *collect* tools. FM-os **certifies** them. FM-os Certified is an
automated, evidence-based quality + safety standard for Small-Language-Model / foundation-model
**tooling** — skills, plugins, and workflows for AI coding agents.

> The category nobody owns is *trust*. skills.sh and friends list ~2,000 skills with **no
> security review and no quality gate** ("audit every skill yourself"). FM-os Certified is the
> trust layer they can point at.

## How scoring works

The rubric is data, not code: [`data/certify.yml`](../data/certify.yml). `scripts/certify.py`
gathers **static evidence** from a tool's own files and scores 8 dimensions:

| Dimension | Weight | Evidence |
|---|--:|---|
| Provenance | 10 | content-hash pin, declared author + source |
| **Security** 🔒 | 25 | data-driven scan: no `curl\|bash`, no `rm -rf /`, no hardcoded secrets, no exfil |
| Relevance | 15 | genuinely about SLM / FM-ops (pretrain/finetune/RL/serve/eval) |
| Docs | 15 | SKILL.md/manifest with description, trigger, and a usage example |
| Correctness | 10 | ships an example/test (static presence in v0.1; **executed in v1**) |
| Cross-runtime | 10 | runs beyond one host (Claude Code / Codex / Hermes / OpenClaw) |
| Eval | 5 | ships an eval / verification if it touches model quality |
| Freshness | 10 | recent commits (measured only when git history is present) |

**Discipline (inherited from the BRACE playbook):** evidence over claims · **no evidence ⇒ No**
(a dimension with no evidence is *not measured* and excluded from the score, never a fake pass) ·
**Security and Relevance are blocking gates** — a tool cannot be Certified if security fails, and
a gate cannot pass on unmeasured evidence.

**Tiers:** `✅ certified` (≥75 and gates pass) · `🟡 provisional` (≥55) · `❌ rejected` ·
`⚪ not-applicable` (out of SLM/FM-ops scope).

> v0.1 is **static only** — it never executes an untrusted tool. Sandboxed runtime eval
> (does the example actually run? does the eval pass?) is v1.

## Certify your own tool (self-certification)

Run it locally:

```bash
curl -fsSL https://raw.githubusercontent.com/wjlgatech/FM-os/main/scripts/certify.py -o certify.py
# (also grab data/certify.yml next to a scripts/ dir; see the CI action for the exact layout)
python3 certify.py --target . --gate 75 --json
```

Or gate it in your CI and earn the badge:

```yaml
# .github/workflows/certify.yml in YOUR repo
jobs:
  fm-os-certify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: wjlgatech/FM-os/.github/actions/fm-os-certify@main
        with:
          target: .
          gate: "75"
```

Then embed the badge (publish the emitted JSON, e.g. to your Pages, or use the FM-os-hosted one
once you're listed in [`data/registry.yml`](../data/registry.yml)):

```md
![FM-os Certified](https://img.shields.io/endpoint?url=https://wjlgatech.github.io/FM-os/badges/YOUR-TOOL.json)
```

## Get listed on the FM-os hub

Open a PR adding your tool to `data/registry.yml`:

```yaml
- name: your-tool
  kind: skill        # skill | plugin | workflow
  path: path/in/this/repo    # optional — if present, the hub certifies it in CI
  author: your-handle
  source: https://github.com/you/your-tool
```

Tools with a `path` are scored automatically. Tools without one are listed as **⏳ submitted**
until you self-certify — we never score a tool without runnable evidence.
