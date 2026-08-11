#!/usr/bin/env python3
"""Stage A -- generate the photorealistic marketing scene with OpenAI.

This script produces ONLY the surrounding scene: people, facial expressions,
hands, a physically plausible book (thickness, edges, perspective, contact
shadows), and lighting. It must never be asked to render, redraw, or
approximate an approved LiorTales cover -- describe a neutral/blank
book-cover plane instead. The exact cover artwork is composited in
afterward, deterministically, by compose_cover.py -- see
../../shared/production-tools/openai-image-pipeline.md for the full
two-stage contract this script is one half of.

Requires OPENAI_API_KEY in the environment (see openai_client.py). Never
pass the key on the command line, in a prompt, or write it to a file.

Usage:
    python3 generate_scene.py --prompt "..." --output scene.png
"""
from __future__ import annotations

import argparse
import base64
import sys
from pathlib import Path

from openai_client import MissingAPIKeyError, build_client

DEFAULT_MODEL = "gpt-image-1"

# Heuristic-only courtesy check: catches obvious attempts to ask the model to
# render a specific title's cover art. This is NOT the fidelity guarantee --
# it's easy to word around, and free-text prompts can't be reliably policed.
# The real guarantee is architectural: compose_cover.py never uses any pixel
# this script produces as final cover artwork, regardless of what the model
# drew here. See shared/production-tools/openai-image-pipeline.md.
_COVER_WARNING_HINTS = ("book cover", "cover art", "cover artwork", "front cover", "the cover of")


def _warn_if_prompt_targets_cover(prompt: str) -> None:
    lowered = prompt.lower()
    if any(hint in lowered for hint in _COVER_WARNING_HINTS):
        print(
            "WARNING: prompt mentions a book cover. Stage A must only "
            "describe a neutral/placeholder book-cover plane -- never a "
            "specific title, character artwork, or cover design. Review the "
            "prompt before using this output; the exact approved cover is "
            "composited in later by compose_cover.py regardless of what "
            "this generates.",
            file=sys.stderr,
        )


def generate_scene(
    prompt: str,
    output: Path,
    model: str = DEFAULT_MODEL,
    size: str = "1024x1536",
    quality: str = "high",
    n: int = 1,
) -> list[Path]:
    if not prompt or not prompt.strip():
        raise ValueError("--prompt must not be empty")
    if n < 1:
        raise ValueError("--n must be at least 1")

    _warn_if_prompt_targets_cover(prompt)
    client = build_client()

    try:
        result = client.images.generate(
            model=model,
            prompt=prompt,
            size=size,
            quality=quality,
            n=n,
        )
    except Exception as exc:
        # openai raises typed exceptions (AuthenticationError, APIError, ...);
        # the message itself never contains the key, only surface it as-is.
        raise RuntimeError(f"OpenAI image generation failed: {exc}") from exc

    if not getattr(result, "data", None):
        raise RuntimeError("OpenAI response contained no image data.")

    output.parent.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for i, item in enumerate(result.data):
        if not getattr(item, "b64_json", None):
            raise RuntimeError(
                "OpenAI response did not include image data (b64_json). "
                "Check the model/response format."
            )
        image_bytes = base64.b64decode(item.b64_json)
        path = output if n == 1 else output.with_stem(f"{output.stem}_{i}")
        path.write_bytes(image_bytes)
        written.append(path)
    return written


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--prompt", required=True, help="Scene description. Never name a specific book's cover artwork.")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG path")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--size", default="1024x1536", choices=["1024x1024", "1024x1536", "1536x1024", "auto"])
    parser.add_argument("--quality", default="high", choices=["low", "medium", "high", "auto"])
    parser.add_argument("--n", type=int, default=1)
    args = parser.parse_args()

    try:
        written = generate_scene(args.prompt, args.output, args.model, args.size, args.quality, args.n)
    except MissingAPIKeyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    for path in written:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
