# nomadic-mini-demo — public, password-gated deployment

The shareable version of the local demo (`../webapp/`), deployed to Vercel with a **real backend**:
a static front end on the CDN plus a Python serverless function that calls Claude live.

**Live:** https://nomadic-mini-demo.vercel.app — 🔒 password-gated (ask Paul for the demo password).

## Layout

```
public/           # static, served from / by the CDN
  index.html      # the demo page (password overlay · copilot · "Analyze your own clip" panel)
  results.json    # real analysis results (built from ../out/*.json)
  data/*.mp4      # the two driving clips (gitignored; build.sh copies from ../data)
api/
  chat.py         # REAL backend — @vercel/python; streams Claude (copilot) over SSE
  analyze.py      # REAL pipeline — @vercel/python; user clip → Gemini native video → events,
                  #   streaming SSE stage progress (download→upload→process→generate→parse→done)
  blob-upload.js  # @vercel/node — Vercel Blob client-upload handshake (password-gated), so the
                  #   browser uploads big clips DIRECT to Blob (bypasses the 4.5 MB function limit)
  _knowledge.txt  # build-time bundle of every lab doc + engine source (the copilot's grounding)
package.json      # @vercel/blob (for the Node handshake fn)
vercel.json       # explicit polyglot builds (2× python + node + static); analyze maxDuration 60
```

## Live "Analyze your own clip"

Drop a video (or paste a direct URL) → 1-click **Analyze** → **real progress bar** (upload % is
genuine, from Blob client-upload; then live SSE analysis stages) → events rendered on a clickable
timeline, same schema as the bundled results. Gemini native video (no ffmpeg needed in the
runtime); fast mode to fit the ~60 s function budget — **best for short, low-res clips; longer ones
may time out** (surfaced honestly, never a fake result). Gated by `APP_PASSWORD`; spends Gemini
quota per run.

Env vars (Vercel Production): `ANTHROPIC_API_KEY` · `GEMINI_API_KEY` · `APP_PASSWORD` ·
`BLOB_READ_WRITE_TOKEN` (injected by the connected Blob store `nomadic-demo-uploads`).

## Security model (honest scope)

- **`APP_PASSWORD`** gates `/api/chat` — the only endpoint that spends Anthropic credits. Wrong/no
  password → `unauthorized`, no model call. The page shows a password overlay before you can chat.
- The static page/videos/results are on the public CDN (fetchable by direct URL) — they're
  non-sensitive demo content. The credit-spending path is what's protected.
- No secrets in this repo: `ANTHROPIC_API_KEY` and `APP_PASSWORD` are Vercel **Production env vars**,
  read at runtime via `os.environ`. Nothing is committed.

## Build & deploy

```bash
./build.sh                 # regenerate _knowledge.txt + results.json, copy clips
vercel deploy --prod --yes # deploy (project: nomadic-mini-demo)
```

Deploy gotchas already solved (see `vercel.json`): explicit `builds` avoids Vercel's single-ASGI
Python autodetect; SSO deployment protection was disabled via the API so the site is publicly
reachable (the app-level password gate replaces it).
