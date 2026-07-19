.PHONY: check build validate test ainative sync site certify distill distill-check clean help

help:
	@echo "FM-os — data-driven, SLM-first foundation-model ops hub"
	@echo ""
	@echo "  make build     Regenerate README.md from data/*.yml"
	@echo "  make validate  Schema-gate data/*.yml (required fields + URLs)"
	@echo "  make test      Run the pytest suite (build/validate/certify logic)"
	@echo "  make check     validate + test + build + drift-gate (CI's finish line)"
	@echo "  make sync      Refresh live repo stars/releases (needs network)"
	@echo "  make certify   Re-certify the tooling registry + refresh badges"
	@echo "  make ainative  Self-audit vs AI-native / loop-engineering principles"
	@echo "  make jdfit JD=<file>   Score FM-os coverage of a job description"
	@echo ""

build:
	python3 scripts/build_readme.py

validate:
	python3 scripts/validate.py

test:
	python3 -m pytest -q

# Self-audit: does our own operation still follow the AI-native / loop-engineering
# principles? Gates at 85 so a regression in HOW we work also fails CI.
ainative:
	python3 scripts/ainative.py --gate 85

# The finish line: code behaves (pytest), data is well-formed (validate), the
# committed README matches the generator (drift), AND we stay AI-native (audit).
check: validate test ainative distill-check
	python3 scripts/build_readme.py --check

# Distill cited repos -> per-repo knowledge graph + tooling scaffold under distill/.
#   make distill              regenerate every distilled repo (spec = data/repos.yml)
#   make distill SLICE=a,b,c  distill a thin slice
distill:
	python3 scripts/distill.py $(if $(SLICE),--slugs $(SLICE),--all)

# Validate every distilled graph (provenance, no orphans/dangling edges) + flag drift. Gates CI.
distill-check:
	python3 scripts/distill.py --check

sync:
	python3 scripts/sync.py
	python3 scripts/build_readme.py

site:
	python3 scripts/build_site.py

# Re-run certification across the registry, refresh badges + README.
certify:
	python3 scripts/certify.py --registry
	python3 scripts/build_readme.py

# Score how well FM-os equips a candidate for a JD:  make jdfit JD=path/to/jd.txt
jdfit:
	python3 scripts/jdfit.py --jd $(JD)

clean:
	rm -f data/_stars.yml site/data.json
