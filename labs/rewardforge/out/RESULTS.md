# RewardForge M1 — eval-derived preference pairs → LoRA-DPO → held-out gate

- **model**: `HuggingFaceTB/SmolLM2-135M-Instruct` (LoRA r=16 on q/v_proj, lr=1e-05, beta=0.2, epochs=1) · device `mps` · 2026-07-27
- **pairs**: 162 — chosen/rejected labeled by FM-os's certified gates (syndata-bare alignment gate + vlm-failure-probe paper failures), zero human labels
- **held-out**: 8 fact worlds sharing no content words with training

| metric | before (base) | after (DPO) |
|---|---|---|
| hallucination rate | 0.398 | 0.287 |
| avg words | 7.1 | 6.2 |

**Gate:** SHIP

## Sample held-out generations (evidence)

**horse_meadow** — facts: ['fence', 'horse', 'meadow']
- before: 'Horse (brown), fence, meadow.'
- after:  'Horse (brown), fence, meadow.'

**laptop_desk** — facts: ['desk', 'laptop', 'mug']
- before: 'laptop (open), desk, mug.'
- after:  'laptop (open), desk, mug.'

**boat_harbor** — facts: ['boat', 'harbor', 'rope']
- before: 'The harbor is a popular spot for tourists.'
- after:  'The harbor is a busy place.'

**violin_stage** — facts: ['stage', 'stand', 'violin']
- before: 'The violin is a musical instrument that is played by bowing the strings.'
- after:  'The violin is a musical instrument that is played by bowing the strings.'

**cactus_pot** — facts: ['cactus', 'gravel', 'pot']
- before: 'cactus (spiky), gravel, pot.'
- after:  'cactus (spiky), gravel, pot.'

**kite_field** — facts: ['field', 'kite', 'string']
- before: 'The kite is a symbol of freedom and adventure.'
- after:  'kite (striped), field, string.'

## Training telemetry

```json
[
 {
  "step": 50,
  "loss": 0.6720839738845825
 },
 {
  "step": 100,
  "loss": 0.6408278346061707
 },
 {
  "step": 150,
  "loss": 0.6192742586135864
 }
]
```
