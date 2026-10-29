# EDITS2 for kings/theory/LOOPY.md (K29 referee 2, 2026-10-29). Replacement NEW blocks for the four edits of K29/EDITS.md; the OLD blocks are the same as there.
# Every OLD occurs exactly once in the current LOOPY.md (checked by `verify/r2/scripts/mkedits2.py` at write time). Changes against K29/EDITS.md: T_P is not called T; flat 7×6 survivors stated correctly;
# the weight of the 107 re-checked classes stated; the referee numbers added.

### EDIT item 6 (section 8, universal zeros)
<<<<<<< OLD
6. **Universal zeros** (CONJECTURE, after Proposition 2.10(b); revised after K23, 2026-10-27). The zero of Z_T is
   context-dependent in P (P13, CHECKED-2). Is there a frozen group with T ≥ 2 that acts as 0 beside every context,
   for instance one whose sortie king cannot reach the buffer before the punisher wins? Solving candidates
   exhaustively on contexts of at most two pawns a side, as K23 did for Z_T (`kings/delegate/out/K23/scripts/` and
   `kings/delegate/out/K23/verify/`), is feasible in P.
=======
6. **Universal zeros** (answered for a bounded context class in the exact-P sense, CHECKED-2; CONJECTURE beyond it; revised after K29 and its referees, 2026-10-29). The zero of Z_T is
   context-dependent in P (P13, CHECKED-2). K29 (`kings/delegate/out/K29/findings.txt`; referee reports `VERIFY.md`, `VERIFY2.md`) listed the 1,236 bare groups with P value (L, W) and at most two Z-pawns a side
   on F_Z (446 symmetry classes; cyl:7×6, cyl:8×6, flat 7×6 and flat 8×6; |F_Z| = 3 and 4; kings anywhere on F_Z) and solved each against contexts of at most two pawns a side, ranks 2–5, on the files at
   distance ≥ 2 from F_Z, with Φ = Ψ as the test (Z acts as 0 beside H). K29 measures the punishment by T_P, the exact P-win length (the number of moves the winner makes, the promoting move included, after the
   loser's longest-resisting move). T_P is not the T of Definition 2.6, which was not computed for these groups. A sortie with T_P ≥ 3 excludes a one-move certificate (PROVED from Theorem 2.7(a), K29 addendum), so
   the groups below are not T = 1 groups of Proposition 2.10(a). Answer for the class: **yes**. On cyl:7×6 (F_Z = a–c; all 885 contexts on e,f, both sides to move) four classes (14 groups) act as 0 beside every
   context and have T_P ≥ 2 on both sides, for example `Kb3 Pa2 Pc2 kb1 pa3 pc3` (two locked pawn pairs, kings on b3 and b1; after every White move Black needs exactly 4 moves to win, and after every Black move White needs exactly 5; the other three classes have (T_P(w), T_P(b)) = (2, 8), (6, 7), (6, 7), where T_P(s) is the winner's move count against the longest resistance of s). CHECKED-2: K29, and the K29 referee on all 60 groups of cyl:7×6, solved every group against all 885 contexts
   (46 groups fail, 14 act as 0; `kp_p` and `ref3` for P, `kpsolve --frozen` and `ref3 --frozen` for the frozen model with two different parking squares; 0 differences). The same four classes act as 0 on
   cyl:8×6 (885 contexts on e,g, the two neighbours of the buffer); two of them (T_P (4, 5) and (2, 8)) act as 0 on flat 7×6 (885 contexts on e,f; the two classes with T_P (6, 7) fail there); all four act as 0 on
   flat 7×6 with F_Z = c–e (885 contexts on a,g, translated). Of the 107 surviving classes that K29 re-checked with two solvers, 17 were checked on such 885-context sets (four boards) and 90 on one context file
   only (63 contexts, the |F_Z| = 4 boards), which is a much weaker statement; 70 more survive only a screen of the first 300 contexts (COMPUTED-1). 269 classes fail, each beside a witness
   context confirmed by two solvers (the referee re-solved 47 witnesses, 25 of them for non-representative class members, all confirmed). The guess in this item (a sortie king that cannot reach the buffer in
   time) is not necessary for a zero: the survivors' sortie kings do reach the buffer, and the slack T_P(m) minus the king's arrival time does not separate survivors from failures (COMPUTED-1); whether groups whose sortie kings cannot reach the buffer in time are zeros was not isolated and stays open. The zero depends on the context class: two of the four cyl:7×6 survivors
   (`Kb3 Pa2 Pa4 ka5 pa3 pb4` and `Kb3 Pc2 Pa4 ka5 pc3 pb4`, two different classes) fail beside `Pf2 pf3 pf4 pf5` (one white and three black pawns; CHECKED-2, K29 and referee). Still open (CONJECTURE): whether `Kb3 Pa2 Pc2 kb1 pa3 pc3` and
   `Kb1 Pa2 Pb3 ka3 pb2 pc5` act as 0 beside every context of every size (no failing context among the first 2,682 of the 3,237 contexts of at most three pawns a side on e,f, COMPUTED-1, one code (K29); the referee re-solved with `ref3` alone, for each of the two groups, 150 of the 980 four-pawn, 400 of the 1,120 five-pawn and 200 of the 560 six-pawn contexts (80 random and the 120 with at least two locked pawn pairs) and found none (COMPUTED-1, one solver; the six-pawn tier is not complete)); whether these groups are frozen groups with T ≥ 2 in the sense of Definition 2.6 (the local game was not run for them);
   a mechanism that forces failure or success; and groups outside the enumeration (three or more Z-pawns of one colour, pawns off F_Z, e.p. layers).
>>>>>>> NEW

### EDIT P2.10(b) status row
<<<<<<< OLD
For every frozen group with T ≥ 2 it is a CONJECTURE. P4 does not show it in P: its six rows equal the convention there | R3 item 5; K23 |
=======
For every frozen group with T ≥ 2 it is a CONJECTURE, and K29 does not refute it: bare groups whose exact-P punishment is T_P ≥ 2 on both sides exist that act as 0 beside all 885 contexts of at most two pawns a side on the files at distance ≥ 2 from F_Z on cyl:7×6 (four classes, `Kb3 Pa2 Pc2 kb1 pa3 pc3` among them, CHECKED-2; two of the four fail beside the context `Pf2 pf3 pf4 pf5`); whether they are frozen groups with T ≥ 2 in the sense of Definition 2.6 was not computed (§8 item 6). P4 does not show it in P: its six rows equal the convention there | R3 item 5; K23; K29 |
>>>>>>> NEW

### EDIT P2.10 row (the CONJECTURE clause)
<<<<<<< OLD
for every frozen group with T ≥ 2 it is a CONJECTURE (revised after K23, 2026-10-27) |
=======
for every frozen group with T ≥ 2 it is a CONJECTURE (revised after K23, 2026-10-27; K29, 2026-10-29: not refuted; for contexts of at most two pawns a side, bare groups with T_P ≥ 2 that act as 0 beside every context exist on cyl:7×6, CHECKED-2, §8 item 6) |
>>>>>>> NEW

### EDIT conjecture block of Proposition 2.10(b) (what remains)
<<<<<<< OLD
What is open: groups in which no sortie king can reach the buffer in time (they might be universal zeros
    even with T ≥ 2), and every group other than these two.
=======
What is open (revised after K29, 2026-10-29): K29 solved the 1,236 bare groups on F_Z (§8 item 6) against all contexts of at most two pawns a side on the files at distance ≥ 2 (cyl:7×6: all 885): 269 of 446
    classes fail, and four classes act as 0 beside all 885 contexts on cyl:7×6 (CHECKED-2) with exact-P punishment T_P ≥ 2 on both sides; two of the four fail beside `Pf2 pf3 pf4 pf5`. K29 did not compute the
    T of Definition 2.6 for them, so the CONJECTURE stands as stated; the exceptions are at the level of T_P and of contexts of at most two pawns a side. For `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5`
    there is no failing context in the samples named in §8 item 6 (CONJECTURE that none exists). Open as well: groups in which no sortie king can reach the buffer in time (K29 did not isolate them), and every group outside the enumeration.
>>>>>>> NEW
