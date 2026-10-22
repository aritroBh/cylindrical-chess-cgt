# K9: a complete proof of the sharp form of Theorem 1.14

## 5-line summary

- The sharp form is proved: a D-winning strategy for the D-winner σ transfers to a P-winning strategy provided
  (V2) holds at the terminals the strategy reaches, (V3) holds in the strong form at every loser-to-move node
  (all of σ̄'s legal Z-moves are P-losses), and (V1a) splits into legality of σ's moves and D-option status of
  σ̄'s moves.
- (V1b) (no stalemate) is needed only at the loser-to-move nodes of the strategy, not globally.
- Lemma 1.6 is used to ignore σ's extra legal chess moves; Lemma 1.7 is not used, because Z is not deleted and
  the conclusion is a strategy win, not a normal-play result.
- Sharpness: §5.3 breaks (V3), §5.4 breaks (V1b), P4 breaks (V2) (context passers); (V1a) has no isolated
  counterexample in the note and remains conjectural.
- Label proposed: PROVED after repair; the corresponding LOOPY.md rows are updated (3 edits applied, 0 rejected).

## 1. Statement

**Theorem 1.14 (sharp form).** Let X be a K+P position with pawn components G_1,...,G_k and king group Z.
Let σ be a side that is the D-winner of D(X), i.e. σ has a D-winning strategy in D(X). Assume there is a
D-winning strategy Σ for σ in D(X) (finite-time win) such that, along every play consistent with Σ, the
following hold:

1. **(V2') Decisiveness along the strategy.** Every terminal reached by Σ is a P-win for σ.
2. **(V3') Strong freeze along the strategy.** At every loser-to-move node of Σ, every legal Z-move of σ̄ is a
   P-loss for σ̄.
3. **(V1a'-i) Legality of the winner's moves.** Every move prescribed by Σ is a legal chess move.
4. **(V1a'-ii) Loser's chess moves are D-options.** At every loser-to-move node of Σ, every legal chess move
   of σ̄ is a D-option of D(X) (possibly a terminal).
5. **(V1b') No stalemate at loser's nodes.** At every loser-to-move node of Σ that is not a terminal, σ̄ has at
   least one legal chess move.

Then σ wins P(X) by following Σ (playing the prescribed chess moves).

**What counts.**
- A *D-winning strategy with finite-time win* in a (possibly loopy) finite D-game is a choice of σ-move at
  every position reachable under it such that every consistent play reaches a σ-terminal (⊕ if σ = White,
  ⊖ if σ = Black) in finitely many moves; no infinite play occurs under it.
- *Nodes that count:* the positions occurring in plays consistent with Σ, split by side to move. The terminals
  reached by Σ (for (V2')) and the loser-to-move nodes of Σ (for (V3'), (V1a'-ii), (V1b')).

**How (V1b) enters.** (V1b') is needed only at the loser-to-move nodes of Σ that are not terminals. At σ's
nodes, Σ's prescribed move itself is a legal move, so no separate no-stalemate condition is required there.
This is the restriction of the global (V1b) to the strategy's loser nodes.

## 2. Proof

**Step 1 — Shadowing plays.** We build a P-play under Σ against any chess play of σ̄, shadowed by a D-play
under Σ. Initially both are at X. At a σ-turn, σ plays the move prescribed by Σ; it is a legal chess move by
(V1a'-i), so it is admissible in P, and it is the same D-move, so the D-play follows Σ. At a σ̄-turn, σ̄'s
chess move is a D-option by (V1a'-ii), so the D-play can follow it; the position in P after the move is some
chess position, and the shadow D-position is the corresponding D-option result. Thus every P-move of σ̄ is
admissible in D, and σ's reply is admissible in P.

**Step 2 — Finite time in D.** Σ wins D(X) in finite time, so the shadow D-play reaches a σ-terminal after
finitely many moves, whatever D-options σ̄ uses. The P-moves are a subset of those options, so the actual P-play
also reaches, in at most the same number of moves, a position that is a D-terminal under Σ.

**Step 3 — Terminals are P-wins.** The reached terminal is one of those covered by (V2'), hence the
corresponding P-position is a P-win for σ. If the P-game has not already ended (a D-terminal may be a passer or
a punished Z-move, which P does not treat as an immediate end), append the finite P-winning strategy whose
existence is (V2'). The total number of moves is finite.

**Step 4 — No infinite Z-loop under Σ.** Under Σ, σ never plays a Z-move: such a move would be a decisive
event for σ̄ (a suicide), contradicting that Σ wins. σ̄'s Z-moves are P-losses by (V3'), hence terminal
σ-wins in D, so they end the D-play rather than looping. Thus the finite-time win survives the loopy king
group Z.

**Step 5 — Stalemate.** If at a loser-to-move node σ̄ had no legal move, (V1b') (for non-terminals) rules it
out; a terminal node is already handled by (V2'). So no draw by stalemate occurs, and D's normal-play "no move
loses" maps to a P-loss.

**Step 6 — Extra moves are irrelevant.** σ may have legal chess moves that are not D-options. By Lemma 1.6,
adding options for a player never lowers that player's result, so ignoring them keeps the win. Conversely,
D may grant σ̄ options not available in chess; Σ wins against the larger set, hence against the subset that is
actually available in P.

**Conclusion.** σ wins P(X) by following Σ. ∎

**Where Lemma 1.6 is used.** Step 6: σ's extra legal chess moves (beyond his D-options) cannot hurt him, so the
D-strategy, which uses only D-moves, remains a winning P-strategy.

**Where Lemma 1.7 is not needed, and why the earlier "needed only for terminals" wording was false.** The
original (i) used Lemma 1.7 to delete Z's suicides and identify D with the component sum G_1 ⊞ ... ⊞ G_k.
The sharp form never deletes Z and does not identify D with a sum; (V3') is used directly as the statement that
the loser's Z-moves are P-losses, and the conclusion is a strategy win rather than a normal-play result. Hence
suicide deletion is unnecessary. The earlier wording "needed only for terminals" was false because an
unpunished loser Z-move is not a terminal in the P-relevant sense: D would still score it as a terminal
(suicide) but P would continue with σ̄ holding a non-losing move. The D-play would then fail to map to a
P-win, and σ̄ could repeat Z-moves to create an infinite play, defeating the finite-time win. That is why (V3')
must cover *all* legal Z-moves at the node, not only those that are played.

## 3. Sharpness

Weakening any one hypothesis breaks the statement; the examples below are from the note.

| Hypothesis | Weakening | Counterexample | Status |
|---|---|---|---|
| (V2') decisiveness | require decisiveness only for Z-terminals, ignoring context decisive events | P4: Z_T + {H*, H*2, H0}; kpsolve gives draws/losses instead of the predicted wins because a context passer is not a P-win | COMPUTED-1 (`kings/results/PREDICTIONS.md`, `theory_P4_cap2_moves.txt`) |
| (V3') strong freeze | allow an unpunished loser Z-move | §5.3 (7.3): Black's Z-move f7-f8=Q is not a P-loss (it wins); the loser escapes | PROVED in P (§5.3) |
| (V1b') no stalemate | drop no-stalemate at loser's nodes | §5.4 stalemate trap: `Ka5 Pb4 Pc5 Pe2 Pe4 / kc6 pb5 pe5` is (D,D) while the convention reads (W,W) | PROVED / COMPUTED-1 (`kings/kpsolve --frozen`) |
| (V1a') split | drop the requirement that all loser chess moves be D-options | no isolated counterexample in the note; the need for (V1a) remains a CONJECTURE (R1 item 4, R2 item 7) | CONJECTURE |

## 4. Relation to Theorem 2.4

Theorem 2.4 is the same transfer principle with Z as the only component and G a short normal-play game: clause
(a) requires every Z-move in every state and context to be punished; clause (b) sharpens this to the positions
reached under a winning strategy of the G-winner at which the loser moves, which is exactly the restriction
made by the sharp form; clause (c) handles games that may draw. Theorem 1.14 sharp form is the
multi-component, decisive-event version: the context is a sum of pawn components with game-ending passers, the
terminals are decisive events rather than ordinary CGT terminals, and the conclusion is a strategy win in P
rather than equality of results. Thus Theorem 2.4(b) is the special case in which the components are absent and
G is short, and the sharp form is its lift to the decisive-event model.

## Proposed label

PROVED after repair. The proof above is complete; the remaining work items (CGSuite modelling, opposition,
Gafni re-examination) are unrelated open questions of §8.6 and do not affect this theorem.

## Reproduce

- Abstract/regime and solver checks: see `kings/delegate/out/K3/REPORT.md` reproduce commands.
- Edit application check:
  `python3 kings/delegate/apply_edits.py kings/theory/LOOPY.md kings/delegate/out/K9/LOOPY_preview.md kings/delegate/out/K9/EDITS.md`
  (result: 3 applied, 0 rejected).
- The proof itself uses only definitions and lemmas already in `kings/theory/LOOPY.md` (Definitions 1.1-1.5,
  Lemma 1.6, Theorem 1.14(i)-(iii)); no computation is required.