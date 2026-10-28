# PROOF.md (K27): Z_B is exactly two-shuttle in the P model

Task K27, 2026-10-27. All squares, moves and positions below are on the **flat 7x6 board**, files a-g, ranks 1-6.
Labels: PROVED = a proof that can be checked by hand (it is also machine-checked, see section 9); CHECKED-2 = two independent
implementations agree; COMPUTED-1 = one implementation.

## 0. What is proved

**Theorem A (PROVED; also CHECKED-2 and re-checked by a third engine).** Let Z_B be the position type
`Kb2/Kc3` (White king, shuttling), `ka4/kb5` (Black king, shuttling), pawns `Pa3 Pb4 pb3 pc4`, flat 7x6, P model (first promotion
wins for the promoter; kings move normally; SPEC.md rules). At each of the 8 roots (4 king states x side to move)
1. the mover's shuttle step is legal (Lemma S), and it leads to another root;
2. every other legal move of the mover (26 moves in all) loses by force: the opponent promotes first (or mates) within at most
   11 plies after the move;
3. hence Z_B alone has value (D, D) at all 8 roots: neither side can win against a player who shuttles until the other
   deviates.

**Theorem B (PROVED, by a symmetry).** The mirror group `Ka3/Kb2, kb5/kc4, Pb4 Pc3 pa4 pb3` is the image of Z_B under
tau = "flip the ranks (r -> 7 - r), swap the colours, swap the side to move". tau is a symmetry of the P model and of chess on
the flat 7x6 board (not the file mirror a <-> c, which is *not* a symmetry because file a is an edge and file c is not). So
Theorem A holds for the mirror group with White and Black exchanged.

(The mirror is therefore not a new group: it is Z_B with the colours reversed. Z_B is invariant under sigma = tau followed by the
file reflection a <-> c (it maps Pa3, Pb4, pb3, pc4 to pc4, pb3, Pb4, Pa3 and the king squares {b2, c3}, {a4, b5} to {b5, a4}, {c3, b2}), which is why the file mirror
of Z_B equals tau(Z_B). sigma itself is only a local symmetry of the pawn and king-shuttle structure, not of the board, so it is
not used.)

## 1. Conventions

* White pawns move up and promote on rank 6; Black pawns move down and promote on rank 1. A pawn captures diagonally forward.
  A **White** pawn on (f, r) attacks (f -/+ 1, r + 1); a **Black** pawn on (f, r) attacks (f -/+ 1, r - 1). Pawn moves are written
  `a3-a4`; captures `Kxb3`; a move that gives check carries `+`.
* P model: the first promotion ends the game and is won by the promoter (to any piece). Checkmate is a loss for the side to
  move, stalemate a draw, a game that never ends a draw (SPEC.md, section Results). A *winning strategy* is therefore a
  strategy that forces a promotion by the winner (or mate) in finitely many moves.
* There are no sliders in this position class: a king is attacked only by an enemy pawn or by the enemy king, and a
  pawn move can never expose its own king. A move is legal iff the mover's king is not attacked afterwards. Kings are never
  adjacent. A king may not capture a pawn that is protected (by a pawn or by the other king).
* **No en passant ever arises.** An e.p. capture needs a pawn that has just made a double step. A double step starts on the
  pawn's second rank (rank 2 for White, rank 5 for Black). In every position reachable from Z_B White pawns stand on ranks
  3 or higher and Black pawns on ranks 4 or lower (pawns never move backwards, captures are forward), so no double step is
  possible, and all positions in this proof have e.p. target `-`.
* Positions are written `White pieces | Black pieces`, e.g. `Kb2 Pa3 Pb4 | ka4 pb3 pc4`.

## 2. Z_B

White king shuttle squares {b2, c3}; Black king shuttle squares {a4, b5}; static pawns `Pa3 Pb4 pb3 pc4`. The eight roots are
the 4 king states (b2,a4), (b2,b5), (c3,a4), (c3,b5) with White or Black to move. Pawn squares: `a3` and `b4` are White, `b3` and `c4` Black.
Attacks of the pawns: pb3 attacks a2 and c2; pc4 attacks b3 and d3; Pa3 attacks b4; Pb4 attacks a5 and c5.

## 3. The shuttle (hand proof)

**(K1)** None of the four king squares b2, c3, a4, b5 is attacked by an enemy pawn: the Black pawns attack a2, c2, b3, d3, the
White pawns attack b4, a5, c5; none of the four squares occurs. None of them is occupied by a pawn.
**(K2)** In each of the four combined king states the kings are at (Chebyshev) distance at least 2:
d(b2,a4) = 2, d(b2,b5) = 3, d(c3,a4) = 2, d(c3,b5) = 2.

**Lemma S.** At each of the 8 roots the mover has a legal shuttle step (White b2 <-> c3, Black a4 <-> b5), and the result
is again a root with the other side to move.
*Proof.* The squares b2 and c3 are adjacent (diagonal), and so are a4 and b5. Let X be the mover and X' the other shuttle square of X's king.
X' is empty (the only pieces are the four pawns and the two kings, and X' is not a pawn square nor the opponent king's square);
by (K1) it is not attacked by an enemy pawn; by (K2) applied to the combined state after the step, it is not adjacent to the enemy king.
Hence the step is legal, and the new position has the same pawns, kings on shuttle squares, so it is a root. Moreover at a root
the mover is not in check by (K1), (K2), so it is not mated; having a legal move, it is not stalemated. QED

