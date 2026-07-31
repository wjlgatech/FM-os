# vlm-failure-probe — live multi-model run

- **models**: claude-opus-5, claude-sonnet-5, claude-haiku-4-5-20251001 · 2026-07-31
- **stimuli**: deterministic synthetic frames (`stimuli.py`), the paper's own methodology
- **baseline**: the VSS paper's observed failures, canned verbatim (`MockVSS`)
- n.m. = not measured (no key/credits) — excluded, never a fake pass

| failure mode | VSS baseline | claude-opus-5 | claude-sonnet-5 | claude-haiku-4-5-20251001 | min |
|---|---|---|---|---|---|
| spatial_directional | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |
| temporal_cross_chunk | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |
| prompt_multipart | 0.42 | 0.67 | 1.00 | 0.83 | 0.75 |
| retrieval_reranking | 0.00 | 1.00 | 1.00 | 0.50 | 0.50 |
| grounding_hallucination | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |

**claude-opus-5 gate:** FAIL — prompt_multipart: 0.67 < threshold 0.75
**claude-sonnet-5 gate:** PASS
**claude-haiku-4-5-20251001 gate:** PASS

## Raw answers (evidence)

## claude-opus-5
### spatial_directional
- `squares_race` [1.00] The **red** square wins — it moves fastest across the frames and is the only one touching/crossing the dashed finish line by the final frame.
- `squares_stack` [1.00] From top to bottom, the squares are yellow, green, blue, and red. This order stays the same throughout all four frames.
- `snowboarders_left` [1.00] The snowboarder in the **orange jacket** is the one on the left, positioned higher up and toward the middle-left of the slope. The blue-jacketed rider stays to the right throughout all four frames.
- `circled_letter` [1.00] The circled letter is **H** — the fourth letter of TECHNOLOGY, marked with a red oval between the "C" and the "N".

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No. The figure only leans/twists its upper body slightly to one side and returns upright, remaining standing on its feet the whole time.
- `sport_stays_tennis` [1.00] **Tennis.** The final frames show two players with rackets on a tennis court, with the ball in play near the net on the near player's side.
- `shirt_stays_white` [1.00] The person wears a white shirt (white top) in every frame, with a black waistband/belt below it and blue pants.

### prompt_multipart
- `summary_count_clothing` [0.33] **Summary:** A single stick‑figure character stands in the middle of a gray floor between brown boxes, barely moving — just shifting/drifting slightly to the right across the frames.

**People present:** One.

**Clothing:** A yellow short‑sleeved top and blue pants (with a dark belt/waist area).
- `describe_and_closer` [1.00] The ball is hit from the bottom player up over the net to the far player, who returns it back down toward the near player — a rally passing over the net and back. The

### retrieval_reranking
- `forklift_fork_direction` [1.00] The fork is moving **up**. Across the frames, the fork (with the brown box on it) rises steadily along the vertical mast, from near ground level in the first frame to near the top of the mast in the last.
- `end_of_video` [1.00] The truck keeps driving to the right and finally exits the frame entirely, leaving only the tan building and empty road in view.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray — a flat, medium-gray surface that fills the lower portion of the frame.

## claude-sonnet-5
### spatial_directional
- `squares_race` [1.00] The red square crosses the finish line first, moving fastest toward the dashed line while the other squares lag behind.
- `squares_stack` [1.00] Yellow, green, blue, red (from top to bottom), consistent across all four frames.
- `snowboarders_left` [1.00] The snowboarder in the orange jacket is on the left, while the blue jacket snowboarder is on the right throughout the sequence.
- `circled_letter` [1.00] The letter **H** is circled in the word TECHNOLOGY.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person remains standing upright throughout all frames with no indication of falling.
- `sport_stays_tennis` [1.00] Tennis is being played, shown on a doubles court with two players hitting the ball back and forth over the net.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video.

### prompt_multipart
- `summary_count_clothing` [1.00] One person is present, standing between two brown boxes on the left and one on the right; they are wearing a yellow shirt, black pants, and blue shoes, with a slight walking/idle animation across the frames.
- `describe_and_closer` [1.00] The video shows a rally between two tennis players, with the ball moving upward toward the net and back down again toward the player near the bottom of the court. The player in the white shirt is closer to the camera, positioned in the lower half of the court.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The forklift's fork is moving upward, lifting the box higher on the mast with each frame.
- `end_of_video` [1.00] The truck-like vehicle drives off to the right side of the screen and disappears out of frame, leaving only the tan building/box visible on the left.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray.

## claude-haiku-4-5-20251001
### spatial_directional
- `squares_race` [1.00] # The Red Square Crosses First

Based on the progression shown across the six frames, the **red square** crosses the finish line (dashed line) first. It consistently moves faster than the other three colored squares throughout the sequence.
- `squares_stack` [1.00] # Answer

The four squares stacked vertically from top to bottom are: **yellow, green, blue, and red**.

This color arrangement remains consistent across all four frames shown.
- `snowboarders_left` [1.00] The snowboarder on the left is wearing the orange jacket. This person remains in the left position throughout all four frames while the blue-jacketed snowboarder stays on the right.
- `circled_letter` [1.00] # Answer

The letter **H** is circled.

This can be determined by observing the progressive building of the word "TECHNOLOGY" across the frames, where the final frame shows a red circle around the "H" in the word.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person does not fall. Throughout the 6 frames shown, the person remains standing upright in the same position.
- `sport_stays_tennis` [1.00] # Tennis

Based on the progression of frames showing a yellow ball being hit back and forth across a net on a rectangular court, the sport being played is **tennis**. The final frames show the ball in play on the lower court, demonstrating an active rally between the two players.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video. You can see the white torso/shirt consistently displayed on the stick figure in all six frames.

### prompt_multipart
- `summary_count_clothing` [0.67] # Summary

One person is present in the video. The person is wearing a yellow shirt and blue pants.
- `describe_and_closer` [1.00] # Volleyball Game Analysis

In this video, a player is hitting a volleyball over the net toward the opposing team. The **player closer to the camera is the one in the bottom court** (the one in blue who is receiving/preparing to play the ball).

### retrieval_reranking
- `forklift_fork_direction` [0.00] The forklift's fork is moving **down**. You can see the brown box on the fork gradually lowering from the top frame to the bottom frame as the sequence progresses.
- `end_of_video` [1.00] # Answer

The truck completely disappears off the right side of the screen. By the final frame, only the stationary tan building and gray ground remain visible.

### grounding_hallucination
- `floor_color` [1.00] # Warehouse Floor Color

The warehouse floor is **gray**. It remains a consistent gray color throughout all four frames of the video.
