# Möbius and Klein tablebase repair (job 1)

All numbers below come from the raw logs in `logs/`. Originals under `research/mobius/` and `research/twisted_tablebases/` were not touched.

## a. What is affected

Two programs have the overflow: `research/mobius/mobius_replica.c` (T9, 4-man tablebases) and `research/mobius/kpsolve_mob.c` (KPK). Both declare `rayL` and `rayBefore` as `[64][8][8]`. A Möbius or Klein horizontal ray has up to 15 squares, so entries 8 to 14 are written and read past the end of the row.

Not affected: the two programs behind the paper's sentence. `research/twisted_tablebases/A/replica.c` declares `rayL[64][8][64]` and `rayBefore[64][8][64]`. `research/twisted_tablebases/B/twist.c` uses `rays[64][8][64]`. Under `-fsanitize=address,undefined` both ran KRK on Möbius and Klein with no report (`logs/asan_A_*`, `logs/asan_B_*`).

Published numbers that depend on the bug:
- `research/mobius/REPORT.md` Part A tables (Möbius and Klein legal counts, the Klein KRK 0.79%, Möbius KRBK max DTM 9, Klein KBK/KBNK max DTM). These are corrupted.
- The "no pawns" parts of T9 only. The KPK numbers (78.94%) use `kpsolve_mob.c`. A fixed copy gives a byte-identical output file (`cmp` says identical, `logs/kpk_mob8x8_results_fixed.txt`), so KPK is unchanged.

Numbers that do not depend on it: the paper's Möbius/Klein KRK sentence (it quotes A and B, not T9).

## b. Repair

Copies: `fixed_replica.c` (RAYMAX 16 for `rayL` and `rayBefore`, abort on `k >= RAYMAX`), `fixed_kpsolve_mob.c` (same), `orig_replica.c` (unchanged copy). The assertion never fired on mobius or klein, so 16 is enough.

ASAN/UBSAN, KRK on Möbius (`logs/asan_*_mobius_R.log`, `asan_*_klein_R.log`):
- `orig_replica.c`: runtime errors at lines 102, 104, 119 and 260 (index 8 and index 14 out of bounds). Klein has 2 reports. The original does overflow.
- `fixed_replica.c`: no report on either board.

I ran every material (Q R B N QR RR QQ BB NN BN RB) on both boards with the original and the fixed build.

## c. Old against repaired (White to move; flags L=legal count changed, W=won count changed, D=max DTM changed)

```
board  endgame  old_legal old_won% old_dtm | new_legal new_won% new_dtm | changed(legal/win%/dtm)
mobius KQK                99013  100.0000   5 |      98956  100.0000   5 | LW-
mobius KRK               148171  100.0000  12 |     147776  100.0000  12 | LW-
mobius KBK               158580  100.0000  21 |     158852  100.0000  21 | LW-
mobius KNK               198560    0.0000   0 |     198560    0.0000   0 | ---
mobius KQRK              4106675  100.0000   3 |    4103984  100.0000   3 | LW-
mobius KRRK              6010104  100.0000   4 |    5974912  100.0000   4 | LW-
mobius KQQK              2688412  100.0000   2 |    2683320  100.0000   2 | LW-
mobius KBBK              6981116  100.0000   7 |    7005328  100.0000   7 | LW-
mobius KBBK(opp-col)     3553780  100.0000   6 |    3566776  100.0000   6 | LW-
mobius KBBK(same-col)    3427336  100.0000   7 |    3438552  100.0000   7 | LW-
mobius KNNK             10861312    0.0077   1 |   10861312    0.0077   1 | ---
mobius KBNK              8852656  100.0000  20 |    8883740  100.0000  20 | LW-
mobius KRBK              6687157  100.0000   9 |    6694356  100.0000   7 | LWD
klein  KQK                52376  100.0000   2 |      54424  100.0000   2 | LW-
klein  KRK               145746    0.7945   1 |     145344    0.6605   1 | LW-
klein  KBK                93113  100.0000   6 |      95856  100.0000   7 | LWD
klein  KNK               190592    0.0000   0 |     190592    0.0000   0 | ---
klein  KQRK              2222942  100.0000   2 |    2407440  100.0000   2 | LW-
klein  KRRK              5893330  100.0000   4 |    5856768  100.0000   4 | LW-
klein  KQQK               760100  100.0000   1 |     800960  100.0000   1 | LW-
klein  KBBK              2427088  100.0000   2 |    2538784  100.0000   2 | LW-
klein  KBBK(opp-col)     1106070  100.0000   2 |    1192736  100.0000   2 | LW-
klein  KBBK(same-col)    1321018  100.0000   2 |    1346048  100.0000   2 | LW-
klein  KNNK             10129536    0.0000   0 |   10129536    0.0000   0 | ---
klein  KBNK              5152366  100.0000   5 |    5459136  100.0000   6 | LWD
klein  KRBK              3985692  100.0000   4 |    4228024  100.0000   4 | LW-
```

Win percentages are 100% before and after for every ending that was 100%. Only Klein KRK moves: 0.7945% (old) to 0.6605% (repaired, 960 of 145,344, all mate in 1). Möbius KNNK 0.0077% and Klein KNNK 0% are unchanged.

## d. Second and third programs

- Repaired `fixed_replica` against A (`twisted_tablebases/A/results_*.txt`): 22 of 22 shared rows (legal, won, max DTM) match exactly (`logs/compare_fixed_vs_A_B.txt`). A has no KBK/KNK rows.
- Repaired `fixed_replica` against B rerun by me with `-r 1` (A's ray rule): 26 of 26 rows match, including the KBBK colour split.
- Bishop and queen endings depend on the ray rule (COMPARE.md). All of this is for A's ray rule.

## Paper sentences

- `paper/ieee/sections/10_tablebases.tex:67-68`: "KRK wins everywhere on the Möbius strip ... but only 0.66% on the Klein bottle, which also joins ranks 1 and 8 [C2]". Still holds. Repaired T9 code gives Möbius 147,776/147,776 and Klein 960/145,344 = 0.6605%. The old T9 figure 0.79% was the corrupted one.
- `paper/ieee/sections/14_conclusion.tex:19-21`: pawn play across the seam is open. Not affected.
- `RESULTS.md:425-426`: "A and B agree exactly under A's ray rule. KRK wins every position on the Möbius strip and on RP² but only 0.66% on the Klein bottle (CHECKED-2)". Holds. The RP² part was not rerun here.
- `RESULTS.md:327`: Möbius KPK 78.94% CHECKED-2. Holds (fixed `kpsolve_mob` output is byte-identical).

Nothing in the paper or RESULTS.md needs changing. `research/mobius/REPORT.md` Part A (not paper) still shows the corrupted numbers; it should be marked superseded by `research/twisted_tablebases/`.

## Not done

- The pawn parts of T9 (Part B) and the `mobius_pawns.py` items were not looked at; they do not use the C arrays.
- I did not rerun plane, cylinder, torus or RP².
- ASAN was run on KRK only, as asked; the other 20 tables were run with the optimised builds.
