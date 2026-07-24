.PHONY: check e2e botorch helix mcp clean help

help:
	@echo "merge-bo — closed-loop Bayesian optimization lab + Helix DBTL copilot"
	@echo "  make check    Offline gate: pytest (engine + Helix product: 21 tests)"
	@echo "  make e2e      Run the BO demo, regenerate out/RESULTS.md (numpy only)"
	@echo "  make botorch  Run the same loop on the real BoTorch stack (if installed)"
	@echo "  make helix    Regenerate the Helix product dashboard (out/helix-dashboard.html)"
	@echo "  make mcp      Start the Helix MCP server (stdio JSON-RPC)"

check:
	python3 -m pytest -q tests

e2e:
	python3 run_demo.py

botorch:
	python3 -m merge_bo.botorch_adapter

helix:
	python3 -m helix.build_dashboard

mcp:
	python3 -m helix.mcp_server

clean:
	rm -rf .pytest_cache */__pycache__ tests/__pycache__ helix/campaigns/*.json helix/campaigns/*.csv
