# K6: when does spare tempo matter in K+P vs K? A test of K4's odd-width conjecture

Who did what:
- a Sonnet 5.5 agent ran a copy of the K4 pipeline (built by Sonnet) on 17 new boards;
- a second Sonnet agent re-ran them with K4's independent verifier-B pipeline, which has its own move generator,
  its own test games and its own C solver (workflow `wf_bb881d4e-55f`);
- this report was written by the orchestrating session from both agents' numbers.

The convention is the same as K4's ([../K4/REPORT.md](../K4/REPORT.md) §1): normal play in the sum, so stalemate
loses, and infinite play draws.

A quiet placement is **tempo-sensitive** if its result (White starts, Black starts) changes either against the
11 finite test games or in x ⊞ n for some n = −10 … 10.

## Summary

1. **CHECKED-2.** All 17 new boards were reproduced by the independent pipeline with 0 differences. That covers
   209,486 placements, 6.7 M signature entries, 56,803 difference tests and 2,943,507 kpsolve positions.
2. **The odd-width observation holds (CHECKED-2).** All 8 odd-width cylinders computed are tempo-insensitive:
   widths 3, 5 and 7, with 4 to 6 ranks (80,574 placements).
3. **Odd width is not the cause.** The 6- and 8-file cylinders are insensitive too (5 boards, 74,912 placements).
   The only sensitive cylinders have exactly 4 files. K4's "triangulation around an odd seam" explanation is
   therefore unsupported. It is withdrawn as an odd-width effect.
4. **Every flat board is sensitive.** For width ≥ 4 the count depends only on the ranks: 22, 86 and 174
   placements on 4, 5 and 6 ranks. The deepest threshold also deepens with the ranks: n = −1, −2 and −3.
5. **CONJECTURE (from the data; tested further by K8, [../K8/REPORT.md](../K8/REPORT.md)).** K8 confirmed all 8
   new predictions. It also found that the effect belongs to normal play, where stalemate loses: under the
   chess stalemate rule the 5-, 6- and 7-file cylinders are sensitive, and only Black's stalemate rule matters. Across all 27 boards (K4 and K6), a board has tempo-sensitive placements
   exactly when White can be stalemated in front of its own pawn, that is, when the off/off+\* class exists.
   - That happens on flat boards, in a corner.
   - It happens on 4-file cylinders, where one Black king two files away covers both of the White king's
     neighbours across the seam.
   - It does not happen on 3-file or 5-to-8-file cylinders.

## Cylinders (K4 and K6, number of tempo-sensitive placements)

| files | 4 ranks | 5 ranks | 6 ranks |
|---|---:|---:|---:|
| 3 | 0 (K4) | 0 (K4) | 0 |
| 4 | 24 (K4) | 68 (K4) | 144 |
| 5 | — | 0 (K4) | 0 |
| 6 | 0 | 0 | 0 |
| 7 | 0 | 0 | 0 |
| 8 | 0 | 0 | — |

K6 boards are CHECKED-2 by verifier B. K4 boards were checked by K4's two verifiers.

## Flat boards (number of tempo-sensitive placements, and the thresholds that occur)

| files | 4 ranks | 5 ranks | 6 ranks |
|---|---|---|---|
| 3 | 10; n ∈ {−1, 0} (K4) | 38; {−2, −1, 0} (K4) | 76; {−3, −2, −1, 0} |
| 4 | 22; {−1, 0} (K4) | 86; {−2, −1, 0} (K4) | — |
| 5 | — | 86; {−2, −1, 0} (K4) | 174; {−3, −2, −1, 0} |
| 6 | 22; {−1, 0} | 86; {−2, −1, 0} | — |
| 7 | 22; {−1, 0} | 86; {−2, −1, 0} | — |

The 4-file cylinders have thresholds {−1, 0} on 4 ranks, {−2, −1, 0} on 5 and {−3, −2, −1, 0} on 6.

## Further facts

- **Thresholds.** Every result change is between a draw and a White win, and every threshold lies in
  n ∈ {−3, …, 0}. No threshold occurs at n ≥ 1 or n ≤ −4.
- **Classes.** Every sensitive placement is in K4's "unmatched, T-dependent" class.
- **Examples:**
  - flat 6×4 and 7×4, `Ka3 Pa2 kc3`: DD for n ≤ −1, DW at n = 0, WW for n ≥ 1;
  - cyl 4×6, `Ka3 Pa2 kc3`: DD for n ≤ −3, DW at n = −2, WW for n ≥ −1;
  - every sensitive placement, per board, is listed in `tempo_detail_<board>.json`.
- **The off class.** off/off+\* is exactly "White to move has no legal move and is not in check". It has 4
  placements on each flat board, 8 on cyl 4×6, and none on the other cylinders.
- **Verifier's side observation on cyl 4×6.** In the 144 sensitive placements the two kings are never one file
  apart: 116 have them two files apart (opposite each other on 4 files), and 28 on the same file.
- **Matched classes.** Classes, signatures and the candidates matched are as in K4. No class appears beyond
  WHITE-WINS-ALL, on/on+\*, off/off+\*, dud and the two unmatched classes. The per-board class counts are in
  `summary.json`.
- **Rule 7.** Every board took at most 68 s and 386 MB (builder), or 242 s and 455 MB (verifier). One process
  ran at a time, under nice.

## What is and is not shown

- **Not computed:**
  - widths above 8 (outside SPEC);
  - more than 6 ranks;
  - cyl 5×4, cyl 8×6 and flat 4×6;
  - width-4 cylinders with 7 or 8 ranks, which the conjecture predicts are sensitive.
- **The stalemate mechanism is a CONJECTURE.** Under normal play, stalemate is a loss, which plausibly lets
  Black win tempo battles that run White out of moves. That is consistent with the data but not proved.
  - Whether the same pattern survives the chess convention, where stalemate is a draw, was not tested.
- **The negative controls only partly cover the insensitive boards.** Corrupting a finite test game made no
  difference on cyl 3×6, because every placement there gives the same answer. So "insensitive" rests on the
  test games being right. Three things support that:
  - the bisimulation check of all test games;
  - the CGT fact table;
  - the same pipeline finding sensitivity on flat and 4-file boards.
- **Partial independence.** The verifier reused K4's verifier-B code unchanged, and both pipelines compare
  against the same kpsolve.

## Reproduce

From the project root:

    nice -n 10 cc -O2 -o kings/delegate/out/K6/kp kings/kpsolve.c
    PYTHONPATH=. nohup sh kings/delegate/out/K6/run_all.sh cyl:6x4 cyl:7x4 cyl:8x4 cyl:3x6 cyl:6x5 cyl:7x5 cyl:8x5 cyl:4x6 cyl:5x6 flat:6x4 flat:7x4 flat:6x5 flat:7x5 flat:3x6 flat:5x6 cyl:7x6 cyl:6x6 &

The run takes about 12 minutes. The independent check is
`sh kings/delegate/out/K6/verify/run_verify6.sh`, then `sh kings/delegate/out/K6/verify/run_extra6.sh`.

The per-placement `.jsonl` files and the kpsolve logs in `check1/` are kept locally, not in git, as
`bulk_regenerable.tar.zst` (14 MB). Unpack it with
`zstd -dc kings/delegate/out/K6/bulk_regenerable.tar.zst | tar -xf - -C kings/delegate/out/K6`.
The verifier's 304 MB of intermediates (`verify/work/`) were deleted; `run_verify6.sh` regenerates them.
