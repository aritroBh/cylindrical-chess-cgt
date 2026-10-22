# T47: do the reproduce commands still point at real files? (read-only, light)

**Output directory:** `notes/repro_paths_t47/` (write `REPORT.md` there; edit nothing else).

On 2026-10-22 large raw files under `research/` were compressed with zstd (`FILE` became `FILE.zst`; see
`research/*/COMPRESSED.md`), and some logs moved into `research/star2_seven_check/census7/driver_logs/`.

**Task:** go through `RESULTS.md`, `README.md`, `delegate/REVIEW.md` and every `research/*/REPORT*.md` and
`*.sh` reproduce script. For each file path or command they mention, check whether the path exists now
(also as `.zst`). List:
- paths that no longer exist, and whether a `.zst` copy or a moved copy exists (give the new path);
- scripts that read a now-compressed file directly (they need `zstdcat` or a restore first);
- paths that never existed (typos).

Do not run any heavy command; `ls`, `test -e` and reading files are enough. Finish with the list of fixes
someone should make, grouped by file.
