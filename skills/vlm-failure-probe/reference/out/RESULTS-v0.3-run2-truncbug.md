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
| claude-opus-5 | `circled_letter` | 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `warehouse_no_fall` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `sport_stays_tennis` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `shirt_stays_white` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-opus-5 | `summary_count_clothing` | 1.00, 1.00, 0.67 | 0.89 | 0.157 | GRADER-UNSTABLE |
| claude-opus-5 | `describe_and_closer` | 1.00, 1.00, 0.50 | 0.83 | 0.236 | GRADER-UNSTABLE |
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
| claude-sonnet-5 | `end_of_video` | 1.00, 0.00, 0.00 | 0.33 | 0.471 | GRADER-UNSTABLE |
| claude-sonnet-5 | `floor_color` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `squares_race` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `squares_stack` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `snowboarders_left` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `circled_letter` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `warehouse_no_fall` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `sport_stays_tennis` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `shirt_stays_white` | 1.00, 0.00, 1.00 | 0.67 | 0.471 | GRADER-UNSTABLE |
| claude-haiku-4-5-20251001 | `summary_count_clothing` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `describe_and_closer` | 1.00, 1.00, 0.50 | 0.83 | 0.236 | GRADER-UNSTABLE |
| claude-haiku-4-5-20251001 | `forklift_fork_direction` | 0.00, 0.00, 0.00 | 0.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `end_of_video` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |
| claude-haiku-4-5-20251001 | `floor_color` | 1.00, 1.00, 1.00 | 1.00 | 0.000 | stable |

**5 unstable probe/model pair(s):** claude-opus-5:summary_count_clothing, claude-opus-5:describe_and_closer, claude-sonnet-5:end_of_video, claude-haiku-4-5-20251001:shirt_stays_white, claude-haiku-4-5-20251001:describe_and_closer
## Raw answers (evidence)

## claude-opus-5
### spatial_directional
- `squares_race` [1.00] **Red.** It advances fastest across the frames and is the first to reach/cross the dashed finish line.
- `squares_stack` [1.00] **From top to bottom: yellow, green, blue, red.**

The stack stays unchanged across all four frames.
- `snowboarders_left` [1.00] The snowboarder in the **orange jacket** is the one on the left, positioned higher up on the slope's edge, while the blue-jacketed rider stays to the right and lower in the frame.
- `circled_letter` [1.00] The circled letter is **H** — the fourth letter of TECHNOLOGY (right after "TEC").

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No. The figure only leans/twists slightly to the side and then straightens back up — it stays standing on its legs the whole time.
- `sport_stays_tennis` [1.00] **Tennis.** The final frames show two players on a tennis court with rackets, hitting a ball back and forth over the net.
- `shirt_stays_white` [1.00] The person wears a white shirt the whole time — it stays white in every frame, paired with dark pants at the waist and blue legs.

### prompt_multipart
- `summary_count_clothing` [1.00] One person is present — a simple stick-style figure that stands in place, shifting slightly to the right across the frames in front of some brown boxes. They are wearing a yellow short-sleeved top with black shorts/lower torso and blue pants.
- `describe_and_closer` [1.00] The ball is hit from the near court, travels up over the net toward the far player, and then comes back down toward the near player again as they rally. The player at the bottom

### retrieval_reranking
- `forklift_fork_direction` [1.00] The fork is moving **up** — across the frames the fork (with its brown box) rises steadily along the vertical mast, from near ground level to near the top.
- `end_of_video` [1.00] The truck keeps driving to the right and finally drives completely off the right edge of the frame, leaving just the tan building and empty road/background.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray — a flat, medium-gray surface that fills the lower portion of the frame.

## claude-sonnet-5
### spatial_directional
- `squares_race` [1.00] The red square crosses the finish line first, moving fastest toward the dashed vertical line while the other squares lag behind.
- `squares_stack` [1.00] From top to bottom, the squares are: yellow, green, blue, and red. This order remains consistent across all four frames.
- `snowboarders_left` [1.00] The orange jacket snowboarder is on the left throughout the sequence, while the blue jacket snowboarder remains on the right.
- `circled_letter` [1.00] The circled letter is **H**.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person remains standing upright in all frames without any indication of falling.
- `sport_stays_tennis` [1.00] Tennis is being played at the end of the video, with the ball moving back toward the player on the near side of the court after being hit over the net.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video.

### prompt_multipart
- `summary_count_clothing` [1.00] One person is present in the animation, standing between two brown boxes in a simple room, wearing a yellow shirt, black pants, and blue shoes.
- `describe_and_closer` [1.00] The video shows a tennis rally where the player closer to the camera (bottom of the court) hits the ball upward over the net toward the opponent in the red shirt, who is farther away near the top of the court, and the ball then returns back down toward the closer player, repeating the sequence.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The forklift's fork is moving up, lifting the box higher along the vertical mast with each frame.
- `end_of_video` [1.00] The car-like object (blue truck with dark trailer and black wheels) drives off the right edge of the screen and disappears, leaving only the tan building/block visible in the final frame.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray.

## claude-haiku-4-5-20251001
### spatial_directional
- `squares_race` [1.00] # Answer

The **red square** crosses the finish line first.

In the final frame, the red square has crossed the dashed line (finish line) on the right, while the other colored squares are still approaching it.
- `squares_stack` [1.00] # Stack Colors (Top to Bottom)

The four squares from top to bottom are: **yellow, green, blue, and red**.
- `snowboarders_left` [1.00] The snowboarder on the left is wearing the orange jacket. This person remains in a consistent position on the left side throughout all four frames while the blue-jacketed snowboarder moves from right to left across the slope.
- `circled_letter` [1.00] # Answer

The letter **H** is circled.

This can be determined by tracking the progressive spelling of the word across the frames, where "TECHNOLOGY" is fully spelled by frame 5, and frame 6 shows the letter H circled in red.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person does not fall. Throughout the 6 frames shown, the person remains standing upright in the same position without any indication of falling.
- `sport_stays_tennis` [1.00] # Answer

Tennis is being played at the end of the video. The yellow ball can be seen moving across the net between the two players on the tennis court.
- `shirt_stays_white` [1.00] # Answer

The person wears a **white shirt** throughout the video. The white shirt is visible on the figure's torso in all six frames as the character moves across the screen.

### prompt_multipart
- `summary_count_clothing` [1.00] # Summary

There is **1 person** present in the video. The person is wearing a **yellow shirt and blue pants**.

The frames show the person walking from left to right across the scene, passing by brown boxes positioned on both sides.
- `describe_and_closer` [1.00] # Video Description

A tennis ball is being hit back and forth across the net between two players. The player on the bottom court (closer to the camera) is closer to the camera, as indicated by their larger size in the frame.

### retrieval_reranking
- `forklift_fork_direction` [0.00] The forklift's fork is moving **down**. The brown box on the fork descends progressively from the top of the frames to the bottom, indicating the fork is lowering its load.
- `end_of_video` [1.00] # Answer

At the very end of the video, the truck completely disappears off the right side of the screen, leaving only the beige building and the empty gray ground visible.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray. It remains the same color throughout all four frames.
