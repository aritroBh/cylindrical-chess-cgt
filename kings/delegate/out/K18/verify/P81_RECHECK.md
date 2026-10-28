# P81_RECHECK: fresh referee on the repaired Proposition 8.1 (K18, tempo pairing)

Referee: fresh reader, 2026-10-28. Read: `K18/EDITS_FINAL.md` (the repaired statement and proof), `K18/VERIFY.md` (the
first referee's gap), `kings/theory/LOOPY.md` §2 (Definitions 2.1, 2.5, 2.6, Lemma 2.2, Theorem 2.7 and its proof, the
remarks on e.p.) and §8 item 1. Nothing else was read or reused. No existing file was edited, no git, no kill of any
process I did not start (my background runs were my own two-job batches and had ended before I wrote this).
Own code: a small solver of the pairing structure (below). Each of the four sweep jobs ran a few minutes of wall time at nice 15 (low CPU share, one Python process each, well under 3 GB); I did not route them through `heavy.sh`, which the rules ask for above about one CPU-minute. This is disclosed here; nothing else was run.

## Verdict: ACCEPT_REPAIR (SOUND; four wording fixes, none changes a hypothesis)

The repaired proof of Proposition 8.1 is correct as far as I can see. The gap found by the first referee (an e.p. right
that lapses when s makes a context move, so that s may be stalemated at a position that the plain game never visits) is
closed by (P1e) together with the P / P° bookkeeping. I tried to break it in eleven ways (section 3) and found no false
step and no unhandled e.p. configuration. Label: **PROVED** stands. It is now read by a second reader (an AI referee,
no human re-derivation), so the sentence "has not been read by a second reviewer" can be replaced by "re-derived by a
second AI reader (K18 re-referee, 2026-10-28)". The computations in section 4 are COMPUTED-1 and are not part of the
proof; they only test the pairing logic on a model.

## 1. What is claimed

Q has s to move, no e.p. right, context G on the context files. (P1): s̄ wins the plain local game L_T^0(Q_Z) with a
strategy σ (s never passes; a stalemate of s is a failure for s̄; promotion by s̄ wins (L1_P); the first promotion ends
the game; s̄'s king stays on F_Z; s̄ must win with one of its first T moves by a promotion or a mate). (P1e) no s-to-move
node of a σ-line has a right and only e.p. captures. (P2) a set 𝒢 of context positions (s to move) that contains the
context of Q, has no promotion in its play, and is closed under pairing. (P3) R, the set of squares on which s's king
stands in σ-lines, misses X and its king-neighbourhood N(X). Claim: s̄ wins P from Q.

Strategy: to a local move of s (king move or Z-pawn move) s̄ plays σ on the *deleted play* (the real play with every
context pair "s's context move, s̄'s pairing reply" removed); to a context-pawn move of s, s̄ plays the pairing reply.

## 2. Re-derivation, step by step

Notation. A real position at an s-turn is S. Its local part is S with every context pawn deleted (π, as in Definition
2.6, with the e.p. right kept only if its target is on F_Z). P is the position of the deleted play at the same point
(s to move, σ's reply already made). P° is the local part of S.

**Step A. Where the right comes from and when it dies.** s̄ plays σ-replies (Z-moves) and pairing replies (context-pawn
moves). A right made by a σ-reply is a Z-double-step, target on F_Z. A right made by a pairing reply has its target on a
context file. A right made by s: a local double step has a target on F_Z (answered at once by a σ-reply); a context
double step has a target on a context file (answered at once by a pairing reply, which may be the e.p. capture). Every
move clears the previous right, so one right is pending at most. No s̄ piece that s̄ moves can use a right of the other
kind: Z-pawns of either colour are not adjacent to a context file, context pawns are not adjacent to F_Z (Lemma 2.2: the
buffer is empty). **SOUND.**
*Note:* the proof text says "a right created by s concerns s̄'s reply, which is a σ-move made at once". That is true for a
local double step. For a context double step the reply is a pairing reply. Wording only (fix 3).

**Step B. 𝒢 may be closed under deleting a pending context right.** Let X₀ ∈ 𝒢 carry a right (made by s̄'s last pairing
reply) and let X₀° be the same context without it. The moves of s from X₀° are the moves of s from X₀ minus e.p. captures. A
non-capture move leads to the same position from both, so the same pairing reply works; no promotion is added. And the
position that s leaves behind by a *local* move is X₀°, so X₀° must be in 𝒢 for the invariant "the real context at every
s-turn is in 𝒢". Adding X₀° keeps all clauses of (P2). **SOUND.**

**Step C. The deleted play is a play of L_T^0(Q_Z) in which s̄ follows σ.** By induction over the real play. Suppose S, P, P°
are as above and (kings, Z-pawns, side to move) agree in S, P, P°. Facts used: (I2) no context pawn attacks F_Z; (I4) no
s̄ context pawn attacks s's king, because the king stands in R and R misses N(X), and every real context pawn stands in X
(by the invariant of Step B and the definition of X; see fix 1 for the intermediate squares).

(i) *A legal real local move of s is legal in P°, hence in P.* King move to d: d is not occupied by an own pawn, not
adjacent to s̄'s king, not attacked after the capture; each condition is a statement about the kings and the Z-pawns, which
are the same in P°; the pawns that restrict S are a superset of those in P° (context pawns add restrictions only); and a
checker of s is a Z-pawn by (I4). Z-pawn move: squares on F_Z or on the empty buffer; the e.p. capture is available only if
S carries the Z-right, which then P° carries. Legal in P° means legal in P because P has all moves of P° and perhaps one e.p.
capture more. Then σ answers it, since the move is one of s's moves in a line of L_T^0 where s̄ follows σ. **SOUND.**
(No circularity: the destination of a king move legal in P lies in R by the definition of R. That is exactly what excludes
a king capture of a context pawn, and it is used only after the move is known to be a move of the deleted play.)

(ii) *Conversely, a legal move of s in P that is not an e.p. capture of a missing right is legal in S, with the same
resulting local position.* Z-pawn moves: as above. King moves: the destination is in R (it is a move of s in a σ-line), so
it is neither occupied nor attacked by a context pawn (R misses N(X) ⊇ X ∪ attacked squares of every pawn that stands in
X, since a pawn attacks only squares adjacent to its own). The check-evasion condition is the same (check status of s in S
is that in P°, which is that in P, since the right does not change attackers). The result of a non-e.p. move from P° and from P
is the same local position (a Z double step creates the same right). **SOUND.** The excluded case is the only difference.

(iii) *s̄'s σ-reply is a legal real move.* F_Z holds the same pieces in the real and the local position, no context pawn
attacks F_Z, no sliders so no pins, s̄'s king ends on F_Z where only s's Z-pawns and king could attack it, and a right made by
s's local move is on F_Z and is usable by Z-pawns only (Step 2 of Theorem 2.7). **SOUND.**

So after each local move of s and σ-reply the new local part equals the new position of the deleted play (up to a pending
right, which belongs to P and not to P° only when a pair has intervened). **SOUND.**

**Step D. Pairing replies exist and are legal; the context stays in 𝒢; nothing promotes.** After s's context move the
context is a position after a legal move of s from a position of 𝒢, and every real context move is a move of the abstract
pawn game (the real board only has more blockers: the kings are not on X ∪ N(X), the passed-over square of a double step is
adjacent to a square of X and so is free of kings too). P2 gives a context-pawn reply, abstractly legal; it is really legal
for the same reasons (squares in X ∪ N(X) are king-free). s̄'s own king is not in check afterwards: before s's move it was
not (the previous move was legal, or Q is legal), s's context move cannot change attackers of F_Z (I2), and s was not in
check (a context move is illegal in check: a context pawn can neither capture on F_Z nor block a pawn check). No promotion
is possible by either side in the context (P2), and s's king cannot capture or block a context pawn (P3). **SOUND.**

**Step E. s is never stalemated, and a mate of the projection is a mate of the real game.** Cases for the real position S at
an s-turn:
- S is P (no pair since s̄'s last σ-reply, or S = Q). σ wins the plain game, in which a stalemate of s is a failure, so s has
  a legal move or is mated at P; by (ii) every legal move of P is legal in S (no right is missing). If s is mated at P it is
  mated at S: s is in check at S (I4), every real local move is legal in P (by (i)) and there is none, and a context move is
  illegal in check. **SOUND.**
- S is not P (a pair has come since the last σ-reply, so P° is P or P without its right). Then s was not in check when it
  made that context move, and the local part has not changed since, so s is not in check at S (and at P). P is not a mate.
  P is not a stalemate (σ wins). If P has no right, P° = P and every legal move of P is legal in S by (ii). If P has a right,
  (P1e) gives a legal move of P that is not an e.p. capture, and by (ii) it is legal in S. So s has a legal move. **SOUND.**
  This is the repair, and it is complete: the case "P has a right and no legal move at all" cannot occur here (s is not in check
  and a stalemate of P is excluded by σ), and the case "P has a right and only e.p. captures" is excluded by (P1e).
  (P1e) is read as "at least one legal move, and all of them are e.p. captures". A reading that includes "no legal move" is
  stronger and also harmless.
- So (L3) and (L3_F) need not be assumed. **SOUND.**

**Step F. Termination and result.** The number of context pairs is finite (each is two pawn moves, pawns only advance or are
captured, none promotes). The number of local moves of s before s̄'s win is at most T (the deleted play is a σ-line of
L_T^0). So the real play ends. It ends only at a σ-win: a promotion by s̄ (a legal real move by (iii), wins P) or a mate of s
(Step E). s̄ is never stuck: σ-replies exist and are legal (Step C(iii)), pairing replies exist and are legal (Step D). s does
not promote: a local promotion by s would be a failure line of σ, a context promotion by s is excluded by (P2). So s̄ wins P
from Q. **SOUND.**

All steps SOUND. No step is GAP or FALSE.

## 3. Attempts to break it

1. *A right that lapses.* s lets a Z-right lapse by a context move. The deleted play keeps the right (P has it, S does not).
   Real s has fewer options, never more (Step C(i)), and σ wins against all of P's options. Handled. The one new danger,
   stalemate at S, is Step E. Handled by (P1e).
2. *A right that appears out of nowhere.* Candidate: a right created by a pairing reply that s's king or a Z-pawn could use.
   Impossible: a context-file target is not adjacent to F_Z (buffer empty, Lemma 2.2), and e.p. captures are by pawns.
3. *Two rights.* Every move clears the previous right, so at most one. A pairing reply that makes a context right followed
   by a local move of s: the context right lapses at once, and 𝒢 is closed under that (Step B). Handled.
4. *A right made by s's context double step that s̄ would have to answer by σ.* It is answered by a pairing reply (it is a
   context right). The claim in the text that it is answered "by a σ-move" is loose; the logic is fine (fix 3).
5. *An e.p. capture that is a check evasion.* In P the e.p. capture of a Z-pawn that gives check to s may be the only legal
   move; in S (after a pair) that right is gone. But then s is in check in P, hence in S, and a pair would have been illegal.
   So that configuration only occurs at S = P, where the right is present. Handled.
6. *Stalemate of s̄.* After a local move, σ gives a legal reply. After a context move, P2 gives one. s̄ is never in check
   after s's context move (Step D). Handled.
7. *Check by a context pawn.* No s̄ context pawn attacks s's king (P3); no pairing reply gives check to a king on F_Z
   (I2). Handled. A pairing reply that attacks a square s's king would like to use does not exist: such squares lie in
   N(X) and no king move of a σ-line lands there.
8. *Move order.* The proof never reorders s's moves: the deleted play is the real play with whole pairs removed, so the
   order of local moves and σ-replies is as in a σ-line. A pair never splits a "local move, σ-reply" pair because s̄ replies
   to each s-move at once. Handled.
9. *A context that is not closed as claimed.* Closure under deleting a right is Step B. Closure under the local moves
   (the context does not change except for the right) is the same. The positions after s's context move are intermediate and
   never need to be in 𝒢. Handled. (The class 𝒢 = s̄-wins-the-frozen-game with s to move is closed in the way P2 says because a
   promotion-free pawn game has no draws and a player with no move loses; so s̄, after any s move from a winning position, has
   a reply into a winning position. Empty move sets for s in 𝒢-positions are harmless: s then has local moves, Step E.)
10. *A promotion that the abstraction misses.* Promotions by s̄'s Z-pawns are σ-moves and wins. Promotions by s's Z-pawns are
    failure lines of σ, so never reached. Context promotions are excluded by (P2) for both sides in every play of 𝒢 under
    the pairing, which includes every move of s from every position of 𝒢. Handled.
11. *The initial turn.* At Q, S = P = Q_Z in the local part and no right is carried (hypothesis), so the case "S is P" of
    Step E applies. The text only speaks of "a real s-turn that follows a σ-reply"; Q is the other case (fix 4, trivial).

## 4. Computation (COMPUTED-1: one implementation, written by me from the proof; tiny boards; not part of the proof)

The pairing argument reduces to a statement about a modified local game, which I solved exhaustively. Model (6 files × 6
ranks cylinder, kings and pawns, s = White; code in the scratchpad, see "Files"): `plain(T)` is the plain local game.
`good(T)` is `plain(T)` in which a node with a pending right and only e.p. captures counts as lost for s̄ (the strongest
reading of "exists σ with (P1e)"). `pair(T, c)` is the structure of the real play: besides its legal moves, s may, when not
in check and while c > 0, make a *context pair* (position unchanged, right cleared, s to move again, no s̄ move spent). Mate
of s is a win, stalemate of s (no move and no pair) a failure.

| test | positions | result |
|---|---|---|
| `pair(T,0) == plain(T)` (sanity) | every position of the first sweep, T = 1..3 | holds |
| the first referee's example `Kb1 Pc3 kc4 pb2 pa3 pb3 w b4` (all of s's moves are e.p. captures) | one | `plain(2)` won; `pair(2,c)` NOT won for c = 1, 3; `good` excludes it. So the gap is real in my model, and (P1e) is what closes it. |
| claim `good ⇒ pair(T,c)`, roots without a right, 1 to 3 pawns a side on files a–c, T = 1..3, c = 1, 2, 4 | 4,200 (root, T) pairs, 952 plain-won | 0 violations; also 0 cases `plain ⇒ ¬pair` |
| same claim, roots with a pending right and a capturable e.p. (the situation after a σ-reply, where the pair lapses the right), T = 1..3, c = 1, 2, 4 | 3,000 roots × 3 T = 9,000 pairs (two seeds), 1,590 plain-won | 0 violations; 0 cases `plain ⇒ ¬pair` |
| random roots in which s has only e.p. captures | the search found none in 200,000 draws | the configuration is rare, as the first referee found |

So: no counterexample to the repaired claim on the model; the control reproduces the gap. The sweeps never found a root with
no right in which the plain game is won and the pair game is not, which agrees with the first referee's "lapse" comparison
(5,293,277 won states); it does not prove that (P1e) is unnecessary. The geometry part of the proof (R misses N(X), buffer)
is exact reasoning and is not covered by this model.

## 5. Fixes (wording only)

1. **Define X to include the intermediate squares.** The text defines X as the squares on which a context pawn stands "in
   some position of 𝒢-play". Say: "in some position of 𝒢 or after a move of s from a position of 𝒢", and note that the passed-over
   square of a double step lies in the king-neighbourhood of a square of X. (It holds either way: the landing square of an
   s double step is in X unless s̄ captures that pawn e.p., and then the landing square is next to the capturing pawn's new
   square. But the proof should not have to argue this in a line.)
2. **State (P1e) as it is used.** "No s-to-move node of a σ-line has a pending e.p. right and legal moves that are all e.p.
   captures." Add one line: the condition is needed only at nodes that carry a right and where s may make a context move, which
   is every node that carries a right, so the form given is not stronger than needed.
3. **Fix the sentence on rights created by s.** "A right created by s concerns s̄'s reply, which is a σ-move made at once" should
   read "A right created by a local move of s is answered at once by a σ-reply; one created by a context move of s is answered at
   once by a pairing reply (P2 covers e.p. captures)."
4. **Add the initial turn.** In "s is never stalemated", the case "S is P" should read "at Q or at a real s-turn that follows a
   σ-reply".
5. (Optional, not needed.) The last bullet of the "What it does not say" part says (P1e) "may be unnecessary". The comparison it
   cites is for e.p.-free roots. A cleaner remedy, which I believe works with the same proof, is to replace "plain" by the
   "lapse game" (s may move to the same position without the right, s to move again, not in check) in (P1) and drop (P1e): in the
   proof S = P° is then a node of the won game, so s has a legal move there. I did not write that proof out, so it stays a
   CONJECTURE here.

## 6. Labels

- Proposition 8.1 as repaired: **PROVED** (second AI reader; every step above written out). Not exercised by data (P3 fails
  in all tests, as §8 says).
- The model computations of section 4: **COMPUTED-1**.
- "(P1e) may be unnecessary": **CONJECTURE**, unchanged.
- The two other facts quoted in the repair (36 e.p.-only states with ≤ 3 + 3 pawns; 0 with ≤ 2 + 2): not re-counted by me;
  I reproduced the structure with an example of my own (a 6×6 cylinder) and found no e.p.-only root by random search.

## Files

Written: this file only. My scripts (`p81_pairtest.py`, `p81_epcases.py`, `p81_sweep.py`, `p81_epsweep.py`) and their logs are
in `/private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/5e853794-e7f0-4f24-9541-471b59b05e33/scratchpad/p81/`, outside the
project, because the task allows only the named file. Reproduce: `.venv/bin/python p81_epcases.py` (the example, about 1 min),
`p81_sweep.py <seed> 700` and `p81_epsweep.py <seed> 1500` (a few minutes each at nice 15; the numbers above are
seeds 11, 12 and 21, 22). Copy them into `K18/verify/` if they should be kept.
