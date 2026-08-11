# OpenAI Image Production Pipeline

Two-stage tool for producing marketing images that include an approved
LiorTales book cover, without ever letting a generative model touch the
cover artwork itself.

See `../../shared/production-tools/openai-image-pipeline.md` for the full
workflow contract (why this exists, how it's forbidden/allowed to be used,
how it fits into Agent 05 / 06 / 07). This file is the practical CLI
reference for running the scripts directly.

## Install

```bash
pip install -r requirements.txt
```

## Stage A — generate the scene (calls OpenAI, costs money)

```bash
export OPENAI_API_KEY=...   # never hard-code, never commit

python3 generate_scene.py \
  --prompt "A warm, softly lit kitchen. A mother and her ~5-year-old \
daughter lean over a wooden table together, both smiling. The child holds \
a closed hardcover picture book resting flat on the table, propped at a \
slight angle toward camera, both hands resting on its edges (not gripping \
the front cover). The book's front cover is a plain neutral cream surface \
with visible page-block thickness and a soft contact shadow on the table. \
Photorealistic, natural window light, shallow depth of field." \
  --output scene.png
```

`--prompt` must describe a **neutral/placeholder book-cover plane** —
never a specific title, character, or cover design. `generate_scene.py`
prints a warning (not a hard block — free text can't be reliably policed)
if the prompt mentions "book cover" et al.; review it either way. The real
guarantee that the cover stays untouched is Stage B, not this check.

Flags: `--model` (default `gpt-image-1`), `--size`
(`1024x1024`/`1024x1536`/`1536x1024`/`auto`), `--quality`
(`low`/`medium`/`high`/`auto`), `--n` (number of variants).

## Stage B — composite the exact cover (no OpenAI call, no network)

First, a cover must be registered and pinned once — see
`../../product-assets/approved-master-covers/README.md`. Then, for each generated scene, find
the four corners (in pixels, TL → TR → BR → BL) of the book-cover plane
visible in that specific image, and run:

```bash
python3 compose_cover.py \
  --scene scene.png \
  --title "Olivia and the Enchanted Bunny" \
  --corners "180,420 560,395 545,760 165,790" \
  --output composited.png \
  [--occlusion-mask hand_mask.png]
```

- `--corners` is required and manual per image — there is no automatic
  book-plane detection in this tool. Read the corner pixel coordinates off
  the generated scene (e.g. in an image editor) before calling this.
- `--occlusion-mask` is a grayscale image the same content area as the
  scene: **white = keep the original scene on top** (e.g. fingers gripping
  the book), **black = show the composited cover**. Required for any
  handheld shot to have a chance at passing
  `workflows/pipeline-control-rules.md` §10 — omitting it is valid only for
  non-handheld placements (book resting/propped/standing).
- The script refuses to run — and writes nothing — if the named cover
  isn't pinned in the registry, or if its pinned hash doesn't match the
  file currently on disk. See error messages for the exact fix.
- On success it writes `<output>` and `<output>.manifest.json` — the audit
  trail QC (Agent 07, area 15/16) requires as evidence.

## Product Fidelity Check (spot-check after the fact)

```bash
python3 verify_composite.py --composite composited.png
```

Re-derives the expected cover-region pixels from the manifest + registry
and diffs them against the actual file. Use this to catch drift — e.g. the
file was hand-edited after compositing, or the registry's pinned cover
changed since. `PASS`/exit 0, or a specific failure reason/exit 1.

## Registry maintenance

```bash
python3 covers_registry.py list
python3 covers_registry.py check "Olivia and the Enchanted Bunny"
python3 covers_registry.py pin "Olivia and the Enchanted Bunny"
```

## Tests

No API key needed — the tests never call OpenAI, only synthetic
runtime-generated images.

```bash
python3 tests/run_all.py
```

## What this tool will never do

- Never asks a generative model to draw, redraw, inpaint, or edit cover
  artwork — Stage A only ever generates the surrounding scene.
- Never composites a cover file that isn't pinned in the registry, or
  whose hash doesn't match the pin.
- Never logs, prints, or writes `OPENAI_API_KEY` anywhere.
