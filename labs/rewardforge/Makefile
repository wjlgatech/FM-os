.PHONY: check e2e help

help:
	@echo "RewardForge — eval-derived preference pairs → LoRA-DPO → held-out gate"
	@echo "  make check   offline gates: pairs provenance/leakage, DPO math, gate math"
	@echo "  make e2e     REAL fine-tune (downloads SmolLM2-135M, ~5-15 min on MPS)"

check:
	python3 -m pytest tests -q

e2e:
	python3 -m rewardforge.run
