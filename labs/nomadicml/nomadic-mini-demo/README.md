# nomadic-mini-demo — public, password-gated deployment

The shareable version of the local demo (`../webapp/`), deployed to Vercel with a **real backend**:
a static front end on the CDN plus a Python serverless function that calls Claude live.

**Live:** https://nomadic-mini-demo.vercel.app — 🔒 password-gated (ask Paul for the demo password).

## Layout

```
public/           # static, served from / by the CDN
  index.html      # the demo page (+ password overlay)
  results.json    # real analysis results (built from ../out/*.json)
  data/*.mp4      # the two driving clips (gitignored; build.sh copies from ../data)
api/
  chat.py         # REAL backend — @vercel/python serverless fn; streams Claude over SSE
  _knowledge.txt  # build-time bundle of every lab doc + engine source (the copilot's grounding)
vercel.json       # explicit builds (python fn + static) so Vercel doesn't force a single ASGI app
```

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
