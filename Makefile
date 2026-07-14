.PHONY: check build validate sync site clean help

help:
	@echo "FM-os — data-driven, SLM-first foundation-model ops hub"
	@echo ""
	@echo "  make build     Regenerate README.md from data/*.yml"
	@echo "  make validate  Schema-gate data/*.yml (required fields + URLs)"
	@echo "  make check     validate + build + drift-gate (CI's finish line)"
	@echo "  make sync      Refresh live repo stars/releases (needs network)"
	@echo ""

build:
	python3 scripts/build_readme.py

validate:
	python3 scripts/validate.py

# The finish line: data is well-formed AND the committed README matches what
# the generator would produce right now. Fails if either is off.
check: validate
	python3 scripts/build_readme.py --check

sync:
	python3 scripts/sync.py
	python3 scripts/build_readme.py

site:
	python3 scripts/build_site.py

clean:
	rm -f data/_stars.yml site/data.json
