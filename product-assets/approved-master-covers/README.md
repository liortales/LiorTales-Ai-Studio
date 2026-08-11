# Approved Master Book Covers — versioned, immutable, committed

This folder holds the actual, versioned copies of LiorTales' approved
master book cover files. Mirrors the Canva folder
`LiorTales - Approved Book Assets` → `00_APPROVED_MASTER_COVERS_DO_NOT_MODIFY`
(registry: `shared/product/product-bible.md` §18).

## Why these files are committed to this private repository

Production tooling (`tools/openai-image-pipeline/`) runs in ephemeral
cloud containers that only contain whatever this repo's git history
provides — nothing outside git persists between sessions. These cover
files are not secrets and are not derived/regenerable content; they are
LiorTales' own product IP and the literal, load-bearing input the
deterministic compositor needs to run at all. Excluding them from git (an
earlier design in this repo) meant every fresh container was missing the
one thing the whole pipeline exists to protect. They are committed here
instead, so any clone of this repo has what it needs.

## Integrity, not just presence

Committing the file doesn't replace verification — `tools/openai-image-pipeline/covers_registry.json`
still pins each file's SHA-256 hash, and `compose_cover.py` refuses to run
against a file that doesn't match its pin. That guards against silent
corruption or an accidental future edit to a committed file, the same way
it always guarded against a bad local cache.

## Current contents

| Title | File | Canva Asset ID | Pinned |
|---|---|---|---|
| Olivia and the Enchanted Bunny | `olivia-and-the-enchanted-bunny.png` | `MAHR7kjIXWA` | Yes |
| Mia and the Missing Star | `mia-and-the-missing-star.png` | `MAHR7spCO30` | Not yet added |
| Adam, Lev & Olivia: Monsters from the Stars | `adam-lev-and-olivia-monsters-from-the-stars.png` | `MAHR7hILHjs` | Not yet added |
| Rostislav: The Glitch in the Green Forest | `rostislav-the-glitch-in-the-green-forest.png` | `MAHR7hdvibw` | Not yet added |

Only Olivia's file exists in this folder today. The other three are listed
in `covers_registry.json` with a `local_path` already pointing here, but no
file has been added or pinned for them yet.

## Adding another cover

1. Obtain the exact approved cover file for a title — from Canva, or from
   whoever holds a verified original — and place it here using the
   filename already listed in `../../tools/openai-image-pipeline/covers_registry.json`
   (`local_path`).
2. Visually confirm it matches the registered title, character artwork,
   colors, and logo before pinning — pinning trusts whatever file is at
   that path, so this check is the human gate.
3. From `tools/openai-image-pipeline/`, run:
   `python3 covers_registry.py pin "<Title>"`
4. Commit the new file and the updated `covers_registry.json` together.

## Hard rule

**Never modify, resize, recompress, or re-export a file in this folder
once pinned.** If a cover needs to change, that's a new approved master
from Daryna — update it here deliberately, in its own commit, and re-pin;
never edit it silently as a side effect of an unrelated change.
