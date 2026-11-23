# K45 referee report (2026-11-23)

AI work, no human re-derivation. Verdict: **CONFIRMED, with two small wording fixes.** Every number checked is
reproduced. `verify/EDITS.md` is a full replacement set of the 9 edits with those two fixes (it applies cleanly: 9 of 9,
tested with apply_edits.py on a copy outside the repo). The investigator's EDITS.md also applies cleanly (9 of 9).

## Own implementation
`verify/r45.cpp` is a new P solver and Definition 4.8 test, written from SPEC.md and LOOPY Definition 4.8 before reading
the investigator's code. It works layer by layer (pawn sets, children first, memoised), uses retrograde counters inside a
layer, and evaluates e.p. states on demand. Modes: `val`, `moves`, `group` (clauses O1 to O4, with every move listed),
`enum` (exhaustive, the same domain as K45) and `layers`. The over orientation is tested as the colour mirror of the under
test. Binaries were deleted after the runs.

Solver check: 1,500 random positions on cyl:8x6 (seeded, `gen_random.py`; 0 to 4 + 4 pawns, 64 with an e.p. square)
were compared with ref3m (K23, compiled as a fresh copy and then deleted). 0 differences
(`rnd8.r45`, `rnd8.ref3m`; values W 532, L 523, D 109, X 336).

## Results (all COMPUTED with r45 and in agreement with K45's A and B, so CHECKED-2 or better)
1. **cyl:8x6 group** `Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5`, shuttle d4-d5. (O1)-(O4) all hold.
   - Black has 6 moves at d4 and 7 at d5, all losing.
   - White's only non-losing move is e2-e4 at d4 and e2-e3 at d5.
   - After the freeze Black has 4 / 5 moves and White 6 / 6, all losing.
   - The mirror under group `Kd2 kf2 Pa3 Pb2 Pe2 pb3 pb5 pe5` (d2-d3) and the reflected group `Ke5 kg4 Pa2 Pa4 Pf2 pb4 pa5 pf5` (g4-g5) are exact.
   - The same group is exact on cyl:9, 10, 11, 12, 14 and 16 x6.
2. **2 + 3 group** `Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5` (f6-g6) and its mirror `Kf1 kg3 Pa2 Pb3 Pe2 pb4 pe5` (f1-g1).
   - Exact on cyl:10x6, with freezes e2-e3 / e2-e4. After the freeze Black has 5 / 4 moves and White 6 / 4, all losing.
   - The same placement is not exact on 8, 9, 11, 12, 14 or 16: (O1) fails on 8 and 9, and (O3) fails on 11 and up.
3. **K44 roots** `Kc3 ka4/ka5 Pa2 pa3 Pc4 pc5 Pf2 pf3` on cyl:10x6, 11x6 and 12x6: (O1)-(O3) hold and (O4) fails at all four freezes.
   - Black has 3 moves at a4 and 6 at a5.
   - The freezes are Kc3-c2 and Kc3-d2 at both roots. At the a4 root, c3-d3 loses. At the a5 root, b3 and d3 lose.
   - After the freeze Black has 4 / 7 moves. After Kc2, White has 6 (a4) / 7 (a5) moves, and Kc2-c3 and Kc2-d2 both win. After Kd2, Kd2-c2, Kd2-c3 and Kd2-e3 win.
   - The mirror under root (Pa2 pa3 Pc4 pc5 Ph4 ph5, shuttle c2-c3, king a4) fails (O4) the same way. Its freezes are the king moves a4-j5 and a4-a5.
4. **Exhaustive enumeration, own code** (`enum_W_files.out`): all six file classes on cyl:6x6, 7x6, 8x6 and 10x6, at most 3 + 3 pawns, every placement.
   - The placements, F1 (O1), promotion-freeze, F2, loose and exact counters equal K45's results.tsv (A, W=10) and results_ball.tsv (B, W=6, 7, 8, 10) exactly, in every row.
   - Exact hits (under orientation): none on 6x6 or 7x6. On 8x6, one each for {a,b,e} and {a,b,f} (the 3 + 3 group and its reflection). On 10x6, two for {a,b,e} (the 3 + 3 and 3 + 2 mirrors).
   - So no exact group has at most 2 + 2 pawns on these boards.
   - cyl:9x6, 11x6, 12x6, 14x6 and 16x6 were not re-enumerated.
5. **K44 batteries** (`battery_W10/11/12.out`): the 378 blocked-pair configurations of configs_all.txt, both orientations (756 layer lines), every placement, on cyl:10x6, 11x6 and 12x6. The result is 0 exact, as claimed. This is the battery layers themselves; sub-layers are covered for W=10 by item 4.
6. **A against B**: the investigator's compare_all.py, re-run on the xz logs (`compare_all_xz.py`), prints 1,199,596 layer lines with 0 differences and equal hit sets.
   - The funnel sums of findings.txt are reproduced: 6,123,475,980 placements, F1 1,785,025,756, F2 409,533,071, loose 385,499,965, and 4 exact.
   - The A table against ref3m dump agrees on 1,500 of 1,500 positions.
7. **Contexts**: own values for the 88 context positions equal ctx_ref3m.out and ctx_kpp.out (0 differences each). The tally is W 60, L 27, X 1.

## Problems (minor; fixed in verify/EDITS.md)
- **Wording of "realised".** "Second half, realised" and the status row "realised in P" should say *in the sense of Definition 4.8*. The groups' equality with over in sums is not tested, and the investigator says so in findings.txt.
- **Missing exception in the context sample.** The EDITS bullet says a free White pawn leaves all four roots White wins. It omits that Ph5 makes one root of the 2 + 3 group illegal (X). The summary has the same omission.
- **Not an edit problem.** During one cross-check, three solver processes ran for about 4 minutes (two heavy.sh slots plus one nice-15 ref3m/r45 sample run outside heavy.sh).
