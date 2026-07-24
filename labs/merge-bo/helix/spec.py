"""The spec compiler — turn a scientist's plain-language brief into a typed contract.

This is the "encode domain-specific priors and constraints" + "serve to non-domain
experts" half of the JD. A wet-lab scientist should not have to know what an acquisition
function is; they should be able to say:

    "Optimize a peptide for binding affinity. I can run 8 assays a week, ~40 total.
     Keep synthesis cost under 0.7 and also maximize thermostability."

…and get back a machine-checkable OptimizationSpec. The parser is deterministic and
HONEST: it extracts what it can and records what it could not as `open_questions`, never
inventing an objective the scientist did not state. An LLM can pre-fill the same dataclass
(see compile_spec(..., parsed=<dict>)); the schema is the single source of truth either way.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Objective:
    name: str
    direction: str = "max"      # "max" | "min"
    weight: float = 1.0

    def __post_init__(self):
        if self.direction not in ("max", "min"):
            raise ValueError(f"objective direction must be max/min, got {self.direction!r}")


@dataclass
class Constraint:
    name: str
    op: str                     # "<=" | ">="
    threshold: float

    def __post_init__(self):
        if self.op not in ("<=", ">="):
            raise ValueError(f"constraint op must be <= or >=, got {self.op!r}")


@dataclass
class OptimizationSpec:
    """The typed contract the optimizer runs against. Data, not prose — so it can't drift."""
    title: str
    objectives: list[Objective] = field(default_factory=list)
    constraints: list[Constraint] = field(default_factory=list)
    dim: int = 6                       # feature dimensionality of a candidate
    batch_size: int = 4                # experiments proposed per DBTL cycle
    total_budget: int = 40             # total experiments the campaign can afford
    open_questions: list[str] = field(default_factory=list)

    @property
    def is_multi_objective(self) -> bool:
        return len(self.objectives) > 1

    def validate(self) -> list[str]:
        """Return a list of problems; empty means ready to run."""
        errs = []
        if not self.objectives:
            errs.append("no objective defined — what should the campaign maximize/minimize?")
        if self.batch_size < 1:
            errs.append("batch_size must be >= 1")
        if self.total_budget < self.batch_size:
            errs.append("total_budget must be >= batch_size")
        return errs

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "OptimizationSpec":
        return cls(
            title=d.get("title", "campaign"),
            objectives=[Objective(**o) for o in d.get("objectives", [])],
            constraints=[Constraint(**c) for c in d.get("constraints", [])],
            dim=int(d.get("dim", 6)),
            batch_size=int(d.get("batch_size", 4)),
            total_budget=int(d.get("total_budget", 40)),
            open_questions=list(d.get("open_questions", [])),
        )


# ── deterministic natural-language parsing ────────────────────────────────────
_MAX_WORDS = ("maximize", "maximise", "increase", "improve", "boost", "higher")
_MIN_WORDS = ("minimize", "minimise", "reduce", "lower", "decrease", "under", "below", "cheaper")
# nouns a scientist commonly optimizes — enough to seed; the LLM path handles the long tail
_OBJECTIVE_NOUNS = (
    "affinity", "binding", "potency", "activity", "selectivity", "stability",
    "thermostability", "solubility", "expression", "yield", "efficacy", "fluorescence",
)
_CONSTRAINT_NOUNS = ("cost", "toxicity", "synthesis", "size", "weight", "off-target")


_BUDGET_WORDS = ("week", "total", "overall", "batch", "cycle", "day", "month")


def _nearest_direction(text: str, idx: int) -> str:
    """Direction from whichever max/min verb sits CLOSEST to the objective noun."""
    best_word, best_dist, best_dir = None, 10**9, "max"
    for word, direction in [(w, "max") for w in _MAX_WORDS] + [(w, "min") for w in _MIN_WORDS]:
        for m in re.finditer(re.escape(word), text):
            dist = abs(m.start() - idx)
            if dist < best_dist and dist < 40:
                best_dist, best_dir, best_word = dist, direction, word
    return best_dir


def _threshold_after(text: str, noun: str) -> Optional[float]:
    """A limit stated for a constraint noun: 'cost under 0.7', 'toxicity below 5'.

    Requires a limit cue (under/below/</max) between the noun and the number, and rejects
    numbers that belong to a budget phrase ('6 a week') so we never bind the wrong value.
    """
    idx = text.find(noun)
    tail = text[idx: idx + 40]
    m = re.search(r"(under|below|less than|<=?|max(?:imum)?|at most)\s*([0-9]+(?:\.[0-9]+)?)", tail)
    if not m:
        return None
    # reject if a budget word sits right after the number (e.g. "6 a week")
    after = tail[m.end(): m.end() + 12]
    if any(b in after for b in _BUDGET_WORDS):
        return None
    return float(m.group(2))


def _budget_number(text: str, cue: str) -> Optional[float]:
    """A number tied to a budget cue: '~30 total', '6 a week', '8 per batch'."""
    m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*(?:a|per|/)?\s*" + re.escape(cue), text)
    if m:
        return float(m.group(1))
    m = re.search(re.escape(cue) + r"[^0-9]{0,10}([0-9]+(?:\.[0-9]+)?)", text)
    return float(m.group(1)) if m else None


def parse_brief(text: str, title: str = "campaign") -> OptimizationSpec:
    """Best-effort deterministic parse. Records what it couldn't infer as open_questions."""
    lc = text.lower()
    spec = OptimizationSpec(title=title)

    for noun in _OBJECTIVE_NOUNS:
        if noun in lc and not any(o.name == noun for o in spec.objectives):
            spec.objectives.append(Objective(name=noun, direction=_nearest_direction(lc, lc.find(noun))))
    # collapse overlapping head nouns: "binding affinity" is one objective, not two
    names = {o.name for o in spec.objectives}
    if {"binding", "affinity"} <= names:
        spec.objectives = [o for o in spec.objectives if o.name != "binding"]

    for noun in _CONSTRAINT_NOUNS:
        if noun in lc:
            thr = _threshold_after(lc, noun)
            if thr is not None:
                spec.constraints.append(Constraint(name=noun, op="<=", threshold=thr))
            else:
                spec.open_questions.append(f"you mentioned '{noun}' — what is the limit/threshold?")

    total = _budget_number(lc, "total") or _budget_number(lc, "overall")
    if total:
        spec.total_budget = int(total)
    per = _budget_number(lc, "week") or _budget_number(lc, "batch") or _budget_number(lc, "cycle")
    if per:
        spec.batch_size = int(per)

    if not spec.objectives:
        spec.open_questions.append("no objective detected — what quantity should Helix optimize?")
    return spec


def compile_spec(brief: str = "", *, title: str = "campaign",
                 parsed: Optional[dict] = None) -> OptimizationSpec:
    """Front door: compile a brief (deterministic) or accept a pre-parsed dict (LLM path)."""
    if parsed is not None:
        return OptimizationSpec.from_dict({"title": title, **parsed})
    return parse_brief(brief, title=title)
