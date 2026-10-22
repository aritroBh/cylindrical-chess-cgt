### EDIT 1: R1 item 3, R3 items 2 and 3 — Definition 2.6 (L1) and (L3′)
<<<<<<< OLD
**Definition 2.6 (local certificate LC_T).** Let m be a Z-move of s, and r the punishing reply of s̄ (a
king capture of a Z-pawn). Let Q be the position after m and r, with s to move. Let Q_Z be Q with every
context pawn deleted: only the kings and the remaining Z-pawns are left, on the whole board. LC_T(m) holds
at Y if:

- **(L1) local forced promotion against a passing defender.** For every *pass budget* k ∈ {0, 1, 2, …, ∞}, s̄
  wins the following game in Q_Z within T of its own moves:
  - s may pass up to k times, but not while in check;
  - s with no legal move and no pass left is stalemated, which counts as a failure for s̄;
  - s̄ wins by promoting to a queen that s cannot capture at once;
  - s̄'s king never leaves F_Z.

  The budget models s's spare moves in the context. "Every k" is needed because the dependence on k goes
  both ways. More passes let s dodge a zugzwang. Fewer passes let s escape by stalemate, since a side that
  still has a pass cannot be stalemated.
- **(L2) no faster counter-promotion.** Let μ_s be the least number of s-moves (king and pawns) in which s
  could promote in Q if s̄ never moved, s̄'s Z-pieces were removed and s̄'s context pawns stood fixed.
  Then μ_s ≥ T + 1.
  - **(L2⁺)**, the recommended margin before invoking (A_Q), is μ_s ≥ T + 2. With μ_s = T + 1, s's pawn
    reaches its seventh rank just as s̄ queens, and queen-against-seventh-rank-pawn endings can be drawn.
- **(L3) no stalemate in the window.** At every s-turn during the window, s has a legal move in the real
  position.
  - (L1) already excludes stalemate in Q_Z. The extra danger is context pieces taking away king squares that
    are free in Q_Z.
  - Sufficient (L3′): every square within distance T + 1 of s's king (after m) lies on F_Z. Then s's king has
    the same legal moves as in Q_Z.
  - For T = 1, (L3) is a single check: after r, s has a legal move.
=======
**Definition 2.6 (local certificate LC_T).** Let m be a Z-move of s, and r the punishing reply of s̄ (a
king capture of a Z-pawn). Let Q be the position after m and r, with s to move. Let Q_Z be Q with every
context pawn deleted: only the kings and the remaining Z-pawns are left, on the whole board. LC_T(m) holds
at Y if:

- **(L1) local forced promotion against a passing defender.** s̄ wins the following game in Q_Z within T of its
  own moves against a defender s who may pass **arbitrarily many times** (k = ∞):
  - s may pass at any turn, but not while in check;
  - s with no legal move and no pass left is stalemated, which counts as a failure for s̄;
  - s̄ wins by promoting to a queen that s cannot capture at once;
  - s̄'s king never leaves F_Z.

  The unlimited budget models the fact that s's spare moves in the context are not known in advance; the real
  defender's options are a subset of the k = ∞ game's, and its only gain from having fewer options is
  stalemate, which (L3) excludes. The earlier phrasing "for every k" and the remark that "every k is needed"
  are withdrawn (revised after review: R1 item 3, R3 items 2 and 3).
- **(L2) no faster counter-promotion.** Let μ_s be the least number of s-moves (king and pawns) in which s
  could promote in Q if s̄ never moved, s̄'s Z-pieces were removed and s̄'s context pawns stood fixed.
  Then μ_s ≥ T + 1.
  - **(L2⁺)**, the recommended margin before invoking (A_Q), is μ_s ≥ T + 2. With μ_s = T + 1, s's pawn
    reaches its seventh rank just as s̄ queens, and queen-against-seventh-rank-pawn endings can be drawn.
- **(L3) no stalemate in the window.** At every s-turn during the window, s has a legal move in the real
  position.
  - (L1) already excludes stalemate in Q_Z. The extra danger is context pieces taking away king squares that
    are free in Q_Z.
  - Sufficient (L3′): every square within distance T + 1 of s's king (after m) lies on F_Z. Then s's king has
    the same legal moves as in Q_Z. **This condition can never apply for T ≥ 2 on a 3-file group, because the
    ball of radius T+1 spans at least 5 files while |F_Z| = 3.** (revised after review: R1 item 8)
  - For T = 1, (L3) is a single check: after r, s has a legal move.
>>>>>>> NEW

### EDIT 2: R1 item 3, R3 items 2 and 3 — Theorem 2.7 (proof rewritten)
<<<<<<< OLD
**Theorem 2.7 (sufficiency of the certificate). PROVED (in P).** If LC_T(m) holds at Y, then the Z-move m
is decisively punished in P.

*Proof.* s̄ plays r and then follows its local winning strategy σ_Z, using only Z-moves. It ignores the
context. Check that the strategy survives in the full position, for t ≤ T.

- **s's moves map onto the local game.** A king move of s is the same king move in Q_Z. In Q_Z there are
  fewer pieces, so it is still legal there, and a capture of a context pawn becomes a plain move to the same
  square. A context move of s is a pass in Q_Z. It is never made while s is in check, unless it answers a
  check given by a context pawn, and in Q_Z that check does not exist, so the pass is allowed there. The
  number of such passes is some k, which (L1) covers.
- **s̄'s prescribed moves are legal.** s̄'s king stays on F_Z, so by Lemma 2.2 no context pawn attacks it,
  occupies its squares or gives it check. s̄'s pawn moves stay on F_Z. Without sliders there are no pins.
- **s does not promote first.** After r, s moves first. Before s̄'s T-th move, s has made T moves, and by
  (L2) it needs at least T + 1. The removed Z-pieces of s̄ could only slow s down, so μ_s is a lower bound.
  s's own Z-pawns are part of Q_Z, and σ_Z wins against them.
- **No other way out.**
  - (L3) excludes stalemate of s in the real position. (L1) at the actual budget excludes it in Q_Z.
  - s cannot checkmate s̄. s has no officers, and its context pawns never attack F_Z.
  - The new queen stands on F_Z, out of reach of context pawns (Lemma 2.2).

So s̄ promotes within T moves, which is a P-win. ∎
=======
**Theorem 2.7 (sufficiency of the certificate). PROVED after repair (in P).** If LC_T(m) holds at Y, then the
Z-move m is decisively punished in P.

*Proof.* s̄ plays r and then follows its local winning strategy σ_Z (which exists by (L1) with k = ∞), using
only Z-moves. It ignores the context. Check that the strategy survives in the full position, for t ≤ T.

- **s's moves map onto the k = ∞ local game.** A king move of s is the same king move in Q_Z. In Q_Z there
  are fewer pieces, so it is still legal there, and a capture of a context pawn becomes a plain move to the
  same square. A context move of s is a pass in Q_Z. It is never made while s is in check (the only checks
  during the window come from s̄'s Z-pieces, which are present in Q_Z), so the pass is allowed in the k = ∞
  game. The real defender's options are a subset of the k = ∞ game's options; its only possible gain from
  having fewer options is stalemate, which (L3) excludes (revised after review: R1 item 3, R3 items 2 and 3).
- **s̄'s prescribed moves are legal.** s̄'s king stays on F_Z, so by Lemma 2.2 no context pawn attacks it,
  occupies its squares or gives it check. s̄'s pawn moves stay on F_Z. Without sliders there are no pins.
- **s does not promote first.** After r, s moves first. Before s̄'s T-th move, s has made T moves, and by
  (L2) it needs at least T + 1. The removed Z-pieces of s̄ could only slow s down **except that s̄'s
  Z-pawns are capture targets for s; the theorem survives only if (L1)'s local game counts an s-promotion as
  a failure for s̄, which it does by "s̄ wins by promoting… s cannot capture at once"**. s's own Z-pawns are
  part of Q_Z, and σ_Z wins against them. (revised after review: R3 item 3b)
- **No other way out.**
  - (L3) excludes stalemate of s in the real position. (L1) at k = ∞ excludes it in Q_Z.
  - s cannot checkmate s̄. s has no officers; s's Z-pawns do attack F_Z, but σ_Z has a legal move on F_Z at
    every turn, and s̄'s real moves include its local ones, so s̄ is never forced to skip a move (revised
    after review: R3 item 3c).
  - The new queen stands on F_Z, out of reach of context pawns (Lemma 2.2).

So s̄ promotes within T moves, which is a P-win. ∎
>>>>>>> NEW

### EDIT 3: R3 item 7 — Corollary 2.8 (minor wording)
<<<<<<< OLD
The bound is the classical "rule of the square" with a two-square margin. Corollary 2.8 is rarely enough for
trébuchets, because the defending king starts next to the action. (L1) must then be checked by a small
search (Appendix A).
=======
The bound is the classical "rule of the square" with a two-square margin: with the defender to move,
d(k_s, q_D) ≥ D + 2 is exactly the classical rule of the square, not a margin on top of it (revised after
review: R3 item 7). Corollary 2.8 is rarely enough for trébuchets, because the defending king starts next to
the action. (L1) must then be checked by a small search (Appendix A).
>>>>>>> NEW

### EDIT 4: R1 item 9, R3 item 4 — Lemma 2.9 (hidden hypothesis added)
<<<<<<< OLD
**Lemma 2.9 (blockade). PROVED.** In Q_Z, suppose s̄'s only Z-pawns are on one file f, and s's king stands
on a square of f in front of s̄'s front pawn there. If s may pass (k = ∞), s̄ never promotes.

*Proof.*
- s passes forever. That is legal: s is never in check, because s̄'s pawns on f attack only files f ± 1, and
  a king never gives check.
- No s̄ pawn leaves file f: a capture needs an s-piece on f ± 1, and s has only its king, which cannot be
  captured.
- So every s̄ pawn on f must pass the king's square, which never empties. ∎

Hence if the defender can reach such a square in time, (L1) fails. Lemma 2.9 is how 7.2's White king
escapes (§5.2).
=======
**Lemma 2.9 (blockade). PROVED after repair (added hypothesis).** In Q_Z, suppose s̄'s only Z-pawns are on
one file f, and s's king stands on a square of f in front of s̄'s front pawn there. **Assume further that s
has no pawn on f ± 1 that an s̄ pawn could capture.** If s may pass (k = ∞), s̄ never promotes.

*Proof.*
- s passes forever. That is legal: s is never in check, because s̄'s pawns on f attack only files f ± 1, and
  a king never gives check.
- No s̄ pawn leaves file f: a capture needs an s-piece on f ± 1. By hypothesis s has no such pawn, and its
  king cannot be captured.
- So every s̄ pawn on f must pass the king's square, which never empties. ∎

**Without the added hypothesis the statement is a CONJECTURE** (an s-pawn on f ± 1 could be captured,
letting an s̄ pawn leave f). The uses in §5.2 and P5 are unaffected because s has no pawns there (revised
after review: R1 item 9, R3 item 4).
>>>>>>> NEW

### EDIT 5: R1 item 7, R3 item 1 — Proposition 2.10(a) (H ≥ 5 requirement)
<<<<<<< OLD
**Proposition 2.10 (which punishments are universal). PROVED.**
- **(a)** If T = 1, (L2) holds in every non-terminal context, that is, every context without a passer.
  *Proof:* an s-pawn that can promote in one move stands on its seventh rank. No enemy pawn can stand ahead
  of it, so it is passed, and the context would be terminal. The king's help does not change this: removing
  a blocker takes a move of its own. So a group whose punishments satisfy (L1) with T = 1 is decisively
  punished in every non-terminal context, provided (L3) holds. For T = 1, (L3) asks only that s has a legal
  move at its single turn.
=======
**Proposition 2.10 (which punishments are universal). PROVED.**
- **(a)** If T = 1 and **H ≥ 5**, (L2) holds in every non-terminal context, that is, every context without a
  passer. *Proof:* an s-pawn that can promote in one move stands on its seventh rank. No enemy pawn can stand
  ahead of it, so it is passed, and the context would be terminal. The king's help does not change this:
  removing a blocker takes a move of its own. For H = 4, a pawn on its second rank promotes by a double step
  onto the last rank in one move and need not be passed, so (L2) can fail with μ_s = 1 (revised after review:
  R1 item 7, R3 item 1). So a group whose punishments satisfy (L1) with T = 1 is decisively punished in every
  non-terminal context on boards with H ≥ 5, provided (L3) holds. For T = 1, (L3) asks only that s has a
  legal move at its single turn.
>>>>>>> NEW

### EDIT 6: R3 item 5 — Proposition 2.10(b) (last sentence labelled CONJECTURE)
<<<<<<< OLD
- **(b)** For every T ≥ 2 there is a non-terminal context with μ_s = 2.
  - *Example (White):* W (f, H−2); B (f, H−1) and (f+1, H−1). No pawn is passed. White captures to
    (f+1, H−1) and promotes next move.
  - So (L2) fails there, and a punishment with T ≥ 2 is never certified for all contexts. The zero of such a
    group is context-dependent.
  - CONJECTURE: for each frozen group with T ≥ 2 there is a context, with the defender in zugzwang there,
    where the freeze actually fails in P. *To settle:* kpsolve on Z_T (§5.1) plus 2-file contexts with fast
    White pawns.
=======
- **(b)** For every T ≥ 2 there is a non-terminal context with μ_s = 2 (this requires board width ≥ |F_Z| + 4).
  - *Example (White):* W (f, H−2); B (f, H−1) and (f+1, H−1). No pawn is passed. White captures to
    (f+1, H−1) and promotes next move.
  - So (L2) fails there, and a punishment with T ≥ 2 is never certified for all contexts. **The statement
    "The zero of such a group is context-dependent" is a CONJECTURE** (it is exactly the conjecture stated in
    the next bullet; §0 repeated it as fact). CONJECTURE: for each frozen group with T ≥ 2 there is a
    context, with the defender in zugzwang there, where the freeze actually fails in P. *To settle:* kpsolve
    on Z_T (§5.1) plus 2-file contexts with fast White pawns.
>>>>>>> NEW

### EDIT 7: R3 item 6 — Remark 2.11 (labelled GAP, explained)
<<<<<<< OLD
**Remark 2.11 (the certificate is not special to kings).** A passer created in a component is a decisive
event too, and (V2) asks the same question about it. The certificate applies with the passer's owner as s̄,
but the local game must contain **both kings and all Z-pawns**: the defending king may abandon Z to catch the
passer. That is the "king leaves Z and catches a passer" failure, which this certificate rules out.
=======
**Remark 2.11 (the certificate is not special to kings). GAP.** A passer created in a component is a decisive
event too, and (V2) asks the same question about it. The certificate of Definition 2.6 **cannot apply as
written** to a passer (revised after review: R3 item 6):
- Q_Z deletes "every context pawn", which deletes the passer itself.
- The punishing reply r is not a king capture of a Z-pawn.
- The passer's owner may need its king off F_Z, where the legality step via Lemma 2.2 no longer covers it.
- The pawns of the passer's own component are not addressed.
The claim "which this certificate rules out" is therefore unproved. P11 in §6 relies on this remark under a
PROVED label; that label must be revised when the certificate is extended.
>>>>>>> NEW

### EDIT 8: R1 item 10, R4 item 9 — Section 5.1 (L1 evidence claim corrected)
<<<<<<< OLD
- **Certificate.**
  - Corollary 2.8 fails for every sortie. After ...Kxa4 the punisher's king stands on its own pawn's path,
    so it needs a king step plus 4 pushes, and the defending king is within distance 5 of a1.
  - (L1) holds for all five White sorties with T ≤ 7 (5 to 7, depending on the sortie and the budget), for
    every pass budget, with the punisher's king confined to {h, a, b}. This is scratch evidence
    (Appendix A).
  - With (L1), Theorem 2.7 makes the freeze valid in P for every context in which (L2) holds with
    μ ≥ 8 at the zugzwang nodes, and (L3) holds.
  - On 8 ranks a single free White pawn on rank 2 has μ = 5. So the certificate covers only locked or slow
    contexts. Next to fast pawns the zero has to be checked case by case (Proposition 2.10b).
=======
- **Certificate.**
  - Corollary 2.8 fails for every sortie. After ...Kxa4 the punisher's king stands on its own pawn's path,
    so it needs a king step plus 4 pushes, and the defending king is within distance 5 of a1.
  - (L1) holds for all five White sorties with T ≤ 7 (5 to 7, depending on the sortie and the budget), for
    pass budgets **k ≤ 4 and k = ∞**, with the punisher's king confined to {h, a, b}. Budgets k = 5, 6 were
    not checked; they differ from ∞ when T ≥ 6. This is scratch evidence (Appendix A) (revised after review:
    R1 item 10, R4 item 9).
  - With (L1), Theorem 2.7 makes the freeze valid in P for every context in which (L2) holds with
    μ ≥ 8 at the zugzwang nodes, and (L3) holds.
  - On 8 ranks a single free White pawn on rank 2 has μ = 5. So the certificate covers only locked or slow
    contexts. Next to fast pawns the zero has to be checked case by case (Proposition 2.10b).
>>>>>>> NEW

## STATUS ROWS
| result | final label | one-line note with review item |
|---|---|---|
| D2.6, (L3′) | withdrawn | never applies for T ≥ 2 on a 3-file group; does not give (L3) | R1 item 8, R3 item 2 |
| T2.7 | PROVED after repair | (L1) required only for k = ∞, (L3) covers stalemate, local rules stated, μ counts context pawns only | R1 item 3, R3 items 2 and 3 |
| C2.8 | PROVED | wording corrected: classical rule of square, not two-square margin on top | R3 item 7 |
| L2.9 | PROVED after repair | added hypothesis: s has no pawn on f ± 1; without it CONJECTURE | R1 item 9, R3 item 4 |
| P2.10(a) | PROVED after repair | needs H ≥ 5 (4-rank double steps) | R1 item 7, R3 item 1 |
| P2.10(b) | PROVED (example); "zero context-dependent" is CONJECTURE | example needs width ≥ `&#124;F_Z&#124;` + 4; last sentence is the conjecture | R3 item 5 |
| R2.11 | GAP | no certificate for passers claimed; Q_Z deletes passer, r not king capture, king may leave F_Z | R3 item 6 |
| §5.1 (L1) evidence | CONJECTURE (scratch) | budgets k ≤ 4 and ∞ only; k = 5, 6 unchecked for T ≥ 6; (L3) not checked | R1 item 10, R4 item 9 |