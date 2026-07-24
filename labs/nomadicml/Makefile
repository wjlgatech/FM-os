.PHONY: check unit e2e parity webapp clean

# Visual demo + lab copilot at http://127.0.0.1:8787 (needs ANTHROPIC_API_KEY for chat)
webapp:
	python3 webapp/server.py

# Fast gate: schema contracts + unit tests (no network, no keys needed)
check:
	cd nomadic_mini && python3 -m pytest tests -m "not live and not vlm" -q
	cd interview && python3 -m pytest -q

# Live rehearsal of the interview solution on the real video (needs GEMINI_API_KEY)
interview-live:
	cd interview && python3 run_live.py

# Full local pipeline on the bundled clips (needs GEMINI_API_KEY or ANTHROPIC_API_KEY)
e2e:
	cd nomadic_mini && python3 -m pytest tests -m vlm -q

# Term-by-term parity vs the real NomadicML API (needs NOMADICML_API_KEY; skips honestly without)
parity:
	cd nomadic_mini && python3 -m pytest tests -m live -q

clean:
	find . -name __pycache__ -type d -exec rm -rf {} + 2>/dev/null; true
