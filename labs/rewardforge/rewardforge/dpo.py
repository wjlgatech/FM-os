"""Minimal Direct Preference Optimization — from scratch on torch + peft.

The DPO loss (Rafailov et al., arXiv:2305.18290), nothing hidden behind a
framework: for a pair (x, y_w, y_l),

    loss = -log sigmoid( beta * [ (logpi(y_w|x) - logref(y_w|x))
                                 - (logpi(y_l|x) - logref(y_l|x)) ] )

Completion-token log-probs only (prompt tokens masked). The frozen reference
log-probs are precomputed once before LoRA is attached — one model in memory.
Runs on MPS / CUDA / CPU. Deterministic given a seed.
"""
from __future__ import annotations

import torch
import torch.nn.functional as F


def device() -> str:
    if torch.backends.mps.is_available():
        return "mps"
    return "cuda" if torch.cuda.is_available() else "cpu"


def encode_pair(tokenizer, prompt: str, completion: str, max_len: int = 96):
    """Token ids + a mask selecting ONLY completion tokens."""
    p = tokenizer(prompt, add_special_tokens=False).input_ids
    c = tokenizer(completion, add_special_tokens=False).input_ids
    ids = (p + c)[:max_len]
    mask = ([0] * len(p) + [1] * len(c))[:max_len]
    return torch.tensor(ids), torch.tensor(mask)


def completion_logprob(model, ids: torch.Tensor, mask: torch.Tensor) -> torch.Tensor:
    """Sum of log p(token) over completion positions (next-token aligned)."""
    logits = model(ids.unsqueeze(0)).logits[0, :-1]  # predicts ids[1:]
    targets, tmask = ids[1:], mask[1:]
    logps = F.log_softmax(logits.float(), dim=-1)
    tok_lp = logps.gather(1, targets.unsqueeze(1)).squeeze(1)
    return (tok_lp * tmask).sum()


@torch.no_grad()
def reference_logprobs(model, batch: list[tuple[torch.Tensor, torch.Tensor]]) -> list[float]:
    model.eval()
    return [completion_logprob(model, ids.to(model.device), m.to(model.device)).item()
            for ids, m in batch]


def dpo_loss(pi_w, pi_l, ref_w: float, ref_l: float, beta: float = 0.1) -> torch.Tensor:
    margin = beta * ((pi_w - ref_w) - (pi_l - ref_l))
    return -F.logsigmoid(margin)


def train_dpo(model, tokenizer, pairs: list[dict], *, beta: float = 0.1, lr: float = 1e-4,
              epochs: int = 2, seed: int = 0, log_every: int = 50) -> dict:
    """LoRA-DPO over preference pairs. `model` must already carry LoRA adapters;
    reference log-probs are supplied per-pair under key '_ref' (w, l)."""
    torch.manual_seed(seed)
    dev = model.device
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=lr)
    history, step = [], 0
    model.train()
    for _ in range(epochs):
        for pair in pairs:
            ids_w, m_w = pair["_enc_w"]
            ids_l, m_l = pair["_enc_l"]
            pi_w = completion_logprob(model, ids_w.to(dev), m_w.to(dev))
            pi_l = completion_logprob(model, ids_l.to(dev), m_l.to(dev))
            loss = dpo_loss(pi_w, pi_l, *pair["_ref"], beta=beta)
            opt.zero_grad()
            loss.backward()
            opt.step()
            step += 1
            if step % log_every == 0:
                history.append({"step": step, "loss": float(loss.item())})
    return {"steps": step, "history": history}
