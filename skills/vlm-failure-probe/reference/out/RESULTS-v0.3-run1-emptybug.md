# vlm-failure-probe — live multi-model run

- **models**: claude-opus-5, claude-sonnet-5, claude-haiku-4-5-20251001 · 2026-07-31
- **stimuli**: deterministic synthetic frames (`stimuli.py`), the paper's own methodology
- **baseline**: the VSS paper's observed failures, canned verbatim (`MockVSS`)
- n.m. = not measured (no key/credits) — excluded, never a fake pass

| failure mode | VSS baseline | claude-opus-5 | claude-sonnet-5 | claude-haiku-4-5-20251001 | min |
|---|---|---|---|---|---|
| spatial_directional | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |
| temporal_cross_chunk | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |
| prompt_multipart | 0.42 | 0.33 | 1.00 | 0.83 | 0.75 |
| retrieval_reranking | 0.00 | 1.00 | 1.00 | 1.00 | 0.50 |
| grounding_hallucination | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |

**claude-opus-5 gate:** FAIL — prompt_multipart: 0.33 < threshold 0.75
**claude-sonnet-5 gate:** PASS
**claude-haiku-4-5-20251001 gate:** PASS

## Temporal Grounding Score (tgs_spec v1.0, floor 0.75)

| model | order | anchor | persistence | **TGS** | gate |
|---|---|---|---|---|---|
| claude-opus-5 | 1.00 | 1.00 | 1.00 | **1.000** | PASS |
| claude-sonnet-5 | 1.00 | 1.00 | 1.00 | **1.000** | PASS |
| claude-haiku-4-5-20251001 | 1.00 | 1.00 | 1.00 | **1.000** | PASS |

VSS baseline (the paper's observed failures, canned): **TGS = 0.000**

Formula, weights and degenerate cases: `tgs_spec.yml`. Arithmetic pinned to hand computation in `test_tgs.py`. An unmeasured component is excluded and the weights renormalize — never zeroed (a fake failure), never assumed (a fake pass).

## Grader stability — 3 repeats per model (spec v0.3)

sd is over REPEATS of an identical, deterministic stimulus. Any sd > 0 is
grader instability (or model nondeterminism the grader fails to absorb) —
never a property of the failure mode being probed.

| model | probe | scores | mean | sd | flag |
|---|---|---|---|---|---|
| claude-opus-5 | `squares_race` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `squares_stack` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `snowboarders_left` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `circled_letter` | 1.00, 0.00, 1.00 | 0.67 | 0.471 | GRADER-UNSTABLE |
| claude-opus-5 | `warehouse_no_fall` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `sport_stays_tennis` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `shirt_stays_white` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `summary_count_clothing` | 0.67, 1.00, 1.00 | 0.89 | 0.157 | GRADER-UNSTABLE |
| claude-opus-5 | `describe_and_closer` | 0.00, 1.00, 0.00 | 0.33 | 0.471 | GRADER-UNSTABLE |
| claude-opus-5 | `forklift_fork_direction` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `end_of_video` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `floor_color` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `squares_race` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `squares_stack` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `snowboarders_left` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `circled_letter` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `warehouse_no_fall` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `sport_stays_tennis` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `shirt_stays_white` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `summary_count_clothing` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `describe_and_closer` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `forklift_fork_direction` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `end_of_video` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-sonnet-5 | `floor_color` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `squares_race` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `squares_stack` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `snowboarders_left` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `circled_letter` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `warehouse_no_fall` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `sport_stays_tennis` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `shirt_stays_white` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `summary_count_clothing` | 0.67, 0.67, 1.00 | 0.78 | 0.157 | GRADER-UNSTABLE |
| claude-haiku-4-5-20251001 | `describe_and_closer` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `forklift_fork_direction` | 1.00, 0.00, 0.00 | 0.33 | 0.471 | GRADER-UNSTABLE |
| claude-haiku-4-5-20251001 | `end_of_video` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `floor_color` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |

**5 unstable probe/model pair(s):** claude-opus-5:circled_letter, claude-opus-5:summary_count_clothing, claude-opus-5:describe_and_closer, claude-haiku-4-5-20251001:summary_count_clothing, claude-haiku-4-5-20251001:forklift_fork_direction
## Raw answers (evidence)

## claude-opus-5
### spatial_directional
- `squares_race` [1.00] **Red.** It advances the fastest across the frames and is the first to reach (and overlap) the dashed finish line.
- `squares_stack` [1.00] From top to bottom, the stack is: yellow, green, blue, then red. The arrangement stays the same throughout all four frames.
- `snowboarders_left` [1.00] The snowboarder in the **orange jacket** is on the left, positioned higher up on the slope's white area, while the blue-jacketed snowboarder is off to the right and lower down.
- `circled_letter` [1.00] The circled letter is **H** — the fourth letter of TECHNOLOGY (highlighted by the red ellipse between "TEC" and "NOLOGY").

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No. The figure only leans/twists slightly to one side and then returns to an upright standing position, never going to the ground.
- `sport_stays_tennis` [1.00] **Tennis.** The final frames show two players with rackets on a tennis court, with the ball in play near the net.
- `shirt_stays_white` [1.00] Throughout the video the figure wears a white shirt (a white torso top), paired with blue pants and a dark band at the waist.

### prompt_multipart
- `summary_count_clothing` [0.67] One person is present — a simple stick-style figure standing in place and shifting slightly to the right across the frames. They are wearing a yellow shirt, blue pants, and have no visible facial features.
- `describe_and_closer` [0.00] 

### retrieval_reranking
- `forklift_fork_direction` [1.00] The fork is moving **up**. Across the frames, the fork (with the brown box on it) rises steadily from near ground level up along the vertical mast.
- `end_of_video` [1.00] The truck keeps driving to the right until it moves completely out of frame, leaving only the tan building and empty road in the final shot.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray — a medium, neutral gray tone that fills the lower half of the frame.

## claude-sonnet-5
### spatial_directional
- `squares_race` [1.00] The red square crosses the finish line first, moving fastest toward the dashed line while the other squares lag behind.
- `squares_stack` [1.00] From top to bottom: yellow, green, blue, red. This order remains consistent across all four frames.
- `snowboarders_left` [1.00] The orange jacket snowboarder is on the left, while the blue jacket snowboarder remains on the right throughout the frames.
- `circled_letter` [1.00] The circled letter is **H**.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person remains standing upright throughout all frames without falling.
- `sport_stays_tennis` [1.00] Tennis is being played at the end of the video, shown by the court layout, net, and players with rackets hitting the ball back and forth.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video.

### prompt_multipart
- `summary_count_clothing` [1.00] A simple animated scene shows one person standing between two wooden crates, walking in place with a subtle bobbing motion. The person is wearing a yellow shirt, black pants, and has blue shoes/legs visible.
- `describe_and_closer` [1.00] The video shows a tennis rally where the player closer to the camera (bottom of court, in white shirt) hits the ball, which travels up and over the net toward the player in the red shirt at the far baseline, then the sequence repeats as if looping. The player in the white shirt is closer to the camera.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The forklift's fork is moving up, lifting the box higher along the vertical mast with each frame.
- `end_of_video` [1.00] The truck-like vehicle moves off-screen to the right and disappears, leaving only the tan building visible in the final frame.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray.

## claude-haiku-4-5-20251001
### spatial_directional
- `squares_race` [1.00] # The Red Square Crosses First

The red square crosses the finish line (the dashed vertical line) first. By the final frame, the red square has reached and crossed the dashed line, while the other colored squares are still approaching it.
- `squares_stack` [1.00] # Color Stack (Top to Bottom)

The four stacked squares are colored yellow, green, blue, and red from top to bottom. This arrangement remains consistent across all four frames shown.
- `snowboarders_left` [1.00] # Answer

The snowboarder on the left is wearing the **orange jacket**. This figure remains consistently on the left side throughout all four frames, while the blue-jacketed snowboarder stays on the right.
- `circled_letter` [1.00] # Answer

The letter **H** is circled.

The frames show the word "TECHNOLOGY" being built letter by letter, and in the final frame, the letter "H" (the 4th letter) is highlighted with a red circle.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person does not fall. Throughout all 6 frames, the figure remains standing upright in the same position with consistent posture.
- `sport_stays_tennis` [1.00] # Tennis

Based on the sequence of frames showing a ball being hit back and forth over a net between two players on opposite sides of a court, the sport being played is **tennis**. The players are engaged in a rally, with the ball traveling across the net between them.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video. The shirt remains consistently white across all six frames.

### prompt_multipart
- `summary_count_clothing` [0.67] # Summary

One person is present in the video. The person is wearing a yellow shirt and blue pants.
- `describe_and_closer` [1.00] # Tennis Rally Analysis

A tennis rally is in progress where the ball is being hit back and forth across the net. The **player at the bottom of the court (in blue) is closer to the camera**, as this is a view from behind their baseline looking toward the net and opponent's court.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The forklift's fork is moving **up**. Across the six frames, the brown load on the fork progressively rises higher relative to the vertical black post, indicating an upward motion.
- `end_of_video` [1.00] # Answer

The truck completely disappears off the right side of the screen. By the final frame, only the beige building and empty ground remain visible.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray. It remains the same gray color consistently across all four frames.
