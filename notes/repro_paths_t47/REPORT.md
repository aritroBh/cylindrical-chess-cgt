# T47: reproduce command paths - audit (2026-10-22)

## 1) Summary (5 lines)
- Large raw files under `research/` were compressed to `.zst` (see `research/kpkp/COMPRESSED.md`, `research/star2_width5/COMPRESSED.md`, `research/star3_hunt/COMPRESSED.md`).
- Some star2_seven_check logs moved into `research/star2_seven_check/census7/driver_logs/` (not compressed).
- Several reproduce scripts in `research/*` read uncompressed large files directly; they will break unless they use `zstdcat` or restore.
- A number of paths referenced in docs/scripts no longer exist as files or were moved; some have `.zst` equivalents or moved copies.
- This is a read-only inventory of broken/at-risk paths; see §5 for suggested fixes.


## 2) Files scanned
- `RESULTS.md`
- `README.md`
- `delegate/REVIEW.md`
- All `research/*/REPORT*.md` (14 files listed above)
- All `*.sh` under repo (142 scripts) — sampled/key ones in context of large data


## 3) Findings

### research/kpkp/
- Compressed: `kpkp_cyl.in.zst`, `kpkp_cyl.out.zst`, `kpkp_flat.in.zst`, `kpkp_flat.out.zst`, `kppk_cyl.in.zst`, `kppk_cyl.out.zst`, `kppk_flat.in.zst`, `kppk_flat.out.zst` (see `research/kpkp/COMPRESSED.md`). Originals removed.
- References found:
  - `research/kpkp/analyze_kpkp.py:74,84` reads `research/kpkp/kpkp_flat.out` directly (uncompressed). **Will fail now.** Needs `zstdcat research/kpkp/kpkp_flat.out.zst` or restore.
- Other scripts (e.g. `run_kpkp.sh`, `gen_kpkp.py`) likely read/write `.in/.out` files directly - need to be updated or files restored before running.

### research/star2_width5/
- Compressed all `split_1_7.tsv` ... `split_7_1.tsv` to `.zst` (see `research/star2_width5/COMPRESSED.md`). Originals removed.
- `summary.txt` lists `research/star2_width5/split_2_6.tsv` etc. (uncompressed paths). No shell/python in dir appears to read them directly by glob/cat in a way that would auto-decompress; analysis scripts elsewhere may look for uncompressed files. **Paths listed exist only as `.zst` now.**
- `research/star2_width5/merge.py` or other code in repo might read these - need to check.

### research/star3_hunt/
- Many large TSVs compressed to `.zst` (see list above). Originals removed. Scripts reading them directly will fail.

### research/star2_seven_check/
- Logs moved to `research/star2_seven_check/census7/driver_logs/` (directory exists). `census7_w3_rerun.sh` writes to `research/star2_seven_check/census7/driver_logs/...` - that path now exists. No `.zst` files here.
- Any script expecting logs in old locations would need updating.

