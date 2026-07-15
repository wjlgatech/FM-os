.PHONY: check build validate test sync site certify clean help

help:
	@echo "FM-os — data-driven, SLM-first foundation-model ops hub"
	@echo ""
	@echo "  make build     Regenerate README.md from data/*.yml"
	@echo "  make validate  Schema-gate data/*.yml (required fields + URLs)"
	@echo "  make test      Run the pytest suite (build/validate/certify logic)"
	@echo "  make check     validate + test + build + drift-gate (CI's finish line)"
	@echo "  make sync      Refresh live repo stars/releases (needs network)"
	@echo "  make certify   Re-certify the tooling registry + refresh badges"
	@echo "  make jdfit JD=<file>   Score FM-os coverage of a job description"
	@echo ""

build:
	python3 scripts/build_readme.py

validate:
	python3 scripts/validate.py

test:
	python3 -m pytest -q

# The finish line: code behaves (pytest), data is well-formed (validate), AND the
# committed README matches what the generator produces now (drift). Any miss fails.
check: validate test
	python3 scripts/build_readme.py --check

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
