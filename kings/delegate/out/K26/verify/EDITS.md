# K26 referee: replacement edits for kings/theory/LOOPY.md

Each OLD occurs exactly once in the current LOOPY.md (checked by `scripts/chk_edits.py EDITS.md`). They replace the blocks of the same label in `../EDITS.md`; the other seven blocks of `../EDITS.md` stand as written (their OLD blocks also occur once, and their NEW texts are accurate).
The tag date `2026-10-27` follows the task text.

### EDIT 5.7 Z_B on other boards, Z_C, contexts (new, K26)
<<<<<<< OLD
  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact, and 225
    of the 885 contexts are untested. It is open on the cylinder and on other boards.
=======
  - **Other boards and the cylinder (new, K26, 2026-10-27). The searches CHECKED-2 for at most 2 + 2 pawns and for 3 + 2 and 2 + 3 on flat 7×6, cyl:7×6 and cyl:8×6 (revised after the K26 referee, 2026-10-27), the 8 roots and their move lists CHECKED-2 (kpp and ref3m).**
    Z_B has total leak count 0 (every non-shuttle move loses at once in P, at all 8 roots) on cyl:7×6, cyl:8×6 and flat 8×6,
    and on every six-rank board that was tried: flat width 5, 7, 8, 9, 10 and cylinder width 5 to 10 (widths 9 and 10: ref3m only, COMPUTED-1; kpp stops at width 8).
    Widths 11 and 12 (66 and 72 squares) were also run, but ref3m keeps its pawn sets in 64-bit masks, so they are not claimed (revised after the K26 referee, 2026-10-27). It fails on 5, 7 and 8 ranks (8 to 13 leaks; flat 7×7, 7×5 and 8×8, cyl 8×5, 6×7 to 9×7, 8×8). On cyl:7×6 it has two more
    legal Black moves, Ka4–g3 and Ka4–g5 (the wrap), and the mirror has Ka3–g2 and Ka3–g4. They lose at once as well. K27's 26 certificates
    do not cover them, so Z_B is **not PROVED** exact on the cylinder.
    The search of K26 (`kings/delegate/out/K26/`; F_Z = {a, b, c}, no cut-off; at most 2 + 2 pawns, then 3 + 2 and 2 + 3; 817,270 placements for 2 + 2
    and 1,886,421 for 3 + 2 and 2 + 3) finds exactly Z_B and its mirror on flat 7×6, flat 8×6 (at most 2 + 2 pawns only) and cyl:7×6 (all three pawn limits; 3 + 2 and 2 + 3 were also searched on flat 7×6 and cyl:8×6). For 2 + 2 this is CHECKED-2: a second
    enumerator and a second solver (ref3m) agree on 2.4 to 2.8 million root move lists per board, 0 differences. The K26 referee's own enumerator (`kings/delegate/out/K26/verify/scripts/ref_enum.py`, ref3m only) reproduces the counts of total leaks 0, 1, 2 on all four boards and for 3 + 2 and 2 + 3 on flat 7×6, cyl:7×6 and cyl:8×6 (revised after the K26 referee, 2026-10-27). On flat 7×7 (at most 2 + 2 pawns only) no placement has
    leak count 0 (the minimum is 1, with 12 placements; CHECKED-2: the referee's own enumerator gives the same counts; revised after the K26 referee, 2026-10-27).
  - **A second exact group, Z_C (new, K26, 2026-10-27).** On cyl:8×6 the search also finds White king c2/c3 (shuttle), Black king a4/a5 (shuttle), pawns
    Pa2 Pc4 / pa3 pc5, and its colour mirror. All four pawns are blocked, so no pawn can move, and it has no textbook passer. Every king move off the
    shuttles loses at once at all 8 roots (CHECKED-2). Among the boards tried it is exact alone only on cyl:8×6 and cyl:9×6: it has 8 leaks on cyl:6×6, 7×6 and 10×6, 12 on cyl:5×6
    and 16 on every flat board of six ranks tried (width 5 to 10) and on flat 7×7 (its mirror has 6 there). In chess with cap 1 the bounds of Z_C alone are (W, L) at all 8 roots (kpsolve, COMPUTED-1), so chess is open for it. It is **not** a two-shuttle component beside contexts: with at most 3 context pawns on files e–g of cyl:8×6, 131 of 2,049 contexts (35 of the 264 with two pawns, 96 of the 1,760 with three, none with fewer; 754 of 16,392 roots) give
    a P-result different from r(G ⊞ dud_D) (CHECKED-2: K26's kpp and `dmodel.py`, and the referee's ref3m and its own predictor `verify/scripts/dud_ctx.py`, give the same counts; revised after the K26 referee, 2026-10-27). One of the smallest is Pe2 pe3, where P is (W, W) at all 8 roots, because Kc2–d3 wins there (it loses alone). So (Pun) fails for Z_C
    beside a pawn that its king can reach (CHECKED-2; revised after the K26 referee, 2026-10-27).
  - **Contexts beside Z_B (new, K26, 2026-10-27). CHECKED-2** (K26: kpp against its own D-model predictor `dmodel.py`; the K26 referee: ref3m against its own implementation of Theorem 3.4(a) with the e.p. flag, `verify/scripts/dud_ctx.py`; same result; revised after the K26 referee, 2026-10-27). Every placement of at most 3
    context pawns of either colour on ranks 2 to H−1: cyl:8×6, files e–g: 2,049 contexts, 0 differ from r(G ⊞ dud_D); cyl:7×6, files e–f: 577 contexts, 0 differ;
    flat 7×6, files e–g: 2,049 contexts: 0 differ. (Each context at 8 roots.) Files d and h (next to F_Z) were not tried.
  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact. It holds in every context tried (the K14 and K27
    families and the exhaustive families above; revised after K26, 2026-10-27). Open: a hand proof on the cylinder, chess, other contexts.
>>>>>>> NEW

### EDIT status table P3.2′ row tail
<<<<<<< OLD
Open: chess (those five deviations, cap 2), the cylinder, other boards. Z_A (§5.7) is a second group, with one White break (Kxb4).
=======
Open: chess (those five deviations, cap 2). On the cylinder, Z_B and a passer-free group Z_C are exact at the 8 roots in P, and Z_B equals dud_D in every context tried (K26; §5.7; CHECKED-2 for the exhaustive contexts of at most 3 pawns beside Z_B, COMPUTED-1 for the earlier samples; revised after K26 and its referee, 2026-10-27). Z_A (§5.7) is a second group, with one White break (Kxb4).
>>>>>>> NEW

### EDIT 8 item 2 question
<<<<<<< OLD
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist? Both
   need wider searches. (After K14
=======
2. Do both-sides-shuttle (dud) groups exist without a pawn break on the cylinder? Do over-groups exist?
   **Answered in part by K26 (P model; revised after K26, 2026-10-27).** Dud groups: yes. Z_B (§5.7) and a new passer-free group Z_C (Pa2 Pc4 / pa3 pc5, kings
   c2/c3 and a4/a5, every pawn blocked) have every non-shuttle move losing at once at all 8 roots on the cylinder: Z_B on cyl:7×6 and cyl:8×6 (and on every
   six-rank board tried), Z_C on cyl:8×6 and cyl:9×6. CHECKED-2 for the roots and move lists (kpp and ref3m); the exhaustive search of F_Z = {a, b, c} with at most
   2 + 2 pawns is CHECKED-2 on flat 7×6, flat 8×6, cyl:7×6 and cyl:8×6 (second enumerator, second solver, and the referee's third), CHECKED-2 for 3 + 2 and 2 + 3 on flat 7×6, cyl:7×6 and cyl:8×6 (the same groups, no new one), and CHECKED-2 for 2 + 2 on flat 7×7 (no exact dud there; minimum leak count 1) (revised after the K26 referee, 2026-10-27). No hand proof on the cylinder. Z_B equals dud_D in all 2,049 + 577 + 2,049 contexts of at most 3 pawns tried (CHECKED-2); Z_C does not (131 of 2,049, CHECKED-2).
   Over groups: no exact over or under (Definition 4.8) was found in any searched range (Conjecture 4.7). Wider searches: not done (more than 4 files, more than 3 + 2 pawns, F_Z elsewhere on a flat board).
   (After K14
>>>>>>> NEW

### EDIT 4.7 conjecture, definition 4.8, lemma 4.9
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
A promotion by Black is a decisive event, not a freeze to 0: a group in which some freeze is a promotion is not exact (such placements are counted separately below). (Rules for promotion, e.p. and check added after the K26 referee, 2026-10-27; they are what both searches did.)
The colour mirror (ranks flipped, colours swapped) is an *exact over group*. Dropping (U4) gives a *loose* under group: after the freeze only White is in zugzwang.

**Lemma 4.9 (no king freeze). PROVED** (new, K26, 2026-10-27). In an exact under group no freeze is a king move that captures nothing.
*Proof.* Let m be such a freeze, b0 → b1, and q the position after it. In q (with Black to move, a legal position by K1 for the White king's square) Black can play b1 → b0: b0 is empty, no White pawn attacks it (K1, the pawns have not moved), and it is not
next to the White king, which has not moved (K2). No e.p. right exists (no pawn moved). The result is the root with White to move. By (U2) and (U3) the other Black-to-move root has a freeze to a position of
value L (a White loss; if that freeze is a promotion, the root is a Black win at once), so that root has value L. By (U1) every non-shuttle White move at the first root loses at once, and the shuttle leads to the second root, value L.
So the first root has value L, the move b1 → b0 does not lose at once, and (U4) fails. ∎ So a freeze of an exact group is a pawn move or a king capture of a group pawn.

- **CONJECTURE 4.7 (revised after K26 and its referee, 2026-10-27; tested in P: CHECKED-2 for the searches on 3 files named below except flat 8×6, COMPUTED-1 for the four-file search):** no exact over group (Definition 4.8) with ≤ 2 + 2 pawns fits on 3 files of the 8×6
  cylinder, but over is realisable on the cylinder with wider groups.
  - *First half: supported.* K26 searched with no cut-off: F_Z = {a, b, c}, every placement of the kings and of at most 2 + 2, then 3 + 2 and 2 + 3 pawns
    (`kings/delegate/out/K26/scripts/over2.py` and `over3.py`). It found **no** exact under or over group on cyl:8×6 (631,179 placements for 2 + 2; 1,602,414 for 3 + 2; 1,517,293 for 2 + 3).
    It found none for 2 + 2 on cyl:7×6, flat 7×6 and flat 8×6 either. The K26 referee's own search (`verify/scripts/ref_under.py`, ref3m, no king filter, no use of Lemma 4.9) reproduces the 2 + 2 result on cyl:8×6, cyl:7×6 and flat 7×6 (CHECKED-2; flat 8×6 not repeated). The 3 + 2 and 2 + 3 runs on cyl:8×6 (1,602,414 and 1,517,293 placements) were repeated by the referee without the king filter: no exact group, and the counts of placements with (U1), (U2) and value L after every freeze are 254,258 and 545,277 (revised after the K26 referee, 2026-10-27). The four-file run was not repeated.
  - Placements with (U1), (U2) and value L after every freeze (a promotion counts as value L), at all four roots: 144,159 on cyl:8×6 for 2 + 2 (without the king filter), 144,411 on cyl:7×6, 140,389 on flat 7×6; the K26 referee's own enumerator with ref3m counts the same numbers (revised after the K26 referee, 2026-10-27).
    None is an exact group: each fails (U4) at some freeze or has a promotion as a freeze. The split between these two depends on the order in which the freezes are tried (K26: 141,293 and 2,866; referee: 143,831 and 328 on cyl:8×6); the sum does not. In 5,791 of the (U4) failures on cyl:8×6 the freezing pawn gives check.
  - *Second half: no support, not refuted.* The search with four files (a–d) and at most 2 + 2 pawns (5,793,156 placements; 66,476 pass the king filter and (U1)–(U3) at one root, 55,331 at all four roots) found no exact group.
    So "realisable with wider groups" is neither supported nor refuted.
  - *Loose* groups are plentiful. With exactly one freeze at every root there are 120 on cyl:8×6 (2 + 2, 3 files), 142 on flat 7×6, 118 on cyl:7×6 (all three CHECKED-2 by the referee's count) and 626 on cyl:8×6 with four files (reused from K26, not repeated).
    Beside contexts Proposition 4.6 holds in 537 of the 552 premise roots of K26's final sample (762 of 768 in an earlier sample); the failures were not diagnosed. Loose groups are not over_D anyway: after the freeze Black still has a move that does not lose.
  - The earlier scratch search is replaced by this one (Appendix A). *To settle:* wider groups (more files, more pawns), then kpsolve.
>>>>>>> NEW

### EDIT status table C4.7 row
<<<<<<< OLD
| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched) | R1 item 10, R4 item 8 |
=======
| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched); exhaustive search in P by K26 (revised after K26, 2026-10-27): no exact over or under group (Definition 4.8) in ≤ 2 + 2, 3 + 2 and 2 + 3 pawns on 3 files of cyl:8×6 (and in ≤ 2 + 2 on cyl:7×6, flat 7×6 and 8×6), CHECKED-2 for the 3-file searches except flat 8×6 (revised after the K26 referee, 2026-10-27), COMPUTED-1 for the four-file search; Lemma 4.9 PROVED (no king freeze) | R1 item 10, R4 item 8; K26 |
>>>>>>> NEW

