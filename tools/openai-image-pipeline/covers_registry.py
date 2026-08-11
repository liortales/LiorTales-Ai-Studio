#!/usr/bin/env python3
"""Registry of LiorTales approved master book covers.

Source of truth for which titles exist: shared/product/product-bible.md §18
in the repo root. This module never edits that document -- it only reads a
local JSON mirror (covers_registry.json) that a human keeps in sync with it.

A cover entry only becomes usable by compose_cover.py once it has been
"pinned": a human has placed a verified local copy of the approved cover
file at `local_path` and run `covers_registry.py pin <title>`, which records
its SHA-256 hash here. Nothing in this pipeline will use, warp, or composite
a cover file whose hash isn't pinned and matching -- that is the guard
against silently compositing a stale, corrupted, or wrong file in place of
the real approved artwork.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

REGISTRY_PATH = Path(__file__).parent / "covers_registry.json"


class CoverNotFoundError(Exception):
    pass


@dataclass
class CoverEntry:
    id: str
    title: str
    canva_asset_id: str
    local_path: Path
    sha256: Optional[str]
    pinned_at: Optional[str]
    registry_path: Path


def _load_raw(registry_path: Path) -> dict:
    if not registry_path.exists():
        raise FileNotFoundError(f"Registry file not found: {registry_path}")
    with registry_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def list_covers(registry_path: Path = REGISTRY_PATH) -> list[CoverEntry]:
    data = _load_raw(registry_path)
    base_dir = registry_path.parent
    return [
        CoverEntry(
            id=c["id"],
            title=c["title"],
            canva_asset_id=c["canva_asset_id"],
            local_path=(base_dir / c["local_path"]).resolve(),
            sha256=c.get("sha256"),
            pinned_at=c.get("pinned_at"),
            registry_path=registry_path,
        )
        for c in data["covers"]
    ]


def get_cover(title_or_id: str, registry_path: Path = REGISTRY_PATH) -> CoverEntry:
    needle = title_or_id.strip().lower()
    for entry in list_covers(registry_path):
        if entry.id == title_or_id or entry.title.strip().lower() == needle:
            return entry
    raise CoverNotFoundError(
        f"No approved cover registered under title/id {title_or_id!r}. "
        f"Approved titles live in shared/product/product-bible.md §18 -- "
        f"add it there first, then to {registry_path.name}, before use."
    )


def _sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_cover_file(entry: CoverEntry) -> tuple[bool, str]:
    """Return (ok, reason). ok=False means the compositor MUST refuse to run."""
    if not entry.local_path.exists():
        return False, (
            f"PRODUCT_ASSET_MISSING: {entry.local_path} does not exist. "
            f"Place the verified approved cover file for '{entry.title}' "
            f"there, then run: python3 covers_registry.py pin \"{entry.title}\""
        )
    if not entry.sha256:
        return False, (
            f"NOT_PINNED: {entry.local_path} exists but has not been pinned. "
            f"Verify it is the exact approved cover for '{entry.title}' "
            f"(Canva asset {entry.canva_asset_id}), then run: "
            f"python3 covers_registry.py pin \"{entry.title}\""
        )
    actual = _sha256_of(entry.local_path)
    if actual != entry.sha256:
        return False, (
            f"PRODUCT_FIDELITY_FAIL: {entry.local_path} does not match its "
            f"pinned hash. The file changed since it was verified -- possible "
            f"corruption, wrong file, or unauthorized edit. Expected "
            f"{entry.sha256}, got {actual}. Do not composite; re-verify "
            f"against Canva asset {entry.canva_asset_id} before re-pinning."
        )
    return True, "OK"


def pin_cover(title_or_id: str, registry_path: Path = REGISTRY_PATH) -> str:
    """Compute and store the SHA-256 of the currently-present local file.

    This is a deliberate, explicit action -- never done automatically by the
    compositor -- so that pinning a wrong or stale file always requires a
    human to type the command and look at the title/asset id it names.
    """
    entry = get_cover(title_or_id, registry_path)
    if not entry.local_path.exists():
        raise FileNotFoundError(
            f"Cannot pin '{entry.title}': {entry.local_path} does not exist. "
            f"Place the verified file there first."
        )
    digest = _sha256_of(entry.local_path)
    data = _load_raw(registry_path)
    for c in data["covers"]:
        if c["id"] == entry.id:
            c["sha256"] = digest
            c["pinned_at"] = datetime.now(timezone.utc).isoformat()
    with registry_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")
    return digest


def _cmd_list(args):
    for entry in list_covers(args.registry):
        status = "PINNED" if entry.sha256 else "NOT PINNED"
        exists = "file present" if entry.local_path.exists() else "file MISSING"
        print(f"[{entry.id}] {entry.title} ({entry.canva_asset_id}) - {status}, {exists}")


def _cmd_check(args):
    entry = get_cover(args.title, args.registry)
    ok, reason = verify_cover_file(entry)
    print(reason if not ok else f"OK: {entry.title} verified against pinned hash {entry.sha256}")
    sys.exit(0 if ok else 1)


def _cmd_pin(args):
    digest = pin_cover(args.title, args.registry)
    print(f"Pinned {args.title!r} -> sha256 {digest}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="List all registered covers and their pin status")
    p_list.set_defaults(func=_cmd_list)

    p_check = sub.add_parser("check", help="Verify a cover's local file against its pinned hash")
    p_check.add_argument("title", help="Cover title or registry id")
    p_check.set_defaults(func=_cmd_check)

    p_pin = sub.add_parser("pin", help="Pin the current local file's hash for a cover")
    p_pin.add_argument("title", help="Cover title or registry id")
    p_pin.set_defaults(func=_cmd_pin)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
