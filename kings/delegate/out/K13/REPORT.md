# K13: independent re-check of the sharp form of Theorem 1.14

## Summary

- **PROVED:** The sharp simulation lemma is sound for finite D-games, including loopy ones.
- **PROVED:** Its rank is finite on the D-winning region; shortness of the entire graph is not needed.
- **SOUND:** S1, S2 and S3 handle winner moves, every loser reply, checkmate and stalemate as claimed.
- **GAP:** The one-sided chess bridge's printed V1a does not fit D = G ⊞ on_D if Black has legal Z-moves; scope it to modeled moves.
- **PROVED:** Corollary 2.7′ follows by the same transfer; no optional computations were run.

## Independent proof

### The abstract rank

Fix a side σ and write a D-state as a position together with the side to move. Its outgoing edges may lead to another D-state or to a terminal result. Let A₀ be empty. At stage n+1, retain Aₙ and add (i) each σ-to-move state with an edge to a σ-win terminal or to Aₙ, and (ii) each σ̄-to-move state all of whose edges go to a σ-win terminal or to Aₙ. The universal condition in (ii) includes the state with no edges, which loses for its mover under the D-game's normal-play rule.

Definition 1.1 makes the D-state set finite. Therefore these stages stabilize after finitely many additions, even if the D graph has cycles. For a state in the union, let ρ be its first stage. At a σ-state of finite rank there is a winning edge of lower rank (or to a σ terminal); at a σ̄-state of finite rank every ordinary D-edge goes to a lower-rank state and no edge goes to a σ̄-win terminal. An edge leaving the position set for a terminal is not an ordinary D-move. Infinite plays are outside this attractor.

Thus the induction parameter in the sharp form is well-defined. It is not justified by saying that D itself is short: the sharp form explicitly permits a loopy D, including G ⊞ on_D. The separate proof of Theorem 1.14(i) does make D short after V3 turns every Z-move into a terminal and those losing options are deleted.

### Transfer from a certified set

Take y in N and induct on ρ(y), assuming every lower-rank member of N is a P-win for σ. A closing move already gives σ a P-win: it either promotes for σ or leaves a position from which σ can force a finite P-win.

If σ is to move, S1 supplies either such a closing move or a legal non-promoting chess move whose image is an ordinary D-option at a lower-rank member y′ of N. In the latter case the induction hypothesis supplies the winning continuation from y′. The other chess moves available to σ do not matter; σ chooses the certified move.

Now suppose σ̄ is to move. S3 rules out stalemate. If σ̄ has no legal move, S3 therefore says σ̄ is in check: that is checkmate, so σ already wins. Otherwise take any legal reply. By S2, it is closing, or it is an ordinary D-move to some y′ in N. In the second case it is an in-position D-option from a finite-rank σ̄-state. The D attractor rule puts its image at strictly smaller rank. Induction says the resulting P-position is a σ-win. A promotion by σ̄ cannot be a closing move, and it is not a D-move by definition; so S2 rules such a winning reply out.

Every non-closing move in the resulting strategy lowers ρ. Once a closing move occurs, its P-win is finite by definition. Hence no line can continue forever: y is a finite P-win for σ. This proves the sharp form without deleting Z or requiring σ to stay out of Z.

At check nodes, no extra hypothesis is missing. If σ̄ is checked and has replies, S2 covers every legal reply. If checked with no legal reply, it is checkmate and S3 is satisfied. The only no-legal-move case excluded by S3 is an unchecked stalemate. At a σ-to-move node, S1 itself guarantees a legal winning move.

## Step-by-step audit of LOOPY.md

| Proof step | Verdict | Independent check |
|---|---|---|
| Theorem 1.14(i): V3 makes Z-options suicides; Lemma 1.7 deletes them in the normal-play D-game, leaving the short pawn sum | **SOUND** | Deleting a losing option preserves normal-play results, including when it was the only option. The no-move issue in chess is separately excluded by V1b. |
| The D-winner avoids Z-moves | **SOUND** | Such a move is a terminal win for the opponent, so it cannot be a winning choice. This is specific to V3 and is not used in the sharp form. |
| The loser’s chess moves are D-options, and cannot be options to a loser-winning terminal at a D-winning loser node | **SOUND** | V1a supplies the correspondence; the fixed-point rule at a σ̄-node in Wσ supplies the outcome restriction. |
| The original play terminates | **SOUND** | Nonterminal pawn moves lie in the short D-game; V1b rules out a chess no-move ending before a decisive event. V1b is stronger than the sharp form needs. |
| V2 turns the reached decisive event into a P-win for its beneficiary | **SOUND** | This is exactly the needed bridge at the terminal. V4 is not used in (i); it is needed for (ii), the S-to-D comparison. |
| Sharp-form rank induction, σ-to-move/S1 case | **SOUND** | A closing move wins directly; otherwise the certificate itself supplies a lower-rank member of N. |
| Sharp-form rank induction, σ̄-to-move/S2 case | **SOUND** | Every chess reply is covered. For an ordinary D-edge, the attractor rule gives the strict rank drop; a closing reply gives a P-win directly. |
| Sharp-form stalemate and check case, S3 | **SOUND** | S3 excludes exactly stalemate. Checkmate satisfies S3 and is already a σ-win; checked replies are covered by S2. |
| “D is short” as a justification for the sharp-form rank | **FALSE if asserted** | The sharp setting allows loopy D. The conclusion still follows because D is finite and only states in its finite-win attractor receive the natural-number rank. No such false premise is needed by the displayed sharp proof. |

I found no false step in the sharp-form induction. The K3 report's “no full proof written” was a documentation gap at that point; this derivation fills it independently. K9's strategy-transfer intuition agrees, but the attractor-rank argument above is sufficient on its own.

## Uses

### Proposition 3.2 chess bridge

**PROVED conditionally:** The transfer argument works for the intended hypotheses, including White's shuttle. Here D = G ⊞ on_D and π identifies the two White shuttle states with ω. A White shuttle is a legal Z-move and maps to Left's ordinary loop option in on_D. If the rank-lowering D-winning strategy chooses that pass, it is the S1 move. The rank drop follows from the choice of a winning edge in the attractor, not merely from changing the side to move. The old proof of Theorem 1.14(i), which relies on the winner never moving in Z, would not cover it.

For S2, each Black move at a node of N must have one of two treatments: (a) a non-closing context move matches an ordinary D-option, with its successor in N; an event for White is closing by the decisive-event hypothesis; or (b) a Black Z-move is closing because the punishment hypothesis says it is a P-loss for Black. S3 follows from “Black always has a legal move,” which is stronger than merely excluding stalemate. These are exactly the checks needed by the sharp form. White’s unused king moves need not be modeled.

**GAP in the printed bridge wording:** its V1a says every legal chess move of the side to move is a D-option of G ⊞ on_D. Black’s non-shuttle Z-moves are legal moves but are not options of on_D (Right has no on_D move); the separate punishment bullet is meant to handle precisely those moves as closing. As written, V1a either rules out those moves or makes the application unusable when they exist. Repair V1a to require matching only for White’s selected strategy moves and Black’s non-closing moves; require every remaining Black move to be closing. With that scope correction, the chess bridge follows from the sharp form. White shuttle legality/matching is checked by Proposition 3.2 and Lemma 2.2; Black Z punishment and reached G-event decisiveness are the two per-context assumptions; S3 is the legal-move condition.

### Corollary 2.7′

**PROVED:** To make the D-game explicit, take pre-promotion positions as D positions; ordinary legal pawn moves are D-edges, promotions are terminals for their movers, and legal king moves are terminals against their movers. Give no-option positions the D normal-play rule. This D is finite and short because pawn moves progress or remove pawns and all king moves end the D-play. Let N be the positions reached under a finite F-winning strategy S. In F, S never chooses σ’s own king move, since it loses at once. A selected non-promoting pawn move is legal in P and goes to a lower-rank member of N; a σ promotion is closing in P. At a σ̄-node, every ordinary pawn reply is an F reply and must remain in σ’s winning region (a promotion for σ̄ would defeat S). Every legal king reply by σ̄ is closing by the corollary’s assumption that it is a P-loss for σ̄. S cannot reach stalemate, so S3 holds; if a side has no moves in N, it is checkmated, not stalemated, and the D no-option result agrees with the F win. Thus N is σ-certified. The first implication follows. Its “for every winning strategy” consequence is the contrapositive; the final failure of every LC_T certificate is the contrapositive of Theorem 2.7(a).

This is a P-model conclusion only. The chess conclusion additionally needs (A_Q)(X), the per-position implication from a P-win at X to a chess win at X.

### Solver semantics checked

`kpsolve.c`’s header and move generator agree with the corollary’s F: `--frozen` represents each legal king move as an immediate loss for its mover, and each promotion as an immediate win for its promoter. It does not compute the free-king P-model. “Frozen” here means king moves are losing terminals, not that they silently disappear.

`--cap C` limits the number of promoted officers retained in a state. A promotion beyond C is assigned a White win in the first bound and a Black win in the second; when a capped promotion is encountered the solver runs both bounds. Agreement is an exact result for that query under the cap analysis; disagreement is unresolved. In `--frozen`, promotion terminates before an officer is retained, so this cap branch does not affect the F transfer. No solver run or cap-dependent result is claimed here.

## Computations and reproducibility

No small-board computation was needed or run. There are no computed counts or numerical results in this report; the claims above are proof audits from the definitions and the cited source text. I did not build or run the existing K13 `kp` binary.

## Recommended label

**Theorem 1.14, sharp form: PROVED**, for finite D-games as defined in LOOPY.md, including loopy graphs; independently re-derived here. **Proposition 3.2 chess bridge: GAP as literally worded, PROVED after the V1a scope repair above. Corollary 2.7′: PROVED in P**, with the chess form conditional on (A_Q)(X).
