"""Preference pairs from FM-os's OWN eval artifacts — provenance on every pair.

Two certified sources, no human labeling, no vibes:
  1. syndata-bare's BARE loop (skills/syndata-bare): chosen = the refined,
     fully-grounded caption; rejected = the base draft that hallucinated a
     decoy object. The alignment gate that certified the skill IS the label.
  2. vlm-failure-probe (skills/vlm-failure-probe): chosen = PatchedVSS's
     grounded answer; rejected = MockVSS's observed-failure answer.

The training task is text-conditioned grounding: given a fact list, write a
caption/answer using ONLY those facts. Held-out fact worlds share zero
content words with training facts or decoys (leakage is a tested property).
"""
from __future__ import annotations

import random
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "skills" / "syndata-bare" / "reference"))
sys.path.insert(0, str(REPO / "skills" / "vlm-failure-probe" / "reference"))

import bare_loop  # noqa: E402  (the certified BARE generators)

PROMPT_TMPL = "Facts: {facts}.\nWrite one short sentence using only these facts.\nCaption:"

# held-out fact worlds — content words disjoint from bare_loop.IMAGES and DECOYS
HELDOUT_IMAGES = [
    {"id": "horse_meadow", "main": "horse", "attr": "brown", "objects": {"horse", "meadow", "fence"}},
    {"id": "laptop_desk", "main": "laptop", "attr": "open", "objects": {"laptop", "desk", "mug"}},
    {"id": "boat_harbor", "main": "boat", "attr": "red", "objects": {"boat", "harbor", "rope"}},
    {"id": "violin_stage", "main": "violin", "attr": "polished", "objects": {"violin", "stage", "stand"}},
    {"id": "cactus_pot", "main": "cactus", "attr": "spiky", "objects": {"cactus", "pot", "gravel"}},
    {"id": "kite_field", "main": "kite", "attr": "striped", "objects": {"kite", "field", "string"}},
    {"id": "owl_branch", "main": "owl", "attr": "gray", "objects": {"owl", "branch", "moon"}},
    {"id": "train_bridge", "main": "train", "attr": "blue", "objects": {"train", "bridge", "river"}},
]


def _facts_str(image: dict) -> str:
    return f"{image['main']} ({image['attr']}), " + ", ".join(
        sorted(image["objects"] - {image["main"]})
    )


def _prompt(image: dict) -> str:
    return PROMPT_TMPL.format(facts=_facts_str(image))


def bare_pairs(n_per_image: int = 25, seed: int = 0) -> list[dict]:
    """chosen = refined (grounded) caption · rejected = hallucinated base draft."""
    rng = random.Random(seed)
    pairs = []
    for image in bare_loop.IMAGES:
        made = 0
        while made < n_per_image:
            draft = bare_loop.base_model(image, rng)
            if bare_loop.alignment(image, draft) >= 1.0:
                continue  # only drafts the gate would REJECT become 'rejected'
            refined = bare_loop.refine(image, draft)
            pairs.append(
                {
                    "prompt": _prompt(image),
                    "chosen": " " + refined + ".",
                    "rejected": " " + draft + ".",
                    "provenance": f"syndata-bare/{image['id']} (alignment gate label)",
                }
            )
            made += 1
    return pairs


def probe_pairs() -> list[dict]:
    """chosen = PatchedVSS grounded answer · rejected = MockVSS observed failure."""
    from probe_runner import MockVSS, PatchedVSS, load_spec

    spec = load_spec()
    out = []
    for mode in spec["failure_modes"]:
        for probe in mode["probes"]:
            out.append(
                {
                    "prompt": probe["question"] + "\nAnswer:",
                    "chosen": " " + PatchedVSS.ANSWERS[probe["id"]],
                    "rejected": " " + MockVSS.ANSWERS[probe["id"]],
                    "provenance": f"vlm-failure-probe/{probe['id']} (paper-observed failure)",
                }
            )
    return out


def training_pairs(seed: int = 0) -> list[dict]:
    pairs = bare_pairs(seed=seed) + probe_pairs()
    random.Random(seed).shuffle(pairs)
    return pairs


def heldout_prompts() -> list[dict]:
    """Held-out grounding prompts (facts the training never saw)."""
    return [{"image": im, "prompt": _prompt(im)} for im in HELDOUT_IMAGES]


def train_vocabulary() -> set[str]:
    """Every content word the training worlds contain — for leakage tests."""
    vocab = set(bare_loop.DECOYS)
    for im in bare_loop.IMAGES:
        vocab |= im["objects"] | {im["attr"], im["main"]}
    return vocab
