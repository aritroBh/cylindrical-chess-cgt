# K26 proposed edits to kings/theory/LOOPY.md

Each OLD text occurs exactly once in LOOPY.md as it stood when this file was written (checked by `scripts/build_edits.py --check-only`).

### EDIT 5.7 Z_B on other boards, Z_C, contexts (new, K26)
<<<<<<< OLD
  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact, and 225
    of the 885 contexts are untested. It is open on the cylinder and on other boards.
=======
  - **Other boards and the cylinder (new, K26, 2026-10-27). The searches COMPUTED-1, the 8 roots and their move lists CHECKED-2 (kpp and ref3m).**
    Z_B has total leak count 0 (every non-shuttle move loses at once in P, at all 8 roots) on cyl:7×6, cyl:8×6 and flat 8×6,
    and on every six-rank board that was tried: flat width 5, 7, 8, 9, 10, 12 and cylinder width 5 to 12 (width 9 and more: ref3m only,
    COMPUTED-1). It fails on 5, 7 and 8 ranks (8 to 13 leaks; flat 7×7, 7×5 and 8×8, cyl 8×5, 6×7 to 9×7, 8×8). On cyl:7×6 it has two more
    legal Black moves, Ka4–g3 and Ka4–g5 (the wrap), and the mirror has Ka3–g2 and Ka3–g4. They lose at once as well. K27's 26 certificates
    do not cover them, so Z_B is **not PROVED** exact on the cylinder.
    The search of K26 (`kings/delegate/out/K26/`; F_Z = {a, b, c}, no cut-off; at most 2 + 2 pawns, then 3 + 2 and 2 + 3; 817,270 placements for 2 + 2
    and 1,886,421 for 3 + 2 and 2 + 3) finds exactly Z_B and its mirror on flat 7×6, flat 8×6 and cyl:7×6. For 2 + 2 this is CHECKED-2: a second
    enumerator and a second solver (ref3m) agree on 2.4 to 2.8 million root move lists per board, 0 differences. On flat 7×7 no placement has
    leak count 0 (the minimum is 1; COMPUTED-1).
  - **A second exact group, Z_C (new, K26, 2026-10-27).** On cyl:8×6 the search also finds White king c2/c3 (shuttle), Black king a4/a5 (shuttle), pawns
    Pa2 Pc4 / pa3 pc5, and its colour mirror. All four pawns are blocked, so no pawn can move, and it has no textbook passer. Every king move off the
    shuttles loses at once at all 8 roots (CHECKED-2). It is exact alone only on cyl:8×6 and cyl:9×6: it has 8 leaks on cyl:6×6, 7×6, 10×6, 11×6 and 12×6, 12 on cyl:5×6
    and 16 on every flat board of six ranks and on flat 7×7. In chess with cap 1 the bounds of Z_C alone are (W, L) at all 8 roots (kpsolve, COMPUTED-1), so chess is open for it. It is **not** a two-shuttle component beside contexts: with at most 3 context pawns on files e–g of cyl:8×6, 131 of 2,049 contexts give
    a P-result different from r(G ⊞ dud_D). One of the smallest is Pe2 pe3, where P is (W, W) at all 8 roots, because Kc2–d3 wins there (it loses alone). So (Pun) fails for Z_C
    beside a pawn that its king can reach (COMPUTED-1).
  - **Contexts beside Z_B (new, K26, 2026-10-27). COMPUTED-1** (kpp; the sampled runs were partly re-solved with ref3, 0 mismatches). Every placement of at most 3
    context pawns of either colour on ranks 2 to H−1: cyl:8×6, files e–g: 2,049 contexts, 0 differ from r(G ⊞ dud_D); cyl:7×6, files e–f: 577 contexts, 0 differ;
    flat 7×6, files e–g: 2,049 contexts: 0 differ. (Each context at 8 roots.)
  - *CONJECTURE* that Z_B is exactly two-shuttle in P in every context. Not proved: (Pun) is a per-context fact. It holds in every context tried (the K14 and K27
    families and the exhaustive families above; revised after K26, 2026-10-27). Open: a hand proof on the cylinder, chess, other contexts.
>>>>>>> NEW

### EDIT 5.3 scratch evidence withdrawn
<<<<<<< OLD
- *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. This is the earlier scratch search on the cylinders only, with
    one-ply tests, not re-run; it says nothing about flat boards, where Z_B exists (§5.7). "dud may not occur in small
    K+P groups" remains a CONJECTURE for chess and for the cylinder.
=======
- *Scratch evidence (withdrawn; revised after K26, 2026-10-27):* the earlier scratch statement "no both-sides-shuttle group without a pawn
    break exists among 3-file groups with ≤ 2 + 2 pawns and no passer on the 8×6 cylinder" is **false**. K26 searched exhaustively, with no cut-off
    (§5.7): on cyl:8×6 the group Z_C (Pa2 Pc4 / pa3 pc5, kings c2/c3 and a4/a5) has no textbook passer, no pawn that can move, and every non-shuttle
    move loses at once at all 8 roots in P (CHECKED-2). Z_B of §5.7 also works on cyl:7×6 and cyl:8×6. "dud may not occur in small K+P groups" is
    therefore refuted in P on the cylinder and remains open in chess.
>>>>>>> NEW

### EDIT 3 loopy kings bullet tail
<<<<<<< OLD
(cap 2), the cylinder, other boards (§8, item 2). Z_A (§5.7) has one White break.
=======
(cap 2). On the cylinder Z_B and a passer-free group Z_C are exact at the 8 roots in P (CHECKED-2, §5.7; new, K26, 2026-10-27), and Z_C
  is not exact beside every context. Z_A (§5.7) has one White break.
>>>>>>> NEW

### EDIT status table P3.2′ row tail
<<<<<<< OLD
Open: chess (those five deviations, cap 2), the cylinder, other boards. Z_A (§5.7) is a second group, with one White break (Kxb4).
=======
Open: chess (those five deviations, cap 2). On the cylinder, Z_B and a passer-free group Z_C are exact at the 8 roots in P, and Z_B equals dud_D in every context tried (K26; §5.7; COMPUTED-1; revised after K26, 2026-10-27). Z_A (§5.7) is a second group, with one White break (Kxb4).
>>>>>>> NEW

### EDIT 7 downgraded dud bullet tail
<<<<<<< OLD
and the cylinder and other boards are open.)
=======
and see §5.7 for the cylinder and other boards: in P Z_B and Z_C work on cyl:8×6 (K26; revised after K26, 2026-10-27).)
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
   2 + 2 pawns is CHECKED-2 on flat 7×6, flat 8×6, cyl:7×6 and cyl:8×6 (second enumerator, second solver), and COMPUTED-1 for 3 + 2, 2 + 3 and flat 7×7 (no exact
   dud there; minimum leak count 1). No hand proof on the cylinder. Z_B equals dud_D in all 2,049 + 577 + 2,049 contexts of at most 3 pawns tried; Z_C does not (131 of 2,049).
   Over groups: no exact over or under (Definition 4.8) was found in any searched range (Conjecture 4.7). Wider searches: not done (more than 4 files, more than 3 + 2 pawns, F_Z elsewhere on a flat board).
   (After K14
>>>>>>> NEW

### EDIT 8 item 2 tail
<<<<<<< OLD
CHECKED-2; five are not settled at cap 1, among them Kc3–d2 with bounds (D, L); cap 2 not run), the cylinder, other boards.)
=======
CHECKED-2; five are not settled at cap 1, among them Kc3–d2 with bounds (D, L); cap 2 not run). Chess on the cylinder and on the other boards is open as well.)
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
- (U3) after each freeze, a position q, White to move has a legal move and every legal White move loses at once;
- (U4) the same q with Black to move: Black has a legal move and every legal Black move loses at once. So q is a mutual zugzwang, the position 0_D of Definition 4.4.
The colour mirror (ranks flipped, colours swapped) is an *exact over group*. Dropping (U4) gives a *loose* under group: after the freeze only White is in zugzwang.

**Lemma 4.9 (no king freeze). PROVED** (new, K26, 2026-10-27). In an exact under group no freeze is a king move that captures nothing.
*Proof.* Let m be such a freeze, b0 → b1, and q the position after it. In q Black can play b1 → b0: b0 is empty, no White pawn attacks it (K1), and it is not
next to the White king, which has not moved (K2). The result is the root with White to move. By (U2) and (U3) the other Black-to-move root has a freeze to a position of
value L (a White loss), so that root has value L. By (U1) every non-shuttle White move at the first root loses at once, and the shuttle leads to the second root, value L.
So the first root has value L, the move b1 → b0 does not lose at once, and (U4) fails. ∎ So a freeze of an exact group is a pawn move or a king capture of a group pawn.

- **CONJECTURE 4.7 (revised after K26, 2026-10-27; tested in P, COMPUTED-1):** no exact over group (Definition 4.8) with ≤ 2 + 2 pawns fits on 3 files of the 8×6
  cylinder, but over is realisable on the cylinder with wider groups.
  - *First half: supported.* K26 searched with no cut-off: F_Z = {a, b, c}, every placement of the kings and of at most 2 + 2, then 3 + 2 and 2 + 3 pawns
    (`kings/delegate/out/K26/scripts/over2.py` and `over3.py`). It found **no** exact under or over group on cyl:8×6 (631,179 placements for 2 + 2; 1,602,414 for 3 + 2; 1,517,293 for 2 + 3).
    It found none for 2 + 2 on cyl:7×6, flat 7×6 and flat 8×6 either.
  - Placements with (U1), (U2) and value L after every freeze, at all four roots: 144,159 on cyl:8×6 for 2 + 2 (without the king filter).
    Of these, 141,293 fail (U4) and 2,866 have a promotion as the freeze. A promotion is a decisive event, not a group move.
  - *Second half: no support, not refuted.* The search with four files (a–d) and at most 2 + 2 pawns (5,793,156 placements; 66,476 pass the king filter and (U1)–(U3) at one root, 55,331 at all four roots) found no exact group.
    So "realisable with wider groups" is neither supported nor refuted.
  - *Loose* groups are plentiful. With exactly one freeze at every root there are 120 on cyl:8×6 (2 + 2, 3 files), 142 on flat 7×6, 118 on cyl:7×6 and 626 on cyl:8×6 with four files.
    Beside contexts Proposition 4.6 holds in 762 of the 768 premise roots tested. So they are not over_D. The six failures were not diagnosed.
  - The earlier scratch search is replaced by this one (Appendix A). *To settle:* wider groups (more files, more pawns), then kpsolve.
>>>>>>> NEW

### EDIT Appendix A group search bullet
<<<<<<< OLD
  - no dud and no over group. (This scratch search covered the cylinders only. K14 repeated the dud search on the 7×6
=======
  - no dud and no over group. (**False for dud groups on the cylinder**: K26 (2026-10-27) found Z_B and Z_C on cyl:8×6 and Z_B on cyl:7×6 (§5.7); the statement "no over group" is
    replaced by Conjecture 4.7 as revised after K26, which refers to exact over groups. This scratch search covered the cylinders only. K14 repeated the dud search on the 7×6
>>>>>>> NEW

### EDIT status table C4.7 row
<<<<<<< OLD
| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched) | R1 item 10, R4 item 8 |
=======
| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched); exhaustive search in P by K26 (revised after K26, 2026-10-27): no exact over or under group (Definition 4.8) in ≤ 2 + 2, 3 + 2 and 2 + 3 pawns on 3 files of cyl:8×6 (and in ≤ 2 + 2 on cyl:7×6, flat 7×6 and 8×6), COMPUTED-1; Lemma 4.9 PROVED (no king freeze) | R1 item 10, R4 item 8; K26 |
>>>>>>> NEW

