# OpenAI Image Production Pipeline — Workflow Contract

Canonical reference for how Agent 05 and Agent 06 produce marketing images
that include an approved LiorTales book, using OpenAI for scene generation
and a local deterministic script for cover compositing. Referenced by
`agents/05-visual-creative-director/README.md`,
`agents/06-reels-video-producer/README.md`,
`agents/07-quality-control-brand-guardian/README.md`, and
`workflows/pipeline-control-rules.md` §9/§10 rather than duplicated there.

## Why this exists

The prior approach — placing the flat cover image as a layout element over
an unrelated photo in Canva — reads as a pasted sticker: no perspective
match, no hand occlusion, no shared lighting or shadow. It cannot produce a
believable physical book in a person's hands. This pipeline replaces it for
any shot where the book needs to look physically present in a photorealistic
scene.

## Two-stage architecture

**Stage A — generative, scene only.** OpenAI (`gpt-image-1` via the Images
API) generates the complete photorealistic scene: people, facial
expressions, hands, a physically plausible book (thickness, edges,
perspective, contact with hands, contact shadows), and scene lighting. The
book's front-cover plane in this generated image must be neutral/blank —
suitable for compositing onto, not a finished design.

**Stage B — deterministic, cover only.** A local script
(`tools/openai-image-pipeline/compose_cover.py`) then:

1. loads the exact approved LiorTales cover source asset from a locally
   cached, hash-verified file (never re-fetched from a generative model);
2. takes the four corners of the visible book-cover plane in the Stage A
   image (supplied by the operator — there is no automatic detection);
3. computes a deterministic perspective transform of the cover image onto
   those four corners;
4. composites the warped cover onto the scene;
5. preserves the source artwork's actual pixels — the transform only ever
   resamples the cover's own image data, never generates new pixel content;
6. optionally re-composites the original scene's foreground back on top
   using a supplied occlusion mask, so fingers/hands that were in front of
   the book in Stage A stay in front of the composited cover;
7. never invokes any image-generation model on the cover artwork at any
   point in this stage.

Perspective transformation required by the book's physical orientation in
the scene is exactly what step 3 does, and is the only transformation ever
applied to the cover. **Generative reinterpretation of the cover artwork —
including masked/inpainting-style generative edits confined to the cover
region — is never used and is forbidden**, per
`workflows/pipeline-control-rules.md` §9. Masking a region so a generative
model can *fill* it is not compositing; only a geometric transform of the
source file's own pixels counts.

## What Stage A may and may never do

- May: generate any number of candidate scenes, iterate on prompt, pose,
  lighting, framing.
- Must: leave the book's front-cover plane neutral/blank in the prompt —
  never name a specific LiorTales title, character, or cover design.
- Never: be asked to render, approximate, or "match" the actual cover
  artwork. If a candidate scene's book plane comes back with invented
  cover-like content anyway, discard that plane for compositing purposes —
  Stage B will still only use the registered source file, but a
  cover-shaped hallucination in the base image makes it harder to place
  the real cover convincingly and is a sign the prompt needs tightening.

## Fidelity guarantee (how cover pixels are protected)

Three layers, from `tools/openai-image-pipeline/`:

1. **Construction-time refusal.** `compose_cover.py` will not run against a
   cover title unless the local cached file's SHA-256 hash matches a value
   a human explicitly pinned (`covers_registry.py pin`) after visually
   verifying it against the Canva registry
   (`shared/product/product-bible.md` §18). Missing file, unpinned file, or
   hash mismatch all hard-stop before any image is written.
2. **Audit manifest.** Every successful composite writes a
   `<output>.manifest.json` recording the title, Canva asset ID, the exact
   cover file hash used, the corners, whether an occlusion mask was
   applied, and `compositing_method: deterministic_perspective_transform` /
   `generative_model_touched_cover_pixels: false`.
3. **Post-hoc spot check.** `verify_composite.py` re-derives the expected
   cover region from the manifest + currently-pinned registry file and
   diffs it against the actual output, to catch later re-edits or registry
   drift.

None of this depends on visually inspecting a flattened final image after
the fact for "does it look right" — fidelity is enforced by controlling
what feeds the compositor, not by forensics on the output.

## Handoff to Canva

Canva is used only for layout, typography, and caption work on the
finished image (or for formats that don't need a photorealistic book at
all) — never to reconstruct, redraw, or re-touch the cover. This
deprecates the flat-layout-element-as-final-cover pattern.

## Credentials

`OPENAI_API_KEY` comes only from an environment variable / the runtime's
own secret mechanism. Never in a script, a Canva design, a chat message, or
committed anywhere in this repo. See
`tools/openai-image-pipeline/openai_client.py` and the setup note in that
tool's README.

## QC linkage

Agent 07 QC area 15 (Product Asset Identity) and area 16 (Handheld
Physical Realism) — `agents/07-quality-control-brand-guardian/README.md` —
require the compositing manifest as evidence when this pipeline was used.
A missing manifest, or one that doesn't show the deterministic method, is
treated as a fidelity failure by default rather than accepted on visual
inspection alone.

## The Capability Test still applies

This pipeline raises the ceiling on what's achievable for handheld shots —
it does not waive `workflows/pipeline-control-rules.md` §10's four-criteria
Capability Test. Every handheld shot still needs verified: exact cover
pixels, believable book geometry, natural hand occlusion (an occlusion mask
was actually supplied and used), and believable contact shadows/lighting.
A shot that fails any of these routes to
`HANDHELD_PRODUCT_COMPOSITING_UNSUPPORTED` and a non-handheld redesign, per
§10 — same as before this pipeline existed.
