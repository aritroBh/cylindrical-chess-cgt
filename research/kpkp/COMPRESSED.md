# Compressed raw files

On 2026-10-22 the large raw files in this directory (scanner TSVs, kpsolve `.in`/`.out`) were compressed with zstd
to free disk space; each archive was tested (`zstd -t`) before its original was removed. Read one with
`zstdcat FILE.zst | head`, or restore it with `zstd -d FILE.zst`. Scripts that read the raw files need the
originals restored first, or `zstdcat` in place of `cat`.

**Warning (2026-10-22, T44):** the old `kpkp_*.in/.out.zst` and `kppk_*.zst` files are NOT KPKP/KPPK. `enumerate.c` wrote the
black pawn as `P`, so they hold K+2P v K and K+3P v K. Do not use them. The correct KPKP tables are in `t44/`.
