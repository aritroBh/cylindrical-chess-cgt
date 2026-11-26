# Audit: Black's double-step rank in `crosscheck/minimax.py` (2026-11-25)

Found while writing the rules in Lean (`lean/notes/L1.md`, item D1). Audit by a Sonnet agent; evidence rechecked by the main session.

## Verdict

The bug was real. `crosscheck/minimax.py` took Black's double-step rank to be 7 on every board (move generator and race distance); the right rank is `ranks - 1`. On a 7-rank board with `W a2 / B c6` it gave Black only c6-c5, where `cylcgt` gives c6-c5 and c6-c4 (`step1_movelists.out`).

No published number is wrong, and no "two programs agree" label rests on the faulty program:
- Every use of `minimax.py` for a result builds an 8-rank board, where 7 = 8 - 1 and the bug does nothing. With the fix, the 8-rank comparison output is byte-identical (`rerun_8rank_orig.out`, `rerun_8rank_fixed.out`).
- Every result on a board of another height was checked by other programs (`research/tall_boards/tw.c`, `delegate/out/T80/check.c`, `cylcgt`, the kings solvers), none of which has the bug.
- Had the faulty program been used on those boards it would have contradicted the paper, not confirmed it: on 1,200 random positions with 5, 6, 7 and 9 ranks it disagrees with `cylcgt` on 133; the fixed copy on none (`step4_random_sweep.out`). On eight positions of the paper on other heights the fixed copy agrees on all eight (`step4_named_positions.out`).

## Fixed

`crosscheck/minimax.py`: `7` replaced by `board.ranks - 1` in both places; `crosscheck/test_minimax.py` tests the double step on 5, 6, 7 and 9 ranks (the test fails on the old file).

## Left open

- Supplement, Remark after A.7 ("(E) cannot be dropped"): "a separately written minimax" is `lemmas/common.py`, not `crosscheck/minimax.py`. The sentence should name it.
- The sum-safety census on 4 files by 6 ranks cites a brute-force check by its report only; that program is not in the repository.
- Older copies of the file under `delegate/out/T79/` (ignored) keep the bug; the anonymous code copy is rebuilt from the fixed file.

Lists behind the audit: `users_of_minimax.txt`, `dbl_files.txt`, `start_lines.txt`.
