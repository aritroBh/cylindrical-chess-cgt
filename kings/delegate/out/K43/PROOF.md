# K43 PROOF: two lemmas on exact under (and over) groups

Setting: model P (first promotion wins, e.p. on, real kings, stalemate and infinite play are draws), Definition 4.8 of `kings/theory/LOOPY.md`
(K26). An *exact under group* is a placement (pawn structure, adjacent White king squares z_0, z_1 satisfying K1, Black king b_0 satisfying K1
and K2 against both) with, at the four roots (z_a, b_0, side to move):

- (U1) with White to move every non-shuttle White move loses at once (the position after it is a Black win) and the shuttle z_a to z_(1-a) is legal;
- (U2) with Black to move some legal move does not lose at once (a *freeze*), and no freeze is a promotion;
- (U3) after every freeze m, in the position q_m (with the e.p. flag if m is a double step) White to move has a legal move and every legal move loses at once;
- (U4) q_m with Black to move (no flag) is a legal position, Black has a legal move and every legal Black move loses at once.

The exact **over** group is the colour mirror (ranks flipped, colours swapped, side to move swapped). Everything below is stated for under;
the over statements follow by the mirror.

"A move loses at once" means the position after it, with the opponent to move, is a win for the opponent (value in P).

## Lemma 4.10 (a freeze cannot serve both roots). PROVED

Let G be an exact under group, a in {0, 1}, m a freeze at the root R_a = (z_a, b_0, Black to move), q = q_m the position after m with the White king
on z_a, White to move. Assume the shuttle move z_a to z_(1-a) is a legal move in q (the square z_(1-a) is empty, not attacked by a Black pawn of q and
not adjacent to Black's king in q). Write q^ for the position that arises from q by that move (White king on z_(1-a), same Black pieces, Black to move)
and q^_W for q with the White king on z_(1-a) and White to move. Then:

1. q^ is a Black win.
2. m is not a freeze at the other root R_(1-a). If m is a legal move there, it loses at once, so q^_W (the position after m from R_(1-a)) is a White win.
3. Hence the position q_m(z_a) is a mutual zugzwang (a zero, both sides to move lose) and the same pawns and kings with the White king on z_(1-a)
   are a position in which the player to move wins, whoever it is.

*Proof.* (1) By (U3) every legal White move in q loses at once. The shuttle is legal by hypothesis, and the position after it is q^, so q^ is a Black win.
(2) Suppose m were a freeze at R_(1-a). Its position after m is q^_W (White to move) and by (U4) q^ (Black to move) is a position in which Black has a legal
move and every legal Black move loses at once, so q^ is a White win. That contradicts (1). If m is legal at R_(1-a) and not a freeze, then by the definition of a
freeze it loses at once, i.e. q^_W is a White win (White to move). (3) By (U3) and (U4) at R_a the position q has value L for White to move and for Black to move;
(1) and (2) give the two wins at z_(1-a). ∎

Remarks (not used below). (i) A Black pawn move that is legal at R_a is legal at R_(1-a) unless it puts a pawn on z_(1-a) or double-steps across z_(1-a) (the White king
stands there at R_(1-a)). A king capture m: b_0 to x that is illegal at R_(1-a) has x adjacent to z_(1-a), but then z_(1-a) is adjacent to Black's king in q, so the shuttle is
illegal in q and the hypothesis fails. (ii) Mechanical check (COMPUTED-1, `plocal.cpp`, `lemma410` field of the RESULT lines): on every placement with a root R_a whose freezes
all lead to zeros and whose shuttle is legal in q, the statements 1 and 2 hold: 0 violations (counts in `findings.txt`).

## Lemma 4.11 (the shuttle also loses at once; closures reduce to pairs). PROVED

In an exact under group every White move at a White-to-move root loses at once, the shuttle included. Consequently the choice of "the" shuttle in (U1) does not matter, and a
group with a larger closure is detected by the pair test.

*Proof.* Let R = (z_a, b_0, White to move) and let s be the shuttle, leading to R' = (z_(1-a), b_0, Black to move). By (U2) and (U3) at R' there is a freeze m with q_m
White to move lost for White; so Black wins from R' by playing m. So s loses at once. The other moves lose at once by (U1). ∎

*Closure form.* Let C be a set of at least two White king squares, pairwise connected by king steps inside C, Black's king on b_0, a fixed pawn structure, such that at every state
(z, b_0) with z in C: K1 and K2 hold; every White move that is not a king step to a square of C loses at once; some king step to C exists; and the Black-to-move conditions (U2) to (U4)
hold at (z, b_0). Take two adjacent squares z, z' of C. The step z to z' leads to a state of C at which (U2) and (U3) hold, so by the argument above it loses at once as well.
So all White moves at (z, b_0) and at (z', b_0) lose at once, and {z, z'} is an exact pair in the sense of Definition 4.8 with shuttle z to z'. Hence no exact group of any closure
exists unless an exact *pair* exists, and a negative result of the pair search covers every closure of this form. (Closures in which White also has pawn moves that stay inside the group are not covered by this argument and are not claimed.) ∎

## What is not proved

No proof that an exact over group does not exist. (U1) to (U4) are four conditions on one pawn structure and two king states. Lemma 4.10 says that the two roots need different
freezes, and that at the zero of one root the other state is a first-player win. The data (`findings.txt`) show that for placements satisfying (U1) to (U3) at both roots
the position q has a winning Black move in almost every case, and that exactly one root can be made a zero (the "half-exact" placements); no argument is known that forbids the
second root. The result is a search bound.
