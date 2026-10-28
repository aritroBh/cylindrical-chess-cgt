# K36 blind packet: definitions and statements only (extracted from kings/theory/LOOPY.md at commit 94079e64)

Proofs and verification notes are omitted on purpose. Do not read LOOPY.md itself until Phase 2.

## §1.2 (Definitions 1.1–1.5)

### 1.2 Games with decisive terminals, and four models

**Definition 1.1 (D-game).** A *D-game* is a finite set X of positions with, for each x ∈ X, finite option
sets L(x) and R(x) contained in X ∪ {⊕, ⊖}.
- ⊕ is the terminal "White has won". ⊖ is the terminal "Black has won".
- The D-game is *short* if the directed graph of moves on X is acyclic, and *loopy* otherwise.
- ∅ denotes a position with no options.

**Definition 1.2 (play and results).**
- Play alternates from (x, s), where s is the player to move.
- A move to ⊕ or ⊖ ends the play with that result.
- A player with no option loses (*normal play*).
- Infinite play is a draw.
- r(x, s) = W if White can force a White win in finitely many moves, L if Black can, and D otherwise.

KNOWN: on a finite game graph these values are the least fixed point computed by retrograde analysis
([S] ch. VI; this is also what kpsolve computes). A short D-game has no draws (Zermelo).

**Definition 1.3 (sum with chess semantics).** For D-games A₁, …, A_k, the sum A₁ ⊞ … ⊞ A_k works as follows.
- Its positions are tuples.
- A move is a move in one coordinate.
- A move to ⊕ or ⊖ in *any* coordinate ends the *whole* play. This is "the first decisive event ends the
  game".
- A player with no option in any coordinate loses.

**Definition 1.4 (BIG translation).** For a short D-game A and an integer B ≥ 1, A^B is the short CGT game
obtained by replacing ⊕ with the integer B and ⊖ with −B. For a sum, (A₁ ⊞ … ⊞ A_k)^B := A₁^B + … + A_k^B
(the disjunctive CGT sum). In this sum a ±B summand does **not** end play: the other components continue.

**Definition 1.5 (four models of a king-and-pawn position X).**
- **C(X), chess.** The rules of `kings/SPEC.md`: checkmate wins, stalemate is a draw, infinite play is a draw.
- **P(X), the promotion model.** Chess, except that the first promotion ends the game as a win for the
  promoter. Stalemate and infinite play are still draws.
  - `kpsolve --frozen` computes the frozen-king model F of Corollary 2.7′ (a king move loses at once for the mover), not P. P itself, with free kings, is computed by K7's build `kings/delegate/out/K7/scripts/draft/kp_p.c` (its flag is `--pmodel`; `kings/kpsolve.c` has no such flag) and by the independent solvers of K19 and K24 (revised after K24, 2026-10-27: this line used to say that `--frozen` computes P).
- **D(X), the decisive-event model.** A D-game. Its positions are the positions before the first decisive
  event. Its terminals are the decisive events:
  - a passer appears (as in `cylcgt`), with races scored by a race rule;
  - a punished move in the king group (§2). Under (V3) of Theorem 1.14 *every* move inside Z is a punished
    move, so the king group then contributes only suicides and is deleted by Lemma 1.7; the setup of
    Theorem 1.14 and this definition agree under (V3) (revised after review: R2 item 10).
- **S(X), the BIG convention.** The BIG value of X: at every node of the game tree the position is split
  into its components (files separated by an empty file, and an empty file stays empty), each component is
  translated separately, and the translations are summed; a component with a passer is worth ±BIG, races being
  scored by the race rule. This is the value `cylcgt.pawns.value` computes (COMPUTED-1, `cylcgt/pawns.py`).
  - *What S(X) is not* (revised after review: R2 item 2): it is not the BIG translation D(X)^B of the D-game of
    §1.2, in which the components are those of the root and the first decisive event ends the whole play.
    `cylcgt` re-splits at every node, and a passer freezes only its own component, so the two differ as soon
    as a component splits. Example: flat 7×6, e.p. on, count rule, `W: b2 d3 f2 / B: c4 c5 e5 g5` is one
    component at the root, yet o(S) = 𝓝 while the decisive-event result is 𝓡 (COMPUTED-1, `lemmas/common.py`:
    o(S) = N, o(W) = R).
  - The re-splitting is why (V4) of Theorem 1.14 has to be checked hereditarily; see Theorem 1.11(c).

The models are connected by bridges, each with its own hypotheses:

*Notation.* o(G) is the outcome class of a CGT game G (𝓛, 𝓡, 𝓝, 𝓟); W(X) is the whole-board convention game
of a pawn position X, in which the first passer ends the game (`notes/lemmas.md`); S(X) is the BIG value of
§1.5; and HSS, hereditary sum-safety, is the hypothesis (HSS) of Theorem 1.11(c). (Revised after review:
R1 item 11: §6 used o(W(X)) and "hereditarily sum-safe" without defining them.)

```
S  --Thm 1.11(c) (V4)-->  D  --Thm 1.14 (V1-V3)-->  P  --(A_Q)(X)-->  C
```

**Axiom (A_Q)(X) (per-position hypothesis, checked by kpsolve).** For a fixed position X: if X is a P-win
for σ, then X is a C-win for σ.
- **FALSE as a general statement (revised after review: R1 item 6, R2 item 8).** cyl:7×6 `Ke2 Pb5 ka5 w -` is
  a P-win (b6=Q at once; `kpsolve --frozen` gives W W) and a chess draw (exact D D: every White move draws);
  flat:4×4 `Kd1 Pb3 ka3 w -` is the same (b4=Q is met by Kxb4). So (A_Q) is not an axiom: it is a hypothesis
  to be checked at each position, and every "PROVED in P" claim below is a chess claim only where it holds.
- *Evidence for:* the cylinder KQK tables agree in two independent solvers ([RESULTS.md](../../RESULTS.md) §2:
  KQK is 100% won on the 8×8 cylinder).
- *Evidence against, in general:* L4.4 of `notes/lemmas.md` is a promotion race lost to a promotion with check.
- *Settled by:* kpsolve with `--cap 1` computes C exactly whenever its bounds agree (A = B), and `--frozen`
  computes P; the two runs decide (A_Q)(X) for that X.


## Definition 2.1

**Definition 2.1 (king group, buffer).** A *king group* Z consists of:
- a set F_Z of files (an arc on a cylinder);
- both kings and some pawns, the Z-pawns, all on F_Z.

All other pawns, the *context*, stand on files at distance ≥ 2 from F_Z. The files at distance exactly 1
are pawn-free; they are the *buffer*. A *Z-move* is a move of a king or of a Z-pawn.
- On the 7×6 cylinder with F_Z = {a, b, c}, the buffer is {d, g} and the context lies on {e, f}.

## Lemma 2.2 (statement only)

**Lemma 2.2 (buffer invariance). PROVED.** Before the first promotion:
- no pawn ever stands on a buffer file;
- context pawns stay on context files, and Z-pawns stay on F_Z;
- hence a king standing on F_Z is never attacked by a context pawn, and a context pawn never attacks a
  square of F_Z.

## Definition 2.5

**Definition 2.5 (decisive punishment, in chess terms).** A Z-move m of side s, made at a chess position Y
(context plus Z), is *decisively punished* if the opponent s̄ has a forced win in P (or in C) from the
position after m. The win must hold against every defence of s:
- s's moves in the context, including creating passers, starting races and capturing en passant;
- s's king going anywhere, back into Z or into the context;
- s promoting;
- s steering for stalemate.

"Whatever the other components contain" means: for every context in the class one claims the zero for.
Theorem 2.4(b) needs this only at positions where s is losing the context.

## Definition 2.6

**Definition 2.6 (local certificate LC_T). (revised after K7, 2026-10-22)**

*Data.*
- Y is a position as in Definition 2.1 with s to move: both kings on F_Z, the Z-pawns on F_Z, the context on files
  at distance ≥ 2 from F_Z, the buffer empty, no officer, no promotion yet. An e.p. right carried by Y is cleared by m. The proof of (a) does not
  use that Y is chess-legal: it uses that m and r are legal moves (see (b)).
- m is a legal Z-move of s that is not a promotion. It may take s's king off F_Z.
- r is a legal reply of s̄ to m that is not a promotion, is a Z-move, and leaves s̄'s king on F_Z. The standard r
  is a king capture of a Z-pawn of s. (If s̄ can promote at once there is nothing to certify: that is a P-win.)
- Q is the position after m and r, with s to move. T ≥ 1 is an integer.
- The *window* is the sequence s, s̄, s, s̄, … from Q. So s̄'s t-th move after r comes after s's t-th move, and
  s̄ must have won by its T-th move.
- The *projection* π(R) of a position R is R with every pawn deleted that stands off F_Z, of both colours. The
  kings (wherever they stand), the Z-pawns, the side to move, and an e.p. right whose target square is on F_Z
  are kept. Put Q_Z = π(Q). (Earlier text: "Q with every context pawn deleted". The e.p. right and the place of
  s's king were not said.)
- In (a), r is a Z-move, so an e.p. right carried by Q has its target on F_Z. In the window form (b) the
  target may be anywhere, and (L2) accounts for it (revised after K7, 2026-10-22).

LC_T(m) holds at Y if some such reply r satisfies (L1), (L2) and (L3).

- **(L1) local forced promotion against a passing defender.** The *local game* L_T(Q_Z) is played on the same
  board (same files and ranks, flat or cylinder) from Q_Z with s to move, by the rules of chess, with these
  changes:
  1. *Promotion (P semantics).* The first promotion by either side ends the game. A promotion by s is a win for
     s, whatever happens to the new piece: it is a **failure** for s̄. A promotion by s̄ is a win for s̄ if the
     new queen cannot be captured at once, that is, if no legal move of s captures it. An unsafe
     promotion ends the game as a failure for s̄.
  2. *Passes.* s may pass at any turn in which it is not in check, as often as it likes (k = ∞). s̄ may not
     pass. A pass changes only the side to move and clears the e.p. right.
  3. *Confinement.* s̄'s king may only step onto squares of F_Z. s̄'s pawn moves are not restricted; by Lemma 2.2
     they stay on F_Z.
  4. *Mate and stalemate.* If s is in check and has no legal move, s is mated and s̄ wins. With unlimited
     passes s can never be stalemated in the local game. If s̄ has no permitted move at its turn (checkmate,
     stalemate, or only king moves that leave F_Z), that is a failure for s̄.
  5. *Time.* s̄ must win with one of its first T moves, by a promotion as in 1 or by a move that mates s.
     Anything else is a failure.

  (L1) holds if s̄ has a strategy that wins L_T(Q_Z) against every behaviour of s, passes included.
  **(L1_P)** is the weaker condition in which every promotion by s̄ is a win (no queen clause). Theorem 2.7 holds
  with (L1_P) in place of (L1); the queen clause is for the chess statement (A_Q).
  - The unlimited budget models the fact that s's spare moves in the context are not known in advance; the real
    defender's options are a subset of the k = ∞ game's, and its only gain from having fewer options is
    stalemate, which (L3) excludes. The earlier phrasing "for every k" and the remark that "every k is needed"
    are withdrawn (revised after review: R1 item 3, R3 items 2 and 3).
  - The earlier clause "s with no legal move and no pass left is stalemated, which counts as a failure for s̄"
    has no content for k = ∞. Stalemate enters in two places only: a stalemate of s̄ is a failure (rule 4),
    and a stalemate of the *real* s is excluded by (L3).
- **(L2) no faster counter-promotion by a context pawn.** Let Q° be Q with s̄'s king and all Z-pawns of both
  colours deleted. s's king and the context pawns of both colours stay. Let μ_s be the least number of
  consecutive s-moves (s̄ never moves) after which a context pawn of s promotes in Q°, and ∞ if none can. The
  moves are chess moves: a king may not step onto a square attacked by a pawn of s̄, an s̄ context pawn stays
  where it is unless s captures it, and no e.p. right exists except the one described next. If Q carries an
  e.p. right whose target square is **off F_Z**, Q° keeps it: s may use it at its first move, and only then
  (the capture lands on the target and removes the s̄ pawn that has just double-stepped). A right whose target
  is on F_Z concerns Z-pawns only, which Q° has deleted, so it is dropped. In (a) Q carries no right of the first
  kind. Then **μ_s ≥ T + 1**.
  - μ_s is a breadth-first search over s's king and context pawns. A king move that captures an s̄ context
    blocker is one of the moves, so the king's help is counted, and so is the e.p. capture just described.
  - **Which s-pawns are counted.** Only the context pawns. s's Z-pawns are not counted by (L2): their
    promotions belong to the local game, where s̄'s Z-pieces stay on the board and a promotion by s is a failure
    for s̄. This replaces the earlier text, in which μ_s counted s's king and all pawns, Z-pawns included, with
    s̄'s Z-pieces removed. Reasons:
    - The proof needs (L2) only for the promotions that (L1) cannot see, and what (L1) deletes is the context.
    - The earlier count was not a lower bound for a Z-pawn: deleting s̄'s Z-pieces can raise or lower it (R3
      item 3b: 3 moves against the real 2).
    - As a hypothesis it was stronger than needed. `Ke6 ka1 Pc4 pb3 pc5`, White to move (cyl:7×6), is a Black
      win in P. Black's local win has T = 2 (b2, b1=Q), no White context pawn exists, but the old count gave
      μ_s = 2 for White's Z-pawn c4 once Black's c5 was deleted, although c5 locks it. (L1), (L2), (L3) as now
      stated all hold; the old (L2) failed.
    - With context pawns only, Proposition 2.10(a) needs no Z-pawn proviso: s's Z-pawns are covered by (L1),
      whatever their distance from promotion (a promotion by s is a failure for s̄ in the local game).
    - Anyone who wants the stronger hypothesis may assume both; the theorem holds a fortiori.
  - **μ_s ≥ T + 1 is the exact bound for P.** Step 4 shows that s promotes no earlier than its (T + 1)-th turn, and
    s̄ queens on its T-th move, which follows s's T-th turn. With μ_s = T, s promotes first (example below).
  - **(L2⁺)**, μ_s ≥ T + 2, is only a margin, and it does not give a chess win. With μ_s = T + 1, s promotes at once
    after s̄ queens (queen against queen, not against a pawn on its seventh rank). With μ_s = T + 2, s̄ has one move
    with its new queen, and a draw can still follow. No margin of μ_s replaces (A_Q) at the position (examples in
    "What Theorem 2.7 does not give"). The earlier wording, "queen-against-seventh-rank-pawn endings can be
    drawn", described the T + 1 case wrongly (revised after K7, 2026-10-22).
- **(L3) no stalemate of s in the window.** A *guided strategy* of s̄ is a strategy in the real game that at each
  of its turns plays a Z-move (a king step onto a square of F_Z, a move of a Z-pawn, or a promotion) whose
  projection is a winning move of L_T(Q_Z) at the projected position, with the remaining time. s̄ never moves a
  context pawn. (A winning strategy of the local game, read in the real game, is guided.) (L3) asks for a
  guided strategy such that, in every real play from Q in which s̄ follows it and s plays legal moves as it
  likes, s is never stalemated at one of its turns in the window. A mate of s ends the play in s̄'s favour and
  is not excluded.
  - (L1) cannot see (L3): it lets s pass, while the real s has only the context moves that exist. The danger is
    a context pawn taking away king squares that are free in Q_Z, or the context running out of moves.
  - **Sufficient local condition (L3_F).** In every line of L_T(Q_Z) in which s̄ plays only winning moves, s has
    at each of its turns before s̄'s win a legal Z-pawn move or a legal king move onto a square of F_Z. By
    Lemma 2.2 nothing off F_Z occupies or attacks a square of F_Z, so that move is legal in every real position
    reached as well.
  - The earlier sufficient condition (L3′) (every square within distance T + 1 of s's king lies on F_Z) can never
    apply for T ≥ 2 on a 3-file group, because the ball of radius T + 1 spans at least 5 files while
    |F_Z| = 3 (revised after review: R1 item 8).
  - For T = 1, (L3) is a single check: s is not stalemated at Q.

## Theorem 2.7 (statement only)

**Theorem 2.7 (sufficiency of the certificate).**
(The first K7 draft of (b) had no e.p. clause in (L2) and was FALSE; see the example in the list "The conditions
cannot be dropped" below.)
- **(a)** If LC_T(m) holds at Y, with reply r, then s̄ has a forced win in P after m: it plays r and then wins
  with one of its next T moves. So m is decisively punished in P.
- **(b) Window form.** The proof does not use how Q arose. Let Q be a position with s to move which is
  chess-legal, or which arises from a position Y of Definition 2.1 by legal moves m and r as in (a), and in which
  every pawn is a Z-pawn on F_Z or a context pawn on a context file, the buffer is empty, there is no officer,
  s̄'s king stands on F_Z, and no s̄ context pawn attacks s's king (automatic if s's king is on F_Z). Q may
  carry an e.p. right with its target anywhere: (L2) counts a right whose target is off F_Z, and π keeps a
  right whose target is on F_Z. If (L1),
  (L2) and (L3) hold at Q, s̄ has a forced win in P from Q. This is the form used in §5.3 and P8, with Q = Y.
  The window form does not cover a legal position in which s is in check from an s̄ context pawn that has just
  moved (s's king on a context or buffer file): there (I4) fails, and the theorem says nothing.


