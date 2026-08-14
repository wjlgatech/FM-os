#!/usr/bin/env python3
"""Real-VLM adapter: run the probe suite against an actual vision model.

Exposes the same `answer(probe) -> str | None` seam the runner grades, backed
by the Anthropic Messages API: each probe's synthetic stimulus (stimuli.py)
is subsampled to a handful of ordered frames and sent with the question.

Honesty rules (no evidence ⇒ No — and equally, no evidence ⇒ not a FAILURE):
- no ANTHROPIC_API_KEY  → every answer is None → every mode "not measured"
- an API error after retries → that probe is None, never a guessed string
- an EMPTY response (no text block) → None, never the empty string: "" scores 0.0
  and would be published as a model failure it never committed
"""
from __future__ import annotations

import base64
import io
import os
import sys

import stimuli

DEFAULT_MODEL = os.environ.get("VLM_PROBE_MODEL", "claude-sonnet-5")
MAX_FRAMES = 6
# 200 was too tight: compound-prompt answers were cut off MID-WORD ("...A yellow
# short") and the missing tail was then graded as a missing sub-answer — a fake
# failure. Found by the 3-repeat variance run. 400 is ample for the "one or two
# short sentences" the prompt asks for; truncation is ALSO detected below, because
# a bigger budget reduces truncation but cannot rule it out.
MAX_TOKENS = int(os.environ.get("VLM_PROBE_MAX_TOKENS", "400"))


def _b64(frame) -> str:
    buf = io.BytesIO()
    frame.save(buf, format="PNG")
    return base64.standard_b64encode(buf.getvalue()).decode()


def _subsample(frames: list, k: int = MAX_FRAMES) -> list:
    if len(frames) <= k:
        return frames
    step = (len(frames) - 1) / (k - 1)
    return [frames[round(i * step)] for i in range(k)]


def get_adapter(model: str):
    """Route a model name to its provider adapter (anthropic claude-* / openai gpt-*)."""
    if model.startswith("claude"):
        return RealVLM(model)
    if model.startswith(("gpt-", "o4", "gpt4")):
        return OpenAIVLM(model)
    raise ValueError(f"no adapter for model {model!r}")


class OpenAIVLM:
    """answer(probe) via an OpenAI vision model over the probe's stimulus."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.model = model
        self._client = None
        if os.environ.get("OPENAI_API_KEY"):
            from openai import OpenAI

            self._client = OpenAI()

    def __call__(self, probe: dict) -> str | None:
        if self._client is None:
            return None  # no key -> not measured, never a fake answer
        frames = _subsample(stimuli.generate(probe["id"]))
        content = [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{_b64(f)}"}}
            for f in frames
        ]
        content.append({
            "type": "text",
            "text": (
                f"These {len(frames)} frames are sampled in chronological order from a "
                f"short video. {probe['question']} Answer in one or two short sentences."
            ),
        })
        try:
            r = self._client.chat.completions.create(
                model=self.model, max_completion_tokens=MAX_TOKENS,
                messages=[{"role": "user", "content": content}],
            )
            if r.choices[0].finish_reason == "length":  # truncated ⇒ not measured
                print(
                    f"  ! {probe['id']}: response TRUNCATED at max_tokens={MAX_TOKENS}"
                    " — NOT MEASURED",
                    file=sys.stderr,
                )
                return None
            text = (r.choices[0].message.content or "").strip()
            if not text:  # empty ⇒ not measured, never a fake FAILURE (see RealVLM)
                print(
                    f"  ! {probe['id']}: empty response (finish_reason="
                    f"{r.choices[0].finish_reason}) — NOT MEASURED, not scored 0",
                    file=sys.stderr,
                )
                return None
            return text
        except Exception as exc:  # noqa: BLE001 — any API failure means "not measured"
            print(f"  ! {probe['id']}: API error, probe not measured ({exc})", file=sys.stderr)
            return None


class RealVLM:
    """answer(probe) via a vision-capable Claude model over the probe's stimulus."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self._client = None
        if os.environ.get("ANTHROPIC_API_KEY"):
            import anthropic

            self._client = anthropic.Anthropic()

    def __call__(self, probe: dict) -> str | None:
        if self._client is None:
            return None  # no key -> not measured, never a fake answer
        frames = _subsample(stimuli.generate(probe["id"]))
        content = [
            {
                "type": "image",
                "source": {"type": "base64", "media_type": "image/png", "data": _b64(f)},
            }
            for f in frames
        ]
        content.append(
            {
                "type": "text",
                "text": (
                    f"These {len(frames)} frames are sampled in chronological order from a "
                    f"short video. {probe['question']} Answer in one or two short sentences."
                ),
            }
        )
        try:
            msg = self._client.messages.create(
                model=self.model,
                max_tokens=MAX_TOKENS,
                messages=[{"role": "user", "content": content}],
            )
            text = "".join(b.text for b in msg.content if b.type == "text").strip()
            # A TRUNCATED answer must not be graded either: the content the matcher
            # is looking for may be in the part that was cut off, so scoring it is
            # the same fake failure as scoring an empty one. Not measured.
            if getattr(msg, "stop_reason", None) == "max_tokens":
                print(
                    f"  ! {probe['id']}: response TRUNCATED at max_tokens={MAX_TOKENS}"
                    " — NOT MEASURED (grading a cut-off answer invents a failure)",
                    file=sys.stderr,
                )
                return None
            # An EMPTY response is NOT a wrong answer. Returning "" here would score
            # 0.0 and be reported as a model failure — a FAKE FAILURE, the exact
            # mirror of the fake pass this suite is built to prevent. Found live:
            # 3 of 5 "GRADER-UNSTABLE" pairs in the first 3-repeat run were empty
            # responses (no text block — e.g. all tokens spent on a non-text block,
            # or a bare refusal) silently graded as wrong.
            if not text:
                print(
                    f"  ! {probe['id']}: empty response (stop_reason="
                    f"{getattr(msg, 'stop_reason', '?')}, blocks="
                    f"{[b.type for b in msg.content]}) — NOT MEASURED, not scored 0",
                    file=sys.stderr,
                )
                return None
            return text
        except Exception as exc:  # noqa: BLE001 — any API failure means "not measured"
            print(f"  ! {probe['id']}: API error, probe not measured ({exc})", file=sys.stderr)
            return None
