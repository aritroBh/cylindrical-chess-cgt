# K48 referee report (final)

Everything is in `verify/`: scripts, logs and `pids.log`.
- The solvers were built fresh and run only through `kings/delegate/heavy.sh`.
- All referee processes have ended. The binaries are deleted.
- No single output is over 256 KB (`verify/logs` totals 1.1 MB), so nothing needed compressing.

**Verdict: apply `verify/EDITS.md`, not the investigator's set.**

## Claim 1 (chess, cyl:8x6, cap 1): CONFIRMED

**How the bound pairs are read.**
- In kpsolve, kp39 and own39, bound A scores a promotion past the cap as a White win. That makes A an upper bound for White.
- Bound B scores it as a Black win, so B is a lower bound.
- The pair is printed as (A, B). A value is exact when A = B, so "exactly W" needs B = W.
- The investigator reads the pairs this way. The capture refinement in kp39 and own39 is sound for the side the bound favours (K39).

**The investigator's raw logs.** My parser `verify/scripts/p1_check.py` finds:
- 49 move values, of which 28 are exact: 27 lose, and e2-e4 at the d4 root wins.
- 9 values at (D, L) and 12 at (W, L).
- kp39 --refine and own39 differ in 0 places.
- Plain kpsolve differs from them in 12 places, and is always the weaker bound there.

**Fresh runs** (`verify/logs/own39_*`, `kpsolve_d4q.*`) on the d4 root (White to move) and on q = `Kf5 kd4 Pb2 Pb4 Pe4 pa4 pb5 pe5` with each side to move:

| Position | own39 A (refined) | own39 B (refined) | kpsolve (A, B) |
|---|---|---|---|
| d4 root, White to move | W | W | (W, W) |
| e2-e4 from that root | W | W | (W, W) |
| other root moves | — | all L | — |
| q, Black to move | W, all 4 moves W | W, all 4 moves W | (W, W), all 4 moves W |
| q, White to move | L, all 6 moves L | L, all 6 moves L | (L, L), all 6 moves L |

So the root is exactly W and e2-e4 wins exactly. In q both bounds agree with either side to move, in two independent code families. A promotion past the cap therefore cannot change the value, and "exact zero in chess" is justified.

**Not repeated:** the other roots and the d5 positions. They come from the investigator's logs only, which I parsed.

## Claim 2 (flat boards): CONFIRMED (counts from the logs; every named group with my own checker)

**Counts.** `verify/scripts/cmp_logs.py` reads the raw A (p45a) and R (r48) outputs, not `flat_table.txt`.
- On all 32 classes, A's under counters equal its over counters, and both equal R's counters, all six of them. The hit sets agree. A and R print in different formats, so I compared counter lines and hit lists, not raw lines.
- Totals per orientation:
  - flat 8x6: 2,515,002,479 placements, 3 exact;
  - flat 9x6: 891,994,478 placements, 4 exact;
  - flat 10x6: 1,454,473,915 placements, 5 exact;
  - cyl:8x7: 873,305,946 placements, 4 exact.
- The class lists are complete: 20 classes on 8x6, and the 5 and 6 classes of the group's shape on 9x6 and 10x6.

**My own checker.** `verify/scripts/def48.py` is written from Definition 4.8 and reads only `--moves` values. It found:
- flat 8x6: Z_O, its translates onto b, c, f and c, d, g, the reflected form `Ka5 kc4 ...`, and the left-right reflection of Z_O all PASS. So do the three under mirrors. Both ref3m and kp_p pass every one.
- flat 9x6: the 4 translates PASS with both ref3m and kp_p.
- flat 10x6: the 5 translates PASS with kp_p (no ref3m on 10-file boards).

My checker first read the letter b in a file name as a bishop, so it rejected two groups whose freeze is a b-pawn move. I fixed it (`def48.py` line 92). The re-runs PASS in `logs/groups_ref3m_rerun.txt`, and the kp_p pass already used the fixed script.

**Problem in the edits:** "exactly 3" counts one group per left-right reflection class. On a flat board each reflection is a different exact group (I checked the reflection of Z_O), so there are 6 in all.

## Claim 3 (cyl:8x7, files a, b, e): CONFIRMED
- The A and R counters and the 4 hits agree (see above).
- My checker passes all 4 groups with ref3m and kp_p.
- Z_O fails on cyl:8x7, with both solvers:
  - (O1): Kd4-c4 and e5-e4 at d4, and Kd5-c4 and e5-e4 at d5, do not lose;
  - (O2): the d5 root has no freeze.

## Claim 4 (not-done items stated where they limit a claim): MOSTLY CONFIRMED
The edits state these limits: cap 2 not completed, the other 9x6 and 10x6 classes not searched, cyl:8x8 not searched.

Two limits are missing from the edits: chess on flat boards was not run, and the other file classes of cyl:8x7 were not searched. A third item, the cached r48 binary not being re-validated against ref3m, is covered by the A = R agreement and by my group checks.

## Edits
The investigator's `EDITS.md` applies cleanly (4 applied, 0 rejected, cell counts unchanged, bold markers balanced). It still needs three changes:
1. Add "up to left-right reflection" to the flat 8x6 count, in three places.
2. Add "of Definition 4.8" wherever the new groups are called over groups, and say their values in sums were not computed (the K47 rule).
3. Add the two missing scope notes.

**Apply `verify/EDITS.md`.** It uses the same anchors and makes these changes. Every phrase in it is backed by the finished checks above. Applied to the current `LOOPY.md`: 4 applied, 0 rejected, table cell counts unchanged, `**` count 958 before and after. The scratch copy is deleted.

## Peak memory
- kpsolve (cap 1, cyl:8x6): 3.02e9 bytes = 2.81 GiB, at the 3 GB limit. The investigator saw 1.9 GB on the same run; future runs need care.
- own39: 0.95 GB.
- ref3m and kp_p: at most 55 MB.
