# vlm-failure-probe — live multi-model run

- **models**: claude-opus-5, claude-sonnet-5, claude-haiku-4-5-20251001 · 2026-07-31
- **stimuli**: deterministic synthetic frames (`stimuli.py`), the paper's own methodology
- **baseline**: the VSS paper's observed failures, canned verbatim (`MockVSS`)
- n.m. = not measured (no key/credits) — excluded, never a fake pass

| failure mode | VSS baseline | claude-opus-5 | claude-sonnet-5 | claude-haiku-4-5-20251001 | min |
|---|---|---|---|---|---|
| spatial_directional | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |
| temporal_cross_chunk | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |
| prompt_multipart | 0.42 | 1.00 | 1.00 | 1.00 | 0.75 |
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

## Grader stability — 3 repeats per model (spec v0.3)

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
| claude-sonnet-5 | `end_of_video` | 1.00, 0.00, 1.00 | 0.67 | 0.471 | GRADER-UNSTABLE |
| claude-sonnet-5 | `floor_color` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `squares_race` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `squares_stack` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `snowboarders_left` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `circled_letter` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `warehouse_no_fall` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `sport_stays_tennis` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `shirt_stays_white` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `summary_count_clothing` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `describe_and_closer` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `forklift_fork_direction` | 0.00, 1.00, 1.00 | 0.67 | 0.471 | GRADER-UNSTABLE |
| claude-haiku-4-5-20251001 | `end_of_video` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `floor_color` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |

**2 unstable probe/model pair(s):** claude-sonnet-5:end_of_video, claude-haiku-4-5-20251001:forklift_fork_direction
## Raw answers (evidence)

## claude-opus-5
### spatial_directional
- `squares_race` [1.00] **Red.** It advances fastest across the frames and is the one touching/crossing the dashed finish line by the final frame, while blue, green, and yellow lag well behind.
- `squares_stack` [1.00] From top to bottom the squares are yellow, green, blue, and red — unchanged across all four frames.
- `snowboarders_left` [1.00] The snowboarder in the orange jacket is the one on the left; the blue-jacketed rider is farther down to the right.
- `circled_letter` [1.00] The circled letter is **H** — the fourth letter of "TECHNOLOGY," marked with a red ellipse in the final frame.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No. The figure stays upright the whole time — it only leans/shifts its torso slightly and returns to its original standing pose.
- `sport_stays_tennis` [1.00] Tennis — at the end of the clip two players are still rallying a ball across the net on a tennis court.
- `shirt_stays_white` [1.00] The person consistently wears a white shirt (with a black waistband/belt area beneath it) in every frame.

### prompt_multipart
- `summary_count_clothing` [1.00] **Summary:** A single stick-figure person stands in a plain gray room with brown boxes/crates on the floor to either side, shifting only slightly to the right over the six frames.

**People present:** One.

**Clothing:** A yellow short-sleeved top and blue pants (with a dark belt/waist area).
- `describe_and_closer` [1.00] The ball is rallied back and forth across the net — it travels up toward the far player in the red shirt, then comes back down toward the near player. The player in the white shirt and blue shorts at the bottom of the frame is closer to the camera.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The fork is moving **up**. Across the frames, the fork (with its brown box) rises from near ground level up along the mast toward the top.
- `end_of_video` [1.00] The truck keeps driving to the right and finally disappears off the right edge of the frame, leaving only the tan building and the empty road/background in view.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray — a flat, medium‑gray surface that fills the lower portion of the frame.

## claude-sonnet-5
### spatial_directional
- `squares_race` [1.00] The red square crosses the finish line first, as it moves fastest across the frames and reaches the dashed line by the final frame.
- `squares_stack` [1.00] From top to bottom, the squares are: yellow, green, blue, and red. This order remains consistent across all four frames.
- `snowboarders_left` [1.00] The snowboarder in the orange jacket is on the left, while the one in the blue jacket is on the right.
- `circled_letter` [1.00] The circled letter is **H**.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person remains standing upright throughout all frames without falling.
- `sport_stays_tennis` [1.00] Tennis is being played at the end of the video, shown by the two players on a tennis court hitting a ball back and forth over the net with rackets.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video.

### prompt_multipart
- `summary_count_clothing` [1.00] There is 1 person in the video, standing between two brown boxes on the left and one on the right, appearing to walk or shift in place. The person is wearing a yellow shirt, black pants, and has blue-colored legs/shoes visible below the pants.
- `describe_and_closer` [1.00] The video shows a rally where the player closer to the camera (bottom of court, in white/blue) hits the ball, which travels up and over the net toward the player in the back (red/white, near the net), then returns back down, repeating the exchange. The player in white with blue pants at the bottom of the frame is closer to the camera.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The forklift's fork is moving up, lifting the box higher along the vertical mast with each frame.
- `end_of_video` [1.00] The car/truck moves off-screen to the right and disappears, leaving only the tan building visible in the final frame.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray.

## claude-haiku-4-5-20251001
### spatial_directional
- `squares_race` [1.00] # Answer

The **red square** crosses the finish line first. You can see it reaches the dashed line (finish line) in the sixth and final frame, ahead of the other colored squares.
- `squares_stack` [1.00] # Stack of Colored Squares

From top to bottom, the colors are: **yellow, green, blue, and red**.

This arrangement remains consistent across all four frames shown.
- `snowboarders_left` [1.00] # The snowboarder on the left is wearing the orange jacket.

In all four frames, the figure on the left consistently wears an orange jacket, while the figure on the right wears a blue jacket.
- `circled_letter` [1.00] # Answer

The letter **H** is circled.

The video shows the word "TECHNOLOGY" being progressively written letter by letter, and in the final frame, the letter H (the 4th letter in the word) is circled in red.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person does not fall. Throughout these frames, the figure remains standing upright in the same position with consistent posture.
- `sport_stays_tennis` [1.00] # Tennis

Based on the sequence of frames showing a ball being hit back and forth over a net between two opponents on opposite sides of a court, the sport being played is **tennis**. The net dividing the court and the rally pattern are characteristic of a tennis match.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video. You can see the white rectangular section of their shirt in all six frames, positioned between their head and blue pants.

### prompt_multipart
- `summary_count_clothing` [1.00] # Summary

There is **one person** present in the video. The person is wearing a **yellow shirt and blue pants**.

The frames show the person walking or moving slightly from left to right across the scene, which contains brown boxes on either side.
- `describe_and_closer` [1.00] # Tennis Rally Description

A tennis ball is being volleyed back and forth across the net between two players. The player on the bottom court (closer to the camera) is nearer to the camera.

### retrieval_reranking
- `forklift_fork_direction` [0.00] # The forklift's fork is moving down.

You can see the brown/tan box on the fork descending progressively lower across the frames, moving from a higher position in the first frame to a lower position by the final frame.
- `end_of_video` [1.00] # Answer

The truck completely disappears off the right side of the screen. By the final frame, only the beige building and empty gray background remain visible.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray. It remains the same color throughout all four frames.
