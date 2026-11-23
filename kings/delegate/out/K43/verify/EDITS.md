# K43 proposed edits to kings/theory/LOOPY.md (referee replacement set)

Replaces `kings/delegate/out/K43/EDITS.md`. Same four OLD texts; each occurs exactly once in LOOPY.md as it stood when this file was written.
Changes against the investigator's set: the four-file search is CHECKED-2 (the referee's own solver and test reproduce every counter);
Lemma 4.10 (3) gets the condition it needs (m legal at the other root); the second-implementation ranges are named (kings on the group files);
the near-miss count is corrected (6 king-and-pawn placements, 3 up to the file reflection, not "1 and 4 more"); the role of Lemma 4.10 for the
near misses is stated precisely; Lemma 4.11 is credited as the argument already used in the proof of Lemma 4.9.

### EDIT C4.7 status row (K43, 2026-11-22)
<<<<<<< OLD
Lemma 4.9 PROVED (no king freeze) | R1 item 10, R4 item 8; K15, K15b; K26 and its referee |
=======
Lemma 4.9 PROVED (no king freeze). K43 (2026-11-22): exhaustive search of the exact under/over test of Definition 4.8 (plain P) with every king placement anywhere, at most 3 + 3 pawns on four files, on cyl:6×6, 7×6, 8×6, 9×6 and flat 7×6 (windows a–d, b–e) and 8×6 (a–d, b–e, c–f; the other windows are file mirrors): 6,363,129,120 placements per orientation, **0 exact over and 0 exact under groups** (CHECKED-2: the K43 referee's own solver and test reproduce every counter of every board); Lemma 4.10 (a freeze cannot serve both roots) and Lemma 4.11 (every move at a root loses at once, closures reduce to pairs) PROVED | R1 item 10, R4 item 8; K15, K15b; K26 and its referee; K43 and its referee |
>>>>>>> NEW

### EDIT Conjecture 4.7 second half (K43, 2026-11-22)
<<<<<<< OLD
  - *Second half, CONJECTURE, no support:* nothing was found in either search, and the four-file search of K26 neither supports nor refutes it. "None exists"
    is not claimed: the boundary is at most 8 pawns, 5 files and the empty-context local game (K15), and F_Z = {a, b, c} with at most 3 + 2 or 2 + 3 pawns, or a–d with at most 2 + 2
    (under/over search only) (K26).
=======
  - *Second half, CONJECTURE, no support:* nothing was found in any search. "None exists" is not claimed: the boundary is at most 8 pawns, 5 files and the empty-context local game (K15), F_Z = {a, b, c} with at most 3 + 2 or 2 + 3 pawns, or a–d with at most 2 + 2
    (under/over search only) (K26), and at most 3 + 3 pawns on four files with six ranks (K43, next bullet).
  - *K43 (2026-11-22; `kings/delegate/out/K43/findings.txt`, `PROOF.md`, `VERIFY.md`; AI work, no human re-derivation; CHECKED-2).* A table solver of P (all placements of both kings, every pawn configuration of at most 3 + 3 pawns on four files, ranks 2 to H−1) tests the four roots of Definition 4.8
    (and of its colour mirror, the exact over group) for every placement with the kings anywhere. **0 exact under groups and 0 exact over groups** on cyl:6×6, 7×6, 8×6, 9×6, flat 7×6 (windows a–d, b–e; the others are mirrors) and flat 8×6 (a–d, b–e, c–f), 6,363,129,120 placements per orientation
    (with at most 3 + 3 pawns on four files this covers every smaller window). Loose groups ((U1) to (U3)) number 13.4 to 54.7 million per board and all fail (U4). Checks: the table equals ref3m on 17,200 random states (including cyl:8×7 and 8×8); the test reproduces K26's counts
    (631,179 placements, 120, 118, 142, 142 loose groups with one freeze); with the kings on the group files it equals K26's referee script with ref3m on three further ranges (63,378, 455,385 and 132 placements). The K43 referee's own solver and test (`kings/delegate/out/K43/verify/rv43.cpp`, written from SPEC.md and Definition 4.8) reproduce
    every counter of all nine boards ((U1), (U2), loose, loose with one freeze, exact) and K26's counts, and its table equals ref3m on the same 17,200 states and on 6,700 more. The under and over runs give identical counts. Not run: more than 3 + 3 pawns on four files, five files, other ranks.
    *Near misses.* On cyl:7×6 (3 files, 3 + 3) 40 loose placements per orientation are half-exact (one root has only zero freezes, the other not), 10 of them with exactly one freeze at each root: 6 king-and-pawn placements, 3 up to the file reflection, e.g. `Kb5 kg4 Pa4 Pc2 pa5 pc3 pc5` with shuttle b5–a6 or b5–b6 (ref3m re-check, CHECKED-2); none has two zero roots.
    In each the zero root's freeze is a Black pawn push and the other root's only freeze is a Black king move (a capture of a White pawn in 8 of the 10) whose q is not a zugzwang for Black; the push loses at once at the other root. Lemma 4.10's argument shows the push could not be a freeze satisfying (U4) there.
>>>>>>> NEW

### EDIT Lemmas 4.10 and 4.11 after Lemma 4.9 (K43, 2026-11-22)
<<<<<<< OLD
So a freeze of an exact group is a pawn move or a king capture of a group pawn.
=======
So a freeze of an exact group is a pawn move or a king capture of a group pawn.

**Lemma 4.10 (a freeze cannot serve both roots). PROVED** (new, K43, 2026-11-22; `kings/delegate/out/K43/PROOF.md`; re-derived by the K43 referee). Let G be an exact under group, m a freeze at the root (z_a, b_0, Black to move), q the position after m (White king on z_a, White to move), and suppose the shuttle z_a → z_(1−a) is legal in q.
Let q̂ be q after that shuttle (Black to move). Then (1) q̂ is a Black win; (2) m is not a freeze at the other root, and if it is legal there it loses at once, so the position after m from the other root (White king on z_(1−a), White to move) is a White win; (3) q is a zero, q̂ is a win for Black to move, and if m is legal at the other root the same position with White to move is a White win, so it is won by the player to move.
*Proof.* (1) By (U3) the shuttle loses at once. (2) If m were a freeze at the other root, (U4) there would make q̂ a White win, against (1); a legal non-freeze loses at once. (3) (U3), (U4), (1), (2). ∎ (m can be illegal at the other root only if it is a double step across z_(1−a).) The mechanics were checked on all 38 half-exact roots of cyl:7×6 (3 files, 3 + 3) that have only zero freezes and a legal shuttle in q: 0 violations (COMPUTED-1).

**Lemma 4.11 (the shuttle loses at once; closures reduce to pairs). PROVED** (new, K43, 2026-11-22; the argument is the one used in the proof of Lemma 4.9). In an exact under group every White move at a White-to-move root loses at once, the shuttle included: after the shuttle Black has a freeze whose q is lost for White ((U2), (U3)). So a set of White king squares with all the White-to-move and Black-to-move conditions of Definition 4.8 on every square (a larger closure) contains an exact adjacent pair, and a negative result of the pair search covers it. (Closures with White pawn moves inside the group are not covered.)

*Computable test (K43).* `kings/delegate/out/K43/plocalp3.cpp` (table solver of P for all king placements, 2 bits a state; `--mode under|over|both|dud`): for every pawn configuration, every adjacent pair of safe squares of the shuttling king and every safe square of the other king at distance at least 2 it applies (U1) to (U4) to the four roots; the exact over group is the same test with Black shuttling and White freezing. An independent implementation is `kings/delegate/out/K43/verify/rv43.cpp`.
>>>>>>> NEW

### EDIT Section 8 item 2 over bullet (K43, 2026-11-22)
<<<<<<< OLD
   - *Over, none found.* See Conjecture 4.7: no exact over or under group (Definition 4.8) in K26's ranges, no structural over or under root against free passes in
=======
   - *Over, none found; K43 (2026-11-22) extended the exact search.* 0 exact over and 0 exact under groups with at most 3 + 3 pawns on four files, every king placement, cyl:6×6 to 9×6, flat 7×6 and 8×6 (Conjecture 4.7, K43 bullet; CHECKED-2). See Conjecture 4.7: no exact over or under group (Definition 4.8) in K26's ranges, no structural over or under root against free passes in
>>>>>>> NEW
