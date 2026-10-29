# K15 + K26 merged edits of kings/theory/LOOPY.md

One edit set against the current `kings/theory/LOOPY.md` (after commit 2061cea4, K28). It carries K15 (dud and over groups on the cylinder,
`kings/delegate/out/K15/FINDINGS.md`, referee `kings/delegate/out/K15/VERIFY_K15b.md`) and K26 (exact group census in P without cut-offs,
`kings/delegate/out/K26/FINDINGS.md`, referee `kings/delegate/out/K26/VERIFY.md`), as their referees corrected them: the five standing and three
replacement blocks of K15, the five standing and five replacement blocks of K26. Where both touch the same text there is one block. K28's chess
statements are kept word for word. The reconciliation of the two investigations is in `kings/delegate/out/K15K26/MERGE_NOTES.md`.

### EDIT status row P3.2′ tail
<<<<<<< OLD
Open: chess contexts of Z_B, the cylinder, other boards. Z_A (§5.7) is a second group, with one White break (Kxb4).
=======
Open: chess contexts of Z_B, other boards. On the cylinder (K15, K26 and their referees, 2026-10-27; §5.7, §8 item 2): Z_B is exactly two-shuttle in P at its 8 roots on cyl:7×6 and cyl:8×6 (CHECKED-2; not hand-proved there) and equals r(G ⊞ dud_D) in every exhaustive context of at most 3 pawns tried (CHECKED-2, COMPUTED-1 for the earlier samples); the passer-free group Z_C (cyl:8×6) is exact at its 8 roots but not beside every context; G8a and G8b (cyl:8×6, no pawn move at all) are exactly two-shuttle in P (CHECKED-2) and in chess at cap 2 (COMPUTED-1). Z_A (§5.7) is a second group, with one White break (Kxb4).
>>>>>>> NEW

### EDIT status row C4.7
<<<<<<< OLD
| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched) | R1 item 10, R4 item 8 |
=======
| C4.7 | Over is realisable with wider groups: CONJECTURE, no support. The old first half is now a computation in two readings (revised after K15, K26 and their referees, 2026-10-27): no exact over or under group (Definition 4.8, plain P) on 3 files of cyl:8×6 with ≤ 2 + 2, 3 + 2 or 2 + 3 pawns, nor with ≤ 2 + 2 on cyl:7×6, flat 7×6 and 8×6 (K26; CHECKED-2 except flat 8×6), nor on 4 files of cyl:8×6 with ≤ 2 + 2 (COMPUTED-1); no structural over or under root against free passes in K15's 20 ranges (cyl:8×6 and 7×6: 3 files ≤ 4 + 4, 4 files ≤ 3 + 3, 5 files ≤ 3 + 2; cyl:8×8, 7×7, 8×7 in smaller ranges; flat 7×6), COMPUTED-1, reproduced in 16 of the 20 ranges by K15b (CHECKED-2); the tempo-signature candidates and the near-over groups are refuted beside contexts but one placement without a context file; Lemma 4.9 PROVED (no king freeze) | R1 item 10, R4 item 8; K15, K15b; K26 and its referee |
>>>>>>> NEW

### EDIT section 3 loopy kings text
<<<<<<< OLD
the cylinder, other boards (§8,
  item 2). Z_A (§5.7) has one White break.
=======
other boards (§8,
  item 2). On the cylinder dud groups exist in P (K15, K26 and their referees, 2026-10-27; §5.7, §8 item 2): Z_B and the passer-free
  group Z_C are exactly two-shuttle at their 8 roots on cyl:8×6 (Z_B also on cyl:7×6; CHECKED-2), Z_C is not exact beside every context,
  and G8a, G8b (no pawn move at all) are exactly two-shuttle in P (CHECKED-2) and in chess at cap 2 (COMPUTED-1). Z_A (§5.7) has one White break.
>>>>>>> NEW

### EDIT Conjecture 4.7, Definition 4.8, Lemma 4.9
<<<<<<< OLD
- **CONJECTURE 4.7:** no over-type group with ≤ 2 + 2 pawns fits on 3 files of the 8×6 cylinder, but over
  is realisable on the cylinder with wider groups. *Scratch evidence:* the first half; a geometric search over
  placements of ≤ 2 + 2 pawns on 3 (or 4) files found none (Appendix A). *To settle:* a wider search, then
  kpsolve. (Revised after review: R1 item 10, R4 item 8: the search described in Appendix A covered ≤ 2 + 2
  pawns, not the ≤ 3 + 2 claimed here; the conjecture is restated for what was actually searched.)
=======
**Definition 4.8 (exact under and over groups in P; new, K26, 2026-10-27).** Let White's king shuttle on an adjacent pair z (K1 holds) and Black's king stand on one
square b0 with K1 and K2 against both z squares. Call it an *exact under group* if, in P:
- (U1) at both White-to-move roots every non-shuttle White move loses at once (the position after it is a Black win), and the shuttle is legal;
- (U2) at both Black-to-move roots Black has a move that does not lose at once (a *freeze*);
- (U3) after each freeze, a position q (with the e.p. flag if the freeze is a double step), White to move has a legal move and every legal White move loses at once;
- (U4) the same q with Black to move (no flag): q is a legal position, Black has a legal move and every legal Black move loses at once. So q is a mutual zugzwang, the position 0_D of Definition 4.4. If the freezing pawn gives check, q with Black to move is not legal and (U4) fails.
A promotion by Black is a decisive event, not a freeze to 0: a group in which some freeze is a promotion is not exact (such placements are counted separately below). (Rules for promotion, e.p. and check added after the K26 referee, 2026-10-27; they are what both searches of K26 did.)
The colour mirror (ranks flipped, colours swapped) is an *exact over group*. Dropping (U4) gives a *loose* under group: after the freeze only White is in zugzwang.

**Lemma 4.9 (no king freeze). PROVED** (new, K26, 2026-10-27). In an exact under group no freeze is a king move that captures nothing.
*Proof.* Let m be such a freeze, b0 → b1, and q the position after it. In q (with Black to move, a legal position by K1 for the White king's square) Black can play b1 → b0: b0 is empty, no White pawn attacks it (K1, the pawns have not moved), and it is not
next to the White king, which has not moved (K2). No e.p. right exists (no pawn moved). The result is the root with White to move. By (U2) and (U3) the other Black-to-move root has a freeze to a position of
value L (a White loss; if that freeze is a promotion, the root is a Black win at once), so that root has value L. By (U1) every non-shuttle White move at the first root loses at once, and the shuttle leads to the second root, value L.
So the first root has value L, the move b1 → b0 does not lose at once, and (U4) fails. ∎ So a freeze of an exact group is a pawn move or a king capture of a group pawn.

- **CONJECTURE 4.7 (restated after K15, K26 and their referees, 2026-10-27; `kings/delegate/out/K15/FINDINGS.md`, `kings/delegate/out/K15/VERIFY_K15b.md`,
  `kings/delegate/out/K26/FINDINGS.md`, `kings/delegate/out/K26/VERIFY.md`; AI work, no human re-derivation):** over is realisable on the cylinder with wider groups.
  No over-type group is known. The old first half (no over-type group with ≤ 2 + 2 pawns on 3 files of the 8×6 cylinder) is now a computed result, in each of two
  readings of "over" below, and is no longer conjectured.
  - *Two readings.* K26 tests the exact under and over groups of Definition 4.8 in plain P: there the freeze wins at once (q with White to move is lost for White), and
    (U4) asks that q is a zugzwang for Black as well. K15 tests a structural label "over" of its exact classifier `K15/grp.c` (closures under safe moves) against a
    defender with free passes; in plain P its classifier labels the freezing move a winning move, so only its free-pass reading can output over. The two definitions
    are not the same, and neither search finds a group of its own kind. (Reconciliation: `kings/delegate/out/K15K26/MERGE_NOTES.md`.)
  - *K26, plain P, Definition 4.8 (CHECKED-2 for the searches on 3 files named here except flat 8×6, COMPUTED-1 for the four-file search).* K26 searched with no
    cut-off: F_Z = {a, b, c}, every placement of the kings and of at most 2 + 2, then 3 + 2 and 2 + 3 pawns (`kings/delegate/out/K26/scripts/over2.py` and `over3.py`).
    It found **no** exact under or over group on cyl:8×6 (631,179 placements for 2 + 2; 1,602,414 for 3 + 2; 1,517,293 for 2 + 3), and none for 2 + 2 on cyl:7×6,
    flat 7×6 and flat 8×6 either. The K26 referee's own search (`kings/delegate/out/K26/verify/scripts/ref_under.py`, ref3m, no king filter, no use of Lemma 4.9)
    reproduces the 2 + 2 result on cyl:8×6, cyl:7×6 and flat 7×6 (flat 8×6 not repeated), and repeated the 3 + 2 and 2 + 3 runs on cyl:8×6 without the king filter:
    no exact group, and the counts of placements with (U1), (U2) and value L after every freeze are 254,258 and 545,277.
  - Placements with (U1), (U2) and value L after every freeze (a promotion counts as value L), at all four roots: 144,159 on cyl:8×6 for 2 + 2 (without the king
    filter), 144,411 on cyl:7×6, 140,389 on flat 7×6; the K26 referee's own enumerator with ref3m counts the same numbers. None is an exact group: each fails (U4)
    at some freeze or has a promotion as a freeze. The split between these two depends on the order in which the freezes are tried (K26: 141,293 and 2,866;
    referee: 143,831 and 328 on cyl:8×6); the sum does not. In 5,791 of the (U4) failures on cyl:8×6 the freezing pawn gives check.
  - The search of K26 with four files (a–d) and at most 2 + 2 pawns on cyl:8×6 (5,793,156 placements; 66,476 pass the king filter and (U1)–(U3) at one root,
    55,331 at all four roots) found no exact group (COMPUTED-1, not repeated by the referee).
  - *Loose* groups are plentiful. With exactly one freeze at every root there are 120 on cyl:8×6 (2 + 2, 3 files), 142 on flat 7×6, 118 on cyl:7×6 (all three
    CHECKED-2 by the K26 referee's count) and 626 on cyl:8×6 with four files (reused from K26, not repeated). Beside contexts Proposition 4.6 holds in 537 of the
    552 premise roots of K26's final sample (762 of 768 in an earlier sample); the failures were not diagnosed. Loose groups are not over_D anyway: after the
    freeze Black still has a move that does not lose.
  - *K15, structural over against free passes (COMPUTED-1; the classifier CHECKED-2).* K15's classifier (`K15/grp.c`, own move generator) solves the exact
    local game of model P (real kings, empty context) for every placement of both kings and of at most w White and b Black pawns on the files a..F, ranks 2 to
    H − 1, no officers, with root passers excluded or allowed, with free passes and in plain P. Ranges, on cyl:8×6 and cyl:7×6: F = 3 with w, b ≤ 4 + 4; F = 4
    with ≤ 3 + 3; F = 5 with ≤ 3 + 2. On cyl:8×8: F = 3 with ≤ 3 + 2, F = 4 with ≤ 2 + 2. On cyl:7×7 and cyl:8×7: F = 3 with ≤ 3 + 2. On flat 7×6: F = 3 with
    ≤ 3 + 3. That is 20 ranges, each run in both readings and with root passers excluded and allowed (80 table rows, up to 105 million roots a row). Only the 40
    free-pass rows can output over: **0 over and 0 under roots** in them; the 40 plain-P rows say nothing about over. The referee K15b rebuilt the classifier from
    the definitions (own C++ solver and move generator, no code shared with `grp.c`): it reproduces the frozen, dud, over and under counts of 16 of the 20 ranges
    in both readings (all seven cyl:8×6 ranges, both cyl:8×8 ranges, five of the seven cyl:7×6 ranges, both flat 7×6 ranges), with identical labels root by root
    in 12 runs; 0 over and 0 under (CHECKED-2). Ranges that need over 3 GB of table (cyl:8×8 with F = 3 and ≤ 3 + 3, F = 4 and ≤ 3 + 2, and others) were not run.
  - *K15's earlier classifier check.* An independent Python classifier gives the same label at 772,188 roots (cyl:5×5, 5×6, 6×5, 3 files, ≤ 2 + 2, with passes)
    and at 634,628 roots in plain P; its local game values equal `kp_p`'s on 18,000 random positions (flat 7×6, cyl:7×6, cyl:8×6). It labels Z_B (§5.7) dud in
    plain P (K15b's own classifier agrees on flat 7×6, cyl:7×6 and cyl:8×6).
  - *A tempo-signature search (no structure).* The 16 outcomes of a root beside the contexts (a, b, c) ∈ {0, 1}³ (a private White tempo move, a private Black
    one, a shared one) are compared with those of zero, on, off, dud, over and under. K15 finds no over signature on 3 files with ≤ 3 + 3 pawns (cyl:8×6, 7×6).
    On 4 files with ≤ 2 + 2 pawns it lists 20 roots per board (10 groups), but K15's tempo solver is not plain P: it counts a stalemate as a loss and lets a tempo
    move be played in check, so its tempo-free values differ from plain P at 166 of 1,500 sampled roots (K15b, `ref3`). With plain-P rules the over signature has
    4 roots on cyl:8×6 and 6 on cyl:7×6, all among K15's 20 (they include the two survivors below), so the counts of this census depend on the convention
    (COMPUTED-1, K15b). `kp_p` beside up to 40 pawn contexts and then beside every assignment of one context file refutes all of K15's candidates (COMPUTED-1).
  - *Near-over groups, COMPUTED-1 (K15).* The classifier also lists roots where Black has a shuttle in the free-pass reading and every White safe move freezes,
    but the closure test fails (12 groups on each of cyl:7×6 and cyl:8×6, 4 on cyl:8×8, 1 each on cyl:7×7 and cyl:8×7). Beside contexts every one differs from
    r(G ⊞ over_D) except one placement on cyl:7×6 whose window leaves no context file. The longest survivor is `Kd5 kb5 Pa3 Pb2 Pd2 pa4 pc5 pd4`: it agrees with
    over_D at all 130 positions of the exhaustive single-file contexts with at most 3 pawns on file g of cyl:8×6, and fails at 3 of 130 on file f (cyl:8×6 and
    cyl:7×6). K15b re-solved all 260 positions of cyl:8×6 (files f and g) with `ref3` against its own predictor of r(G ⊞ over_D): 130 of 130 agree on g, the same
    3 of 130 differ on f (CHECKED-2). It has no Black king shuttle in P (all six Black moves lose). A context test on the farthest file alone would have supported it.
  - *Second half, CONJECTURE, no support:* nothing was found in either search, and the four-file search of K26 neither supports nor refutes it. "None exists"
    is not claimed: the boundary is at most 8 pawns, 5 files and the empty-context local game (K15), and F_Z = {a, b, c} or a–d with at most 3 + 2 pawns (K26).
  - *To settle:* more files and pawns, kings off the group files, officers; chess (kpsolve was not run for any over candidate).
  - The scratch search of Appendix A is no evidence for the old first half and is replaced by these two searches. Its script was not kept, so it cannot be
    re-run. Tests of its kind (one-ply: immediate promotion or passed pawn) label Z_B "other" and none of the 41 dud roots of flat 7×6 as dud (K15's `oneply.py`,
    not re-run by K15b), and K15's first classifier of this kind could never output dud. (Revised after K15, K15b, K26 and the K26 referee, 2026-10-27; before, the
    first half rested on that search.)
>>>>>>> NEW

### EDIT 5.3 scratch evidence withdrawn
<<<<<<< OLD
- *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. This is the earlier scratch search on the cylinders only, with
    one-ply tests, not re-run; it says nothing about flat boards, where Z_B exists (§5.7). "dud may not occur in small
    K+P groups" remains a CONJECTURE for chess and for the cylinder.
=======
- *Scratch evidence (withdrawn; revised after K15 and K26, 2026-10-27):* the earlier scratch statement "no both-sides-shuttle group without a pawn
    break exists among 3-file groups with ≤ 2 + 2 pawns and no passer on the 8×6 cylinder" is **false**. K26 searched exhaustively, with no cut-off
    (§5.7): on cyl:8×6 the group Z_C (Pa2 Pc4 / pa3 pc5, kings c2/c3 and a4/a5) has no textbook passer, no pawn that can move, and every non-shuttle
    move loses at once at all 8 roots in P (CHECKED-2). K15's census, run with the no-passer filter of `cylcgt.passed`, found the same group (as its file
    mirror `Ka2 kc4 Pa4 Pc2 pa5 pc3`, `kings/delegate/out/K15/fin2/dud_groups.md`, cyl:8×6 #38) and, on 5 files, G8a and G8b (§8 item 2). Z_B of §5.7
    also works on cyl:7×6 and cyl:8×6. "dud may not occur in small K+P groups" is therefore refuted in P on the cylinder. In chess G8a and G8b are exactly
    two-shuttle at cap 2 (COMPUTED-1, one solver family; K15), Z_B is not exactly two-shuttle on flat 7×6 (K28, §5.7), and Z_C is open (bounds (W, L) at cap 1).
>>>>>>> NEW

### EDIT 5.7 Z_B on other boards and the cylinder, Z_C, contexts
<<<<<<< OLD
  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact, and 225
    of the 885 contexts are untested. It is open on the cylinder and on other boards.
=======
  - **Other boards and the cylinder (new, K26 and K15, 2026-10-27). The searches of K26 CHECKED-2 for at most 2 + 2 pawns and for 3 + 2 and 2 + 3 on flat 7×6, cyl:7×6 and cyl:8×6 (revised after the K26 referee, 2026-10-27), the 8 roots and their move lists CHECKED-2 (kpp and ref3m).**
    Z_B has total leak count 0 (every non-shuttle move loses at once in P, at all 8 roots) on cyl:7×6, cyl:8×6 and flat 8×6,
    and on every six-rank board that was tried: flat width 5, 7, 8, 9, 10 and cylinder width 5 to 10 (widths 9 and 10: ref3m only, COMPUTED-1; kpp stops at width 8).
    Widths 11 and 12 (66 and 72 squares) were also run, but ref3m keeps its pawn sets in 64-bit masks, so they are not claimed (revised after the K26 referee, 2026-10-27). It fails on 5, 7 and 8 ranks (8 to 13 leaks; flat 7×7, 7×5 and 8×8, cyl 8×5, 6×7 to 9×7, 8×8). On cyl:7×6 it has two more
    legal Black moves, Ka4–g3 and Ka4–g5 (the wrap; Ka4–h3 and Ka4–h5 on cyl:8×6), and the mirror has Ka3–g2 and Ka3–g4. They lose at once as well. On cyl:7×6 and cyl:8×6
    the 8 roots have 38 legal moves, of which 8 draw (the shuttles) and 30 lose (K15; `kp_p` and `ref3m` give the same values and move lists, CHECKED-2). K27's 26 certificates
    do not cover the wrap moves, so Z_B is **not PROVED** exact on the cylinder.
    The search of K26 (`kings/delegate/out/K26/`; F_Z = {a, b, c}, no cut-off; at most 2 + 2 pawns, then 3 + 2 and 2 + 3; 817,270 placements for 2 + 2
    and 1,886,421 for 3 + 2 and 2 + 3) finds exactly Z_B and its mirror on flat 7×6, flat 8×6 (at most 2 + 2 pawns only) and cyl:7×6 (all three pawn limits; 3 + 2 and 2 + 3 were also searched on flat 7×6 and cyl:8×6), and on cyl:8×6 Z_B, Z_C (below) and their mirrors. For 2 + 2 this is CHECKED-2: a second
    enumerator and a second solver (ref3m) agree on 2.4 to 2.8 million root move lists per board, 0 differences. The K26 referee's own enumerator (`kings/delegate/out/K26/verify/scripts/ref_enum.py`, ref3m only) reproduces the counts of total leaks 0, 1, 2 on all four boards and for 3 + 2 and 2 + 3 on flat 7×6, cyl:7×6 and cyl:8×6 (revised after the K26 referee, 2026-10-27). On flat 7×7 (at most 2 + 2 pawns only) no placement has
    leak count 0 (the minimum is 1, with 12 placements; CHECKED-2: the referee's own enumerator gives the same counts; revised after the K26 referee, 2026-10-27).
    The brief of K15 filtered roots with a passer by `cylcgt.passed`; all four pawns of Z_B are passed pawns for it (blockaded by the kings), so that filter rejects Z_B.
    K15's classifier labels Z_B dud in plain P and "mixed" against free passes (two pawn pushes then draw), and its one-ply tests (immediate promotion or passed pawn)
    label it "other", because none of the 26 losing deviations is an immediate event (they lose in 3 to 11 plies; K15b's own depth search agrees). Chess: bounds (W, L)
    at cap 1 on cyl:7×6, as on the flat board (cyl:8×6 not run; K15).
  - **A second exact group, Z_C (new, K26, 2026-10-27; also in K15's census).** On cyl:8×6 the search also finds White king c2/c3 (shuttle), Black king a4/a5 (shuttle), pawns
    Pa2 Pc4 / pa3 pc5, and its colour mirror. All four pawns are blocked, so no pawn can move, and it has no textbook passer. Every king move off the
    shuttles loses at once at all 8 roots (CHECKED-2). K15's census lists its file mirror `Ka2 kc4 Pa4 Pc2 pa5 pc3` as a cyl:8×6 dud group in plain P without a root passer
    (`kings/delegate/out/K15/fin2/dud_groups.md`, cyl:8×6 #38). Among the boards tried with these ranks (pawns on ranks 2 to 5) it is exact alone only on cyl:8×6 and cyl:9×6: it has 8 leaks on cyl:6×6, 7×6 and 10×6, 12 on cyl:5×6
    and 16 on every flat board of six ranks tried (width 5 to 10) and on flat 7×7 (its mirror has 6 there). One rank higher, `Kc3 ka5 Pa3 Pc5 pa4 pc6`, it is a dud group of K15's cyl:8×8 census
    (`fin2/dud_groups.md`, cyl:8×8 #22, root check (D, D), every non-draw move loses; COMPUTED-1, see `kings/delegate/out/K15K26/MERGE_NOTES.md`). In chess with cap 1 the bounds of Z_C alone are (W, L) at all 8 roots (kpsolve, COMPUTED-1), so chess is open for it. It is **not** a two-shuttle component beside contexts: with at most 3 context pawns on files e–g of cyl:8×6, 131 of 2,049 contexts (35 of the 264 with two pawns, 96 of the 1,760 with three, none with fewer; 754 of 16,392 roots) give
    a P-result different from r(G ⊞ dud_D) (CHECKED-2: K26's kpp and `dmodel.py`, and the referee's ref3m and its own predictor `verify/scripts/dud_ctx.py`, give the same counts; revised after the K26 referee, 2026-10-27). One of the smallest is Pe2 pe3, where P is (W, W) at all 8 roots, because Kc2–d3 wins there (it loses alone; the shuttle Kc2–c3 wins too). So (Pun) fails for Z_C
    beside a pawn that its king can reach (CHECKED-2; revised after the K26 referee, 2026-10-27). K15 found the same for its mirror: of 192 context positions 46 disagree with dud_D, and with Pe2 pe3 beside it all four king states are W (`ref3`, CHECKED-2, K15b).
  - **Contexts beside Z_B (new, K26, 2026-10-27). CHECKED-2** (K26: kpp against its own D-model predictor `dmodel.py`; the K26 referee: ref3m against its own implementation of Theorem 3.4(a) with the e.p. flag, `verify/scripts/dud_ctx.py`; same result; revised after the K26 referee, 2026-10-27). Every placement of at most 3
    context pawns of either colour on ranks 2 to H−1: cyl:8×6, files e–g: 2,049 contexts, 0 differ from r(G ⊞ dud_D); cyl:7×6, files e–f: 577 contexts, 0 differ;
    flat 7×6, files e–g: 2,049 contexts: 0 differ. (Each context at 8 roots.) Files d and h (next to F_Z) were not tried.
  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact. It holds in every context tried (the K14 and K27
    families and the exhaustive families above; revised after K26, 2026-10-27). Open: a hand proof on the cylinder, chess contexts, other contexts, other boards.
>>>>>>> NEW

### EDIT section 7 dud bullet
<<<<<<< OLD
and the cylinder and other boards are open.)
=======
and other boards are open. On the cylinder dud groups exist in P: Z_B, the passer-free Z_C, and G8a, G8b with no pawn move at all (§5.7, §8 item 2; K15, K26
  and their referees, 2026-10-27; CHECKED-2 at the roots), and G8a, G8b are exactly two-shuttle in chess at cap 2 (COMPUTED-1, one solver family), so in chess the
  question has a computed answer on cyl:8×6, not a proof.)
>>>>>>> NEW

### EDIT section 8 item 2
<<<<<<< OLD
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist? Both
   need wider searches. (After K14 and its referee, and after K27 and its referee, 2026-10-27: on the flat 7×6 board Z_B
   of §5.7 has every non-shuttle move losing by force in P, PROVED by hand (K27), CHECKED-2 for the computations; a search
   of flat 7×6 (F_Z = {a, b, c}, ≤ 2 + 2 pawns, no cut-off) found exactly
   two such placements, mirror images, among 817,270, COMPUTED-1. Beside every context tested its P-result equals that of
   dud_D (COMPUTED-1; 225 of 885 contexts untested). K14's own search had a move-count cut-off (18), which excluded Z_B,
   so its negative statements are withdrawn. In chess Z_B is not exactly two-shuttle (K28 and its referee, 2026-10-28, CHECKED-2: 25 of the 26
   deviations lose, Kc3–d2 from (c3, b5) draws). Open: chess contexts of Z_B, the cylinder, other boards.)
=======
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist? **Answered in part by K15 and K26
   (P model; 2026-10-27; `kings/delegate/out/K15/FINDINGS.md`, `kings/delegate/out/K26/FINDINGS.md`, referee reports `kings/delegate/out/K15/VERIFY_K15b.md`
   and `kings/delegate/out/K26/VERIFY.md`, reconciliation `kings/delegate/out/K15K26/MERGE_NOTES.md`; AI work, no human re-derivation).** Dud groups: yes.
   Over groups: none found (Conjecture 4.7). The two investigations use different definitions and scopes; where they overlap they agree.
   - *Definitions.* K26's *exact* group (the hypothesis of Proposition 3.2′ in the empty context): kings on adjacent pairs, four combined king states, every
     non-shuttle move loses at once in plain P (total leak count 0). K15's *dud in plain P* (reading B): in the closure of the root under the safe (drawing) moves
     of both sides every state has a safe move for each side, and there is no check, no winning move and no safe king move off the group files; a state may have
     several safe moves, so the closure may be larger. K15's *dud against free passes* (reading A) asks the same when the deviator may pass at will; it is stricter
     for deviations (Z_B is dud in B and "mixed" in A). An exact group is a plain-P dud group of K15 whose closure is its four king states.
   - *Exact groups on F_Z = {a, b, c} (K26).* Z_B (§5.7) and a passer-free group Z_C (Pa2 Pc4 / pa3 pc5, kings c2/c3 and a4/a5, every pawn blocked) have every
     non-shuttle move losing at once at all 8 roots on the cylinder: Z_B on cyl:7×6 and cyl:8×6 (and on every six-rank board tried), Z_C on cyl:8×6 and cyl:9×6.
     CHECKED-2 for the roots and move lists (kpp and ref3m); the exhaustive search of F_Z = {a, b, c} with at most 2 + 2 pawns is CHECKED-2 on flat 7×6, flat 8×6,
     cyl:7×6 and cyl:8×6 (second enumerator, second solver, and the referee's third), CHECKED-2 for 3 + 2 and 2 + 3 on flat 7×6, cyl:7×6 and cyl:8×6 (the same
     groups, no new one), and CHECKED-2 for 2 + 2 on flat 7×7 (no exact dud there; minimum leak count 1) (revised after the K26 referee, 2026-10-27). No hand
     proof on the cylinder. Z_B equals dud_D in all 2,049 + 577 + 2,049 contexts of at most 3 pawns tried (CHECKED-2); Z_C does not (131 of 2,049, CHECKED-2).
   - *G8a and G8b (K15; outside K26's scope: five files).* G8a `Kb2 kc4 Pa3 Pe2 pa4 pe3` and G8b `Kb3 kc5 Pa4 Pe3 pa5 pe4` on cyl:8×6 (pawns on files a and e,
     kings between; White shuttles b2–c2, Black c4–d4; two blocked pairs, no pawn move at all, no root passer): the four king states of each have value (D, D) at
     all 16 roots, 16 of the 72 legal moves draw (the shuttles) and the other 56 lose for the mover, also against a defender who may pass. P model, CHECKED-2
     (`kp_p`, `ref3m` and K15's exact classifier agree). Chess: kpsolve at cap 2 is exact at all 16 roots and gives the same 72 move values, so G8a and G8b are
     exactly two-shuttle in chess, COMPUTED-1 (one solver family; `ownchess` is flat-board only). Beside contexts, P: 1,296 positions (every assignment of one
     context file, both sides) equal r(G ⊞ dud_D), 0 differ, re-solved by the referee K15b with the independent solver `ref3` against its own predictor
     (CHECKED-2); 640 random-context positions equal it too, 0 differ (COMPUTED-1); chess at cap 1: five of six contexts agree exactly, the sixth (two racing
     passers) is undecided for one side to move.
   - *K15's census (COMPUTED-1 for the counts, CHECKED-2 for the labels).* Dud groups (dud in the empty context in plain P) in ranges of ≤ 3 + 2 to ≤ 4 + 4 pawns
     on 3 to 5 files. Counted from the whole closures by the referee K15b (own solver; a group = a connected set of dud closures; up to file translation, mirror and
     colour flip): 24 on cyl:7×6, 23 on cyl:8×6, 14 on cyl:8×8 and 7 on flat 7×6 (74, 68, 40 and 10 before the symmetry reduction). K15's own counts (43, 40, 25
     and 9) are not invariants: K15 merged closures by their smallest state and then reduced one representative root by symmetry. All 108 listed groups of
     `kings/delegate/out/K15/fin2/dud_groups.md` are dud in plain P by K15b's classifier, and exactly those marked A+B are dud against free passes. Beside
     contexts the 18 groups that are dud also against free passes all equal dud_D; of the 41 that are dud only in plain P, 7 do not (for example
     `Ka2 kc4 Pa4 Pc2 pa5 pc3` on cyl:8×6, no root passer, the file mirror of Z_C; with `Pe2 pe3` beside it all four king states are W, CHECKED-2 by K15b).
     "Dud in the empty context" is therefore necessary, not sufficient; that the free-pass reading is sufficient is a CONJECTURE.
   - *How the two fit.* The counts are of different classes and do not contradict each other: K26 counts exact placements on F_Z = {a, b, c} with at most
     3 + 2 pawns, K15 counts plain-P dud groups, most of them with larger closures (for example D2 below), more pawns or more files. K15's list contains Z_B
     (cyl:7×6 and cyl:8×6) and Z_C (cyl:8×6 #38), and G8a, G8b lie outside K26's search. A check of the listed six-rank groups against the exact definition
     (`kings/delegate/out/K15K26/MERGE_NOTES.md`) finds no exact 3-file group with at most 3 + 2 pawns in K15's list other than Z_B and Z_C.
   - *Chess is not P.* D2 `Ka1 ka4 Pb4 Pc3 pb3 pc4` and D2m `Ka1 ka6 Pa3 Pb4 pa4 pb3` (cyl:7×6) are (D, D) in chess at cap 1, but 52 of the 108 deviations that
     lose in P draw in chess (COMPUTED-1, K15), so they are not two-shuttle in chess. Z_C alone has bounds (W, L) at cap 1 (K26). Z_B on the cylinder: bounds (W, L) at
     cap 1 on cyl:7×6 (K15; cyl:8×6 not run).
   - *Over, none found.* See Conjecture 4.7: no exact over or under group (Definition 4.8) in K26's ranges, no structural over or under root against free passes in
     K15's ranges, and every over candidate of K15 (a tempo-signature search, the near-over groups) is refuted beside contexts but one placement without a context file.
   - *Open:* more files and pawns (beyond 5 files and K15's pawn limits for dud and over; beyond F_Z = {a, b, c}, a–d and 3 + 2 pawns for K26's exact search),
     F_Z elsewhere on a flat board, kings off the group files, officers, chess (contexts of Z_B, Z_C; the cylinder groups beyond G8a, G8b), hand proofs on the
     cylinder, cyl:8×8 beside contexts.
   (After K14 and its referee, and after K27 and its referee, 2026-10-27: on the flat 7×6 board Z_B
   of §5.7 has every non-shuttle move losing by force in P, PROVED by hand (K27), CHECKED-2 for the computations; a search
   of flat 7×6 (F_Z = {a, b, c}, ≤ 2 + 2 pawns, no cut-off) found exactly
   two such placements, mirror images, among 817,270, COMPUTED-1 (CHECKED-2 after K26 and its referee, above). Beside every context tested its P-result equals that of
   dud_D (COMPUTED-1; 225 of 885 contexts untested; exhaustive contexts of at most 3 pawns on files e–g, CHECKED-2, K26). K14's own search had a move-count cut-off (18), which excluded Z_B,
   so its negative statements are withdrawn. In chess Z_B is not exactly two-shuttle (K28 and its referee, 2026-10-28, CHECKED-2: 25 of the 26
   deviations lose, Kc3–d2 from (c3, b5) draws). Open: chess contexts of Z_B, other boards.)
>>>>>>> NEW

### EDIT Appendix A group search
<<<<<<< OLD
  - no dud and no over group. (This scratch search covered the cylinders only. K14 repeated the dud search on the 7×6
    cylinder and the flat 7×6 and 7×7 boards with kpsolve as the filter, with a move-count cut-off (18), which excluded
    Z_B (§5.7); its negative result is withdrawn. A search of flat 7×6 without the cut-off found Z_B.)
=======
  - no dud and no over group. **Withdrawn (revised after K15, K26 and their referees, 2026-10-27):** false for dud groups on the cylinder: K26 found Z_B and Z_C
    on cyl:8×6 and Z_B on cyl:7×6, and K15's census found these and G8a, G8b (§5.7, §8 item 2). This scratch search used one-ply tests and its script was not kept.
    One-ply tests of that kind label Z_B "other" and find none of the 41 dud roots of flat 7×6 (K15's `oneply.py`; K15's first classifier of this kind could never
    output dud, because a shuttle needed a frozen opponent), so the statement was no evidence. "No over group" is replaced by Conjecture 4.7 as restated after
    K15 and K26 (no exact over group of Definition 4.8 and no structural over root against free passes in the ranges searched).
    (Also: this scratch search covered the cylinders only. K14 repeated the dud search on the 7×6
    cylinder and the flat 7×6 and 7×7 boards with kpsolve as the filter, with a move-count cut-off (18), which excluded
    Z_B (§5.7); its negative result is withdrawn. A search of flat 7×6 without the cut-off found Z_B.)
>>>>>>> NEW
