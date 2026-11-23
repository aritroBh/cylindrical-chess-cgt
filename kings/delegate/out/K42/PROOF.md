# K42: tempo pairing for promotion-free contexts (Proposition 8.1′)

Model P throughout (the first promotion ends the game as a win for the promoter; stalemate and infinite play are
draws). Notation as in `kings/theory/LOOPY.md`: Definition 2.1 (king group Z on the files F_Z, buffer, context),
Lemma 2.2 (buffer invariance), Definition 2.6 (the local game), Theorem 2.7 and Proposition 8.1 (§8 item 1).
s is the side that made the sortie, s̄ the punisher. One derivation, by the K42 investigator (an AI); no referee
yet, no human re-derivation.

## 1. The pawn game of a context, and promotion-freeness

A *context* G is a set of pawns on the context files (files at distance ≥ 2 from F_Z), with an e.p. right or none.
Its *pawn game* is played by the context pawns alone, with chess pawn moves (single and double steps, captures,
e.p. captures right after a double step), alternately; a side with no pawn move loses (normal play).

G is *promotion-free* (K18's definition) if no sequence of legal pawn moves of G alone (both colours, in any
order, captures and e.p. captures included) promotes. Then no play of the pawn game promotes, the pawn game is
finite (every move advances a pawn or removes one), and it has no draws.

**(PF)** G is promotion-free, and in its pawn game the side s, to move, loses.

**Lemma A ((PF) gives (P2)). PROVED.** Assume (PF). Let 𝒢 be any set of pawn-game positions with s to move such
that (a) G ∈ 𝒢, (b) every position of 𝒢 is a loss for the mover s, and (c) for every position c ∈ 𝒢 and every
pawn move of s from c to c′, 𝒢 contains a position c″ reached from c′ by a pawn move of s̄. (Such a set exists:
the set of all positions with s to move that are reachable from G and lost for s.) Then 𝒢 satisfies (P2) of
Proposition 8.1.

*Proof.* (c) is the closure under pairing. Such a c″ exists for every c′, because c′ is won for s̄ to move (c is
lost for s), so s̄ has a move to a position lost for s to move; this is how the stated set satisfies (c). No play
of 𝒢 contains a promotion, because G is promotion-free and every position of 𝒢 is reached from G by pawn moves. A
position of 𝒢 may carry an e.p. right created by s̄'s last move; deleting it keeps (b) and (c), since the moves of s
from the position without the right are among those from the position with it, and the same replies work (this is
the closure step at the start of the proof of Proposition 8.1). ∎

So under (PF), (P2) of Proposition 8.1 is automatic; what remains of it is the class condition "s to move loses
the pawn game of G", which `kpsolve --frozen` certifies as the zero or negative class when G is promotion-free.

## 2. The squares the sortie king must avoid

Fix 𝒢 as in Lemma A. Write 𝒢⁺ for the positions of 𝒢 together with the positions reached from them by one pawn
move of s. Define:
- X: the squares on which a context pawn stands in some position of 𝒢⁺ (this is the X of (P2));
- E: the squares passed over by a double step made by s from a position of 𝒢, or by the pairing reply of s̄ from a
  position of 𝒢⁺ \ 𝒢;
- A: the squares attacked by an s̄ context pawn in some position of 𝒢⁺.

Every square of E is next to a square of X (the landing square of the double step), and every square of A is
diagonally next to a square of X (the attacking pawn's square). So X ∪ E ∪ A lies inside X together with its
king-neighbourhood, the set that (P3) of Proposition 8.1 excludes.

## 3. The statement

**Proposition 8.1′ (tempo pairing for promotion-free contexts). PROVED (one derivation; K42, 2026-11-22).** Let Q
(s to move) be as in Theorem 2.7(b), with no e.p. right at Q: every pawn is a Z-pawn on F_Z or a context pawn on a
context file, the buffer is empty, there is no officer, s̄'s king stands on F_Z, and no s̄ context pawn attacks
s's king. Let G be the context of Q. Assume (P1) and (P1e) of Proposition 8.1 for a strategy σ of s̄ in the plain
local game L_T^0(Q_Z), and
- (PF) as in §1;
- **(P3′)** let R be the set of squares on which s's king can stand in lines of L_T^0(Q_Z) in which s̄ plays σ
  (the king's square at Q included). Then R contains no square of X ∪ E ∪ A.

Then s̄ wins P from Q.

Since X ∪ E ∪ A is contained in X and its king-neighbourhood, (P3′) is implied by (P3), and by Lemma A the
hypotheses of Proposition 8.1 for a promotion-free G imply those of Proposition 8.1′. So Proposition 8.1′ extends
Proposition 8.1 for promotion-free contexts: (P2) is dropped (it follows from (PF)), and (P3) is weakened from
"X and its king-neighbourhood" to "X, the squares passed over by double steps, and the squares attacked by s̄'s
context pawns". The sortie king may stand next to a context pawn, behind it, or diagonally in front of an s pawn;
it may not stand where a context pawn stands or will move, nor where an s̄ context pawn attacks.

**Reading of "each defender tempo answered by a punisher tempo".** s̄ answers every context move of s by a
context move (a pawn move of the pawn game, chosen inside 𝒢), and every local move of s (a king move or a Z-pawn
move) by σ. s̄ never moves a context pawn otherwise and never moves its king off F_Z. This is the reading proved;
the counterexamples of K42 (findings.txt) show that the promotion-free form fails without a hypothesis on the
sortie king.

## 4. Proof

s̄'s strategy is the one of Proposition 8.1: to a local move of s, the σ-reply, read on the deleted play (the
play of L_T^0(Q_Z) obtained by deleting every context pair, a context move of s together with its pairing reply);
to a context move of s, the pairing reply inside 𝒢. We follow the proof of Proposition 8.1 and check each step
where it used (P2) or (P3).

*Invariants.* (J1) At every s-turn the context is a position of 𝒢. At Q it is G ∈ 𝒢. A local move of s and
the σ-reply leave the context unchanged; a context move of s and the pairing reply lead from 𝒢 to 𝒢. (J2) At every
s-turn, s's king stands on a square of R. By induction: the deleted play is a line of L_T^0(Q_Z) in which s̄
plays σ (shown below), so s's king stands on its current square in that line; a context pair does not move the
king. (J3) At every moment s's king stands on a square of R (by (J2), since s's king moves only at s-turns).

*Step 1: s's king never touches the context.* By (J3) and (P3′), s's king never stands on a square of X, so it
never captures a context pawn (a king capture ends on the captured pawn's square, which is in X: the captured
pawn stands there in the current context, which is in 𝒢⁺) and never stands on a square to which a context pawn
moves in a pairing reply or in a move of s from 𝒢 (the target is in X). It never stands on a square passed over
by such a double step (E). So the context moves that are legal in the real game are exactly the moves of the pawn
game (no move of the pawn game is blocked by s's king, and s's king never removes a context pawn), and the context
evolves as a play of the pawn game. In particular no context pawn promotes (PF), and a pairing reply always exists
(Lemma A) and is legal for s̄: its squares are free of s's king (X, E), s̄'s king is on F_Z where no context pawn
interferes (Lemma 2.2), and a context pawn move never exposes s̄'s king (there are no sliders, and no context pawn
attacks F_Z).

*Step 2: no s̄ context pawn ever attacks s's king.* By (J1) and (J3), whenever s's king stands somewhere the
context is in 𝒢⁺ (at s-turns it is in 𝒢; right after a move of s it is in 𝒢⁺; s̄'s σ-replies do not change it).
The squares attacked by s̄'s context pawns in 𝒢⁺ are in A, and s's king is on a square of R, which avoids A. This
replaces the use of the king-neighbourhood in Proposition 8.1 for "a context pawn never attacks s's king" and for
"no context move gives check".

*Step 3: the deleted play is a play of L_T^0(Q_Z) in which s̄ follows σ.* Let s be to move at a real position S,
P the position of the deleted play, P° the local part of S (P, or P without a pending Z-right when a context pair
has come since s̄'s last σ-reply). (i) A legal real move of s is legal in P°: a king move to d is legal in S, so d
is not occupied by a pawn of s, not next to s̄'s king and not attacked by an s̄ pawn after the move; the pawns of P°
are a subset of those of S and the checkers of s in S are Z-pawns (Step 2), so the same holds in P°. A Z-pawn move
involves squares of F_Z and the empty buffer only, which carry the same pieces in S and P°. And a legal move in P°
is legal in P (P has all moves of P° and possibly an e.p. capture more). (ii) Conversely, a legal move of s in P
that is not an e.p. capture of a missing right is legal in S: a Z-pawn move as before; a king move goes to a square
d of R (it is a move of s in a line of σ), d holds no context pawn (R avoids X and the context is in 𝒢) and is not
attacked by an s̄ context pawn (R avoids A), and the remaining conditions are the same in S and P. (iii) s̄'s
σ-reply is a legal real move: F_Z carries the same pieces in the real and the local position, no context pawn
attacks F_Z (Lemma 2.2), and a pending right created by s on F_Z is answered at once (Steps 2 and 3 of Theorem 2.7).
So the deleted play is a legal play of L_T^0(Q_Z), and s̄ answers it by σ.

*Step 4: s is never stalemated, and a mate in the projection is a real mate.* At Q, or at a real s-turn right
after a σ-reply, S has the local part P (no right is missing), and P has a legal move for s, because σ wins the
plain game, in which a stalemate of s is a failure for s̄; by (ii) it is legal in S. At a real s-turn right after a
pairing reply, s was not in check before its context move (a context move is not legal in check: a check comes from
an s̄ Z-pawn by Step 2, and a context pawn can neither capture on F_Z nor block a pawn check), and the pairing reply
gives no check (Step 2). So s is not in check at P°; P has a legal move for s, and by (P1e) one that is not an e.p.
capture of the right that may be missing; by (ii) that move is legal in S. A mate of s in the projection arises
right after a σ-reply, where S has the local part P; there s is in check from an s̄ Z-pawn, the real moves of s are
local moves (none legal) or context moves (not legal in check), so it is a mate in the real game.

*Step 5: end of the play.* The context makes finitely many moves (the pawn game is finite), and the deleted play
ends within T moves of s̄ by a promotion of s̄ (a legal real move by (iii), which wins P) or a mate of s (Step 4).
s's Z-pawn promotions are local moves of the deleted play, which σ prevents; the context does not promote (Step 1).
So every play ends with a win for s̄. ∎

## 5. What the proposition does not say

- It is a sufficient condition. Without a hypothesis on the sortie king the promotion-free form is false: K42 found
  failures in every promotion-free zero context tested, including K18's family (`Pe2 Pg2 pe4 pg4`), and every failure
  needs the sortie king either to enter a context file or to be stalemated by a context pawn's attack (findings.txt).
- (P1e) is kept. The lapse-game remedy of the K18 re-referee (replace the plain game by the game in which s may let a
  pending right lapse, and drop (P1e)) is not written out here.
- (P3′) is a condition on one strategy σ. It can be checked as a game: σ exists with (P1), (P1e) and (P3′) iff s̄ wins
  the plain local game in which a step of s's king onto X ∪ E ∪ A, and an s-turn with a pending right whose legal
  moves are all e.p. captures, are failures for s̄ (and s's king at Q is not on X ∪ E ∪ A). K42's `src/k42.cpp`
  (mode `cert`) computes this game. On the 6,033,423 legal sortie–context pairs of K42's runs (`cyl:7×6`, `cyl:8×6`,
  `cyl:9×6`; groups and contexts of at most 2 + 2 pawns) it certifies 1,213,383 pairs (the certificate of Proposition
  8.1, with X and its king-neighbourhood, certifies 967,308), and none of the 68,395 failures is certified
  (COMPUTED-1, one implementation; a consistency check of the proposition, not part of the proof).
- With 𝒢 replaced by any set satisfying (a)–(c) the sets X, E, A shrink or grow with 𝒢; the statement holds for each
  choice. K42's check uses the closure under all of s̄'s winning replies.
