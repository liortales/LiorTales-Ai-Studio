# Remotion Video Assembly — Workflow Contract

Canonical reference for how Agent 06 uses Remotion. Referenced by
`agents/06-reels-video-producer/README.md` and
`workflows/pipeline-control-rules.md` §11 rather than duplicated there.

## What Remotion is for here

Remotion is a code-driven video assembly and rendering tool — it composes
a finished video from material that already exists (clips, images,
approved covers, text, audio) rather than generating new footage. It sits
alongside KlingAI as a second execution tool for Agent 06, not a
replacement for it and not a second, parallel video-production system.
Agent 06's ownership, inputs, quality standards, PRODUCT ASSET LOCK
obligations, and handoff-to-Agent-07 contract are unchanged regardless of
which tool (or both) produced the asset — only `PRODUCTION_TOOL` changes.

Routing logic (KLING vs. REMOTION vs. KLING_PLUS_REMOTION vs. static
fallback): canonical rule in `workflows/pipeline-control-rules.md` §11 and
§4. This file covers Remotion's implementation side only.

## Why Remotion is inherently lower-risk for cover fidelity

Unlike Kling or any generative model, Remotion doesn't draw pixels from a
prompt — it places existing files (an image, a video clip, a text layer)
at specified positions and times, deterministically. That makes it
structurally similar to the deterministic image compositor
(`shared/production-tools/openai-image-pipeline.md`), not to a generative
tool: there is no risk of Remotion "reinterpreting" a book cover the way a
diffusion/generation model could. That said, this only holds if Agent 06
actually feeds it the exact approved asset file — Remotion will place
whatever image it's given exactly as given, including a wrong or
low-fidelity one, so supplying the correct registered source file is still
Agent 06's responsibility, not something Remotion verifies on its own.

**Never** ask Remotion (or any code you write for it) to regenerate,
redraw, filter, or stylize an approved cover's artwork. Load the exact
approved file (from `product-assets/approved-master-covers/`, verified via
`tools/openai-image-pipeline/covers_registry.py`) and place it — resize,
position, crop-to-frame, and animate its entrances/exits are fine; altering
the pixels inside the cover artwork is not.

## Source of truth for implementation

The installed Remotion skills are the source of truth for how to actually
write and render Remotion projects — do not improvise Remotion API usage
from general knowledge when a skill covers it. Entry point:
`remotion-best-practices` (routes to the others). Relevant for LiorTales
Reel/video assembly work:

- **`remotion-create`** — scaffold a new Remotion project/composition when one doesn't exist yet for the run.
- **`remotion-markup`** — the core assembly reference: transitions, effects, multi-scene sequencing, text/typography, images, audio, video editing, SFX, light leaks, timing. This is what most hook/CTA/end-card/carousel-style assembly work will use.
- **`remotion-captions`** — transcribing, displaying, and animating subtitles/captions from Agent 04's approved copy.
- **`remotion-multimedia`** — reading duration/dimensions of source clips and audio before assembling a timeline.
- **`remotion-render`** — exporting the final video file (`npx remotion render`). Never claim a render succeeded without the tool confirming success and the output file existing.
- **`remotion-studio`** — local preview during assembly, useful for a sanity check before render but not itself a deliverable.
- **`remotion-docs`** — search current Remotion documentation for anything not covered by the above.

`remotion-maps`, `remotion-saas`, `remotion-interactivity`, and
`remotion-upgrade` are installed but not relevant to LiorTales Reel
production (geographic data visualization, building a separate video-editor
app, Studio-specific interactive editing, and dependency upgrades,
respectively) — don't reach for them on a normal content run.

## Typical Remotion-route inputs

- Approved LiorTales book cover(s) from `product-assets/approved-master-covers/` (via the registry, same fidelity rule as static assets).
- Product images / photos already approved for use.
- Previously generated clips (including Kling output, for the KLING_PLUS_REMOTION route).
- Agent 04's approved copy, for on-screen text, captions, and CTA/end-card wording — Remotion may adjust timing/technical presentation, not wording, same rule as elsewhere in Agent 06.
- Brand typography, colors, and motion style from `shared/brand/visual-identity-guide.md`.
- Music/audio, where available and rights-cleared.

## Output

A rendered video file (`PRODUCTION_TOOL: REMOTION` or `KLING_PLUS_REMOTION`
in Agent 06's Video Output Record), handed off to Agent 07 QC exactly like
a Kling-only asset — video quality standard, continuity, child safety, and
PRODUCT ASSET LOCK checks all apply identically.
