# Compressed raw files

On 2026-10-22 the large raw files in this directory (scanner TSVs, kpsolve `.in`/`.out`) were compressed with zstd
to free disk space; each archive was tested (`zstd -t`) before its original was removed. Read one with
`zstdcat FILE.zst | head`, or restore it with `zstd -d FILE.zst`. Scripts that read the raw files need the
originals restored first, or `zstdcat` in place of `cat`.
