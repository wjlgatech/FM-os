#!/usr/bin/env python3
"""The three model roles BARE needs — and an honest account of which are real.

BARE's claim is about *checkpoints*: a *base* model (pre-instruction-tuning)
supplies diversity, an *instruction-tuned* model supplies correctness. Every
model reachable through the Anthropic API is instruction-tuned. So a run driven
by Anthropic alone can fill the base ROLE, but not with a base MODEL.

That distinction is the whole reason this file exists. A run records
`role_fidelity`:

  true_base — the base role is filled by a checkpoint listed in BASE_CHECKPOINTS
  proxy     — the base role is filled by an instruction-tuned model coaxed toward
              entropy with temperature 1.0 and an unconstrained prompt

Under `proxy`, the weaker claim (draft-then-refine beats either single stage at
matched budget) is still measurable. The paper's claim is NOT, and `run_real.py`
refuses to mark it substantiated. Set `--base-model` to a real base checkpoint
served over an OpenAI-compatible endpoint (vLLM, NIM, HF TGI) to earn the
stronger verdict.

Honesty rules inherited from vlm-failure-probe/vlm_adapter.py, for the same
reasons found live there: no key, an API error, an empty response, or a
truncated response all mean NOT MEASURED — never a fabricated caption, and never
an empty string, which would score as a hallucination the model never produced.
"""
from __future__ import annotations

import base64
import io
import os
import sys

import bare_stimuli

MAX_TOKENS = int(os.environ.get("BARE_MAX_TOKENS", "200"))

# Checkpoints that are genuinely pre-instruction-tuning. Additive by design: a
# model absent from this list is treated as a proxy, never assumed to be base.
# "Unknown" resolves to the weaker claim, which is the safe direction.
BASE_CHECKPOINTS = {
    "Salesforce/blip2-opt-2.7b",
    "Salesforce/blip2-flan-t5-xl",
    "Qwen/Qwen2.5-VL-7B",
    "llava-hf/llava-1.5-7b-hf-base",
    "meta-llama/Llama-3.2-11B-Vision",
}

BASE_PROMPT = (
    "Describe this image in one sentence. Be imaginative and vary your phrasing."
)
INSTRUCT_PROMPT = (
    "Describe this image in one sentence. State only what is actually visible: "
    "the exact colours and shapes present, nothing else."
)
REFINE_PROMPT = (
    "Here is a draft caption for this image:\n\n  {draft}\n\n"
    "Rewrite it so that every colour and shape it names is actually present in "
    "the image. Keep the draft's phrasing and structure wherever it is already "
    "correct — change only what is ungrounded. Reply with the caption alone."
)


def is_true_base(model: str) -> bool:
    return model in BASE_CHECKPOINTS


def _b64(img) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.standard_b64encode(buf.getvalue()).decode()


def _warn(scene_id: str, role: str, why: str) -> None:
    print(f"  ! {scene_id} [{role}]: {why} — NOT MEASURED", file=sys.stderr)


class AnthropicRole:
    """One model in one role. Returns a caption, or None for 'not measured'."""

    def __init__(self, model: str, temperature: float, role: str):
        self.model, self.temperature, self.role = model, temperature, role
        # Some current models reject `temperature` outright ("deprecated for this
        # model" — hit live on claude-sonnet-5, which silently zeroed the whole
        # instruct role). We retry once without it and RECORD that the sampling
        # regime was not the one requested, because "matched budget" is a claim
        # this runner makes and an unapplied temperature quietly breaks it.
        self.temperature_applied = True
        self._client = None
        if os.environ.get("ANTHROPIC_API_KEY"):
            import anthropic

            self._client = anthropic.Anthropic()

    def caption(self, scene: dict, prompt: str) -> str | None:
        if self._client is None:
            return None  # no key ⇒ not measured, never a fabricated caption
        img = bare_stimuli.render(scene)
        content = [
            {"type": "image",
             "source": {"type": "base64", "media_type": "image/png", "data": _b64(img)}},
            {"type": "text", "text": prompt},
        ]
        kwargs = {"model": self.model, "max_tokens": MAX_TOKENS,
                  "messages": [{"role": "user", "content": content}]}
        if self.temperature_applied:
            kwargs["temperature"] = self.temperature
        try:
            try:
                msg = self._client.messages.create(**kwargs)
            except Exception as exc:  # noqa: BLE001
                if "temperature" not in str(exc) or not self.temperature_applied:
                    raise
                print(f"  ! {self.role}: this model rejects `temperature` — retrying "
                      f"without it; SAMPLING REGIME IS THE MODEL DEFAULT, not "
                      f"T={self.temperature}", file=sys.stderr)
                self.temperature_applied = False
                kwargs.pop("temperature", None)
                msg = self._client.messages.create(**kwargs)
            if getattr(msg, "stop_reason", None) == "max_tokens":
                _warn(scene["id"], self.role, f"truncated at max_tokens={MAX_TOKENS}")
                return None
            text = "".join(b.text for b in msg.content if b.type == "text").strip()
            if not text:
                _warn(scene["id"], self.role,
                      f"empty response (stop_reason={getattr(msg, 'stop_reason', '?')})")
                return None
            return text
        except Exception as exc:  # noqa: BLE001 — any API failure means not measured
            _warn(scene["id"], self.role, f"API error ({exc})")
            return None


class OpenAICompatRole:
    """Same seam over any OpenAI-compatible endpoint — the way a REAL base
    checkpoint gets plugged in (vLLM / NIM / TGI / HF endpoints)."""

    def __init__(self, model: str, temperature: float, role: str):
        self.model, self.temperature, self.role = model, temperature, role
        self._client = None
        key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("BARE_OPENAI_BASE_URL")  # None ⇒ api.openai.com
        if key:
            from openai import OpenAI

            self._client = OpenAI(api_key=key, base_url=base_url) if base_url else OpenAI()

    def caption(self, scene: dict, prompt: str) -> str | None:
        if self._client is None:
            return None
        img = bare_stimuli.render(scene)
        content = [
            {"type": "image_url",
             "image_url": {"url": f"data:image/png;base64,{_b64(img)}"}},
            {"type": "text", "text": prompt},
        ]
        try:
            r = self._client.chat.completions.create(
                model=self.model, max_completion_tokens=MAX_TOKENS,
                temperature=self.temperature,
                messages=[{"role": "user", "content": content}],
            )
            if r.choices[0].finish_reason == "length":
                _warn(scene["id"], self.role, f"truncated at max_tokens={MAX_TOKENS}")
                return None
            text = (r.choices[0].message.content or "").strip()
            if not text:
                _warn(scene["id"], self.role, "empty response")
                return None
            return text
        except Exception as exc:  # noqa: BLE001
            _warn(scene["id"], self.role, f"API error ({exc})")
            return None


def get_role(model: str, temperature: float, role: str):
    if model.startswith("claude"):
        return AnthropicRole(model, temperature, role)
    return OpenAICompatRole(model, temperature, role)
