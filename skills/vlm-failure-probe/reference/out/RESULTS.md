# vlm-failure-probe — live multi-model run

- **models**: claude-opus-5, claude-sonnet-5, claude-haiku-4-5-20251001 · 2026-07-31
- **stimuli**: deterministic synthetic frames (`stimuli.py`), the paper's own methodology
- **baseline**: the VSS paper's observed failures, canned verbatim (`MockVSS`)
- n.m. = not measured (no key/credits) — excluded, never a fake pass

| failure mode | VSS baseline | claude-opus-5 | claude-sonnet-5 | claude-haiku-4-5-20251001 | min |
|---|---|---|---|---|---|
| spatial_directional | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |
| temporal_cross_chunk | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |
| prompt_multipart | 0.42 | 1.00 | 1.00 | 0.83 | 0.75 |
| retrieval_reranking | 0.00 | 1.00 | 1.00 | 0.50 | 0.50 |
| grounding_hallucination | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |

**claude-opus-5 gate:** PASS
**claude-sonnet-5 gate:** PASS
**claude-haiku-4-5-20251001 gate:** PASS

## Temporal Grounding Score (tgs_spec v1.0, floor 0.75)

| model | order | anchor | persistence | **TGS** | gate |
|---|---|---|---|---|---|
| claude-opus-5 | 1.00 | 1.00 | 1.00 | **1.000** | PASS |
| claude-sonnet-5 | 1.00 | 1.00 | 1.00 | **1.000** | PASS |
| claude-haiku-4-5-20251001 | 0.50 | 1.00 | 1.00 | **0.833** | PASS |

VSS baseline (the paper's observed failures, canned): **TGS = 0.000**

Formula, weights and degenerate cases: `tgs_spec.yml`. Arithmetic pinned to hand computation in `test_tgs.py`. An unmeasured component is excluded and the weights renormalize — never zeroed (a fake failure), never assumed (a fake pass).

## Grader stability — 3 repeats per model (spec v0.4)

sd is over REPEATS of an identical, deterministic stimulus. Any sd > 0 is
grader instability (or model nondeterminism the grader fails to absorb) —
never a property of the failure mode being probed.

| model | probe | scores | mean | sd | flag |
|---|---|---|---|---|---|
| claude-opus-5 | `squares_race` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `squares_stack` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `snowboarders_left` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `circled_letter` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `warehouse_no_fall` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `sport_stays_tennis` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `shirt_stays_white` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `summary_count_clothing` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `describe_and_closer` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
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
| claude-haiku-4-5-20251001 | `summary_count_clothing` | 0.67, 1.00, 1.00 | 0.89 | 0.157 | GRADER-UNSTABLE |
| claude-haiku-4-5-20251001 | `describe_and_closer` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `forklift_fork_direction` | 0.00, 0.00, 0.00 | 0.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `end_of_video` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `floor_color` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |

**1 unstable probe/model pair(s):** claude-haiku-4-5-20251001:summary_count_clothing
## Raw answers (evidence)

## claude-opus-5
### spatial_directional
- `squares_race` [1.00] **Red.** It advances fastest across the frames and is the first to reach/cross the dashed finish line.
- `squares_stack` [1.00] From top to bottom, the squares are yellow, green, blue, and red. They stay in that same order throughout all four frames.
- `snowboarders_left` [1.00] The snowboarder in the **orange jacket** is the one on the left, positioned higher up the slope, while the blue‑jacketed rider stays to the right and lower down.
- `circled_letter` [1.00] The circled letter is **H** — the fourth letter of TECHNOLOGY, marked by the red oval between the "C" and the "N".

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No. The figure stays upright the whole time — it just leans/twists slightly to the side and then returns to a standing position.
- `sport_stays_tennis` [1.00] **Tennis.** The final frames show two players with rackets on a tennis court, hitting a ball back and forth over the net.
- `shirt_stays_white` [1.00] Throughout the video the figure wears a white shirt (a white torso top, with a black waistband/belt area below it before the blue pants).

### prompt_multipart
- `summary_count_clothing` [1.00] There is one person — a simple stick-style figure standing on a gray ground between brown boxes, shifting slightly to the right across the frames. They wear a yellow short-sleeved top with black shorts/waist and blue pants.
- `describe_and_closer` [1.00] The ball is rallied back and forth over the net — it travels up to the far player in the red shirt, comes back down toward the near player, and starts rising again. The larger player in the white shirt at the bottom of the frame is closer to the camera.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The fork is moving **up** — across the frames the fork (with the brown box on it) rises steadily along the vertical mast, from near ground level to near the top of the mast.
- `end_of_video` [1.00] The truck keeps driving to the right until it disappears off the right edge of the frame, leaving only the tan building and empty road in the final shot.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray — a flat, medium gray surface that fills the lower portion of the scene.

## claude-sonnet-5
### spatial_directional
- `squares_race` [1.00] The red square crosses the finish line first, reaching the dashed line by the final frame while the other squares remain farther behind.
- `squares_stack` [1.00] From top to bottom, the squares are: yellow, green, blue, and red.
- `snowboarders_left` [1.00] The snowboarder in the orange jacket is on the left, while the one in the blue jacket is on the right.
- `circled_letter` [1.00] The circled letter is **H**.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person remains standing upright throughout all frames without any indication of falling.
- `sport_stays_tennis` [1.00] Tennis is being played at the end of the video, shown by the two players on opposite sides of the net with rackets and a ball moving between them on a tennis court.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video.

### prompt_multipart
- `summary_count_clothing` [1.00] One person is present, standing in place with a subtle walking/idle animation (legs shifting slightly), wearing a yellow shirt and black pants, positioned between two brown boxes on the left and one on the right against a plain background.
- `describe_and_closer` [1.00] The video shows a rally where the player near the net hits the ball, it travels over the net toward the player at the bottom of the court, and then bounces back down near the bottom player again. The player wearing the white shirt at the bottom of the court is closer to the camera.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The forklift's fork is moving up, lifting the box higher along the vertical mast with each successive frame.
- `end_of_video` [1.00] The car-like vehicle drives off to the right side of the frame and disappears completely, leaving only the tan building/box visible on the left.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray.

## claude-haiku-4-5-20251001
### spatial_directional
- `squares_race` [1.00] # Answer

The **red square** crosses the finish line first. It reaches the dashed line (finish line) in the sixth and final frame, ahead of the blue, green, and yellow squares.
- `squares_stack` [1.00] # Answer

The four squares stacked vertically, from top to bottom, are: **yellow, green, blue, and red**.
- `snowboarders_left` [1.00] The snowboarder on the left is wearing the orange jacket. This figure remains in the left position throughout all four frames while the blue-jacketed snowboarder is on the right.
- `circled_letter` [1.00] # Answer

The letter **H** is circled.

This can be determined by observing that in the final frame, the circle highlights the 4th letter in the word TECHNOLOGY, which is H.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person does not fall. Throughout these frames, the figure maintains an upright standing position with consistent posture and balance.
- `sport_stays_tennis` [1.00] # Tennis

Based on the progression of frames showing players on opposite sides of a net with a ball being volleyed back and forth, tennis is being played at the end of the video.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video. The shirt remains consistently white across all six frames.

### prompt_multipart
- `summary_count_clothing` [0.67] # Summary

One person is present in the video. The person is wearing a yellow shirt and blue pants/legs.
- `describe_and_closer` [1.00] # Video Description

A tennis ball is being hit back and forth over the net between two players. The player on the bottom court (closer to the camera) is closer to the camera, as indicated by their larger size in the frames.

### retrieval_reranking
- `forklift_fork_direction` [0.00] # The forklift's fork is moving down.

You can see the brown box on the fork gradually lowering from the top of the frames to progressively lower positions as the sequence progresses.
- `end_of_video` [1.00] # Analysis of the Video Frames

Looking at the sequence of frames, the truck moves progressively to the right across the screen. In the final frame, the truck has completely disappeared off the right side of the screen, leaving only the beige building and the empty gray ground visible.

**Answer:** The truck drives completely off-screen to the right, exiting the frame entirely.

### grounding_hallucination
- `floor_color` [1.00] # The warehouse floor is gray.

The gray surface is visible at the bottom of each frame and remains consistent throughout all four frames of the video.
