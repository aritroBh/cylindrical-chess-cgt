# EDITS for kings/theory/LOOPY.md (K29, 2026-10-29). Each OLD is copied from the current LOOPY.md (read 2026-10-29 03:30) and occurs exactly once.

### EDIT item 6 (section 8, universal zeros)
<<<<<<< OLD
6. **Universal zeros** (CONJECTURE, after Proposition 2.10(b); revised after K23, 2026-10-27). The zero of Z_T is
   context-dependent in P (P13, CHECKED-2). Is there a frozen group with T ≥ 2 that acts as 0 beside every context,
   for instance one whose sortie king cannot reach the buffer before the punisher wins? Solving candidates
   exhaustively on contexts of at most two pawns a side, as K23 did for Z_T (`kings/delegate/out/K23/scripts/` and
   `kings/delegate/out/K23/verify/`), is feasible in P.
=======
6. **Universal zeros** (answered for a bounded context class, CHECKED-2; CONJECTURE beyond it; revised after K29, 2026-10-29). The zero of Z_T is
   context-dependent in P (P13, CHECKED-2). K29 (`kings/delegate/out/K29/findings.txt`) listed the 1,236 bare groups with P value (L, W) and at most two Z-pawns a side
   on F_Z (446 symmetry classes; cyl:7×6, cyl:8×6, flat 7×6 and flat 8×6; |F_Z| = 3 and 4; kings anywhere on F_Z) and solved each against contexts of at most
   two pawns a side, ranks 2–5, on the files at distance ≥ 2 from F_Z (all 885 of them on cyl:7×6; on the wider boards two context files, or a 300-context screen), with Φ = Ψ as the test (Z acts as 0 beside H). Answer for that class: **yes**. Four classes (14 groups) act as 0
   beside all 885 contexts on e,f of cyl:7×6 and have T_P ≥ 2 on both sides, for example `Kb3 Pa2 Pc2 kb1 pa3 pc3` (two locked pawn pairs, kings on b3 and b1; the exact P-win
   takes 4 White moves after any White move and 5 Black moves after any Black move; T_P is the exact-P number defined in K29, not the T of Definition 2.6). The same classes survive on
   cyl:8×6 (885 contexts on e,g, the two neighbours of the buffer) and on flat 7×6 (885 contexts on e,f; 885 on a,g with F_Z = c–e); 107 surviving classes in all were re-checked on the
   context set stated in K29 (CHECKED-2: `kp_p` and `ref3` for P, `kpsolve --frozen` and `ref3 --frozen` for the frozen model; 0 differences); 269 classes fail, each beside a
   witness context confirmed by two solvers, and 96 sampled class members as well. The guess in this item (a sortie king that cannot reach the buffer in time) is not what separates
   them: the survivors' sortie kings do reach the buffer. The zero depends on the context class: two of the four cyl:7×6 survivors (`Kb3 Pa2 Pa4 ka5 pa3 pb4` and its mirror)
   fail beside `Pf2 pf3 pf4 pf5` (one white and three black pawns; CHECKED-2). Still open (CONJECTURE): whether `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5` act as 0
   beside every context of every size (no failing context among the first 2,682 of the 3,237 contexts of at most three pawns a side on e,f, COMPUTED-1, one code), a mechanism
   that forces failure or success, and groups outside the enumeration (three or more Z-pawns of one colour, pawns off F_Z, e.p. layers).
>>>>>>> NEW

### EDIT P2.10(b) status row
<<<<<<< OLD
For every frozen group with T ≥ 2 it is a CONJECTURE. P4 does not show it in P: its six rows equal the convention there | R3 item 5; K23 |
=======
For frozen groups with T ≥ 2 in general it is a CONJECTURE, and it is false in the form "every such group fails beside some context of at most two pawns a side on the files at distance ≥ 2 from F_Z" (revised after K29, 2026-10-29: four classes on cyl:7×6, `Kb3 Pa2 Pc2 kb1 pa3 pc3` among them, act as 0 beside all 885 such contexts, CHECKED-2; two of the four fail beside a context with three pawns of one colour, `Pf2 pf3 pf4 pf5`; §8 item 6). P4 does not show it in P: its six rows equal the convention there | R3 item 5; K23; K29 |
>>>>>>> NEW

### EDIT P2.10 row (the CONJECTURE clause)
<<<<<<< OLD
for every frozen group with T ≥ 2 it is a CONJECTURE (revised after K23, 2026-10-27) |
=======
for frozen groups with T ≥ 2 in general it is a CONJECTURE, false in the form "fails beside some context of at most two pawns a side" (CHECKED-2, K29; revised after K23, 2026-10-27, and K29, 2026-10-29) |
>>>>>>> NEW

### EDIT conjecture block of Proposition 2.10(b) (what remains)
<<<<<<< OLD
What is open: groups in which no sortie king can reach the buffer in time (they might be universal zeros
    even with T ≥ 2), and every group other than these two.
=======
What is open (revised after K29, 2026-10-29): K29 solved the 1,236 bare groups on F_Z (§8 item 6) against all contexts of at most two pawns a side on the files at distance ≥ 2: 269 of 446 classes fail there, and
    107 surviving classes were re-checked (CHECKED-2); four classes on cyl:7×6 act as 0 beside all 885 contexts, two of them fail beside `Pf2 pf3 pf4 pf5`. The statement above therefore holds only for contexts beyond that class
    (CONJECTURE for `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5`: no failing context among the first 2,682 of 3,237 contexts of at most three pawns a side), and every group outside the enumeration is open.
>>>>>>> NEW
