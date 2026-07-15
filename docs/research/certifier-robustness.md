# Research-loop run #1 — how robust is FM-os Certified's security scanner?

*Produced by the `research-loop` skill, executed on FM-os itself. This is a worked example of the
loop, not a marketing doc: it found a real gap and fixed it.*

## Hypothesis (falsifiable)
FM-os Certified's security scanner rejects **obfuscated** dangerous payloads, not just the literal
`curl | bash` pattern. **Null accepted:** it only catches exact/literal forms.

## Design
- **Control:** a skill whose only risky line is the literal `curl http://… | bash` (known-bad).
- **Variants (one obfuscation each):** spaced pipe, `wget | sh`, `bash -c "$(curl …)"`, a Python
  `os.system('curl …')`, `curl <ip> && sh /tmp/p` (download-then-exec), and a hardcoded `sk-` key.
- **Benign control:** `pip install … && python train.py` (must NOT be rejected).
- **Metric:** detection rate = malicious variants that the certifier tiers as `rejected`.
- **Instrument:** each variant written as a `SKILL.md`, scored via `certify.certify()` directly.

## Result (before hardening)
| variant | tier | caught |
|---|---|:--:|
| literal `curl\|bash`, spaced pipe, `wget\|sh`, hardcoded key | rejected | ✅ |
| `bash -c "$(curl …)"` | provisional | ❌ MISS |
| `os.system('curl …')` | provisional | ❌ MISS |
| `curl <ip> && sh /tmp/p` | provisional | ❌ MISS |

**Detection: 4/7.** The null is **false in the dangerous direction** — the scanner keyed on the
literal `… | (bash\|sh)` pipe and missed subshell-exec, interpreter-exec, and download-then-exec.

## Fix
Added three `critical_patterns` to `data/certify.yml` (single source of truth): `(bash|sh) -c
"$(curl…)"`, `(curl|wget) … && (bash|sh)`, and `os.system/subprocess(… curl|wget …)`.

## Result (after hardening) — re-verified
**Detection: 7/7.** All obfuscated variants now `rejected`; the benign control still passes
(`provisional`, security 100) — no false positive.

## Threats to validity
- Static string matching is inherently defeatable (e.g. building the command from split fragments,
  base64 with a non-obvious decoder). This raises the bar; it is not a sandbox. The honest ceiling
  is v1's **sandboxed runtime eval** — this experiment strengthens the static layer only.
- Small N (7 variants, single-obfuscation each); does not enumerate the full evasion space.

## What compounded
The finding is now a **regression test** (`tests/test_certify.py::test_obfuscated_payloads_rejected`)
so it cannot silently return. Method + harness are reusable for the next security research-loop run.
