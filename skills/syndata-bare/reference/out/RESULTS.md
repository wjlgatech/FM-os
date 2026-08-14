# syndata-bare — live run against real vision models

- **base role**: `claude-haiku-4-5-20251001` @ T=1.0 (`proxy`)
- **instruct role**: `claude-sonnet-5` @ T=0.0 **(REJECTED by the API — model default used)**
- **scenes**: 6 deterministic synthetic compositions (`bare_stimuli.py`), 6 caption(s) per scene per pipeline
- **date**: 2026-08-14 · **repeats**: 1
- alignment = 1 − (captions naming an absent colour/shape) / (captions measured)
- an unmeasured caption is excluded from every aggregate — never scored 0

| pipeline | alignment | diversity | yield | measured | gate |
|---|---|---|---|---|---|
| base_only | 1.00 | 0.58 | 1.00 | 36 | PASS |
| instruct_only | 1.00 | 0.19 | 1.00 | 36 | FAIL — diversity 0.19 < 0.25 |
| bare | 1.00 | 0.59 | 1.00 | 36 | PASS |

## The two claims, scored separately

- **pipeline claim** (draft-then-refine beats either single stage): **UNMEASURED**
- **paper claim** (a BASE checkpoint supplies diversity an instruct model cannot): **UNMEASURED**

  base_only showed no hallucination, but the run lacked the power to detect it: 0 hallucinations in 36; 95% CI for the true rate is [0, 0.083]. That CANNOT exclude the 4.62% reference rate — n≥65 is needed. The zero is uninformative.

### Statistical power — could this run have seen what it looked for?

  0 hallucinations in 36; 95% CI for the true rate is [0, 0.083]. That CANNOT exclude the 4.62% reference rate — n≥65 is needed. The zero is uninformative.

  Rule of three (Hanley & Lippman-Hand, *JAMA* 1983): with 0 events in *n*
  trials the 95% CI for the true rate is [0, 3/n]. Reference rate: 4.62%, the independently published 2026 hallucination rate for
  the default base role. Observing zero does not make the rate zero.

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

## Precondition probe — does the base role hallucinate at all?

Text-interference in colour perception, after *What Color Is It?* (arXiv:2511.13400): a conflicting colour word is printed on the shape and the model is asked the shape's colour. Naming the printed word is unambiguous hallucination — no caption parsing, no synonym trap.

This is a SECOND declared condition, not the plain condition retuned. Both are reported; neither replaces the other.

- **measured**: 72 answers
- **hallucinated**: 0
- **rate**: 0.00
- **power**: ADEQUATE — 0 hallucinations in 72; 95% CI for the true rate is [0, 0.042]. That resolves the 4.62% reference rate.

| scene | true | printed | answer | hallucinated |
|---|---|---|---|---|
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i1_red_circle_labelled_BLUE | red | blue | Red | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| i2_blue_square_labelled_GREEN | blue | green | Blue | no |
| … | | | *48 more in raw_captions.json* | |

## Raw captions (evidence)

### base_only
- **s1_red_circle_blue_square** — true: ['blue', 'red'] ['circle', 'square']
  - A crimson circle and a cobalt square sit separated on a pale background, like two geometric strangers maintaining their distance.
  - A vibrant crimson circle and a cobalt blue square sit apart on a pale background, like two distant thoughts waiting to connect.
  - A vibrant crimson circle and a bold cobalt square sit in solitary contrast against a pale, minimalist background.
  - A crimson circle and an electric blue square face each other across a stark white expanse, like two geometric sentinels standing in silent dialogue.
  - A vibrant crimson circle and a bold cobalt square sit in solitary contrast on a pale canvas, like opposing forces in a minimalist composition.
  - A vibrant crimson circle and a striking cobalt square stand apart on a pale background, creating a simple yet striking composition of geometric contrast.
- **s2_green_triangle_alone** — true: ['green'] ['triangle']
  - A vibrant emerald triangle stands solitary against a pale, minimalist background, its sharp apex pointing skyward like a verdant mountain peak.
  - A vibrant emerald triangle stands solitary against a pale, minimalist background, its sharp apex pointing skyward like a verdant mountain peak.
  - # A vibrant emerald triangle stands alone against a soft, neutral background, its geometric form suggesting stability and growth.
  - A verdant triangle points skyward, its solid emerald form standing alone against a pale backdrop like a pine tree stripped of its branches.
  - A vibrant emerald triangle stands alone against a pale backdrop, resembling a solitary evergreen peak reaching toward the sky.
  - A verdant triangular shape rises majestically against a pristine white backdrop, resembling an evergreen forest condensed into its most elemental geometric form.
- **s3_yellow_square_over_purple_circle** — true: ['purple', 'yellow'] ['circle', 'square']
  - # Image Description

A vibrant golden square hovers above a rich purple circle, creating a striking composition of geometric shapes in contrasting warm and cool tones.
  - A golden rectangle hovers above a vibrant purple circle, creating a simple yet striking composition of geometric shapes in complementary colors.
  - A golden square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric forms.
  - A vibrant golden square hovers above a rich purple circle, creating a simple yet striking composition of geometric shapes in contrasting colors.
  - A cheerful golden square hovers above a vibrant purple circle, creating a simple yet striking geometric composition.
  - # Image Description

A golden square hovers above a vibrant purple circle, creating a minimalist composition of geometric shapes.
- **s4_three_orange_circles** — true: ['orange'] ['circle']
  - Three vibrant orange spheres are arranged in a neat horizontal line against a pale background, resembling glowing orbs or celestial bodies in perfect alignment.
  - Three vibrant orange spheres are arranged in a neat horizontal line against a pale background, resembling a minimalist representation of celestial bodies or simple geometric forms.
  - Three golden orbs sit in a perfect horizontal line, like celestial bodies suspended in a minimalist void.
  - Three golden orbs rest in a tranquil horizontal arrangement, like celestial bodies suspended in a pale void.
  - Three vibrant orange spheres are arranged in a neat horizontal line against a pale background, like glowing orbs of captured sunlight.
  - Three vibrant orange spheres are arranged in a horizontal line, like glowing orbs suspended in a minimalist space.
- **s5_blue_triangle_green_square** — true: ['blue', 'green'] ['square', 'triangle']
  - # Image Description

A vibrant blue triangle stands confidently on the left side while a forest green square holds steady on the right, creating a simple yet striking contrast of geometric shapes and colors against a neutral background.
  - A vibrant blue triangle stands sentinel on the left side of the composition, while a bold emerald square occupies the right, creating a striking contrast between geometric simplicity and primary color harmony.
  - A vibrant blue triangle stands sentinel on the left side of the composition, while a rich emerald green square anchors the right, creating a minimalist study in geometric contrast.
  - A vibrant blue triangle and a rich emerald green square sit apart on a neutral background, representing geometric simplicity and color contrast.
  - A vibrant blue triangle stands sentinel on the left side of the composition, while a bold emerald green square anchors the right, creating a balanced study in geometric contrast.
  - A vibrant blue triangle and an emerald green square sit side by side, creating a simple yet striking composition of geometric shapes.
- **s6_purple_square_red_triangle_yellow_circle** — true: ['purple', 'red', 'yellow'] ['circle', 'square', 'triangle']
  - # Image Description

Three vibrant geometric shapes—a purple square, a crimson triangle, and a golden circle—stand in a harmonious row like primary building blocks of color and form.
  - # Three Geometric Shapes

A vibrant purple square, a striking red triangle, and a cheerful yellow circle are arranged in a row against a light background, forming a simple yet colorful composition of primary shapes.
  - # Image Description

Three primary geometric shapes—a purple square, a crimson triangle, and a golden circle—are arranged in a simple, minimalist composition against a pale background.
  - # A Colorful Geometric Trio

Three vibrant shapes—a purple square, a scarlet triangle, and a golden circle—stand in a row like primary building blocks of artistic expression.
  - # Image Description

Three vibrant geometric shapes—a purple square, a crimson triangle, and a golden circle—are arranged in a cheerful row against a pale background, creating a simple yet striking composition that celebrates primary forms and bold color.
  - # Image Description

Three colorful geometric shapes—a purple square, a red triangle, and a yellow circle—are arranged in a row against a light background, representing the fundamental forms of visual art.

### instruct_only
- **s1_red_circle_blue_square** — true: ['blue', 'red'] ['circle', 'square']
  - A red circle and a blue square are positioned side by side on a white background, with the circle on the left and the square on the right.
  - The image shows a red circle on the left and a blue square on the right, both set against a plain white background.
  - A red circle and a blue square are positioned side by side on a white background.
  - A red circle and a blue square appear on a white background, with the circle on the left and the square on the right.
  - A red circle and a blue square appear side by side on a white background.
  - A red circle and a blue square are positioned side by side on a white background.
- **s2_green_triangle_alone** — true: ['green'] ['triangle']
  - A green triangle on a light gray background.
  - A green triangle on a light gray background.
  - A green triangle on a light gray background.
  - A green triangle on a light gray background.
  - A green triangle centered on a light gray background.
  - A green triangle centered on a light gray background.
- **s3_yellow_square_over_purple_circle** — true: ['purple', 'yellow'] ['circle', 'square']
  - The image shows a yellow square positioned above a purple circle, both centered horizontally against a light gray background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - The image shows a yellow square positioned above a purple circle, both centered horizontally on a light gray background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - A yellow square is positioned above a purple circle on a light gray background.
- **s4_three_orange_circles** — true: ['orange'] ['circle']
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
  - Three orange circles of equal size arranged horizontally in a row on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
- **s5_blue_triangle_green_square** — true: ['blue', 'green'] ['square', 'triangle']
  - The image shows a blue triangle on the left and a green square on the right, both set against a light gray background.
  - The image shows a blue triangle on the left and a green square on the right, both on a white background.
  - The image shows a blue triangle on the left and a green square on the right, both set against a white background.
  - The image shows a blue triangle on the left and a green square on the right, both on a white background.
  - A blue triangle and a green square are positioned side by side on a light gray background.
  - A blue triangle and a green square are shown side by side on a white background.
- **s6_purple_square_red_triangle_yellow_circle** — true: ['purple', 'red', 'yellow'] ['circle', 'square', 'triangle']
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.

### bare
- **s1_red_circle_blue_square** — true: ['blue', 'red'] ['circle', 'square']
  - A vibrant red circle and a striking blue square sit apart on a pale canvas, like two geometric personalities refusing to mingle at a minimalist party.
  - A vibrant red circle on the left side faces off against a bold blue square on the right, creating a simple yet striking contrast of shapes and colors.
  - A vibrant red circle and a bold blue square sit in peaceful opposition across a minimalist white canvas, like two geometric personalities meeting in silent contemplation.
  - A vibrant red circle and a bold blue square sit separated on a pale background, like two geometric friends maintaining their distance.
  - A vibrant red circle and a blue square face each other across a pristine white canvas, like two geometric characters in a minimalist conversation.
  - A vibrant red circle and a bold blue square sit facing each other across a pale background, like two geometric friends in a minimalist standoff.
- **s2_green_triangle_alone** — true: ['green'] ['triangle']
  - A solitary green triangle stands poised like a mountain peak against a pristine gray canvas.
  - A green triangle sits centered in a minimalist composition, its solid hue standing in stark contrast to the pale, neutral background.
  - A vibrant green triangle stands alone against a soft, pale background, its perfectly symmetrical form evoking the silhouette of a majestic evergreen tree.
  - A vibrant green triangle sits poised at the center of a pale, neutral background, creating a striking contrast of color and simplicity.
  - A vibrant green triangle stands poised at the center of a pale, minimalist canvas.
  - A green triangle sits centered in a pale, minimalist composition, casting a quiet geometric presence against the blank canvas.
- **s3_yellow_square_over_purple_circle** — true: ['purple', 'yellow'] ['circle', 'square']
  - A vibrant golden square hovers above a rich purple circle, creating a simple yet striking composition of geometric shapes on a light gray background.
  - A cheerful yellow square hovers above a purple circle, creating a simple yet striking composition of geometric shapes in vibrant contrasting colors.
  - A yellow square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
  - A golden-yellow square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
  - A yellow square hovers above a purple circle in a minimalist composition against a pale background.
  - A golden square hovers above a vibrant purple circle, creating a simple yet striking geometric composition.
- **s4_three_orange_circles** — true: ['orange'] ['circle']
  - Three orange circles sit in perfect alignment, like celestial bodies frozen in a moment of cosmic harmony.
  - Three vibrant orange circles are arranged in a horizontal line against a pale background, resembling a whimsical trio of glowing orbs or celestial bodies.
  - Three vibrant orange circles are arranged in a horizontal line against a pale background, like glowing orbs suspended in space.
  - Three vibrant orange circles are arranged in a horizontal line across a light background, resembling glowing orbs or dots suspended in space.
  - Three vibrant orange circles are arranged in a neat horizontal line against a pristine white backdrop.
  - Three vibrant orange circles are arranged in a horizontal line against a pale background, like glowing orbs suspended in space.
- **s5_blue_triangle_green_square** — true: ['blue', 'green'] ['square', 'triangle']
  - A vibrant blue triangle stands proudly on the left side while a green square holds its ground on the right, creating a simple yet striking composition of geometric contrasts.
  - A vibrant blue triangle stands in contrast to a green square, two geometric shapes positioned separately against a neutral backdrop.
  - A vibrant blue triangle stands in solitary splendor on the left, while a verdant green square claims its own space on the right side of the composition.
  - A vibrant blue triangle and a green square sit apart on a pale background, like two geometric friends maintaining their distance.
  - A vibrant blue triangle stands boldly on the left side while a rich green square anchors the right, creating a simple yet striking geometric composition.
  - A vibrant blue triangle and a green square sit apart from each other on a pale background, like two geometric shapes waiting for a conversation.
- **s6_purple_square_red_triangle_yellow_circle** — true: ['purple', 'red', 'yellow'] ['circle', 'square', 'triangle']
  - # Image Description

Three geometric shapes—a purple square, a red triangle, and a yellow circle—are arranged in a row against a light background, creating a simple yet vibrant composition of primary forms.
  - # Image Description

A trio of vibrant geometric shapes—a purple square, a red triangle, and a yellow circle—stand in bold simplicity against a light background.
  - # Three Geometric Shapes in Vibrant Colors

A vibrant purple square, a bold red triangle, and a bright yellow circle are arranged in a row against a pale background, creating a simple yet striking composition of fundamental geometric forms.
  - # Image Description

A vibrant trio of geometric shapes—a purple square, a crimson triangle, and a golden circle—are arranged in a cheerful line across a soft white background.
  - Three vibrant geometric shapes—a purple square, a red triangle, and a yellow circle—stand in a harmonious row like primary elements of a playful visual composition.
  - Three primary geometric shapes—a purple square, a red triangle, and a yellow circle—stand in a harmonious row like colorful sentinels of basic geometry.
