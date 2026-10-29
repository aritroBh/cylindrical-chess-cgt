# Replacement EDITS for kings/theory/LOOPY.md (K29 referee, 2026-10-29). Each OLD is copied from K29/EDITS.md and occurs exactly once in the current LOOPY.md (checked by verify/scripts/chk_edits.py).

### EDIT item 6 (section 8, universal zeros)
<<<<<<< OLD
6. **Universal zeros** (CONJECTURE, after Proposition 2.10(b); revised after K23, 2026-10-27). The zero of Z_T is
   context-dependent in P (P13, CHECKED-2). Is there a frozen group with T ≥ 2 that acts as 0 beside every context,
   for instance one whose sortie king cannot reach the buffer before the punisher wins? Solving candidates
   exhaustively on contexts of at most two pawns a side, as K23 did for Z_T (`kings/delegate/out/K23/scripts/` and
   `kings/delegate/out/K23/verify/`), is feasible in P.
=======
6. **Universal zeros** (answered for a bounded context class, CHECKED-2; CONJECTURE beyond it; revised after K29, 2026-10-29). The zero of Z_T is
   context-dependent in P (P13, CHECKED-2). K29 (`kings/delegate/out/K29/FINDINGS.md`, referee report `kings/delegate/out/K29/VERIFY.md`) listed the 1,236 bare groups with P value (L, W)
   whose kings and at most two Z-pawns a side (ranks 2-5, at least one pawn) stand on F_Z: 446 symmetry classes on cyl:7×6, cyl:8×6, flat 7×6 and flat 8×6, with |F_Z| = 3 and 4
   (CHECKED-2: the referee's own enumerator gives the same lists; the exact depths agree with a second solver for all 1,236). Each class was solved beside contexts of at most
   two pawns a side, ranks 2-5, on the files at distance ≥ 2 from F_Z, with Φ = Ψ as the test (Z acts as 0 beside H). The context set was complete only on cyl:7×6 (all 885 on e,f).
   On the other boards it was one or two context files (cyl:8×6: e,g; flat 7×6: e,f, and a,g with F_Z = c-e; one file f, 63 contexts, for |F_Z| = 4 on the boards 7 and 8 files wide)
   or a screen of the first 300 contexts. Answer for that class: **yes**. Four classes (14 groups) act as 0 beside all 885 contexts on e,f of cyl:7×6
   (CHECKED-2: the referee re-solved all 885 contexts for all four with its own context generator and two solver pairs, 0 differences). Each has a sortie whose exact punishment takes at least
   3 punisher moves, so no T = 1 certificate LC_1 exists for it (PROVED from Theorem 2.7(a); the local-game T of Definition 2.6 was not computed for these groups, so "T ≥ 2" in the sense of
   Definition 2.6 is not shown). Example: `Kb3 Pa2 Pc2 kb1 pa3 pc3` (two locked pawn pairs, kings on b3 and b1). After every White move Black needs exactly 4 moves to win in P, and after every
   Black move White needs exactly 5 (T_P = 4, 5 in the exact-P number of K29; CHECKED-2). The other three classes have T_P = (2, 8), (6, 7), (6, 7). The same four classes survive on
   cyl:8×6 (885 contexts on e,g) and on flat 7×6 with F_Z = c-e (885 contexts on a,g); two of them (`Kb3 Pa2 Pc2 kb1 pa3 pc3` and the (2, 10) class) survive on flat 7×6 with F_Z = a-c (885 contexts on e,f); K29 checked 107 surviving classes in all on the context set it states
   (CHECKED-2: `kp_p` and `ref3` for P, `kpsolve --frozen` and `ref3 --frozen` for the frozen model; 0 differences; the referee repeated a sample). 269 classes fail, each beside a
   witness context; the referee re-solved all 278 witnesses (269 and the nine of the d3 runs) with two solver pairs, all confirmed (CHECKED-2). The guess in this item (a sortie king that cannot
   reach the buffer in time) was not tested. On cyl:7×6 with F_Z = a-c every enumerated group has a king sortie whose lower bound e(m) on the time to touch a context pawn is at most its exact
   punishment length T_P(m) (COMPUTED-1, K29 `data/S/S_cyl7x6_f3.txt`, recomputed by the referee from that table), so no group of that kind exists there, and the other boards were not examined.
   The survivors are not such groups: Black's sorties Ka3-g4 and Ka3-g2 of `Kb1 Pa2 Pb3 ka3 pb2 pc5` land on the buffer file at once, with exact punishment lengths 8 and 4 (CHECKED-2), and the group
   acts as 0 beside all 885 contexts. The zero depends on the context class: two of the four cyl:7×6 survivors, `Kb3 Pa2 Pa4 ka5 pa3 pb4` and `Kb3 Pc2 Pa4 ka5 pc3 pb4` (two different classes),
   fail beside `Pf2 pf3 pf4 pf5` (one white and three black pawns; CHECKED-2). Still open (CONJECTURE): whether `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5` act as 0
   beside every context of every size (no failing context among the first 2,682 of the 3,237 contexts of at most three pawns a side on e,f, COMPUTED-1, one code; the referee's sample of
   140 further contexts of four to six pawns, two solver pairs, found none either); a mechanism that forces failure or success; groups of the kind in the guess; and groups outside the
   enumeration (three or more Z-pawns of one colour, pawns off F_Z, e.p. layers).
>>>>>>> NEW

### EDIT P2.10(b) status row
<<<<<<< OLD
For every frozen group with T ≥ 2 it is a CONJECTURE. P4 does not show it in P: its six rows equal the convention there | R3 item 5; K23 |
=======
For frozen groups with T ≥ 2 in general it is a CONJECTURE. One bounded form of it is false (revised after K29, 2026-10-29): there are groups with a sortie of exact punishment length ≥ 3 (so no T = 1 certificate) that do not fail beside any context of at most two pawns a side on the files at distance ≥ 2 from F_Z. Four classes on cyl:7×6, `Kb3 Pa2 Pc2 kb1 pa3 pc3` among them, act as 0 beside all 885 such contexts (CHECKED-2); two of the four fail beside a context with three pawns of one colour, `Pf2 pf3 pf4 pf5` (CHECKED-2; §8 item 6). The local-game T of these groups was not computed. P4 does not show it in P: its six rows equal the convention there | R3 item 5; K23; K29 |
>>>>>>> NEW

### EDIT P2.10 row (the CONJECTURE clause)
<<<<<<< OLD
for every frozen group with T ≥ 2 it is a CONJECTURE (revised after K23, 2026-10-27) |
=======
for frozen groups with T ≥ 2 in general it is a CONJECTURE; the bounded form "fails beside some context of at most two pawns a side" is false for groups with a sortie of exact punishment length ≥ 3 (CHECKED-2, K29; revised after K23, 2026-10-27, and K29, 2026-10-29) |
>>>>>>> NEW

### EDIT conjecture block of Proposition 2.10(b) (what remains)
<<<<<<< OLD
What is open: groups in which no sortie king can reach the buffer in time (they might be universal zeros
    even with T ≥ 2), and every group other than these two.
=======
What is open (revised after K29, 2026-10-29): K29 solved the 1,236 bare groups on F_Z (§8 item 6) beside contexts of at most two pawns a side on the files at distance ≥ 2. 269 of 446 classes fail there,
    and 107 surviving classes were re-checked (CHECKED-2). Four classes on cyl:7×6 act as 0 beside all 885 contexts, and two of them fail beside `Pf2 pf3 pf4 pf5`. So the conjecture is not refuted: it needs contexts beyond
    that class for these groups. For `Kb3 Pa2 Pc2 kb1 pa3 pc3` and `Kb1 Pa2 Pb3 ka3 pb2 pc5` it is open (no failing context among the first 2,682 of 3,237 contexts of at most three pawns a side, COMPUTED-1). Also open:
    groups in which no sortie king can reach the buffer in time (they might be universal zeros even with T ≥ 2; none exists among the K29 candidates on cyl:7×6, and the other boards were not examined),
    and every group outside the enumeration.
>>>>>>> NEW
