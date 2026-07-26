# vlm-failure-probe — live run against a real VLM

- **model**: `claude-sonnet-5` (Anthropic Messages API, 2026-07-25)
- **stimuli**: deterministic synthetic frames (`stimuli.py`), the paper's own methodology
- **baseline**: the VSS paper's observed failures, canned verbatim (`MockVSS`)

| failure mode | VSS baseline | real VLM | min | verdict |
|---|---|---|---|---|
| spatial_directional | 0.00 | 1.00 | 0.75 | ✅ pass |
| temporal_cross_chunk | 0.00 | 1.00 | 0.75 | ✅ pass |
| prompt_multipart | 0.42 | 1.00 | 0.75 | ✅ pass |
| retrieval_reranking | 0.00 | 1.00 | 0.50 | ✅ pass |
| grounding_hallucination | 0.00 | 1.00 | 0.75 | ✅ pass |

**Gate:** PASS

## Raw answers (evidence)

### spatial_directional
- `squares_race` [1.00] The red square crosses the finish line first, moving fastest toward the dashed line while the other squares lag behind.
- `squares_stack` [1.00] From top to bottom, the squares are: yellow, green, blue, and red.
- `snowboarders_left` [1.00] The snowboarder in the orange jacket is on the left, while the one in the blue jacket is on the right.
- `circled_letter` [1.00] The letter **H** is circled in the word TECHNOLOGY.

### temporal_cross_chunk
- `warehouse_no_fall` [1.00] No, the person remains standing upright in all frames without any signs of falling.
- `sport_stays_tennis` [1.00] Table tennis (ping pong) is being played, as shown by the two players positioned on opposite sides of a table with a net, hitting a small yellow ball back and forth.
- `shirt_stays_white` [1.00] The person wears a white shirt throughout the video.

### prompt_multipart
- `summary_count_clothing` [1.00] There is 1 person present, standing between two brown boxes on the left and one box on the right, appearing to walk in place or shift slightly with a subtle leg movement. The person is wearing a yellow shirt, black pants, and has blue legs/shoes with a bald head.
- `describe_and_closer` [1.00] The video shows a table tennis rally where the ball moves from the lower player toward the upper player and back, going over the net multiple times. The player in the white shirt (bottom) is closer to the camera.

### retrieval_reranking
- `forklift_fork_direction` [1.00] The forklift's fork is moving up, lifting the box higher along the vertical mast with each frame.
- `end_of_video` [1.00] The car (truck-like vehicle) drives off the right side of the frame and disappears, leaving only the tan building visible on the left side of the scene.

### grounding_hallucination
- `floor_color` [1.00] The warehouse floor is gray.
