# vlm-failure-probe — live multi-model run

- **models**: claude-opus-5, claude-sonnet-5, claude-haiku-4-5-20251001 · 2026-07-31
- **stimuli**: deterministic synthetic frames (`stimuli.py`), the paper's own methodology
- **baseline**: the VSS paper's observed failures, canned verbatim (`MockVSS`)
- n.m. = not measured (no key/credits) — excluded, never a fake pass

| failure mode | VSS baseline | claude-opus-5 | claude-sonnet-5 | claude-haiku-4-5-20251001 | min |
|---|---|---|---|---|---|
| spatial_directional | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |
| temporal_cross_chunk | 0.00 | 1.00 | 1.00 | 0.67 | 0.75 |
| prompt_multipart | 0.42 | 0.83 | 1.00 | 0.58 | 0.75 |
| retrieval_reranking | 0.00 | 1.00 | 1.00 | 0.00 | 0.50 |
| grounding_hallucination | 0.00 | 1.00 | 1.00 | 1.00 | 0.75 |

**claude-opus-5 gate:** PASS
**claude-sonnet-5 gate:** PASS
**claude-haiku-4-5-20251001 gate:** FAIL — temporal_cross_chunk: 0.67 < threshold 0.75; prompt_multipart: 0.58 < threshold 0.75; retrieval_reranking: 0.00 < threshold 0.50

## Raw answers (evidence)

## claude-opus-5
### spatial_directional
- `squares_race` [1.00] **Red** — it advances fastest across the frames and is the one touching/crossing the dashed finish line by the final frame.
- `squares_stack` [1.00] From top to bottom, the squares are yellow, green, blue, and red. This order stays the same throughout all four frames.
- `snowboarders_left` [1.00] The snowboarder in the **orange jacket** is the one on the left. The blue-jacketed snowboarder stays on the right side (and lower down the slope) throughout all four frames.
- `circled_letter` [1.00] The circled letter is **H** — the fourth letter of TECHNOLOGY (in "TEC**H**NOLOGY").

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No. The figure stays upright the whole time — the torso just twists/leans slightly to the side and then returns to the original standing pose.
- `sport_stays_tennis` [1.00] **Tennis** — two players with rackets are rallying a yellow ball over a net on a court, and at the end of the clip the ball is being hit back on the near player's side.
- `shirt_stays_white` [1.00] The person wears a white shirt (white top on the torso) in every frame, paired with blue pants.

### prompt_multipart
- `summary_count_clothing` [0.67] There is one person — a simple cartoon-style figure standing in place (drifting slightly to the right) on a gray floor with brown boxes behind them. They're wearing a yellow short-sleeved top with black shorts/belt area and blue pants.
- `describe_and_closer` [1.00] A tennis rally: the ball is hit from the near player's side up over the net toward the far player in red, then returns back down toward the near court, bouncing back and forth.

The player in the white shirt at the bottom is closer to the camera

### retrieval_reranking
- `forklift_fork_direction` [1.00] **Up.** Across the frames the fork (with its brown box) rises steadily along the mast, going from near ground level to near the top of the mast.
- `end_of_video` [1.00] The truck keeps driving to the right and finally exits the frame completely, leaving just the tan building and empty road in the last shot.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray — a flat, medium gray surface occupying the lower portion of the frames.

## claude-sonnet-5
### spatial_directional
- `squares_race` [1.00] The red square crosses the finish line first, reaching the dashed line by the final frame while the other squares remain further behind.
- `squares_stack` [1.00] From top to bottom, the squares are: yellow, green, blue, and red. This order remains consistent across all four frames.
- `snowboarders_left` [1.00] The snowboarder in the orange jacket is on the left, while the one in the blue jacket is on the right.
- `circled_letter` [1.00] The circled letter is **H**.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person remains standing upright throughout all frames without falling.
- `sport_stays_tennis` [1.00] Table tennis (ping pong) is being played, based on the two players positioned on opposite sides of the net with a ball between them.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video.

### prompt_multipart
- `summary_count_clothing` [1.00] There is 1 person present, standing between two brown boxes on the left and one on the right. The person is wearing a yellow shirt, black pants, and appears to be walking or shifting weight in place, with minimal movement across the frames.
- `describe_and_closer` [1.00] In this video, a table tennis-style rally is shown with the ball moving back and forth between the two players across the net, then returning to its starting position near the bottom player. The player in the white shirt with blue pants is closer to the camera.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The fork is moving up, lifting the box higher along the mast in each successive frame.
- `end_of_video` [1.00] The car (truck) moves to the right and exits the frame, leaving only the tan building visible on the left against the empty road.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray.

## claude-haiku-4-5-20251001
### spatial_directional
- `squares_race` [1.00] # Answer

The **red square** crosses the finish line first. You can see it progressively moving closer to the dashed line across the frames, reaching it before the other colored squares.
- `squares_stack` [1.00] # Stack Colors (Top to Bottom)

The four squares are stacked in the following order from top to bottom: yellow, green, blue, and red. This arrangement remains consistent across all four frames shown.
- `snowboarders_left` [1.00] # Answer

The snowboarder on the left is wearing the **orange jacket**. 

Across all four frames, the orange-jacketed snowboarder consistently remains in the left position while the blue-jacketed snowboarder stays on the right.
- `circled_letter` [1.00] # Answer

The letter **H** is circled in the word TECHNOLOGY.

This can be determined by tracking the progression of the word being built letter by letter across the frames, with the final frame showing the complete word "TECHNOLOGY" with the H circled in red.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person does not fall. Throughout these frames, the figure maintains a standing position with consistent posture and balance.
- `sport_stays_tennis` [0.00] # Analysis

Looking at the sequence of frames, I can see:
- A soccer/football field divided into two halves
- Players positioned on both halves
- An orange ball moving progressively across the field from left to right
- The ball trajectory and player positioning indicate the sport being played

**Answer:** Soccer (association football) is being played. The ball is being passed or moved across the field by the players during a match.
- `shirt_stays_white` [1.00] # Answer

The person wears a **white shirt** throughout the video. The shirt remains consistently white across all six frames as the person moves.

### prompt_multipart
- `summary_count_clothing` [0.67] # Summary

One person is present in the video. The person is wearing a yellow shirt and blue pants.
- `describe_and_closer` [0.50] # Video Description

A volleyball is being passed back and forth between two players across the net. The **player at the bottom** (in the lower court) is closer to the camera, as indicated by their larger size in the frame.

### retrieval_reranking
- `forklift_fork_direction` [0.00] # Forklift Movement Analysis

The forklift's fork is moving **down**. Across the six frames, you can see the brown rectangular load on the fork gradually descending from a higher position in the first frame to a lower position in the final frame.
- `end_of_video` [0.00] # Answer

The truck completely disappears off the right side of the screen. By the final frame, only the beige building and gray ground remain visible.

### grounding_hallucination
- `floor_color` [1.00] # Warehouse Floor Color

The warehouse floor is **gray**. It remains the same color throughout all four frames of the video.
