# labs/ — applied proof-of-capability builds

Hands-on labs that put the FM-os skills to work on a concrete target. Each is self-contained,
test-gated, and built from public surfaces only.

| Lab | What it proves | Gates |
|---|---|---|
| [`nomadicml/`](nomadicml/) | Clean-room, small-scale reverse-engineering of NomadicML's VLM video-analysis product (driving events → structured schema → semantic search), compared term-by-term against their production API. Interview proof-of-capability for a Member-of-Technical-Staff (ML) role. | `make check` (offline) · `make e2e` (real VLM) · `make parity` (live API) · `make webapp` (visual demo + lab copilot) |
