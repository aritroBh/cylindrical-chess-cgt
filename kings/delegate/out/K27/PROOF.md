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


## 4. The legal moves at the eight roots

Each root is listed with every legal move of the side to move (the shuttle and the other moves) and, in brackets, the reasons why the other moves a reader might expect are illegal. A pawn that stands next to the other king does not protect itself: a king may not capture a pawn that is protected by a pawn or is adjacent to the other king.

- Z1. Kb2 Pa3 Pb4 | ka4 pb3 pc4 -- White to move. Shuttle Kb2-c3. Other legal moves (all of them): Kb2-a1, Kb2-b1, Kb2-c1, b4-b5. [Kb2 cannot go to a2 attacked by pb3; a3 own pawn; b3 next to k; c2 attacked by pb3; Pa3 is blocked by ka4]
- Z2. Kb2 Pa3 Pb4 | ka4 pb3 pc4 -- Black to move. Shuttle Ka4-b5. Other legal moves (all of them): c4-c3. [ka4 cannot go to a3 next to K; a5 attacked by Pb4; b3 own pawn; b4 attacked by Pa3; pb3 is blocked by Kb2]
- Z3. Kb2 Pa3 Pb4 | kb5 pb3 pc4 -- White to move. Shuttle Kb2-c3. Other legal moves (all of them): Kb2-a1, Kb2-b1, Kb2-c1, a3-a4. [Kb2 cannot go to a2 attacked by pb3; a3 own pawn; b3 attacked by pc4; c2 attacked by pb3; Pb4 is blocked by kb5]
- Z4. Kb2 Pa3 Pb4 | kb5 pb3 pc4 -- Black to move. Shuttle Kb5-a4. Other legal moves (all of them): Kb5-a6, Kb5-b6, Kb5-c6, c4-c3. [kb5 cannot go to a5 attacked by Pb4; b4 attacked by Pa3; c4 own pawn; c5 attacked by Pb4; pb3 is blocked by Kb2]
- Z5. Kc3 Pa3 Pb4 | ka4 pb3 pc4 -- White to move. Shuttle Kc3-b2. Other legal moves (all of them): Kc3xc4, Kc3-d2, Kc3-d4, b4-b5. [Kc3 cannot go to b3 next to k; b4 own pawn; c2 attacked by pb3; d3 attacked by pc4; Pa3 is blocked by ka4]
- Z6. Kc3 Pa3 Pb4 | ka4 pb3 pc4 -- Black to move. Shuttle Ka4-b5. Other legal moves (all of them): Ka4xa3, b3-b2. [ka4 cannot go to a5 attacked by Pb4; b3 own pawn; b4 next to K; pc4 is blocked by Kc3]
- Z7. Kc3 Pa3 Pb4 | kb5 pb3 pc4 -- White to move. Shuttle Kc3-b2. Other legal moves (all of them): Kc3-d2, Kc3-d4, a3-a4. [Kc3 cannot go to b3 attacked by pc4; b4 own pawn; c2 attacked by pb3; c4 next to k; d3 attacked by pc4; Pb4 is blocked by kb5]
- Z8. Kc3 Pa3 Pb4 | kb5 pb3 pc4 -- Black to move. Shuttle Kb5-a4. Other legal moves (all of them): Kb5-a6, Kb5-b6, Kb5-c6, b3-b2. [kb5 cannot go to a5 attacked by Pb4; b4 next to K; c4 own pawn; c5 attacked by Pb4; pc4 is blocked by Kc3]

That is 4 + 4 + 4 + 3 = 15 White non-shuttle moves (roots Z1, Z3, Z5, Z7) and 1 + 4 + 2 + 4 = 11 Black ones (Z2, Z4, Z6, Z8), 26 in all. (The task text and K14 say 27; the solver move lists, kpp and ref3m, and this list all give 26.)

## 5. How to read the certificates (what has to be checked by hand)

A *certificate* for "X wins at position x with X to move" is a list of entries. Each entry is a position with the side to
move (the winner X), the move X plays (**bold**), and the complete list of the replies of the opponent, each followed by
`->` another entry, or "X wins by <promotion>". There are three kinds of entry: N (replies lead to further entries), R (every
reply is answered by an immediate promotion), and leaves "X wins by p-p=Q". To check an entry by hand:
1. the position is the one reached by the entry that points to it;
2. X's move is legal (mover's king is not attacked afterwards);
3. the list of replies is complete (the bracket after each entry says why the other king moves and pawn moves are illegal:
   squares attacked by a named pawn, squares next to the other king, own pawn, a pawn blocked by a piece, a king in check);
4. each leaf is a legal promotion: the pawn is on its last-but-one rank, its square ahead is empty (or an enemy pawn stands diagonally
   ahead), and X's king is not attacked after the reply (no reply of the opponent attacks it, the only possible checks being those
   noted with `+` and answered in the entry).
The number `d` on an entry is the number of plies, counted from the entry and including X's move, after which X has promoted
(or mated) if the entry is played. Along every arrow `d` decreases by at least 2, so the entries form a finite acyclic
structure and the induction on `d` proves: **X, playing the listed moves, promotes first.** (Mate does not occur in any
certificate; stalemate cannot occur, because every list of replies is non-empty.)


## 6. The 26 deviations

Entries are written `N<k>` (a node whose replies are listed and lead to further entries or to a promotion), `R<k>` (a node whose replies all allow an immediate promotion). Square lists "cannot go to" are the reasons for the exclusion of moves. `d` is the number of plies, counted from the entry and including the winner's next move, within which the winner promotes (or mates): along every arrow `d` drops by at least 2.

#### C01. Root Z1, move Kb2-a1. Position after the move: `Ka1 Pa3 Pb4 ka4 pb3 pc4 b -`

*Idea.* The king gives up the blockade of c3. Black plays c4-c3, and the pair b3+c3 beats a king on the first rank. White has no counterplay: Pa3 is blocked by ka4, and b4-b5 only delays (the king takes it, or the pair goes on).

Certificate (4 entries; the winner is Black):

- N1. Ka1 Pa3 Pb4 | ka4 pb3 pc4 -- Black to move [d=7]: **c4-c3**. White replies: Ka1-b1: ->N2; b4-b5: ->N4. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3; Pa3 is blocked by ka4]
- N2. Kb1 Pa3 Pb4 | ka4 pb3 pc3 -- Black to move [d=5]: **b3-b2**. White replies: Kb1-a2, Kb1-c2: Black wins by b2-b1=Q; b4-b5: ->R3. [Kb1 cannot go to a1 attacked by pb2; b2 attacked by pc3; c1 attacked by pb2; Pa3 is blocked by ka4]
- R3. Kb1 Pa3 Pb5 | ka4 pb2 pc3 -- Black to move [d=3]: **c3-c2+**. White replies: Kb1-a2: Black wins by b2-b1=Q; Kb1xb2: Black wins by c2-c1=Q; Kb1xc2: Black wins by b2-b1=Q. [in check from pc2: only king moves and captures of the checking pawn are legal; Kb1 cannot go to a1 attacked by pb2; c1 attacked by pb2]
- N4. Ka1 Pa3 Pb5 | ka4 pb3 pc3 -- Black to move [d=5]: **b3-b2+**. White replies: Ka1-a2: Black wins by b2-b1=Q; Ka1-b1: ->R3. [in check from pb2: only king moves and captures of the checking pawn are legal; Ka1 cannot go to b2 attacked by pc3]

#### C02. Root Z1, move Kb2-b1. Position after the move: `Kb1 Pa3 Pb4 ka4 pb3 pc4 b -`

*Idea.* As above.

Certificate (5 entries; the winner is Black):

- N1. Kb1 Pa3 Pb4 | ka4 pb3 pc4 -- Black to move [d=7]: **c4-c3**. White replies: Kb1-a1: ->R2; Kb1-c1: ->N3; b4-b5: ->N5. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3; Pa3 is blocked by ka4]
- R2. Ka1 Pa3 Pb4 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2, b4-b5: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2; Pa3 is blocked by ka4]
- N3. Kc1 Pa3 Pb4 | ka4 pb3 pc3 -- Black to move [d=5]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q; b4-b5: ->R4. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2; Pa3 is blocked by ka4]
- R4. Kc1 Pa3 Pb5 | ka4 pc2 pb3 -- Black to move [d=3]: **b3-b2+**. White replies: Kc1xb2: Black wins by c2-c1=Q; Kc1xc2, Kc1-d2: Black wins by b2-b1=Q. [in check from pb2: only king moves and captures of the checking pawn are legal; Kc1 cannot go to b1 attacked by pc2; d1 attacked by pc2]
- N5. Kb1 Pa3 Pb5 | ka4 pb3 pc3 -- Black to move [d=5]: **c3-c2+**. White replies: Kb1-a1, Kb1-b2: Black wins by c2-c1=Q; Kb1-c1: ->R4. [in check from pc2: only king moves and captures of the checking pawn are legal; Kb1 cannot go to a2 attacked by pb3; c2 attacked by pb3]

#### C03. Root Z1, move Kb2-c1. Position after the move: `Kc1 Pa3 Pb4 ka4 pb3 pc4 b -`

*Idea.* As above.

Certificate (5 entries; the winner is Black):

- N1. Kc1 Pa3 Pb4 | ka4 pb3 pc4 -- Black to move [d=7]: **c4-c3**. White replies: Kc1-b1: ->N2; Kc1-d1: ->R4; b4-b5: ->N5. [Kc1 cannot go to b2 attacked by pc3; c2 attacked by pb3; d2 attacked by pc3; Pa3 is blocked by ka4]
- N2. Kb1 Pa3 Pb4 | ka4 pb3 pc3 -- Black to move [d=5]: **b3-b2**. White replies: Kb1-a2, Kb1-c2: Black wins by b2-b1=Q; b4-b5: ->R3. [Kb1 cannot go to a1 attacked by pb2; b2 attacked by pc3; c1 attacked by pb2; Pa3 is blocked by ka4]
- R3. Kb1 Pa3 Pb5 | ka4 pb2 pc3 -- Black to move [d=3]: **c3-c2+**. White replies: Kb1-a2: Black wins by b2-b1=Q; Kb1xb2: Black wins by c2-c1=Q; Kb1xc2: Black wins by b2-b1=Q. [in check from pc2: only king moves and captures of the checking pawn are legal; Kb1 cannot go to a1 attacked by pb2; c1 attacked by pb2]
- R4. Kd1 Pa3 Pb4 | ka4 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kd1-c2, Kd1-e1, Kd1-e2, b4-b5: Black wins by b2-b1=Q. [Kd1 cannot go to c1 attacked by pb2; d2 attacked by pc3; Pa3 is blocked by ka4]
- N5. Kc1 Pa3 Pb5 | ka4 pb3 pc3 -- Black to move [d=5]: **b3-b2+**. White replies: Kc1-b1: ->R3; Kc1-c2, Kc1-d1: Black wins by b2-b1=Q. [in check from pb2: only king moves and captures of the checking pawn are legal; Kc1 cannot go to b2 attacked by pc3; d2 attacked by pc3]

#### C04. Root Z1, move b4-b5. Position after the move: `Kb2 Pa3 Pb5 ka4 pb3 pc4 b -`

*Idea.* b4-b5 is captured, Ka4xb5: White has lost a pawn. Black then threatens c4-c3, b3-b2 and Ka4xa3 and the White king cannot meet them all; the Black king uses its shuttle as a waiting move (Kb5-a4) where that puts White in zugzwang. a3-a4+ only costs Black one capture.

Certificate (37 entries; the winner is Black):

- N1. Kb2 Pa3 Pb5 | ka4 pb3 pc4 -- Black to move [d=11]: **Ka4xb5**. White replies: Kb2-a1: ->N2; Kb2-b1: ->N8; Kb2-c1: ->N16; Kb2-c3: ->N21; a3-a4+: ->N31. [Kb2 cannot go to a2 attacked by pb3; a3 own pawn; b3 attacked by pc4; c2 attacked by pb3]
- N2. Ka1 Pa3 | kb5 pb3 pc4 -- Black to move [d=7]: **c4-c3**. White replies: Ka1-b1: ->N3; a3-a4+: ->N6. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3]
- N3. Kb1 Pa3 | kb5 pb3 pc3 -- Black to move [d=5]: **Kb5-a4**. White replies: Kb1-a1: ->R4; Kb1-c1: ->R5. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3; Pa3 is blocked by ka4]
- R4. Ka1 Pa3 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2; Pa3 is blocked by ka4]
- R5. Kc1 Pa3 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2; Pa3 is blocked by ka4]
- N6. Ka1 Pa4 | kb5 pb3 pc3 -- Black to move [d=5]: **Kb5xa4**. White replies: Ka1-b1: ->R7. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3]
- R7. Kb1 | ka4 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kb1-a2, Kb1-c2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; b2 attacked by pc3; c1 attacked by pb2]
- N8. Kb1 Pa3 | kb5 pb3 pc4 -- Black to move [d=7]: **c4-c3**. White replies: Kb1-a1: ->N9; Kb1-c1: ->N11; a3-a4+: ->N13. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- N9. Ka1 Pa3 | kb5 pb3 pc3 -- Black to move [d=5]: **Kb5-a4**. White replies: Ka1-b1: ->R10. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3; Pa3 is blocked by ka4]
- R10. Kb1 Pa3 | ka4 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kb1-a2, Kb1-c2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; b2 attacked by pc3; c1 attacked by pb2; Pa3 is blocked by ka4]
- N11. Kc1 Pa3 | kb5 pb3 pc3 -- Black to move [d=5]: **Kb5-a4**. White replies: Kc1-b1: ->R10; Kc1-d1: ->R12. [Kc1 cannot go to b2 attacked by pc3; c2 attacked by pb3; d2 attacked by pc3; Pa3 is blocked by ka4]
- R12. Kd1 Pa3 | ka4 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kd1-c2, Kd1-e1, Kd1-e2: Black wins by b2-b1=Q. [Kd1 cannot go to c1 attacked by pb2; d2 attacked by pc3; Pa3 is blocked by ka4]
- N13. Kb1 Pa4 | kb5 pb3 pc3 -- Black to move [d=5]: **Kb5xa4**. White replies: Kb1-a1: ->R14; Kb1-c1: ->R15. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- R14. Ka1 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2]
- R15. Kc1 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- N16. Kc1 Pa3 | kb5 pb3 pc4 -- Black to move [d=7]: **c4-c3**. White replies: Kc1-b1: ->N3; Kc1-d1: ->N17; a3-a4+: ->N19. [Kc1 cannot go to b2 attacked by pc3; c2 attacked by pb3; d2 attacked by pc3]
- N17. Kd1 Pa3 | kb5 pb3 pc3 -- Black to move [d=5]: **c3-c2+**. White replies: Kd1-c1: ->R18; Kd1-d2, Kd1-e1, Kd1-e2: Black wins by c2-c1=Q. [in check from pc2: only king moves and captures of the checking pawn are legal; Kd1 cannot go to c2 attacked by pb3]
- R18. Kc1 Pa3 | kb5 pc2 pb3 -- Black to move [d=3]: **Kb5-a4**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2; Pa3 is blocked by ka4]
- N19. Kc1 Pa4 | kb5 pb3 pc3 -- Black to move [d=5]: **Kb5xa4**. White replies: Kc1-b1: ->R7; Kc1-d1: ->R20. [Kc1 cannot go to b2 attacked by pc3; c2 attacked by pb3; d2 attacked by pc3]
- R20. Kd1 | ka4 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kd1-c2, Kd1-e1, Kd1-e2: Black wins by b2-b1=Q. [Kd1 cannot go to c1 attacked by pb2; d2 attacked by pc3]
- N21. Kc3 Pa3 | kb5 pb3 pc4 -- Black to move [d=9]: **Kb5-a4**. White replies: Kc3-b2: ->N22; Kc3xc4: ->R28; Kc3-d2: ->R29; Kc3-d4: ->R30. [Kc3 cannot go to b3 next to k; b4 next to k; c2 attacked by pb3; d3 attacked by pc4; Pa3 is blocked by ka4]
- N22. Kb2 Pa3 | ka4 pb3 pc4 -- Black to move [d=7]: **c4-c3+**. White replies: Kb2-a1: ->R4; Kb2-b1: ->R10; Kb2-c1: ->R5; Kb2xc3: ->N23. [in check from pc3: only king moves and captures of the checking pawn are legal; Kb2 cannot go to a2 attacked by pb3; a3 own pawn; b3 next to k; c2 attacked by pb3]
- N23. Kc3 Pa3 | ka4 pb3 -- Black to move [d=5]: **Ka4xa3**. White replies: Kc3-c4: ->R24; Kc3-d2: ->R25; Kc3-d3: ->R26; Kc3-d4: ->R27. [Kc3 cannot go to b2 next to k; b3 next to k; b4 next to k; c2 attacked by pb3]
- R24. Kc4 | ka3 pb3 -- Black to move [d=3]: **b3-b2**. White replies: Kc4-b5, Kc4-c3, Kc4-c5, Kc4-d3, Kc4-d4, Kc4-d5: Black wins by b2-b1=Q. [Kc4 cannot go to b3 next to k; b4 next to k]
- R25. Kd2 | ka3 pb3 -- Black to move [d=3]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-d3, Kd2-e1, Kd2-e2, Kd2-e3: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2]
- R26. Kd3 | ka3 pb3 -- Black to move [d=3]: **b3-b2**. White replies: Kd3-c2, Kd3-c3, Kd3-c4, Kd3-d2, Kd3-d4, Kd3-e2, Kd3-e3, Kd3-e4: Black wins by b2-b1=Q.
- R27. Kd4 | ka3 pb3 -- Black to move [d=3]: **b3-b2**. White replies: Kd4-c3, Kd4-c4, Kd4-c5, Kd4-d3, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5: Black wins by b2-b1=Q.
- R28. Kc4 Pa3 | ka4 pb3 -- Black to move [d=3]: **b3-b2**. White replies: Kc4-c3, Kc4-c5, Kc4-d3, Kc4-d4, Kc4-d5: Black wins by b2-b1=Q. [Kc4 cannot go to b3 next to k; b4 next to k; b5 next to k; Pa3 is blocked by ka4]
- R29. Kd2 Pa3 | ka4 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4; Pa3 is blocked by ka4]
- R30. Kd4 Pa3 | ka4 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd4-c3, Kd4xc4, Kd4-c5, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5: Black wins by b2-b1=Q. [Kd4 cannot go to d3 attacked by pc4; Pa3 is blocked by ka4]
- N31. Kb2 Pa4 | kb5 pb3 pc4 -- Black to move [d=7]: **Kb5xa4**. White replies: Kb2-a1: ->N32; Kb2-b1: ->N33; Kb2-c1: ->N34; Kb2-c3: ->N35. [Kb2 cannot go to a2 attacked by pb3; a3 next to k; b3 next to k; c2 attacked by pb3]
- N32. Ka1 | ka4 pb3 pc4 -- Black to move [d=5]: **c4-c3**. White replies: Ka1-b1: ->R7. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3]
- N33. Kb1 | ka4 pb3 pc4 -- Black to move [d=5]: **c4-c3**. White replies: Kb1-a1: ->R14; Kb1-c1: ->R15. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- N34. Kc1 | ka4 pb3 pc4 -- Black to move [d=5]: **c4-c3**. White replies: Kc1-b1: ->R7; Kc1-d1: ->R20. [Kc1 cannot go to b2 attacked by pc3; c2 attacked by pb3; d2 attacked by pc3]
- N35. Kc3 | ka4 pb3 pc4 -- Black to move [d=5]: **Ka4-a3**. White replies: Kc3xc4: ->R24; Kc3-d2: ->R36; Kc3-d4: ->R37. [Kc3 cannot go to b2 next to k; b3 next to k; b4 next to k; c2 attacked by pb3; d3 attacked by pc4]
- R36. Kd2 | ka3 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4]
- R37. Kd4 | ka3 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd4-c3, Kd4xc4, Kd4-c5, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5: Black wins by b2-b1=Q. [Kd4 cannot go to d3 attacked by pc4]

#### C05. Root Z2, move c4-c3. Position after the move: `Kb2 Pa3 Pb4 ka4 pb3 pc3 w -`

*Idea.* c4-c3 is captured, Kb2xc3 (c3 is not protected): Black has lost a pawn. If Kxa3 then b4-b5 runs and promotes (the Black king is too far); if b3-b2 then Kxb2; if Kb5 then Kc3xb3 and the king and pawns win.

Certificate (13 entries; the winner is White):

- N1. Kb2 Pa3 Pb4 | ka4 pb3 pc3 -- White to move [d=11]: **Kb2xc3**. Black replies: Ka4xa3: ->R2; Ka4-b5: ->N3; b3-b2: ->N12. [ka4 cannot go to a5 attacked by Pb4; b3 own pawn; b4 next to K]
- R2. Kc3 Pb4 | ka3 pb3 -- White to move [d=3]: **b4-b5**. Black replies: Ka3-a2, Ka3-a4, b3-b2: White wins by b5-b6=Q. [ka3 cannot go to b2 next to K; b3 own pawn; b4 next to K]
- N3. Kc3 Pa3 Pb4 | kb5 pb3 -- White to move [d=7]: **Kc3xb3**. Black replies: Kb5-a6: ->N4; Kb5-b6: ->N6; Kb5-c6: ->N9. [kb5 cannot go to a4 next to K; a5 attacked by Pb4; b4 next to K; c4 next to K; c5 attacked by Pb4]
- N4. Kb3 Pa3 Pb4 | ka6 -- White to move [d=5]: **Kb3-a4**. Black replies: Ka6-b6: ->R5. [ka6 cannot go to a5 next to K; b5 next to K]
- R5. Ka4 Pa3 Pb4 | kb6 -- White to move [d=3]: **b4-b5**. Black replies: Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a5 next to K; a6 attacked by Pb5; b5 next to K; c6 attacked by Pb5]
- N6. Kb3 Pa3 Pb4 | kb6 -- White to move [d=5]: **a3-a4**. Black replies: Kb6-a6: ->R7; Kb6-c6: ->R8. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4]
- R7. Kb3 Pa4 Pb4 | ka6 -- White to move [d=3]: **a4-a5**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5]
- R8. Kb3 Pa4 Pb4 | kc6 -- White to move [d=3]: **a4-a5**. Black replies: Kc6-b5, Kc6-d5, Kc6-d6: White wins by a5-a6=Q. [kc6 cannot go to b6 attacked by Pa5; c5 attacked by Pb4]
- N9. Kb3 Pa3 Pb4 | kc6 -- White to move [d=5]: **Kb3-c4**. Black replies: Kc6-b6: ->R10; Kc6-d6: ->R11. [kc6 cannot go to b5 next to K; c5 next to K; d5 next to K]
- R10. Kc4 Pa3 Pb4 | kb6 -- White to move [d=3]: **b4-b5**. Black replies: Kb6-a5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 next to K; c5 next to K; c6 attacked by Pb5]
- R11. Kc4 Pa3 Pb4 | kd6 -- White to move [d=3]: **b4-b5**. Black replies: Kd6-e5, Kd6-e6: White wins by b5-b6=Q. [kd6 cannot go to c5 next to K; c6 attacked by Pb5; d5 next to K]
- N12. Kc3 Pa3 Pb4 | ka4 pb2 -- White to move [d=9]: **Kc3xb2**. Black replies: Ka4-b5: ->N13. [ka4 cannot go to a3 next to K; a5 attacked by Pb4; b3 next to K; b4 attacked by Pa3]
- N13. Kb2 Pa3 Pb4 | kb5 -- White to move [d=7]: **Kb2-b3**. Black replies: Kb5-a6: ->N4; Kb5-b6: ->N6; Kb5-c6: ->N9. [kb5 cannot go to a4 next to K; a5 attacked by Pb4; b4 next to K; c4 next to K; c5 attacked by Pb4]

#### C06. Root Z3, move Kb2-a1. Position after the move: `Ka1 Pa3 Pb4 kb5 pb3 pc4 b -`

*Idea.* Black king on b5. The same plan c4-c3; the only extra resource of White is the check a3-a4+, which Black answers by capturing (Kxa4, or Kxb4 when that wins faster).

Certificate (9 entries; the winner is Black):

- N1. Ka1 Pa3 Pb4 | kb5 pb3 pc4 -- Black to move [d=9]: **c4-c3**. White replies: Ka1-b1: ->N2; a3-a4+: ->N4. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3; Pb4 is blocked by kb5]
- N2. Kb1 Pa3 Pb4 | kb5 pb3 pc3 -- Black to move [d=5]: **c3-c2+**. White replies: Kb1-a1, Kb1-b2: Black wins by c2-c1=Q; Kb1-c1: ->R3. [in check from pc2: only king moves and captures of the checking pawn are legal; Kb1 cannot go to a2 attacked by pb3; c2 attacked by pb3]
- R3. Kc1 Pa3 Pb4 | kb5 pc2 pb3 -- Black to move [d=3]: **b3-b2+**. White replies: Kc1xb2: Black wins by c2-c1=Q; Kc1xc2, Kc1-d2: Black wins by b2-b1=Q. [in check from pb2: only king moves and captures of the checking pawn are legal; Kc1 cannot go to b1 attacked by pc2; d1 attacked by pc2]
- N4. Ka1 Pa4 Pb4 | kb5 pb3 pc3 -- Black to move [d=7]: **Kb5xa4**. White replies: Ka1-b1: ->N5; b4-b5: ->N8. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3]
- N5. Kb1 Pb4 | ka4 pb3 pc3 -- Black to move [d=5]: **Ka4xb4**. White replies: Kb1-a1: ->R6; Kb1-c1: ->R7. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- R6. Ka1 | kb4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2]
- R7. Kc1 | kb4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- N8. Ka1 Pb5 | ka4 pb3 pc3 -- Black to move [d=5]: **Ka4xb5**. White replies: Ka1-b1: ->R9. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3]
- R9. Kb1 | kb5 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kb1-a2, Kb1-c2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; b2 attacked by pc3; c1 attacked by pb2]

#### C07. Root Z3, move Kb2-b1. Position after the move: `Kb1 Pa3 Pb4 kb5 pb3 pc4 b -`

*Idea.* As above.

Certificate (10 entries; the winner is Black):

- N1. Kb1 Pa3 Pb4 | kb5 pb3 pc4 -- Black to move [d=9]: **c4-c3**. White replies: Kb1-a1: ->N2; Kb1-c1: ->N4; a3-a4+: ->N6. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3; Pb4 is blocked by kb5]
- N2. Ka1 Pa3 Pb4 | kb5 pb3 pc3 -- Black to move [d=5]: **c3-c2**. White replies: Ka1-b2: Black wins by c2-c1=Q; a3-a4+: ->R3. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2; Pb4 is blocked by kb5]
- R3. Ka1 Pa4 Pb4 | kb5 pc2 pb3 -- Black to move [d=3]: **Kb5xa4**. White replies: Ka1-b2, b4-b5: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2]
- N4. Kc1 Pa3 Pb4 | kb5 pb3 pc3 -- Black to move [d=5]: **b3-b2+**. White replies: Kc1-b1: ->R5; Kc1-c2, Kc1-d1: Black wins by b2-b1=Q. [in check from pb2: only king moves and captures of the checking pawn are legal; Kc1 cannot go to b2 attacked by pc3; d2 attacked by pc3]
- R5. Kb1 Pa3 Pb4 | kb5 pb2 pc3 -- Black to move [d=3]: **c3-c2+**. White replies: Kb1-a2: Black wins by b2-b1=Q; Kb1xb2: Black wins by c2-c1=Q; Kb1xc2: Black wins by b2-b1=Q. [in check from pc2: only king moves and captures of the checking pawn are legal; Kb1 cannot go to a1 attacked by pb2; c1 attacked by pb2]
- N6. Kb1 Pa4 Pb4 | kb5 pb3 pc3 -- Black to move [d=7]: **Kb5xa4**. White replies: Kb1-a1: ->R7; Kb1-c1: ->N8; b4-b5: ->N10. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- R7. Ka1 Pb4 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2, b4-b5: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2]
- N8. Kc1 Pb4 | ka4 pb3 pc3 -- Black to move [d=5]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q; b4-b5: ->R9. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- R9. Kc1 Pb5 | ka4 pc2 pb3 -- Black to move [d=3]: **Ka4xb5**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- N10. Kb1 Pb5 | ka4 pb3 pc3 -- Black to move [d=5]: **c3-c2+**. White replies: Kb1-a1, Kb1-b2: Black wins by c2-c1=Q; Kb1-c1: ->R9. [in check from pc2: only king moves and captures of the checking pawn are legal; Kb1 cannot go to a2 attacked by pb3; c2 attacked by pb3]

#### C08. Root Z3, move Kb2-c1. Position after the move: `Kc1 Pa3 Pb4 kb5 pb3 pc4 b -`

*Idea.* As above.

Certificate (11 entries; the winner is Black):

- N1. Kc1 Pa3 Pb4 | kb5 pb3 pc4 -- Black to move [d=9]: **c4-c3**. White replies: Kc1-b1: ->N2; Kc1-d1: ->N4; a3-a4+: ->N5. [Kc1 cannot go to b2 attacked by pc3; c2 attacked by pb3; d2 attacked by pc3; Pb4 is blocked by kb5]
- N2. Kb1 Pa3 Pb4 | kb5 pb3 pc3 -- Black to move [d=5]: **c3-c2+**. White replies: Kb1-a1, Kb1-b2: Black wins by c2-c1=Q; Kb1-c1: ->R3. [in check from pc2: only king moves and captures of the checking pawn are legal; Kb1 cannot go to a2 attacked by pb3; c2 attacked by pb3]
- R3. Kc1 Pa3 Pb4 | kb5 pc2 pb3 -- Black to move [d=3]: **b3-b2+**. White replies: Kc1xb2: Black wins by c2-c1=Q; Kc1xc2, Kc1-d2: Black wins by b2-b1=Q. [in check from pb2: only king moves and captures of the checking pawn are legal; Kc1 cannot go to b1 attacked by pc2; d1 attacked by pc2]
- N4. Kd1 Pa3 Pb4 | kb5 pb3 pc3 -- Black to move [d=5]: **c3-c2+**. White replies: Kd1-c1: ->R3; Kd1-d2, Kd1-e1, Kd1-e2: Black wins by c2-c1=Q. [in check from pc2: only king moves and captures of the checking pawn are legal; Kd1 cannot go to c2 attacked by pb3]
- N5. Kc1 Pa4 Pb4 | kb5 pb3 pc3 -- Black to move [d=7]: **Kb5xa4**. White replies: Kc1-b1: ->N6; Kc1-d1: ->R9; b4-b5: ->N10. [Kc1 cannot go to b2 attacked by pc3; c2 attacked by pb3; d2 attacked by pc3]
- N6. Kb1 Pb4 | ka4 pb3 pc3 -- Black to move [d=5]: **Ka4xb4**. White replies: Kb1-a1: ->R7; Kb1-c1: ->R8. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- R7. Ka1 | kb4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2]
- R8. Kc1 | kb4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- R9. Kd1 Pb4 | ka4 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kd1-c2, Kd1-e1, Kd1-e2, b4-b5: Black wins by b2-b1=Q. [Kd1 cannot go to c1 attacked by pb2; d2 attacked by pc3]
- N10. Kc1 Pb5 | ka4 pb3 pc3 -- Black to move [d=5]: **b3-b2+**. White replies: Kc1-b1: ->R11; Kc1-c2, Kc1-d1: Black wins by b2-b1=Q. [in check from pb2: only king moves and captures of the checking pawn are legal; Kc1 cannot go to b2 attacked by pc3; d2 attacked by pc3]
- R11. Kb1 Pb5 | ka4 pb2 pc3 -- Black to move [d=3]: **Ka4xb5**. White replies: Kb1-a2, Kb1-c2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; b2 attacked by pc3; c1 attacked by pb2]

#### C09. Root Z3, move a3-a4. Position after the move: `Kb2 Pa4 Pb4 kb5 pb3 pc4 b -`

*Idea.* a3-a4+ is a check; Black takes the other pawn, Kb5xb4 (not Kxa4). Black has won a pawn and again has b3+c4 against the king, with Pa4 harmless.

Certificate (17 entries; the winner is Black):

- N1. Kb2 Pa4 Pb4 | kb5 pb3 pc4 -- Black to move [d=9]: **Kb5xb4**. White replies: Kb2-a1: ->N2; Kb2-b1: ->N8; Kb2-c1: ->N13; a4-a5: ->N17. [Kb2 cannot go to a2 attacked by pb3; a3 next to k; b3 next to k; c2 attacked by pb3; c3 next to k]
- N2. Ka1 Pa4 | kb4 pb3 pc4 -- Black to move [d=7]: **c4-c3**. White replies: Ka1-b1: ->N3; a4-a5: ->N6. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3]
- N3. Kb1 Pa4 | kb4 pb3 pc3 -- Black to move [d=5]: **Kb4xa4**. White replies: Kb1-a1: ->R4; Kb1-c1: ->R5. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- R4. Ka1 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2]
- R5. Kc1 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- N6. Ka1 Pa5 | kb4 pb3 pc3 -- Black to move [d=5]: **Kb4xa5**. White replies: Ka1-b1: ->R7. [Ka1 cannot go to a2 attacked by pb3; b2 attacked by pc3]
- R7. Kb1 | ka5 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kb1-a2, Kb1-c2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; b2 attacked by pc3; c1 attacked by pb2]
- N8. Kb1 Pa4 | kb4 pb3 pc4 -- Black to move [d=7]: **c4-c3**. White replies: Kb1-a1: ->R9; Kb1-c1: ->N10; a4-a5: ->N12. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- R9. Ka1 Pa4 | kb4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2, a4-a5: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2]
- N10. Kc1 Pa4 | kb4 pb3 pc3 -- Black to move [d=5]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q; a4-a5: ->R11. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- R11. Kc1 Pa5 | kb4 pc2 pb3 -- Black to move [d=3]: **Kb4xa5**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- N12. Kb1 Pa5 | kb4 pb3 pc3 -- Black to move [d=5]: **c3-c2+**. White replies: Kb1-a1, Kb1-b2: Black wins by c2-c1=Q; Kb1-c1: ->R11. [in check from pc2: only king moves and captures of the checking pawn are legal; Kb1 cannot go to a2 attacked by pb3; c2 attacked by pb3]
- N13. Kc1 Pa4 | kb4 pb3 pc4 -- Black to move [d=7]: **c4-c3**. White replies: Kc1-b1: ->N3; Kc1-d1: ->R14; a4-a5: ->N15. [Kc1 cannot go to b2 attacked by pc3; c2 attacked by pb3; d2 attacked by pc3]
- R14. Kd1 Pa4 | kb4 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kd1-c2, Kd1-e1, Kd1-e2, a4-a5: Black wins by b2-b1=Q. [Kd1 cannot go to c1 attacked by pb2; d2 attacked by pc3]
- N15. Kc1 Pa5 | kb4 pb3 pc3 -- Black to move [d=5]: **b3-b2+**. White replies: Kc1-b1: ->R16; Kc1-c2, Kc1-d1: Black wins by b2-b1=Q. [in check from pb2: only king moves and captures of the checking pawn are legal; Kc1 cannot go to b2 attacked by pc3; d2 attacked by pc3]
- R16. Kb1 Pa5 | kb4 pb2 pc3 -- Black to move [d=3]: **Kb4xa5**. White replies: Kb1-a2, Kb1-c2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; b2 attacked by pc3; c1 attacked by pb2]
- N17. Kb2 Pa5 | kb4 pb3 pc4 -- Black to move [d=7]: **c4-c3+**. White replies: Kb2-a1: ->N6; Kb2-b1: ->N12; Kb2-c1: ->N15. [in check from pc3: only king moves and captures of the checking pawn are legal; Kb2 cannot go to a2 attacked by pb3; a3 next to k; b3 next to k; c2 attacked by pb3; c3 next to k]

#### C10. Root Z4, move Kb5-a6. Position after the move: `Kb2 Pa3 Pb4 ka6 pb3 pc4 w -`

*Idea.* The Black king leaves the b5/a4 guard. White's pawns a3, b4 march (a3-a4, a4-a5+, b4-b5+), supported by the king; Black's c4-c3+ and b3 are captured by the king with tempo.

Certificate (8 entries; the winner is White):

- N1. Kb2 Pa3 Pb4 | ka6 pb3 pc4 -- White to move [d=9]: **a3-a4**. Black replies: Ka6-b6: ->N2; c4-c3+: ->N4. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; pb3 is blocked by Kb2]
- N2. Kb2 Pa4 Pb4 | kb6 pb3 pc4 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R3; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]
- R3. Kb2 Pb4 Pa5 | ka6 pb3 pc4 -- White to move [d=3]: **b4-b5+**. Black replies: Ka6xa5: White wins by b5-b6=Q; Ka6xb5: White wins by a5-a6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; ka6 cannot go to b6 attacked by Pa5]
- N4. Kb2 Pa4 Pb4 | ka6 pb3 pc3 -- White to move [d=7]: **Kb2xb3**. Black replies: Ka6-b6: ->N5; c3-c2: ->N7. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4]
- N5. Kb3 Pa4 Pb4 | kb6 pc3 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R6; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]
- R6. Kb3 Pb4 Pa5 | ka6 pc3 -- White to move [d=3]: **Kb3-c2**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5; pc3 is blocked by Kc2]
- N7. Kb3 Pa4 Pb4 | ka6 pc2 -- White to move [d=5]: **Kb3xc2**. Black replies: Ka6-b6: ->R8. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4]
- R8. Kc2 Pa4 Pb4 | kb6 -- White to move [d=3]: **b4-b5**. Black replies: Kb6-a5, Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 attacked by Pa4; c6 attacked by Pb5]

#### C11. Root Z4, move Kb5-b6. Position after the move: `Kb2 Pa3 Pb4 kb6 pb3 pc4 w -`

*Idea.* As above.

Certificate (10 entries; the winner is White):

- N1. Kb2 Pa3 Pb4 | kb6 pb3 pc4 -- White to move [d=9]: **a3-a4**. Black replies: Kb6-a6: ->N2; Kb6-c6: ->N4; c4-c3+: ->N5. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4; pb3 is blocked by Kb2]
- N2. Kb2 Pa4 Pb4 | ka6 pb3 pc4 -- White to move [d=5]: **b4-b5+**. Black replies: Ka6-a5: White wins by b5-b6=Q; Ka6-b6: ->R3. [in check from Pb5: only king moves and captures of the checking pawn are legal; ka6 cannot go to b5 attacked by Pa4]
- R3. Kb2 Pa4 Pb5 | kb6 pb3 pc4 -- White to move [d=3]: **a4-a5+**. Black replies: Kb6xa5: White wins by b5-b6=Q; Kb6xb5, Kb6-c5: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a6 attacked by Pb5; c6 attacked by Pb5]
- N4. Kb2 Pa4 Pb4 | kc6 pb3 pc4 -- White to move [d=5]: **b4-b5+**. Black replies: Kc6-b6: ->R3; Kc6-c5, Kc6-d5, Kc6-d6: White wins by b5-b6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; kc6 cannot go to b5 attacked by Pa4]
- N5. Kb2 Pa4 Pb4 | kb6 pb3 pc3 -- White to move [d=7]: **Kb2xb3**. Black replies: Kb6-a6: ->N6; Kb6-c6: ->R8; c3-c2: ->N9. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4]
- N6. Kb3 Pa4 Pb4 | ka6 pc3 -- White to move [d=5]: **Kb3-c2**. Black replies: Ka6-b6: ->R7. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; pc3 is blocked by Kc2]
- R7. Kc2 Pa4 Pb4 | kb6 pc3 -- White to move [d=3]: **b4-b5**. Black replies: Kb6-a5, Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 attacked by Pa4; c6 attacked by Pb5; pc3 is blocked by Kc2]
- R8. Kb3 Pa4 Pb4 | kc6 pc3 -- White to move [d=3]: **a4-a5**. Black replies: Kc6-b5, Kc6-d5, Kc6-d6, c3-c2: White wins by a5-a6=Q. [kc6 cannot go to b6 attacked by Pa5; c5 attacked by Pb4]
- N9. Kb3 Pa4 Pb4 | kb6 pc2 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R10; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]
- R10. Kb3 Pb4 Pa5 | ka6 pc2 -- White to move [d=3]: **Kb3xc2**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5]

#### C12. Root Z4, move Kb5-c6. Position after the move: `Kb2 Pa3 Pb4 kc6 pb3 pc4 w -`

*Idea.* As above.

Certificate (14 entries; the winner is White):

- N1. Kb2 Pa3 Pb4 | kc6 pb3 pc4 -- White to move [d=9]: **a3-a4**. Black replies: Kc6-b6: ->N2; Kc6-d5: ->N4; Kc6-d6: ->N6; c4-c3+: ->N8. [kc6 cannot go to b5 attacked by Pa4; c5 attacked by Pb4; pb3 is blocked by Kb2]
- N2. Kb2 Pa4 Pb4 | kb6 pb3 pc4 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R3; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]
- R3. Kb2 Pb4 Pa5 | ka6 pb3 pc4 -- White to move [d=3]: **b4-b5+**. Black replies: Ka6xa5: White wins by b5-b6=Q; Ka6xb5: White wins by a5-a6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; ka6 cannot go to b6 attacked by Pa5]
- N4. Kb2 Pa4 Pb4 | kd5 pb3 pc4 -- White to move [d=5]: **a4-a5**. Black replies: Kd5-c6, Kd5-d4, Kd5-d6, Kd5-e4, Kd5-e5, Kd5-e6: White wins by a5-a6=Q; c4-c3+: ->R5. [kd5 cannot go to c4 own pawn; c5 attacked by Pb4; pb3 is blocked by Kb2]
- R5. Kb2 Pb4 Pa5 | kd5 pb3 pc3 -- White to move [d=3]: **Kb2xc3**. Black replies: Kd5-c6, Kd5-d6, Kd5-e4, Kd5-e5, Kd5-e6, b3-b2: White wins by a5-a6=Q. [kd5 cannot go to c4 next to K; c5 attacked by Pb4; d4 next to K]
- N6. Kb2 Pa4 Pb4 | kd6 pb3 pc4 -- White to move [d=5]: **a4-a5**. Black replies: Kd6-c6, Kd6-d5, Kd6-e5, Kd6-e6: White wins by a5-a6=Q; c4-c3+: ->R7. [kd6 cannot go to c5 attacked by Pb4; pb3 is blocked by Kb2]
- R7. Kb2 Pb4 Pa5 | kd6 pb3 pc3 -- White to move [d=3]: **Kb2xc3**. Black replies: Kd6-c6, Kd6-d5, Kd6-e5, Kd6-e6, b3-b2: White wins by a5-a6=Q. [kd6 cannot go to c5 attacked by Pb4]
- N8. Kb2 Pa4 Pb4 | kc6 pb3 pc3 -- White to move [d=7]: **Kb2xc3**. Black replies: Kc6-b6: ->N9; Kc6-d5: ->R11; Kc6-d6: ->R12; b3-b2: ->N13. [kc6 cannot go to b5 attacked by Pa4; c5 attacked by Pb4]
- N9. Kc3 Pa4 Pb4 | kb6 pb3 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R10; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]
- R10. Kc3 Pb4 Pa5 | ka6 pb3 -- White to move [d=3]: **Kc3-b2**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5; pb3 is blocked by Kb2]
- R11. Kc3 Pa4 Pb4 | kd5 pb3 -- White to move [d=3]: **a4-a5**. Black replies: Kd5-c6, Kd5-d6, Kd5-e4, Kd5-e5, Kd5-e6, b3-b2: White wins by a5-a6=Q. [kd5 cannot go to c4 next to K; c5 attacked by Pb4; d4 next to K]
- R12. Kc3 Pa4 Pb4 | kd6 pb3 -- White to move [d=3]: **a4-a5**. Black replies: Kd6-c6, Kd6-d5, Kd6-e5, Kd6-e6, b3-b2: White wins by a5-a6=Q. [kd6 cannot go to c5 attacked by Pb4]
- N13. Kc3 Pa4 Pb4 | kc6 pb2 -- White to move [d=5]: **b4-b5+**. Black replies: Kc6-b6: ->R14; Kc6-c5, Kc6-d5, Kc6-d6: White wins by b5-b6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; kc6 cannot go to b5 attacked by Pa4]
- R14. Kc3 Pa4 Pb5 | kb6 pb2 -- White to move [d=3]: **Kc3xb2**. Black replies: Kb6-a5, Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 attacked by Pa4; c6 attacked by Pb5]

#### C13. Root Z4, move c4-c3. Position after the move: `Kb2 Pa3 Pb4 kb5 pb3 pc3 w -`

*Idea.* c4-c3 is answered by Kb2xb3 (b3 lost its protector when the pawn left c4, and the Black king b5 does not guard it); the king then also deals with the c-pawn while the two White pawns run.

Certificate (17 entries; the winner is White):

- N1. Kb2 Pa3 Pb4 | kb5 pb3 pc3 -- White to move [d=9]: **Kb2xb3**. Black replies: Kb5-a6: ->N2; Kb5-b6: ->N7; Kb5-c6: ->N12; c3-c2: ->N17. [kb5 cannot go to a4 next to K; a5 attacked by Pb4; b4 next to K; c4 next to K; c5 attacked by Pb4]
- N2. Kb3 Pa3 Pb4 | ka6 pc3 -- White to move [d=7]: **a3-a4**. Black replies: Ka6-b6: ->N3; c3-c2: ->N5. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4]
- N3. Kb3 Pa4 Pb4 | kb6 pc3 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R4; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]
- R4. Kb3 Pb4 Pa5 | ka6 pc3 -- White to move [d=3]: **Kb3-c2**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5; pc3 is blocked by Kc2]
- N5. Kb3 Pa4 Pb4 | ka6 pc2 -- White to move [d=5]: **Kb3xc2**. Black replies: Ka6-b6: ->R6. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4]
- R6. Kc2 Pa4 Pb4 | kb6 -- White to move [d=3]: **b4-b5**. Black replies: Kb6-a5, Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 attacked by Pa4; c6 attacked by Pb5]
- N7. Kb3 Pa3 Pb4 | kb6 pc3 -- White to move [d=7]: **a3-a4**. Black replies: Kb6-a6: ->N8; Kb6-c6: ->R10; c3-c2: ->N11. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4]
- N8. Kb3 Pa4 Pb4 | ka6 pc3 -- White to move [d=5]: **a4-a5**. Black replies: Ka6-b5: White wins by a5-a6=Q; c3-c2: ->R9. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5]
- R9. Kb3 Pb4 Pa5 | ka6 pc2 -- White to move [d=3]: **Kb3xc2**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5]
- R10. Kb3 Pa4 Pb4 | kc6 pc3 -- White to move [d=3]: **a4-a5**. Black replies: Kc6-b5, Kc6-d5, Kc6-d6, c3-c2: White wins by a5-a6=Q. [kc6 cannot go to b6 attacked by Pa5; c5 attacked by Pb4]
- N11. Kb3 Pa4 Pb4 | kb6 pc2 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R9; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]
- N12. Kb3 Pa3 Pb4 | kc6 pc3 -- White to move [d=7]: **a3-a4**. Black replies: Kc6-b6: ->N3; Kc6-d5: ->R13; Kc6-d6: ->R14; c3-c2: ->N15. [kc6 cannot go to b5 attacked by Pa4; c5 attacked by Pb4]
- R13. Kb3 Pa4 Pb4 | kd5 pc3 -- White to move [d=3]: **a4-a5**. Black replies: Kd5-c6, Kd5-d4, Kd5-d6, Kd5-e4, Kd5-e5, Kd5-e6, c3-c2: White wins by a5-a6=Q. [kd5 cannot go to c4 next to K; c5 attacked by Pb4]
- R14. Kb3 Pa4 Pb4 | kd6 pc3 -- White to move [d=3]: **a4-a5**. Black replies: Kd6-c6, Kd6-d5, Kd6-e5, Kd6-e6, c3-c2: White wins by a5-a6=Q. [kd6 cannot go to c5 attacked by Pb4]
- N15. Kb3 Pa4 Pb4 | kc6 pc2 -- White to move [d=5]: **b4-b5+**. Black replies: Kc6-b6: ->R16; Kc6-c5, Kc6-d5, Kc6-d6: White wins by b5-b6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; kc6 cannot go to b5 attacked by Pa4]
- R16. Kb3 Pa4 Pb5 | kb6 pc2 -- White to move [d=3]: **Kb3xc2**. Black replies: Kb6-a5, Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 attacked by Pa4; c6 attacked by Pb5]
- N17. Kb3 Pa3 Pb4 | kb5 pc2 -- White to move [d=7]: **a3-a4+**. Black replies: Kb5-a6: ->N5; Kb5-b6: ->N11; Kb5-c6: ->N15. [in check from Pa4: only king moves and captures of the checking pawn are legal; kb5 cannot go to a4 next to K; a5 attacked by Pb4; b4 next to K; c4 next to K; c5 attacked by Pb4]

#### C14. Root Z5, move Kc3xc4. Position after the move: `Kc4 Pa3 Pb4 ka4 pb3 b -`

*Idea.* After any White move that leaves c3 and gives up control of b2, Black plays b3-b2 and b2-b1=Q cannot be stopped (3 plies).

Certificate (1 entries; the winner is Black):

- R1. Kc4 Pa3 Pb4 | ka4 pb3 -- Black to move [d=3]: **b3-b2**. White replies: Kc4-c3, Kc4-c5, Kc4-d3, Kc4-d4, Kc4-d5, b4-b5: Black wins by b2-b1=Q. [Kc4 cannot go to b3 next to k; b4 own pawn; b5 next to k; Pa3 is blocked by ka4]

#### C15. Root Z5, move Kc3-d2. Position after the move: `Kd2 Pa3 Pb4 ka4 pb3 pc4 b -`

*Idea.* As above.

Certificate (1 entries; the winner is Black):

- R1. Kd2 Pa3 Pb4 | ka4 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3, b4-b5: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4; Pa3 is blocked by ka4]

#### C16. Root Z5, move Kc3-d4. Position after the move: `Kd4 Pa3 Pb4 ka4 pb3 pc4 b -`

*Idea.* As above.

Certificate (1 entries; the winner is Black):

- R1. Kd4 Pa3 Pb4 | ka4 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd4-c3, Kd4xc4, Kd4-c5, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5, b4-b5: Black wins by b2-b1=Q. [Kd4 cannot go to d3 attacked by pc4; Pa3 is blocked by ka4]

#### C17. Root Z5, move b4-b5. Position after the move: `Kc3 Pa3 Pb5 ka4 pb3 pc4 b -`

*Idea.* b4-b5 is captured, Ka4xb5. White has lost a pawn; Black's king goes back to a4 to attack a3 while the White king is forced to give way (zugzwang on b2/c3), and then c4-c3 or b3-b2 decides.

Certificate (29 entries; the winner is Black):

- N1. Kc3 Pa3 Pb5 | ka4 pb3 pc4 -- Black to move [d=11]: **Ka4xb5**. White replies: Kc3-b2: ->N2; Kc3-d2: ->N15; Kc3-d4: ->N17; a3-a4+: ->N19. [Kc3 cannot go to b3 attacked by pc4; b4 next to k; c2 attacked by pb3; c4 next to k; d3 attacked by pc4]
- N2. Kb2 Pa3 | kb5 pb3 pc4 -- Black to move [d=7]: **Kb5-a4**. White replies: Kb2-a1: ->N3; Kb2-b1: ->N5; Kb2-c1: ->N8; Kb2-c3: ->N11. [Kb2 cannot go to a2 attacked by pb3; a3 own pawn; b3 next to k; c2 attacked by pb3; Pa3 is blocked by ka4]
- N3. Ka1 Pa3 | ka4 pb3 pc4 -- Black to move [d=5]: **Ka4xa3**. White replies: Ka1-b1: ->R4. [Ka1 cannot go to a2 next to k; b2 next to k]
- R4. Kb1 | ka3 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kb1-c2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; a2 next to k; b2 next to k; c1 attacked by pb2]
- N5. Kb1 Pa3 | ka4 pb3 pc4 -- Black to move [d=5]: **c4-c3**. White replies: Kb1-a1: ->R6; Kb1-c1: ->R7. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3; Pa3 is blocked by ka4]
- R6. Ka1 Pa3 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2; Pa3 is blocked by ka4]
- R7. Kc1 Pa3 | ka4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2; Pa3 is blocked by ka4]
- N8. Kc1 Pa3 | ka4 pb3 pc4 -- Black to move [d=5]: **c4-c3**. White replies: Kc1-b1: ->R9; Kc1-d1: ->R10. [Kc1 cannot go to b2 attacked by pc3; c2 attacked by pb3; d2 attacked by pc3; Pa3 is blocked by ka4]
- R9. Kb1 Pa3 | ka4 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kb1-a2, Kb1-c2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; b2 attacked by pc3; c1 attacked by pb2; Pa3 is blocked by ka4]
- R10. Kd1 Pa3 | ka4 pb3 pc3 -- Black to move [d=3]: **b3-b2**. White replies: Kd1-c2, Kd1-e1, Kd1-e2: Black wins by b2-b1=Q. [Kd1 cannot go to c1 attacked by pb2; d2 attacked by pc3; Pa3 is blocked by ka4]
- N11. Kc3 Pa3 | ka4 pb3 pc4 -- Black to move [d=5]: **Ka4xa3**. White replies: Kc3xc4: ->R12; Kc3-d2: ->R13; Kc3-d4: ->R14. [Kc3 cannot go to b2 next to k; b3 next to k; b4 next to k; c2 attacked by pb3; d3 attacked by pc4]
- R12. Kc4 | ka3 pb3 -- Black to move [d=3]: **b3-b2**. White replies: Kc4-b5, Kc4-c3, Kc4-c5, Kc4-d3, Kc4-d4, Kc4-d5: Black wins by b2-b1=Q. [Kc4 cannot go to b3 next to k; b4 next to k]
- R13. Kd2 | ka3 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4]
- R14. Kd4 | ka3 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd4-c3, Kd4xc4, Kd4-c5, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5: Black wins by b2-b1=Q. [Kd4 cannot go to d3 attacked by pc4]
- N15. Kd2 Pa3 | kb5 pb3 pc4 -- Black to move [d=5]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3: Black wins by b2-b1=Q; a3-a4+: ->R16. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4]
- R16. Kd2 Pa4 | kb5 pb2 pc4 -- Black to move [d=3]: **Kb5xa4**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4]
- N17. Kd4 Pa3 | kb5 pb3 pc4 -- Black to move [d=5]: **b3-b2**. White replies: Kd4-c3, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5: Black wins by b2-b1=Q; a3-a4+: ->R18. [Kd4 cannot go to c4 next to k; c5 next to k; d3 attacked by pc4]
- R18. Kd4 Pa4 | kb5 pb2 pc4 -- Black to move [d=3]: **Kb5xa4**. White replies: Kd4-c3, Kd4xc4, Kd4-c5, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5: Black wins by b2-b1=Q. [Kd4 cannot go to d3 attacked by pc4]
- N19. Kc3 Pa4 | kb5 pb3 pc4 -- Black to move [d=9]: **Kb5xa4**. White replies: Kc3-b2: ->N20; Kc3xc4: ->R27; Kc3-d2: ->R28; Kc3-d4: ->R29. [Kc3 cannot go to b3 next to k; b4 next to k; c2 attacked by pb3; d3 attacked by pc4]
- N20. Kb2 | ka4 pb3 pc4 -- Black to move [d=7]: **Ka4-b4**. White replies: Kb2-a1: ->N21; Kb2-b1: ->N22; Kb2-c1: ->N25. [Kb2 cannot go to a2 attacked by pb3; a3 next to k; b3 next to k; c2 attacked by pb3; c3 next to k]
- N21. Ka1 | kb4 pb3 pc4 -- Black to move [d=5]: **Kb4-a3**. White replies: Ka1-b1: ->R4. [Ka1 cannot go to a2 next to k; b2 next to k]
- N22. Kb1 | kb4 pb3 pc4 -- Black to move [d=5]: **c4-c3**. White replies: Kb1-a1: ->R23; Kb1-c1: ->R24. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- R23. Ka1 | kb4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2]
- R24. Kc1 | kb4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- N25. Kc1 | kb4 pb3 pc4 -- Black to move [d=5]: **Kb4-a3**. White replies: Kc1-b1: ->R4; Kc1-d1: ->R26; Kc1-d2: ->R13. [Kc1 cannot go to b2 next to k; c2 attacked by pb3]
- R26. Kd1 | ka3 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd1-c2, Kd1-d2, Kd1-e1, Kd1-e2: Black wins by b2-b1=Q. [Kd1 cannot go to c1 attacked by pb2]
- R27. Kc4 | ka4 pb3 -- Black to move [d=3]: **b3-b2**. White replies: Kc4-c3, Kc4-c5, Kc4-d3, Kc4-d4, Kc4-d5: Black wins by b2-b1=Q. [Kc4 cannot go to b3 next to k; b4 next to k; b5 next to k]
- R28. Kd2 | ka4 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4]
- R29. Kd4 | ka4 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd4-c3, Kd4xc4, Kd4-c5, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5: Black wins by b2-b1=Q. [Kd4 cannot go to d3 attacked by pc4]

#### C18. Root Z6, move Ka4xa3. Position after the move: `Kc3 Pb4 ka3 pb3 pc4 w -`

*Idea.* Black has captured a3; the White b-pawn is free and Black's king on a3 is too far from b5: b4-b5 and b5-b6=Q.

Certificate (1 entries; the winner is White):

- R1. Kc3 Pb4 | ka3 pb3 pc4 -- White to move [d=3]: **b4-b5**. Black replies: Ka3-a2, Ka3-a4, b3-b2: White wins by b5-b6=Q. [ka3 cannot go to b2 next to K; b3 own pawn; b4 next to K; pc4 is blocked by Kc3]

#### C19. Root Z6, move b3-b2. Position after the move: `Kc3 Pa3 Pb4 ka4 pb2 pc4 w -`

*Idea.* b3-b2 is captured by the king (Kxb2), after which Black has one pawn against two and White's king and pawns win the race.

Certificate (19 entries; the winner is White):

- N1. Kc3 Pa3 Pb4 | ka4 pb2 pc4 -- White to move [d=11]: **Kc3xb2**. Black replies: Ka4-b5: ->N2; c4-c3+: ->N12. [ka4 cannot go to a3 next to K; a5 attacked by Pb4; b3 next to K; b4 attacked by Pa3]
- N2. Kb2 Pa3 Pb4 | kb5 pc4 -- White to move [d=7]: **Kb2-c3**. Black replies: Kb5-a4: ->N3; Kb5-a6: ->N5; Kb5-b6: ->N7; Kb5-c6: ->N10. [kb5 cannot go to a5 attacked by Pb4; b4 next to K; c4 own pawn; c5 attacked by Pb4; pc4 is blocked by Kc3]
- N3. Kc3 Pa3 Pb4 | ka4 pc4 -- White to move [d=5]: **Kc3xc4**. Black replies: Ka4xa3: ->R4. [ka4 cannot go to a5 attacked by Pb4; b3 next to K; b4 next to K; b5 next to K]
- R4. Kc4 Pb4 | ka3 -- White to move [d=3]: **b4-b5**. Black replies: Ka3-a2, Ka3-a4, Ka3-b2: White wins by b5-b6=Q. [ka3 cannot go to b3 next to K; b4 next to K]
- N5. Kc3 Pa3 Pb4 | ka6 pc4 -- White to move [d=5]: **Kc3xc4**. Black replies: Ka6-b6: ->R6. [ka6 cannot go to a5 attacked by Pb4; b5 next to K]
- R6. Kc4 Pa3 Pb4 | kb6 -- White to move [d=3]: **b4-b5**. Black replies: Kb6-a5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 next to K; c5 next to K; c6 attacked by Pb5]
- N7. Kc3 Pa3 Pb4 | kb6 pc4 -- White to move [d=5]: **a3-a4**. Black replies: Kb6-a6: ->R8; Kb6-c6: ->R9. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4; pc4 is blocked by Kc3]
- R8. Kc3 Pa4 Pb4 | ka6 pc4 -- White to move [d=3]: **a4-a5**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5; pc4 is blocked by Kc3]
- R9. Kc3 Pa4 Pb4 | kc6 pc4 -- White to move [d=3]: **a4-a5**. Black replies: Kc6-b5, Kc6-d5, Kc6-d6: White wins by a5-a6=Q. [kc6 cannot go to b6 attacked by Pa5; c5 attacked by Pb4; pc4 is blocked by Kc3]
- N10. Kc3 Pa3 Pb4 | kc6 pc4 -- White to move [d=5]: **Kc3xc4**. Black replies: Kc6-b6: ->R6; Kc6-d6: ->R11. [kc6 cannot go to b5 next to K; c5 next to K; d5 next to K]
- R11. Kc4 Pa3 Pb4 | kd6 -- White to move [d=3]: **b4-b5**. Black replies: Kd6-e5, Kd6-e6: White wins by b5-b6=Q. [kd6 cannot go to c5 next to K; c6 attacked by Pb5; d5 next to K]
- N12. Kb2 Pa3 Pb4 | ka4 pc3 -- White to move [d=9]: **Kb2xc3**. Black replies: Ka4xa3: ->R13; Ka4-b5: ->N14. [ka4 cannot go to a5 attacked by Pb4; b3 next to K; b4 next to K]
- R13. Kc3 Pb4 | ka3 -- White to move [d=3]: **b4-b5**. Black replies: Ka3-a2, Ka3-a4: White wins by b5-b6=Q. [ka3 cannot go to b2 next to K; b3 next to K; b4 next to K]
- N14. Kc3 Pa3 Pb4 | kb5 -- White to move [d=7]: **Kc3-b3**. Black replies: Kb5-a6: ->N15; Kb5-b6: ->N16; Kb5-c6: ->N19. [kb5 cannot go to a4 next to K; a5 attacked by Pb4; b4 next to K; c4 next to K; c5 attacked by Pb4]
- N15. Kb3 Pa3 Pb4 | ka6 -- White to move [d=5]: **Kb3-c4**. Black replies: Ka6-b6: ->R6. [ka6 cannot go to a5 attacked by Pb4; b5 next to K]
- N16. Kb3 Pa3 Pb4 | kb6 -- White to move [d=5]: **a3-a4**. Black replies: Kb6-a6: ->R17; Kb6-c6: ->R18. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4]
- R17. Kb3 Pa4 Pb4 | ka6 -- White to move [d=3]: **a4-a5**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5]
- R18. Kb3 Pa4 Pb4 | kc6 -- White to move [d=3]: **a4-a5**. Black replies: Kc6-b5, Kc6-d5, Kc6-d6: White wins by a5-a6=Q. [kc6 cannot go to b6 attacked by Pa5; c5 attacked by Pb4]
- N19. Kb3 Pa3 Pb4 | kc6 -- White to move [d=5]: **Kb3-c4**. Black replies: Kc6-b6: ->R6; Kc6-d6: ->R11. [kc6 cannot go to b5 next to K; c5 next to K; d5 next to K]

#### C20. Root Z7, move Kc3-d2. Position after the move: `Kd2 Pa3 Pb4 kb5 pb3 pc4 b -`

*Idea.* Black king on b5. b3-b2 wins; the check a3-a4+ gains one tempo for White only, answered by Kxb4 or Kxa4.

Certificate (2 entries; the winner is Black):

- N1. Kd2 Pa3 Pb4 | kb5 pb3 pc4 -- Black to move [d=5]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3: Black wins by b2-b1=Q; a3-a4+: ->R2. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4; Pb4 is blocked by kb5]
- R2. Kd2 Pa4 Pb4 | kb5 pb2 pc4 -- Black to move [d=3]: **Kb5xb4**. White replies: Kd2-c2, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3, a4-a5: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2; c3 next to k; d3 attacked by pc4]

#### C21. Root Z7, move Kc3-d4. Position after the move: `Kd4 Pa3 Pb4 kb5 pb3 pc4 b -`

*Idea.* As above.

Certificate (2 entries; the winner is Black):

- N1. Kd4 Pa3 Pb4 | kb5 pb3 pc4 -- Black to move [d=5]: **b3-b2**. White replies: Kd4-c3, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5: Black wins by b2-b1=Q; a3-a4+: ->R2. [Kd4 cannot go to c4 next to k; c5 next to k; d3 attacked by pc4; Pb4 is blocked by kb5]
- R2. Kd4 Pa4 Pb4 | kb5 pb2 pc4 -- Black to move [d=3]: **Kb5xb4**. White replies: Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5, a4-a5: Black wins by b2-b1=Q. [Kd4 cannot go to c3 next to k; c4 next to k; c5 next to k; d3 attacked by pc4]

#### C22. Root Z7, move a3-a4. Position after the move: `Kc3 Pa4 Pb4 kb5 pb3 pc4 b -`

*Idea.* a3-a4 is captured by Kb5xa4; then b3-b2 / c4-c3 break through against the lone king.

Certificate (17 entries; the winner is Black):

- N1. Kc3 Pa4 Pb4 | kb5 pb3 pc4 -- Black to move [d=11]: **Kb5xa4**. White replies: Kc3-b2: ->N2; Kc3xc4: ->R11; Kc3-d2: ->R12; Kc3-d4: ->R13; b4-b5: ->N14. [Kc3 cannot go to b3 next to k; b4 own pawn; c2 attacked by pb3; d3 attacked by pc4]
- N2. Kb2 Pb4 | ka4 pb3 pc4 -- Black to move [d=7]: **Ka4xb4**. White replies: Kb2-a1: ->N3; Kb2-b1: ->N5; Kb2-c1: ->N8. [Kb2 cannot go to a2 attacked by pb3; a3 next to k; b3 next to k; c2 attacked by pb3; c3 next to k]
- N3. Ka1 | kb4 pb3 pc4 -- Black to move [d=5]: **Kb4-a3**. White replies: Ka1-b1: ->R4. [Ka1 cannot go to a2 next to k; b2 next to k]
- R4. Kb1 | ka3 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kb1-c2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; a2 next to k; b2 next to k; c1 attacked by pb2]
- N5. Kb1 | kb4 pb3 pc4 -- Black to move [d=5]: **c4-c3**. White replies: Kb1-a1: ->R6; Kb1-c1: ->R7. [Kb1 cannot go to a2 attacked by pb3; b2 attacked by pc3; c2 attacked by pb3]
- R6. Ka1 | kb4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Ka1-b2: Black wins by c2-c1=Q. [Ka1 cannot go to a2 attacked by pb3; b1 attacked by pc2]
- R7. Kc1 | kb4 pb3 pc3 -- Black to move [d=3]: **c3-c2**. White replies: Kc1-b2, Kc1-d2: Black wins by c2-c1=Q. [Kc1 cannot go to b1 attacked by pc2; c2 attacked by pb3; d1 attacked by pc2]
- N8. Kc1 | kb4 pb3 pc4 -- Black to move [d=5]: **Kb4-c3**. White replies: Kc1-b1: ->R9; Kc1-d1: ->R10. [Kc1 cannot go to b2 next to k; c2 next to k; d2 next to k]
- R9. Kb1 | kc3 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kb1-a2: Black wins by b2-b1=Q. [Kb1 cannot go to a1 attacked by pb2; b2 next to k; c1 attacked by pb2; c2 next to k]
- R10. Kd1 | kc3 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd1-e1, Kd1-e2: Black wins by b2-b1=Q. [Kd1 cannot go to c1 attacked by pb2; c2 next to k; d2 next to k]
- R11. Kc4 Pb4 | ka4 pb3 -- Black to move [d=3]: **b3-b2**. White replies: Kc4-c3, Kc4-c5, Kc4-d3, Kc4-d4, Kc4-d5, b4-b5: Black wins by b2-b1=Q. [Kc4 cannot go to b3 next to k; b4 own pawn; b5 next to k]
- R12. Kd2 Pb4 | ka4 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3, b4-b5: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4]
- R13. Kd4 Pb4 | ka4 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd4-c3, Kd4xc4, Kd4-c5, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5, b4-b5: Black wins by b2-b1=Q. [Kd4 cannot go to d3 attacked by pc4]
- N14. Kc3 Pb5 | ka4 pb3 pc4 -- Black to move [d=9]: **Ka4xb5**. White replies: Kc3-b2: ->N15; Kc3-d2: ->R16; Kc3-d4: ->R17. [Kc3 cannot go to b3 attacked by pc4; b4 next to k; c2 attacked by pb3; c4 next to k; d3 attacked by pc4]
- N15. Kb2 | kb5 pb3 pc4 -- Black to move [d=7]: **Kb5-b4**. White replies: Kb2-a1: ->N3; Kb2-b1: ->N5; Kb2-c1: ->N8. [Kb2 cannot go to a2 attacked by pb3; a3 next to k; b3 next to k; c2 attacked by pb3; c3 next to k]
- R16. Kd2 | kb5 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd2-c2, Kd2-c3, Kd2-d1, Kd2-e1, Kd2-e2, Kd2-e3: Black wins by b2-b1=Q. [Kd2 cannot go to c1 attacked by pb2; d3 attacked by pc4]
- R17. Kd4 | kb5 pb3 pc4 -- Black to move [d=3]: **b3-b2**. White replies: Kd4-c3, Kd4-d5, Kd4-e3, Kd4-e4, Kd4-e5: Black wins by b2-b1=Q. [Kd4 cannot go to c4 next to k; c5 next to k; d3 attacked by pc4]

#### C23. Root Z8, move Kb5-a6. Position after the move: `Kc3 Pa3 Pb4 ka6 pb3 pc4 w -`

*Idea.* The Black king leaves b5/a4: a3-a4 and the pawns a4, b4 run with check on a5/b5.

Certificate (5 entries; the winner is White):

- N1. Kc3 Pa3 Pb4 | ka6 pb3 pc4 -- White to move [d=7]: **a3-a4**. Black replies: Ka6-b6: ->N2; b3-b2: ->N4. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; pc4 is blocked by Kc3]
- N2. Kc3 Pa4 Pb4 | kb6 pb3 pc4 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R3; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]
- R3. Kc3 Pb4 Pa5 | ka6 pb3 pc4 -- White to move [d=3]: **b4-b5+**. Black replies: Ka6xa5: White wins by b5-b6=Q; Ka6xb5: White wins by a5-a6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; ka6 cannot go to b6 attacked by Pa5]
- N4. Kc3 Pa4 Pb4 | ka6 pb2 pc4 -- White to move [d=5]: **b4-b5+**. Black replies: Ka6-a5: White wins by b5-b6=Q; Ka6-b6: ->R5. [in check from Pb5: only king moves and captures of the checking pawn are legal; ka6 cannot go to b5 attacked by Pa4]
- R5. Kc3 Pa4 Pb5 | kb6 pb2 pc4 -- White to move [d=3]: **a4-a5+**. Black replies: Kb6xa5: White wins by b5-b6=Q; Kb6xb5, Kb6-c5: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a6 attacked by Pb5; c6 attacked by Pb5]

#### C24. Root Z8, move Kb5-b6. Position after the move: `Kc3 Pa3 Pb4 kb6 pb3 pc4 w -`

*Idea.* As above.

Certificate (5 entries; the winner is White):

- N1. Kc3 Pa3 Pb4 | kb6 pb3 pc4 -- White to move [d=7]: **a3-a4**. Black replies: Kb6-a6: ->N2; Kb6-c6: ->R4; b3-b2: ->N5. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4; pc4 is blocked by Kc3]
- N2. Kc3 Pa4 Pb4 | ka6 pb3 pc4 -- White to move [d=5]: **a4-a5**. Black replies: Ka6-b5: White wins by a5-a6=Q; b3-b2: ->R3. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5; pc4 is blocked by Kc3]
- R3. Kc3 Pb4 Pa5 | ka6 pb2 pc4 -- White to move [d=3]: **b4-b5+**. Black replies: Ka6xa5: White wins by b5-b6=Q; Ka6xb5: White wins by a5-a6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; ka6 cannot go to b6 attacked by Pa5]
- R4. Kc3 Pa4 Pb4 | kc6 pb3 pc4 -- White to move [d=3]: **a4-a5**. Black replies: Kc6-b5, Kc6-d5, Kc6-d6, b3-b2: White wins by a5-a6=Q. [kc6 cannot go to b6 attacked by Pa5; c5 attacked by Pb4; pc4 is blocked by Kc3]
- N5. Kc3 Pa4 Pb4 | kb6 pb2 pc4 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R3; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]

#### C25. Root Z8, move Kb5-c6. Position after the move: `Kc3 Pa3 Pb4 kc6 pb3 pc4 w -`

*Idea.* As above.

Certificate (7 entries; the winner is White):

- N1. Kc3 Pa3 Pb4 | kc6 pb3 pc4 -- White to move [d=7]: **a3-a4**. Black replies: Kc6-b6: ->N2; Kc6-d5: ->R4; Kc6-d6: ->R5; b3-b2: ->N6. [kc6 cannot go to b5 attacked by Pa4; c5 attacked by Pb4; pc4 is blocked by Kc3]
- N2. Kc3 Pa4 Pb4 | kb6 pb3 pc4 -- White to move [d=5]: **a4-a5+**. Black replies: Kb6-a6: ->R3; Kb6-b5, Kb6-c6: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a5 attacked by Pb4; c5 attacked by Pb4]
- R3. Kc3 Pb4 Pa5 | ka6 pb3 pc4 -- White to move [d=3]: **b4-b5+**. Black replies: Ka6xa5: White wins by b5-b6=Q; Ka6xb5: White wins by a5-a6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; ka6 cannot go to b6 attacked by Pa5]
- R4. Kc3 Pa4 Pb4 | kd5 pb3 pc4 -- White to move [d=3]: **a4-a5**. Black replies: Kd5-c6, Kd5-d6, Kd5-e4, Kd5-e5, Kd5-e6, b3-b2: White wins by a5-a6=Q. [kd5 cannot go to c4 own pawn; c5 attacked by Pb4; d4 next to K; pc4 is blocked by Kc3]
- R5. Kc3 Pa4 Pb4 | kd6 pb3 pc4 -- White to move [d=3]: **a4-a5**. Black replies: Kd6-c6, Kd6-d5, Kd6-e5, Kd6-e6, b3-b2: White wins by a5-a6=Q. [kd6 cannot go to c5 attacked by Pb4; pc4 is blocked by Kc3]
- N6. Kc3 Pa4 Pb4 | kc6 pb2 pc4 -- White to move [d=5]: **b4-b5+**. Black replies: Kc6-b6: ->R7; Kc6-c5, Kc6-d5, Kc6-d6: White wins by b5-b6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; kc6 cannot go to b5 attacked by Pa4]
- R7. Kc3 Pa4 Pb5 | kb6 pb2 pc4 -- White to move [d=3]: **a4-a5+**. Black replies: Kb6xa5: White wins by b5-b6=Q; Kb6xb5, Kb6-c5: White wins by a5-a6=Q. [in check from Pa5: only king moves and captures of the checking pawn are legal; kb6 cannot go to a6 attacked by Pb5; c6 attacked by Pb5]

#### C26. Root Z8, move b3-b2. Position after the move: `Kc3 Pa3 Pb4 kb5 pb2 pc4 w -`

*Idea.* b3-b2 is captured (Kc3xb2); the White king then returns to b3/c4 in time and the two White pawns win.

Certificate (36 entries; the winner is White):

- N1. Kc3 Pa3 Pb4 | kb5 pb2 pc4 -- White to move [d=11]: **Kc3xb2**. Black replies: Kb5-a4: ->N2; Kb5-a6: ->N10; Kb5-b6: ->N14; Kb5-c6: ->N21; c4-c3+: ->N30. [kb5 cannot go to a5 attacked by Pb4; b4 attacked by Pa3; c4 own pawn; c5 attacked by Pb4]
- N2. Kb2 Pa3 Pb4 | ka4 pc4 -- White to move [d=9]: **Kb2-c3**. Black replies: Ka4xa3: ->R3; Ka4-b5: ->N4. [ka4 cannot go to a5 attacked by Pb4; b3 next to K; b4 next to K; pc4 is blocked by Kc3]
- R3. Kc3 Pb4 | ka3 pc4 -- White to move [d=3]: **b4-b5**. Black replies: Ka3-a2, Ka3-a4: White wins by b5-b6=Q. [ka3 cannot go to b2 next to K; b3 next to K; b4 next to K; pc4 is blocked by Kc3]
- N4. Kc3 Pa3 Pb4 | kb5 pc4 -- White to move [d=7]: **a3-a4+**. Black replies: Kb5xa4: ->N5; Kb5-a6: ->R7; Kb5-b6: ->R8; Kb5-c6: ->R9. [in check from Pa4: only king moves and captures of the checking pawn are legal; kb5 cannot go to a5 attacked by Pb4; b4 next to K; c4 own pawn; c5 attacked by Pb4]
- N5. Kc3 Pb4 | ka4 pc4 -- White to move [d=5]: **Kc3xc4**. Black replies: Ka4-a3: ->R6. [ka4 cannot go to a5 attacked by Pb4; b3 next to K; b4 next to K; b5 next to K]
- R6. Kc4 Pb4 | ka3 -- White to move [d=3]: **b4-b5**. Black replies: Ka3-a2, Ka3-a4, Ka3-b2: White wins by b5-b6=Q. [ka3 cannot go to b3 next to K; b4 next to K]
- R7. Kc3 Pa4 Pb4 | ka6 pc4 -- White to move [d=3]: **a4-a5**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5; pc4 is blocked by Kc3]
- R8. Kc3 Pa4 Pb4 | kb6 pc4 -- White to move [d=3]: **b4-b5**. Black replies: Kb6-a5, Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 attacked by Pa4; c6 attacked by Pb5; pc4 is blocked by Kc3]
- R9. Kc3 Pa4 Pb4 | kc6 pc4 -- White to move [d=3]: **a4-a5**. Black replies: Kc6-b5, Kc6-d5, Kc6-d6: White wins by a5-a6=Q. [kc6 cannot go to b6 attacked by Pa5; c5 attacked by Pb4; pc4 is blocked by Kc3]
- N10. Kb2 Pa3 Pb4 | ka6 pc4 -- White to move [d=7]: **a3-a4**. Black replies: Ka6-b6: ->N11; c4-c3+: ->N12. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4]
- N11. Kb2 Pa4 Pb4 | kb6 pc4 -- White to move [d=5]: **Kb2-c3**. Black replies: Kb6-a6: ->R7; Kb6-c6: ->R9. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4; pc4 is blocked by Kc3]
- N12. Kb2 Pa4 Pb4 | ka6 pc3 -- White to move [d=5]: **Kb2-c2**. Black replies: Ka6-b6: ->R13. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; pc3 is blocked by Kc2]
- R13. Kc2 Pa4 Pb4 | kb6 pc3 -- White to move [d=3]: **b4-b5**. Black replies: Kb6-a5, Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 attacked by Pa4; c6 attacked by Pb5; pc3 is blocked by Kc2]
- N14. Kb2 Pa3 Pb4 | kb6 pc4 -- White to move [d=7]: **a3-a4**. Black replies: Kb6-a6: ->N15; Kb6-c6: ->N16; c4-c3+: ->N18. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4]
- N15. Kb2 Pa4 Pb4 | ka6 pc4 -- White to move [d=5]: **Kb2-c3**. Black replies: Ka6-b6: ->R8. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; pc4 is blocked by Kc3]
- N16. Kb2 Pa4 Pb4 | kc6 pc4 -- White to move [d=5]: **b4-b5+**. Black replies: Kc6-b6: ->R17; Kc6-c5, Kc6-d5, Kc6-d6: White wins by b5-b6=Q. [in check from Pb5: only king moves and captures of the checking pawn are legal; kc6 cannot go to b5 attacked by Pa4]
- R17. Kb2 Pa4 Pb5 | kb6 pc4 -- White to move [d=3]: **Kb2-c3**. Black replies: Kb6-a5, Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 attacked by Pa4; c6 attacked by Pb5; pc4 is blocked by Kc3]
- N18. Kb2 Pa4 Pb4 | kb6 pc3 -- White to move [d=5]: **Kb2-c2**. Black replies: Kb6-a6: ->R19; Kb6-c6: ->R20. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4; pc3 is blocked by Kc2]
- R19. Kc2 Pa4 Pb4 | ka6 pc3 -- White to move [d=3]: **a4-a5**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5; pc3 is blocked by Kc2]
- R20. Kc2 Pa4 Pb4 | kc6 pc3 -- White to move [d=3]: **a4-a5**. Black replies: Kc6-b5, Kc6-d5, Kc6-d6: White wins by a5-a6=Q. [kc6 cannot go to b6 attacked by Pa5; c5 attacked by Pb4; pc3 is blocked by Kc2]
- N21. Kb2 Pa3 Pb4 | kc6 pc4 -- White to move [d=7]: **a3-a4**. Black replies: Kc6-b6: ->N11; Kc6-d5: ->N22; Kc6-d6: ->N24; c4-c3+: ->N26. [kc6 cannot go to b5 attacked by Pa4; c5 attacked by Pb4]
- N22. Kb2 Pa4 Pb4 | kd5 pc4 -- White to move [d=5]: **b4-b5**. Black replies: Kd5-c5, Kd5-d4, Kd5-d6, Kd5-e4, Kd5-e5, Kd5-e6: White wins by b5-b6=Q; c4-c3+: ->R23. [kd5 cannot go to c4 own pawn; c6 attacked by Pb5]
- R23. Kb2 Pa4 Pb5 | kd5 pc3 -- White to move [d=3]: **Kb2xc3**. Black replies: Kd5-c5, Kd5-d6, Kd5-e4, Kd5-e5, Kd5-e6: White wins by b5-b6=Q. [kd5 cannot go to c4 next to K; c6 attacked by Pb5; d4 next to K]
- N24. Kb2 Pa4 Pb4 | kd6 pc4 -- White to move [d=5]: **b4-b5**. Black replies: Kd6-c5, Kd6-d5, Kd6-e5, Kd6-e6: White wins by b5-b6=Q; c4-c3+: ->R25. [kd6 cannot go to c6 attacked by Pb5]
- R25. Kb2 Pa4 Pb5 | kd6 pc3 -- White to move [d=3]: **Kb2xc3**. Black replies: Kd6-c5, Kd6-d5, Kd6-e5, Kd6-e6: White wins by b5-b6=Q. [kd6 cannot go to c6 attacked by Pb5]
- N26. Kb2 Pa4 Pb4 | kc6 pc3 -- White to move [d=5]: **Kb2xc3**. Black replies: Kc6-b6: ->R27; Kc6-d5: ->R28; Kc6-d6: ->R29. [kc6 cannot go to b5 attacked by Pa4; c5 attacked by Pb4]
- R27. Kc3 Pa4 Pb4 | kb6 -- White to move [d=3]: **b4-b5**. Black replies: Kb6-a5, Kb6-c5: White wins by b5-b6=Q. [kb6 cannot go to a6 attacked by Pb5; b5 attacked by Pa4; c6 attacked by Pb5]
- R28. Kc3 Pa4 Pb4 | kd5 -- White to move [d=3]: **b4-b5**. Black replies: Kd5-c5, Kd5-d6, Kd5-e4, Kd5-e5, Kd5-e6: White wins by b5-b6=Q. [kd5 cannot go to c4 next to K; c6 attacked by Pb5; d4 next to K]
- R29. Kc3 Pa4 Pb4 | kd6 -- White to move [d=3]: **b4-b5**. Black replies: Kd6-c5, Kd6-d5, Kd6-e5, Kd6-e6: White wins by b5-b6=Q. [kd6 cannot go to c6 attacked by Pb5]
- N30. Kb2 Pa3 Pb4 | kb5 pc3 -- White to move [d=7]: **Kb2xc3**. Black replies: Kb5-a4: ->N31; Kb5-a6: ->N32; Kb5-b6: ->N33; Kb5-c6: ->N36. [kb5 cannot go to a5 attacked by Pb4; b4 next to K; c4 next to K; c5 attacked by Pb4]
- N31. Kc3 Pa3 Pb4 | ka4 -- White to move [d=5]: **Kc3-c4**. Black replies: Ka4xa3: ->R6. [ka4 cannot go to a5 attacked by Pb4; b3 next to K; b4 next to K; b5 next to K]
- N32. Kc3 Pa3 Pb4 | ka6 -- White to move [d=5]: **a3-a4**. Black replies: Ka6-b6: ->R27. [ka6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4]
- N33. Kc3 Pa3 Pb4 | kb6 -- White to move [d=5]: **a3-a4**. Black replies: Kb6-a6: ->R34; Kb6-c6: ->R35. [kb6 cannot go to a5 attacked by Pb4; b5 attacked by Pa4; c5 attacked by Pb4]
- R34. Kc3 Pa4 Pb4 | ka6 -- White to move [d=3]: **a4-a5**. Black replies: Ka6-b5: White wins by a5-a6=Q. [ka6 cannot go to a5 attacked by Pb4; b6 attacked by Pa5]
- R35. Kc3 Pa4 Pb4 | kc6 -- White to move [d=3]: **a4-a5**. Black replies: Kc6-b5, Kc6-d5, Kc6-d6: White wins by a5-a6=Q. [kc6 cannot go to b6 attacked by Pa5; c5 attacked by Pb4]
- N36. Kc3 Pa3 Pb4 | kc6 -- White to move [d=5]: **a3-a4**. Black replies: Kc6-b6: ->R27; Kc6-d5: ->R28; Kc6-d6: ->R29. [kc6 cannot go to b5 attacked by Pa4; c5 attacked by Pb4]

## 7. Proof of Theorem A

*Part 1* is Lemma S. *Part 2*: the legal moves at each root are those of section 4, and every non-shuttle one is one of the
26 deviations C01-C26 of section 6; for each, the certificate shows that the opponent (the winner of the entry) promotes first
in at most 11 plies after the move.
*Part 3.* Let r be a root, Y either colour. Y's strategy: "if it is Y's turn and the opponent has never left the shuttle,
play the shuttle step (legal by Lemma S; the position is again a root); if the opponent leaves the shuttle, he plays one
of the 26 deviation moves (the list of section 4 is complete), and Y wins by the certificate of that case". Against this strategy
either both sides shuttle for ever (every position is a root, nobody promotes, nobody is mated or stalemated: a draw), or the opponent
deviates at some root and Y wins. So each colour can guarantee at least a draw from every root and the value is D for the
side to move, i.e. (D, D). QED

## 8. The mirror group (Theorem B)

tau(f, r) = (f, 7 - r), colours swapped, side to move swapped. It maps the pawn rules to themselves (White pawns forward = up,
promotion on rank 6 <-> Black pawns forward = down, promotion on rank 1; the double-step rank 2 <-> 5; e.p. squares to
e.p. squares), kings and king-adjacency to themselves, so it maps legal moves to legal moves, checkmate/stalemate to the same,
and first-promotion-wins to the same rule. tau(Z_B) = `Ka3/Kb2 (White shuttle), kb5/kc4 (Black shuttle), Pb4 Pc3 pa4 pb3`:
the White king b2/c3 becomes the Black king b5/c4, the Black king a4/b5 becomes the White king a3/b2, Pa3 -> pa4, Pb4 -> pb3,
pb3 -> Pb4, pc4 -> Pc3. A root `(wk, bk, side)` of Z_B goes to the root `(tau(bk), tau(wk), other side)` of the mirror. So
Theorem A for the mirror follows. Machine check (`scripts/tau_check.py`): tau of the 8 roots is the set of the 8 roots of
the mirror group, and the legal-move sets are equivariant on all 22,818 positions reachable from the roots within 8 plies;
the certificates of the 52 children (26 of Z_B, 26 of the mirror) are verified independently, section 9.

## 9. Machine checks (what was run, and what each check covers)

1. `scripts/pm.py` is a third implementation of the P model (written from SPEC.md; independent of kpsolve.c, kp_p.c, ref3.cpp).
   Its move lists at the 16 roots equal those of kpp (`--pmodel --moves`) and ref3m (`--moves`), and its depth-bounded search
   finds no win for either side from any root within 21 plies, and the win of every one of the 52 deviation children
   within at most 11 plies (`scripts/t1.py`).
2. `scripts/verify_certs.py` re-checks every position cited in the certificates (409 opponent-to-move positions, 626 leaf
   positions, 52 deviations of Z_B and its mirror) against **kpp and ref3m**: the set of legal replies of each cited position
   equals the certificate's list, each reply leads to a position valued as a win for the winner, each leaf has a promotion move
   valued as a win. 2,642 reply values, 0 discrepancies.
3. `scripts/tau_check.py`: the symmetry tau (above).
4. Root values: kpp and ref3 both give D at all 16 roots.

