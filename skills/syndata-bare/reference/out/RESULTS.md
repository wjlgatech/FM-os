# syndata-bare — live run against real vision models

- **base role**: `claude-haiku-4-5-20251001` @ T=1.0 (`proxy`)
- **instruct role**: `claude-sonnet-5` @ T=0.0 **(REJECTED by the API — model default used)**
- **scenes**: 6 deterministic synthetic compositions (`bare_stimuli.py`), 3 caption(s) per scene per pipeline
- **date**: 2026-08-14 · **repeats**: 1
- alignment = 1 − (captions naming an absent colour/shape) / (captions measured)
- an unmeasured caption is excluded from every aggregate — never scored 0

| pipeline | alignment | diversity | yield | measured | gate |
|---|---|---|---|---|---|
| base_only | 1.00 | 0.62 | 1.00 | 18 | PASS |
| instruct_only | 1.00 | 0.23 | 1.00 | 18 | FAIL — diversity 0.23 < 0.25 |
| bare | 1.00 | 0.56 | 1.00 | 18 | PASS |

## The two claims, scored separately

- **pipeline claim** (draft-then-refine beats either single stage): **NOT SUBSTANTIATED**
- **paper claim** (a BASE checkpoint supplies diversity an instruct model cannot): **NOT SUBSTANTIATED**

  base_only passed — no hallucination for refinement to fix

  The paper claim is blocked by role fidelity, not by the numbers: the base
  role is filled by `claude-haiku-4-5-20251001`, which is instruction-tuned. Point
  `--base-model` at a real base checkpoint over an OpenAI-compatible endpoint
  to make this claim measurable at all.

## Known limits of this measurement

1. **Alignment is an upper bound.** Only closed-vocabulary decoys (blue, green, orange, purple, red, yellow / circle, square, triangle) can be scored wrong. Any other word is unscored, so a hallucination we did not enumerate is invisible.
2. **High-entropy captions route around the vocabulary.** Observed live: the base role says "crimson", "cobalt", "emerald", "golden", "orbs" rather than the plain colour and shape words. The freer the phrasing, the less surface the detector has — so alignment is a *weaker* bound for the base role than for the instruct role, in the direction that flatters the base role.
3. **Primitive attributes only.** Colour and shape are checkable without a judge; that is why this can run at all. It is a weaker proxy than natural-image captioning, and a result here does not transfer to one without being re-run.

## Variance

**UNMEASURED** — a single run. The base role samples at temperature 1.0, so these figures have unknown spread; `--repeat N` reports it. A single-run score is not yet a measurement (the lesson vlm-failure-probe learned live).

## Raw captions (evidence)

### base_only
- **s1_red_circle_blue_square** — true: ['blue', 'red'] ['circle', 'square']
  - A vibrant red circle and a bold blue square sit apart from each other on a pale background, creating a minimalist composition of contrasting shapes and colors.
  - A vibrant crimson circle and a cobalt blue square face each other across a minimalist canvas, like two geometric souls in quiet contemplation.
  - A vibrant crimson circle rests peacefully on the left side of the canvas while a bold cobalt square stands sentinel on the right, creating a striking study in geometric contrast.
- **s2_green_triangle_alone** — true: ['green'] ['triangle']
  - # Image Description

A verdant emerald triangle stands boldly against a pale backdrop, its sharp apex pointing skyward like a mountain peak or a festive evergreen.
  - A solitary emerald triangle sits centered against a pristine white canvas, its sharp apex pointing upward like a verdant mountain peak.
  - A solitary emerald-hued triangle sits poised in the center of a pale, minimalist canvas.
- **s3_yellow_square_over_purple_circle** — true: ['purple', 'yellow'] ['circle', 'square']
  - A golden square hovers above a vibrant purple circle, creating a minimalist composition that suggests balance between geometric simplicity and organic roundness.
  - A cheerful golden square hovers above a vibrant purple sphere, creating a minimalist composition that evokes balance between geometric forms.
  - A golden square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
- **s4_three_orange_circles** — true: ['orange'] ['circle']
  - Three golden orbs float serenely in a minimalist void, arranged like celestial bodies in perfect horizontal alignment.
  - Three vibrant orange spheres are arranged in a horizontal line, reminiscent of glowing orbs floating in a serene, minimalist space.
  - Three vibrant tangerine-colored spheres are arranged in a horizontal line, resembling a minimalist representation of celestial bodies or a simple visual metaphor for unity and balance.
- **s5_blue_triangle_green_square** — true: ['blue', 'green'] ['square', 'triangle']
  - A vibrant blue triangle and an emerald green square sit apart on a pale background, representing geometric simplicity.
  - A vibrant blue triangle and an emerald green square sit apart from each other against a pale background, creating a minimalist composition of geometric contrast.
  - A vibrant blue triangle and an emerald green square sit separately on a pale background, like two fundamental shapes pondering their geometric existence.
- **s6_purple_square_red_triangle_yellow_circle** — true: ['purple', 'red', 'yellow'] ['circle', 'square', 'triangle']
  - # Three Geometric Shapes in a Row

A vibrant purple square, a bold crimson triangle, and a golden yellow circle are arranged in a harmonious lineup against a pale background.
  - # Image Description

Three vibrant geometric shapes—a purple square, a crimson triangle, and a golden yellow circle—are arranged in a cheerful line across a pale background, like a playful celebration of primary forms.
  - # Three Geometric Shapes

A vibrant purple square, a bold red triangle, and a bright yellow circle are arranged in a cheerful row against a light background.

### instruct_only
- **s1_red_circle_blue_square** — true: ['blue', 'red'] ['circle', 'square']
  - A red circle and a blue square are positioned side by side on a white background.
  - A red circle and a blue square are positioned side by side on a white background.
  - A red circle and a blue square are positioned side by side on a light gray background.
- **s2_green_triangle_alone** — true: ['green'] ['triangle']
  - A green triangle centered on a light gray background.
  - A simple green triangle centered on a light gray background.
  - A green triangle centered on a light gray background.
- **s3_yellow_square_over_purple_circle** — true: ['purple', 'yellow'] ['circle', 'square']
  - A yellow square is positioned above a purple circle on a white background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - The image shows a yellow square positioned above a purple circle, both centered horizontally on a light gray background.
- **s4_three_orange_circles** — true: ['orange'] ['circle']
  - Three orange circles of similar size arranged in a horizontal row on a light gray background.
  - Three orange circles of similar size evenly spaced in a horizontal row on a light gray background.
  - Three orange circles of equal size arranged horizontally in a row on a light gray background.
- **s5_blue_triangle_green_square** — true: ['blue', 'green'] ['square', 'triangle']
  - A blue triangle and a green square are shown side by side on a white background.
  - A blue triangle and a green square are shown side by side on a white background.
  - The image shows a blue triangle on the left and a green square on the right, both set against a light gray background.
- **s6_purple_square_red_triangle_yellow_circle** — true: ['purple', 'red', 'yellow'] ['circle', 'square', 'triangle']
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a white background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.

### bare
- **s1_red_circle_blue_square** — true: ['blue', 'red'] ['circle', 'square']
  - A vibrant red circle and a bold blue square sit apart on a pale gray canvas, like two contrasting personalities maintaining their distance.
  - A vibrant crimson circle and a brilliant cobalt square sit apart on a pale background, like two contrasting geometric personalities keeping their distance.
  - A crimson circle and a blue square sit apart on a pale background, like two geometric personalities keeping their distance.
- **s2_green_triangle_alone** — true: ['green'] ['triangle']
  - A vibrant green triangle sits centered against a pale, minimalist background, its three sharp points creating a simple yet striking geometric form.
  - # A Solitary Green Triangle

A vibrant green triangle sits centered against a pale, minimalist background, its geometric simplicity suggesting both mathematical precision and natural vitality.
  - A solitary green triangle stands centered against a pale, minimalist background.
- **s3_yellow_square_over_purple_circle** — true: ['purple', 'yellow'] ['circle', 'square']
  - A cheerful golden square hovers gracefully above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
  - A yellow square hovers above a vibrant purple circle, arranged vertically like celestial bodies in a minimalist cosmic landscape.
  - A golden yellow square hovers above a vibrant purple circle, creating a minimalist composition of geometric simplicity.
- **s4_three_orange_circles** — true: ['orange'] ['circle']
  - Three vibrant orange circles are arranged in a horizontal line against a light background, like glowing orbs floating in a minimalist space.
  - Three vibrant orange circles arranged in a horizontal line against a light background, resembling a minimalist representation of celestial bodies or a simple visual metaphor for progression.
  - Three vibrant orange circles are arranged in a neat horizontal line against a light background, like gleaming orbs suspended in space.
- **s5_blue_triangle_green_square** — true: ['blue', 'green'] ['square', 'triangle']
  - A vibrant blue triangle stands proudly on the left side while a green square balances it on the right, creating a simple yet striking geometric composition.
  - # Image Description

A vibrant blue triangle stands on the left side of the composition, while a green square occupies the right portion, creating a simple yet striking contrast between two fundamental geometric shapes.
  - A vibrant blue triangle and a green square sit apart on a light gray canvas, like two distinct personalities in a minimalist composition.
- **s6_purple_square_red_triangle_yellow_circle** — true: ['purple', 'red', 'yellow'] ['circle', 'square', 'triangle']
  - # Image Description

Three vibrant geometric shapes—a purple square, a red triangle, and a yellow circle—stand in a cheerful line against a pale background, like primary form companions on a minimalist stage.
  - # Three Geometric Shapes

A vibrant purple square, a bold red triangle, and a bright yellow circle are arranged in a row against a neutral background, creating a simple yet striking composition of vivid colors and fundamental geometric forms.
  - # A Vibrant Trio of Geometric Shapes

Three bold, colorful forms—a purple square, a crimson triangle, and a golden circle—stand in striking alignment against a soft neutral backdrop.
