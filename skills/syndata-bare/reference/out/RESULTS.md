# syndata-bare — live run against real vision models

- **base role**: `claude-haiku-4-5-20251001` @ T=1.0 (`proxy`)
- **instruct role**: `claude-sonnet-5` @ T=0.0 **(REJECTED by the API — model default used)**
- **scenes**: 6 deterministic synthetic compositions (`bare_stimuli.py`), 11 caption(s) per scene per pipeline
- **date**: 2026-08-14 · **repeats**: 1
- alignment = 1 − (captions naming an absent colour/shape) / (captions measured)
- an unmeasured caption is excluded from every aggregate — never scored 0

| pipeline | alignment | diversity | yield | measured | gate |
|---|---|---|---|---|---|
| base_only | 1.00 | 0.60 | 1.00 | 66 | PASS |
| instruct_only | 1.00 | 0.18 | 1.00 | 66 | FAIL — diversity 0.18 < 0.25 |
| bare | 1.00 | 0.55 | 1.00 | 65 | PASS |

## The two claims, scored separately

- **pipeline claim** (draft-then-refine beats either single stage): **NOT SUBSTANTIATED**
- **paper claim** (a BASE checkpoint supplies diversity an instruct model cannot): **NOT SUBSTANTIATED**

  base_only passed with adequate power — this base role genuinely does not hallucinate here, so there is nothing for refinement to fix

### Statistical power — could this run have seen what it looked for?

  0 hallucinations in 66; 95% CI for the true rate is [0, 0.045]. That resolves the 4.62% reference rate.

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
  - A crimson circle and a cobalt square sit apart on a pale background, like two primary shapes contemplating the space between them.
  - A crimson circle and azure rectangle sit in solitary contrast on a pale background, as if representing opposing forces in perfect balance.
  - A vibrant crimson circle and a cobalt blue square sit apart on a pale background, creating a simple yet striking composition of contrasting shapes and colors.
  - A vibrant crimson circle on the left side faces off against a bold cobalt square on the right, creating a minimalist composition of geometric contrast.
  - A vivid red circle and a brilliant blue square sit apart on a pale background, like two primary color sentinels guarding opposite ends of a minimalist canvas.
  - A vibrant crimson circle and a striking cobalt square sit opposite each other on a pristine white canvas, like two geometric dancers frozen mid-performance.
  - A vibrant red circle and a bold blue square sit apart from one another on a pale background, like two simple geometric characters meeting across an empty space.
  - A vibrant crimson circle and a bold cobalt square sit apart on a pale background, creating a simple yet striking composition of geometric contrast.
  - A crimson circle and an azure square sit separated on a pale canvas, like opposing forces in geometric harmony.
  - A vibrant red circle and a bold blue square sit in stark contrast on a pale background, like two geometric personalities meeting across an empty space.
  - A vibrant red circle and a bold blue square sit on opposite sides of a pale background, like two primary-colored sentinels guarding their respective territories.
- **s2_green_triangle_alone** — true: ['green'] ['triangle']
  - # Image Description

A vibrant emerald triangle stands solitary against a pale, minimalist backdrop, its three sides forming a perfect geometric pyramid of verdant simplicity.
  - A vibrant emerald triangle stands majestically against a pale, minimalist background.
  - A verdant triangle stands poised against a pale background, its emerald silhouette suggesting simplicity and geometric harmony.
  - A vibrant emerald triangle stands alone against a soft, neutral backdrop, resembling a majestic evergreen tree or a minimalist geometric symbol.
  - A solitary emerald triangle stands proudly against a pale, minimalist backdrop, its sharp apex pointing toward the heavens like a verdant mountain peak.
  - A vibrant emerald triangle sits centered against a pale, minimalist background, embodying geometric simplicity.
  - A solitary emerald triangle stands centered against a pale, minimalist backdrop, its sharp apex pointing skyward like a verdant mountain peak.
  - A solitary emerald-colored triangle sits poised in the center of a pale, minimalist canvas.
  - A verdant triangle sits centered on a pale background, its sharp apex pointing skyward like a tiny emerald mountain.
  - A vibrant emerald triangle stands alone against a pale backdrop, its sharp apex pointing skyward like a verdant mountain peak.
  - A verdant triangle sits centered in a minimalist composition, its bold emerald hue creating a striking contrast against the pale, neutral background.
- **s3_yellow_square_over_purple_circle** — true: ['purple', 'yellow'] ['circle', 'square']
  - A vibrant golden square hovers above a deep purple circle, creating a simple yet striking composition of geometric shapes in contrasting colors.
  - # Image Description

A cheerful golden square hovers above a vibrant purple circle, creating a simple yet striking composition that evokes thoughts of balance and contrast.
  - A vibrant golden square hovers above a royal purple circle, creating a simple yet striking composition of geometric forms.
  - A bright golden square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
  - A bright golden rectangle hovers above a vibrant purple circle, creating a simple yet striking composition of geometric forms.
  - A vibrant golden square hovers above a rich purple circle, creating a simple yet striking composition of geometric forms in contrasting warm and cool tones.
  - A cheerful golden square hovers above a vibrant purple circle, creating a minimalist composition that suggests a whimsical balance between geometric simplicity and playful color contrast.
  - A golden square rests above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
  - A cheerful golden square sits perched above a vibrant purple circle, creating a simple yet striking composition of geometric forms.
  - A golden square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
  - A bright golden square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric forms in contrasting colors.
- **s4_three_orange_circles** — true: ['orange'] ['circle']
  - Three vibrant orange spheres are arranged in a horizontal line against a pale background, like celestial bodies suspended in space.
  - Three vibrant orange spheres are arranged in a horizontal line, resembling a minimalist representation of celestial bodies or glowing orbs floating in empty space.
  - Three burnt-orange spheres sit in a row, creating a minimalist composition against a pale background.
  - Three vibrant tangerine-colored spheres are arranged in a neat horizontal line against a pristine white backdrop.
  - Three vibrant orange spheres sit in a neat horizontal row, like glowing orbs suspended in a minimalist void.
  - Three golden orbs sit in perfect alignment, like celestial bodies suspended in a minimalist cosmos.
  - Three golden-orange spheres sit in a perfect horizontal line, like luminous orbs suspended in a minimalist void.
  - # Image Description

Three vibrant orange spheres are arranged in a horizontal line against a pale background, like glowing orbs suspended in space.
  - Three luminous amber orbs are arranged in a horizontal line against a pale backdrop, like golden sentinels standing watch.
  - Three vibrant orange spheres float in a row like glowing orbs suspended in a pale void.
  - Three vibrant orange spheres are arranged in a neat horizontal line, resembling glowing orbs floating against a pale background.
- **s5_blue_triangle_green_square** — true: ['blue', 'green'] ['square', 'triangle']
  - A vibrant blue triangle stands sentinel on the left side of the composition, while a forest-green square holds its ground on the right, creating a balanced geometric dialogue between two fundamental shapes.
  - A vibrant cobalt triangle and an emerald square sit apart on a neutral canvas, like two geometric personalities maintaining a respectful distance.
  - A vibrant blue triangle and an emerald green square sit independently on a light background, like two simple geometric shapes waiting for a mathematical lesson to begin.
  - A vibrant blue triangle and a deep green square sit apart on a light background, like two contrasting geometric friends in a minimalist landscape.
  - # Image Description

A vibrant blue triangle and an emerald green square sit in contrasting positions on a pale background, like two geometric characters meeting across an empty stage.
  - A vibrant blue triangle and an emerald green square sit apart on a pale background, like two geometric friends maintaining their distance.
  - A vibrant cobalt triangle and an emerald square sit apart on a pale background, representing contrasting geometric forms.
  - A vibrant blue triangle stands on the left side of the image, while a lush green square occupies the right side, creating a simple yet striking composition of geometric contrasts.
  - A vivid blue triangle stands sentinel on the left side of the composition, while a bold emerald green square anchors the right, creating a simple yet striking geometric dialogue between two fundamental shapes.
  - A vibrant blue triangle sits peacefully on the left side of the composition, while a rich emerald green square occupies the right, creating a minimalist study in geometric contrast.
  - A vibrant blue triangle stands sentinel on the left side of the composition, while a bold emerald square anchors the right, creating a striking geometric dialogue between angular and rectilinear forms.
- **s6_purple_square_red_triangle_yellow_circle** — true: ['purple', 'red', 'yellow'] ['circle', 'square', 'triangle']
  - # Image Description

Three geometric shapes in primary colors—a purple square, a crimson triangle, and a golden circle—sit in a row like colorful sentinels of mathematical simplicity.
  - # Image Description

A vibrant trio of geometric shapes—a purple square, a crimson triangle, and a golden circle—stands in harmonious alignment across a neutral canvas.
  - # Image Description

Three vibrant geometric shapes—a purple square, a crimson triangle, and a golden circle—are arranged in a playful row against a soft, neutral background.
  - # Image Description

Three vibrant geometric shapes—a purple square, a crimson triangle, and a golden circle—stand in harmonious alignment against a pale backdrop.
  - # Image Description

Three geometric shapes—a purple square, a crimson triangle, and a golden circle—stand in a cheerful row like a minimalist parade of primary forms.
  - # Image Description

A vibrant trio of primary shapes—a purple square, a red triangle, and a golden yellow circle—stand together in harmonious simplicity against a pale background.
  - # Three Geometric Shapes

A vibrant purple square, a striking red triangle, and a cheerful yellow circle are arranged in a simple, colorful composition against a neutral background.
  - # Image Description

Three vibrant geometric shapes—a purple square, a crimson triangle, and a golden circle—stand in a harmonious row against a pale background.
  - Three geometric shapes in vibrant colors—a purple square, a red triangle, and a golden yellow circle—stand in a cheerful row against a neutral background, creating a simple yet striking display of primary forms.
  - # Image Description

Three vibrant geometric shapes—a purple square, a red triangle, and a golden yellow circle—are arranged in a playful row against a light background, representing the fundamental building blocks of visual design.
  - # Three Vibrant Geometric Shapes

Three bold primary shapes stand side by side—a regal purple square, a fiery red triangle, and a cheerful golden circle—creating a minimalist composition that celebrates geometric simplicity and chromatic harmony.

### instruct_only
- **s1_red_circle_blue_square** — true: ['blue', 'red'] ['circle', 'square']
  - A red circle and a blue square are positioned on a white background, with the circle on the left and the square on the right.
  - A red circle and a blue square are positioned side by side on a white background.
  - A red circle and a blue square are positioned side by side on a white background.
  - A red circle and a blue square are positioned side by side on a white background, with the circle on the left and the square on the right.
  - A red circle and a blue square are positioned side by side on a white background.
  - A red circle and a blue square are positioned side by side on a white background.
  - A red circle and a blue square are positioned side by side on a light gray background.
  - A red circle and a blue square are positioned side by side on a white background.
  - A red circle and a blue square are positioned side by side on a white background.
  - A red circle and a blue square are positioned side by side on a white background, with the circle on the left and the square on the right.
  - A red circle and a blue square are positioned side by side on a white background.
- **s2_green_triangle_alone** — true: ['green'] ['triangle']
  - A green triangle with a flat base and pointed top, centered on a light gray background.
  - A green triangle centered on a light gray background.
  - A green triangle on a light gray background.
  - A green triangle on a light gray background.
  - A green triangle on a light gray background.
  - A green triangle centered on a light gray background.
  - A green triangle centered on a light gray background.
  - A single solid green triangle centered on a light gray background.
  - A single green triangle centered on a light gray background.
  - A green triangle on a white background.
  - A single solid green triangle centered on a light gray background.
- **s3_yellow_square_over_purple_circle** — true: ['purple', 'yellow'] ['circle', 'square']
  - A yellow square is positioned above a purple circle on a light gray background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - A yellow square is positioned above a purple circle on a white background.
  - A yellow square is positioned above a purple circle on a white background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - A yellow square is positioned above a purple circle on a white background.
  - A yellow square is positioned above a purple circle on a light gray background.
  - A yellow square is positioned above a purple circle on a light gray background.
- **s4_three_orange_circles** — true: ['orange'] ['circle']
  - Three orange circles of similar size arranged in a horizontal row on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
  - Three orange circles of similar size arranged in a horizontal row on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row, evenly spaced, on a light gray background.
  - Three orange circles of equal size arranged horizontally in a row, evenly spaced, on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
  - Three orange circles of equal size, evenly spaced in a horizontal row, on a light gray background.
  - Three orange circles of equal size arranged in a horizontal row on a white background.
  - Three orange circles of equal size arranged in a horizontal row on a light gray background.
- **s5_blue_triangle_green_square** — true: ['blue', 'green'] ['square', 'triangle']
  - A blue triangle and a green square are positioned side by side on a white background.
  - The image shows a blue triangle on the left and a green square on the right, both set against a light gray background.
  - The image shows a blue triangle and a green square on a light gray background.
  - The image shows a blue triangle on the left and a green square on the right, both set against a light gray background.
  - The image shows a blue triangle on the left and a green square on the right, both on a white background.
  - The image shows a blue triangle on the left and a green square on the right, both set against a white background.
  - The image shows a blue triangle on the left and a green square on the right, both set against a plain light gray background.
  - The image shows a blue triangle and a green square on a light gray background.
  - The image shows a blue triangle and a green square, side by side on a white background.
  - The image shows a blue triangle on the left and a green square on the right, both on a white background.
  - A blue triangle and a green square are positioned on a light gray background.
- **s6_purple_square_red_triangle_yellow_circle** — true: ['purple', 'red', 'yellow'] ['circle', 'square', 'triangle']
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged side by side on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row against a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.
  - The image shows a purple square, a red triangle, and a yellow circle arranged in a row on a light gray background.

### bare
- **s1_red_circle_blue_square** — true: ['blue', 'red'] ['circle', 'square']
  - A crimson circle and a blue square sit at opposite ends of a pale canvas, like two solitary dancers on an empty stage.
  - A crimson circle and a blue square sit apart on a pale backdrop, like two geometric personalities maintaining a respectful distance.
  - *(not measured)*
  - A crimson circle and blue square sit as solitary sentinels on a pale canvas, their stark geometry creating a minimalist composition of color and form.
  - A crimson circle and a blue square sit at opposite ends of a pale canvas, like two solitary sentinels guarding their respective territories.
  - A crimson circle and a blue square sit as opposing sentinels on a pale canvas.
  - A vibrant red circle and a striking blue square sit separated on a pale background, like two primary-colored sentinels guarding opposite ends of the canvas.
  - A vibrant red circle sits peacefully on the left side while a bold blue square anchors the right, creating a simple yet striking composition of geometric contrast.
  - A vibrant red circle and a blue square sit apart on a pale background, like two shapes waiting for a geometric conversation to begin.
  - A crimson circle and blue square face each other across a pale background like two geometric rivals in a minimalist standoff.
  - A vibrant red circle and a bold blue square face each other across a pale canvas, like two geometric sentinels standing guard on opposite ends of an empty stage.
- **s2_green_triangle_alone** — true: ['green'] ['triangle']
  - A solitary green triangle sits centered against a pale, minimalist backdrop, its geometric simplicity evoking the essence of a classic evergreen tree or mountain peak.
  - A vibrant green triangle sits peacefully in the center of a minimalist, pale backdrop.
  - A solitary green triangle stands proudly against a pale backdrop, its sharp apex pointing skyward like a verdant peak.
  - A green triangle sits isolated against a pale background, its sharp apex pointing toward the heavens like a miniature evergreen forest condensed into geometric form.
  - A green triangle stands solitary against a pale backdrop, its geometric form evoking the silhouette of a mighty evergreen tree.
  - # Image Description

A solitary green triangle stands centered against a pale, minimalist background, its sharp apex pointing skyward like a verdant mountain peak.
  - A vibrant green triangle sits centered against a pale, neutral background, appearing as a simple yet striking geometric form.
  - A solitary green triangle stands poised against a pale backdrop, its three sides converging to form a sharp apex that pierces the simplicity of the composition.
  - A vibrant green triangle stands alone against a pale, neutral background like a solitary evergreen peak rising from a misty landscape.
  - A vibrant green triangle stands alone against a pale background, its geometric form suggesting stability and growth.
  - A vibrant green triangle stands alone against a pale, minimalist background like a solitary pine tree.
- **s3_yellow_square_over_purple_circle** — true: ['purple', 'yellow'] ['circle', 'square']
  - A yellow square hovers above a vibrant purple circle, creating a striking composition of geometric contrast.
  - A yellow square hovers above a vibrant purple circle, creating a minimalist composition of geometric shapes.
  - A bright golden square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
  - A cheerful golden square hovers above a vibrant purple circle, creating a minimalist composition of geometric shapes.
  - A vibrant golden square hovers above a rich purple circle, creating a simple yet striking composition of geometric shapes on a light gray background.
  - A cheerful golden-yellow square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
  - A vibrant golden square hovers above a rich purple circle, creating a minimalist composition of geometric contrast.
  - A cheerful yellow square hovers above a vibrant purple circle, creating a simple yet striking composition of geometric shapes.
  - A golden square sits above a vibrant purple circle, creating a simple yet striking composition of geometric shapes in contrasting colors.
  - A cheerful golden square hovers above a vibrant purple circle, creating a simple yet playful composition of geometric shapes.
  - A vibrant yellow square hovers above a deep purple circle, creating a simple yet striking composition of geometric shapes in complementary colors.
- **s4_three_orange_circles** — true: ['orange'] ['circle']
  - Three vibrant orange circles are arranged in a neat horizontal line against a soft, neutral background, resembling glowing orbs suspended in space.
  - Three vibrant orange circles are arranged in a neat horizontal line against a soft, pale background.
  - Three vibrant orange circles are arranged in a neat horizontal line against a light background, like gleaming orbs awaiting a magician's trick.
  - Three vibrant orange circles are arranged in a horizontal line against a light background, like glowing orbs suspended in space.
  - Three vibrant orange circles are arranged in a horizontal line, like glowing orbs suspended in a minimalist void.
  - Three vibrant orange circles are arranged in a horizontal line, like celestial bodies suspended in a peaceful, minimalist space.
  - Three vibrant orange circles are arranged in a horizontal line against a pale backdrop, like glowing orbs suspended in space.
  - Three orange circles are arranged in a horizontal line, like celestial bodies suspended in a minimalist void.
  - Three gleaming orange circles sit in perfect alignment, like celestial orbs frozen in a moment of cosmic harmony.
  - Three vibrant orange circles are arranged in a horizontal row, resembling a trio of glowing orbs floating against a pale background.
  - Three vibrant orange circles are arranged in a horizontal line against a light background, like gleaming orbs awaiting discovery.
- **s5_blue_triangle_green_square** — true: ['blue', 'green'] ['square', 'triangle']
  - A vibrant blue triangle and a green square sit apart on a pale background, creating a simple yet striking geometric composition.
  - A vibrant blue triangle stands proudly on the left side of the composition, while a verdant green square anchors the right, creating a simple yet striking geometric contrast.
  - # Image Description

A blue triangle stands peacefully on the left side of the composition, while a green square claims the right portion, creating a simple yet striking geometric dialogue between two fundamental shapes.
  - A vibrant blue triangle and a green square sit apart on a pale background, like two geometric friends maintaining their distance.
  - A vibrant blue triangle and a green square sit apart on a pale background, like geometric sentinels of color.
  - A vivid blue triangle stands sentinel on the left side of the canvas, while a bold green square anchors the right, creating a striking study in geometric contrast.
  - A vibrant blue triangle stands sentinel on the left side while a bold green square holds its ground on the right, creating a simple yet striking geometric composition.
  - A vivid blue triangle sits peacefully on the left side of the composition, while a green square occupies the right, creating a simple yet striking geometric contrast.
  - A vibrant blue triangle stands sentinel on the left while a green square occupies the right side of a minimalist composition.
  - A vibrant blue triangle and a green square sit independently on a neutral background, like two simple geometric characters waiting to meet.
  - A vibrant blue triangle stands boldly on the left side of the image, while a rich green square occupies the right side, creating a simple yet striking contrast of geometric forms.
- **s6_purple_square_red_triangle_yellow_circle** — true: ['purple', 'red', 'yellow'] ['circle', 'square', 'triangle']
  - # Description

Three geometric shapes—a purple square, a red triangle, and a yellow circle—are arranged in a row against a light background, creating a simple yet striking composition of basic forms and vibrant colors.
  - Three vibrant geometric shapes—a purple square, a red triangle, and a yellow circle—are arranged in a cheerful row against a light background.
  - # Image Description

Three geometric shapes—a purple square, a red triangle, and a yellow circle—are arranged in a horizontal line against a light background, forming a simple yet striking composition that celebrates basic mathematical forms.
  - # Image Description

Three vibrant geometric shapes—a purple square, a red triangle, and a yellow circle—are arranged in a playful row against a soft, neutral background.
  - A vibrant trio of geometric shapes—a purple square, a red triangle, and a yellow circle—are arranged in a harmonious line against a soft, neutral background.
  - A vibrant trio of geometric shapes—a purple square, a red triangle, and a yellow circle—stand in harmonious alignment across a pristine white canvas.
  - # Image Description

Three vibrant geometric shapes—a purple square, a red triangle, and a golden yellow circle—stand in a cheerful row against a pale background, creating a simple yet playful composition that celebrates basic forms and bold colors.
  - # Image Description

Three vibrant geometric shapes—a purple square, a red triangle, and a yellow circle—are arranged in a cheerful row against a pale backdrop, creating a simple yet striking composition of primary forms and bold colors.
  - # Image Description

Three vibrant geometric shapes—a purple square, a red triangle, and a yellow circle—are arranged in a cheerful row against a pale background, creating a simple yet striking composition of primary forms and bold colors.
  - A vibrant trio of geometric shapes—a regal purple square, a bold red triangle, and a cheerful yellow circle—stands in harmonious alignment across a pristine white canvas.
  - # A Geometric Trio

Three vibrant shapes—a purple square, a red triangle, and a yellow circle—stand in harmonious alignment across a pale backdrop, creating a minimalist composition of primary forms and bold colors.
