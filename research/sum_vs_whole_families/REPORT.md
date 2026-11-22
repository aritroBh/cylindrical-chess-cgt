# Sum model vs whole board, ring families (cylcgt)

Setting: 8 ranks, race rule "count", e.p. on, e.p.-capturable pawn not passed. "sum" = cylcgt default (splits by capture
components); "whole" = `pawns.components` forced to one component. Every number below is C1 (cylcgt only) unless said.

## Headline

- No disagreement: sum == whole in all 24 (family, n) pairs where both modes finished. C1.
- Three more C9 hit rings (`research/c9_rings/verify_hits/cyl_results.tsv`) also agree, both *2. C1.
- So there is no first n at which the sum model and the whole board differ, on these families, for n <= 11.
- Qo_9 and R_9 are not *3 / *2 (complex value, 4228 and 774 characters); sum and whole give the identical string in both. C1.
- Because nothing disagreed, no diagnosis and no second-route recheck (crosscheck/, sumtest/) was done.

## Pairs where both modes finished (sum == whole)

- odd n = 5, 7, 9, 11: *2.
- even n = 6, 8, 10: *2.
- F n = 7, 8, 9, 10: *2.
- P n = 8, 10: *2.
- Q n = 8, 10: *3.
- Qo n = 11: *3 (Qo_9 complex, equal both ways).
- R n = 11: *2 (R_9 complex, equal both ways).
- N1 n = 9, 10, 11: *2.
- M n = 10: *2.
- O n = 11: *2.

## Largest n reached

- Sum and whole both: odd 11, even 10, F 10, P 10, Q 10, Qo 11, R 11, N1 11, M 10, O 11.
- Sum only (no whole value): odd 13 (*2), even 12 and 14 (*2), F 11 (*2).
- S3 (starts n = 13, 14 pawns) and T3 (starts n = 12, 13 pawns): not run in this session. Not covered.
- M_12, O_13 and N1_12 and up: not run.

## Run notes

- Times and peak RSS are in `table.tsv` (seconds; MB from cylcgt's own maxrss line, or the poller if larger). Nothing reached 3.5 GB; largest is 1317 MB (even 14 sum, 19880 s, from `sum_values.txt`).
- Qo_11 and R_11 sum were started by the queue and stopped by me (SIGTERM on my own PID, after 1154 s and 584 s) because earlier runs show about 5500 s. Their values in the table are the earlier `odd_values.txt` runs (Qo_11 sum 5668 s, whole 4981 s; R_11 sum 5460 s, whole 5019 s), not new runs.
- F_11 whole was cut by my 2.7-hour session deadline at 503 s, not by the 40-minute cap. F_11 sum = *2 (741 s, 824 MB). That pair is incomplete.
- odd_11 whole (*2, 165 s, 91 MB) was run once outside the queue with `/usr/bin/time -l` (95,420,416 bytes).
- No run hit the 40-minute or 3.5 GB cap.
- `table.tsv` also lists "other" rows: a C7 star3 ring (sum only), three C9 hits, and a C11 11-pawn ring (`c4`, not O_11, whole only, complex value, from `npawn_values.txt`). The time columns of the three C9 rows come from an unlabeled column of `cyl_results.tsv`.

## Not done

- Whole mode for odd 13, even 12, even 14 (sum times 1600, 2296, 19880 s). Not attempted.
- S3, T3, and every n >= 12 except the sum-only entries above.
- No second route (crosscheck minimax, sumtest, rg) was run, since sum == whole everywhere. Earlier C2 facts (for example Qo_11 *3, M_10 and O_11 *2) are not re-verified here.
- The `c4` C11 ring (value complex, not *2, whole only) has no sum partner here.

## Files

- `table.tsv`: family, n, ring, pawns, values, times, RSS, sum_eq_whole, sources.
- `runs.tsv`: raw queue output (family, n, mode, pawns, ring, status, value, wall s, polled MB).
- `runq.py` (queue driver), `build_table.py` (builds table.tsv; reads logs, so untar `logs.tar.zst` first), `logs.tar.zst` (tested with `zstd -t`).
