#!/usr/bin/env python3
"""Product Fidelity Check -- confirm a finished composite's cover region
still matches the registered approved source asset, not model-generated or
hand-edited artwork.

Re-derives the exact warped-cover pixels from the manifest's recorded
corners and the registry's currently-pinned cover file, then compares that
region of the actual composited output against it. Construction-time
fidelity is already guaranteed by compose_cover.py refusing to run against
an unpinned or hash-mismatched cover in the first place; this script is a
regression/tamper check for *after* compositing -- e.g. confirming nobody
re-edited the exported file, or that the registry's pinned file hasn't
changed since this composite was produced.

Usage:
    python3 verify_composite.py --composite composited.png
    (looks for composited.png.manifest.json by default)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from covers_registry import REGISTRY_PATH, get_cover, verify_cover_file
from compose_cover import warp_cover_onto_canvas

DEFAULT_MAX_MEAN_DIFF = 6.0  # out of 255, per channel, within the (non-occluded) cover region


def verify(
    composite_path: Path,
    manifest_path: Path,
    registry_path: Path = REGISTRY_PATH,
    max_mean_diff: float = DEFAULT_MAX_MEAN_DIFF,
) -> tuple[bool, str]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    if manifest.get("compositing_method") != "deterministic_perspective_transform":
        return False, (
            "NOT_DETERMINISTIC: manifest does not record the required "
            "deterministic_perspective_transform compositing method -- "
            "cannot treat this asset as fidelity-verified."
        )
    if manifest.get("generative_model_touched_cover_pixels") is not False:
        return False, (
            "GENERATIVE_TOUCH_UNCONFIRMED: manifest does not explicitly "
            "record that no generative model touched the cover pixels."
        )

    entry = get_cover(manifest["title"], registry_path)
    ok, reason = verify_cover_file(entry)
    if not ok:
        return False, f"REGISTRY_CHECK_FAILED: {reason}"

    if entry.sha256 != manifest.get("cover_sha256"):
        return False, (
            "HASH_DRIFT: the registry's currently-pinned hash no longer "
            "matches the hash recorded in this composite's manifest at "
            "generation time -- the cover file was re-pinned since this "
            "image was made. Re-generate the composite before trusting it."
        )

    if not composite_path.exists():
        return False, f"COMPOSITE_MISSING: {composite_path} does not exist."

    composite = Image.open(composite_path).convert("RGBA")
    cover = Image.open(entry.local_path)
    expected_warp = warp_cover_onto_canvas(cover, composite.size, manifest["corners"])

    expected_arr = np.array(expected_warp)
    actual_arr = np.array(composite)

    alpha = expected_arr[:, :, 3].astype(np.float64) / 255.0
    if manifest.get("occlusion_mask_used") and manifest.get("occlusion_mask_path"):
        mask_path = Path(manifest["occlusion_mask_path"])
        if mask_path.exists():
            occl = np.array(Image.open(mask_path).convert("L").resize(composite.size)).astype(np.float64) / 255.0
            alpha = alpha * (1.0 - occl)  # occluded pixels are SUPPOSED to differ -- exclude them

    weight = alpha[:, :, None]
    if weight.sum() < 1.0:
        return False, "EMPTY_REGION: quad/occlusion left no comparable cover pixels -- cannot verify."

    diff = np.abs(expected_arr[:, :, :3].astype(np.float64) - actual_arr[:, :, :3].astype(np.float64))
    weighted_mean_diff = float((diff * weight).sum() / (weight.sum() * 3))

    if weighted_mean_diff > max_mean_diff:
        return False, (
            f"PRODUCT_FIDELITY_FAIL: mean pixel difference in the cover "
            f"region is {weighted_mean_diff:.2f} (threshold {max_mean_diff}). "
            f"The visible cover does not match a deterministic warp of the "
            f"registered source asset -- possible re-edit, generative "
            f"touch-up, or wrong manifest/corners."
        )

    return True, f"PASS: mean pixel difference {weighted_mean_diff:.2f} (threshold {max_mean_diff})"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--composite", required=True, type=Path)
    parser.add_argument("--manifest", type=Path, default=None, help="Defaults to <composite>.manifest.json")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--max-mean-diff", type=float, default=DEFAULT_MAX_MEAN_DIFF)
    args = parser.parse_args()

    manifest_path = args.manifest or args.composite.with_suffix(args.composite.suffix + ".manifest.json")
    if not manifest_path.exists():
        print(f"ERROR: manifest not found at {manifest_path}", file=sys.stderr)
        sys.exit(2)

    ok, message = verify(args.composite, manifest_path, args.registry, args.max_mean_diff)
    print(message)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
