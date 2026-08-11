# Approved cover source files (local cache — not committed)

This directory holds locally verified copies of the approved LiorTales
master book covers, used by `compose_cover.py` for deterministic
compositing. It is **empty in git** — the cover files themselves are
gitignored (see repo-root `.gitignore`).

## Why this directory is empty in the repository

The Canva folder `LiorTales - Approved Book Assets` →
`00_APPROVED_MASTER_COVERS_DO_NOT_MODIFY` (registry:
`shared/product/product-bible.md` §18) is the single source of truth for
cover artwork. Committing binary copies of that art into this git repo
would create a second copy that could silently drift from the source over
time. Instead, each cover is cached here locally on whatever machine runs
the pipeline, and its integrity is enforced by a pinned SHA-256 hash in
`../../covers_registry.json` — not by git history.

## Adding a cover file

1. Obtain the exact approved cover file for a title from the Canva registry
   above, and save it here using the filename already listed for that
   title in `../../covers_registry.json` (`local_path`).
2. Visually confirm it matches the registered title, character artwork,
   colors, and logo before pinning — pinning trusts whatever file is
   currently at that path, so this check is the only human gate.
3. From this tool's directory, run:
   `python3 covers_registry.py pin "<Title>"`
4. `compose_cover.py` refuses to run against a title until this is done,
   and refuses again if the file ever changes without being re-pinned
   (`python3 covers_registry.py check "<Title>"` reports the current status).

No cover file has been placed or pinned as part of building this pipeline —
that step is intentionally left for a human to perform, deliberately, once
real asset access is being exercised. The four approved cover assets
themselves were not touched, copied, or downloaded while building this tool.
