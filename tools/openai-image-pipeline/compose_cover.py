#!/usr/bin/env python3
"""Stage B -- deterministic compositing of an approved LiorTales cover onto
a generated scene.

This script never calls a generative model and never touches OpenAI. It
performs one thing only: a deterministic geometric (perspective) transform
of the exact pinned cover file -- verified byte-for-byte against its
registered SHA-256 hash before use -- alpha-composited onto the scene at the
four corners you supply. See
../../shared/production-tools/openai-image-pipeline.md for the full
contract and why masked generative editing is never an acceptable
substitute for this step.

Usage:
    python3 compose_cover.py \\
        --scene scene.png \\
        --title "Olivia and the Enchanted Bunny" \\
        --corners "120,340 480,310 470,650 100,690" \\
        --output composited.png \\
        [--occlusion-mask hand_mask.png]
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

from covers_registry import REGISTRY_PATH, get_cover, verify_cover_file

TOOL_VERSION = "1.0.0"
DEFAULT_MIN_QUAD_AREA = 1000.0


class CompositingError(Exception):
    pass


def _parse_corners(raw: str) -> list[tuple[float, float]]:
    points = []
    for tok in raw.split():
        try:
            x_str, y_str = tok.split(",")
            points.append((float(x_str), float(y_str)))
        except ValueError as exc:
            raise CompositingError(f"Could not parse corner token {tok!r} as 'x,y'") from exc
    if len(points) != 4:
        raise CompositingError(
            f"Expected exactly 4 corner points (TL TR BR BL), got {len(points)}. "
            f'Example: --corners "120,340 480,310 470,650 100,690"'
        )
    return points


def _quad_area(quad: list[tuple[float, float]]) -> float:
    area = 0.0
    for i in range(4):
        x1, y1 = quad[i]
        x2, y2 = quad[(i + 1) % 4]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2.0


def _find_perspective_coeffs(dest_quad, src_quad) -> tuple:
    """Coeffs for PIL's Image.transform(..., Image.PERSPECTIVE, coeffs).

    Pillow samples the INPUT image at (a*x+b*y+c)/(g*x+h*y+1),
    (d*x+e*y+f)/(g*x+h*y+1) for each (x, y) pixel of the OUTPUT canvas --
    i.e. the coefficients must map OUTPUT/dest coordinates to INPUT/src
    coordinates, not the other way around.

    dest_quad: 4 (x, y) points in the OUTPUT canvas where the source image's
        corners should land.
    src_quad: 4 (x, y) points in the SOURCE image (its own corners, in the
        same TL/TR/BR/BL order as dest_quad).
    """
    matrix = []
    for (x, y), (u, v) in zip(dest_quad, src_quad):
        matrix.append([x, y, 1, 0, 0, 0, -u * x, -u * y])
        matrix.append([0, 0, 0, x, y, 1, -v * x, -v * y])
    a = np.array(matrix, dtype=np.float64)
    b = np.array(src_quad, dtype=np.float64).reshape(8)
    try:
        coeffs = np.linalg.solve(a, b)
    except np.linalg.LinAlgError as exc:
        raise CompositingError(
            "Could not solve the perspective transform for the given corners "
            "-- they may be collinear or otherwise degenerate."
        ) from exc
    return tuple(coeffs.tolist())


def warp_cover_onto_canvas(
    cover: Image.Image,
    canvas_size: tuple[int, int],
    dest_quad: list[tuple[float, float]],
    min_quad_area: float = DEFAULT_MIN_QUAD_AREA,
) -> Image.Image:
    """Return an RGBA image the size of canvas_size with `cover` warped into
    dest_quad and transparent everywhere else.

    The source cover is forced fully opaque before warping, so the warp's
    own alpha channel becomes exactly the destination quad mask: pixels the
    perspective sampler pulls from outside the cover's own bounds come back
    alpha=0 for free, with no separately-drawn polygon mask needed.
    """
    area = _quad_area(dest_quad)
    if area < min_quad_area:
        raise CompositingError(
            f"Target quad area ({area:.1f}px^2) is smaller than the minimum "
            f"({min_quad_area}px^2) -- looks degenerate or mistyped, refusing to warp."
        )
    w, h = cover.size
    src_quad = [(0, 0), (w, 0), (w, h), (0, h)]
    coeffs = _find_perspective_coeffs(dest_quad, src_quad)

    cover_rgba = cover.convert("RGBA")
    cover_rgba.putalpha(Image.new("L", cover_rgba.size, 255))
    warped = cover_rgba.transform(canvas_size, Image.PERSPECTIVE, coeffs, resample=Image.BICUBIC)
    return warped


def compose(
    scene_path: Path,
    title: str,
    corners: list[tuple[float, float]],
    output_path: Path,
    occlusion_mask_path: Path | None = None,
    registry_path: Path = REGISTRY_PATH,
    manifest_path: Path | None = None,
) -> Path:
    entry = get_cover(title, registry_path)
    ok, reason = verify_cover_file(entry)
    if not ok:
        raise CompositingError(reason)

    if not scene_path.exists():
        raise CompositingError(f"Scene image not found: {scene_path}")

    scene = Image.open(scene_path).convert("RGBA")
    cover = Image.open(entry.local_path)

    warped = warp_cover_onto_canvas(cover, scene.size, corners)
    composited = Image.alpha_composite(scene, warped)

    occlusion_used = False
    if occlusion_mask_path is not None:
        if not occlusion_mask_path.exists():
            raise CompositingError(f"Occlusion mask not found: {occlusion_mask_path}")
        mask = Image.open(occlusion_mask_path).convert("L").resize(scene.size)
        composited = Image.composite(scene, composited, mask)
        occlusion_used = True

    output_path.parent.mkdir(parents=True, exist_ok=True)
    composited.convert("RGB").save(output_path)

    manifest = {
        "tool": "compose_cover.py",
        "tool_version": TOOL_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "title": entry.title,
        "canva_asset_id": entry.canva_asset_id,
        "cover_local_path": str(entry.local_path),
        "cover_sha256": entry.sha256,
        "scene_source": str(scene_path),
        "output": str(output_path),
        "corners": corners,
        "occlusion_mask_used": occlusion_used,
        "occlusion_mask_path": str(occlusion_mask_path) if occlusion_mask_path else None,
        "generative_model_touched_cover_pixels": False,
        "compositing_method": "deterministic_perspective_transform",
    }
    manifest_path = manifest_path or output_path.with_suffix(output_path.suffix + ".manifest.json")
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    return output_path


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--scene", required=True, type=Path)
    parser.add_argument("--title", required=True, help="Approved cover title or registry id")
    parser.add_argument("--corners", required=True, help='"x,y x,y x,y x,y" for TL TR BR BL of the book-cover plane in the scene')
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--occlusion-mask", type=Path, default=None, help="White=keep original scene (e.g. fingers) on top, black=show cover")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--manifest", type=Path, default=None)
    args = parser.parse_args()

    try:
        corners = _parse_corners(args.corners)
        result = compose(
            scene_path=args.scene,
            title=args.title,
            corners=corners,
            output_path=args.output,
            occlusion_mask_path=args.occlusion_mask,
            registry_path=args.registry,
            manifest_path=args.manifest,
        )
    except (CompositingError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

    print(f"Wrote {result}")
    if not args.occlusion_mask:
        print(
            "NOTE: no --occlusion-mask supplied. Per pipeline-control-rules.md "
            "§10, a handheld shot cannot pass QC without verified hand "
            "occlusion -- this composite is only valid for non-handheld "
            "placements (resting/propped/standing).",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
