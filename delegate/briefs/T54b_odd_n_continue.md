# T54b: finish the C9 core-plus-wall search (continuation of your T54)

Output directory: `research/odd_n_plus_2/` (yours from T54). Write nothing anywhere else.

You started T54 (brief: `delegate/briefs/T54_odd_n_plus_2.md`) and hit the Codex usage limit before writing
`REPORT.md`. What exists:
- `enumerate.c`;
- `search.py`;
- an unchanged copy of `rg`;
- one finished slice: C9, core width 4, wall offset 2, white rank 2, phase 0. It has 208,633 rings, 0 \*2, 0 \*3
  (`summary_c9_w4_d2_r2_p0.json`).
- The phase-1 run of that slice died at 78,000 rings.

The orchestrator also started a validation run on C8 (`search.py 8 6 2 2 0`). Its log is
`/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/val_c8_w6_p0.log`
(read it if it exists).

## What to do

1. **Validate first.** The search must find the C8 ten-pawn \*2 rings that have a W2/B4 wall. For example
   `W5 B7 W4 W4B7 B6 W3B6 W2 B4` (core width 6, wall offset 2, white rank 2) is \*2. Check that your enumerator emits
   it, up to symmetry, and that the driver records it as NNPN. If the C8 validation run found 0 hits, find the bug.
   Cross-check against the known list `research/star26_rings/c8/p10_5_5_hits.tsv`.
2. Run the remaining C9 slices:
   - core widths 4–7;
   - wall offset 2, then offsets 1 and 3;
   - white ranks 2–5;
   - both phases.

   Run the most promising slices first: width 6 with offset 2 and rank 2 is the analogue of the even family. Use at
   most 2 processes.
3. For every \*2 or \*3 found, run the same ring with the wall extended by two files on C11.
4. Write `REPORT.md`:
   - a 5-line summary;
   - exact counts per slice;
   - every hit;
   - the validation result;
   - the commands to reproduce;
   - COMPUTED-1 or CHECKED-2 labels. Confirm any hit with cylcgt whole-board.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. The machine is shared and heavily loaded.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS.
- No git. No file over 50 MB.
