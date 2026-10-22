### EDIT 1: status row T1.14 sharp form
<<<<<<< OLD
| T1.14, sharp form | GAP → GAP (proof incomplete): every legal Z-move of the loser at its turns must be a P-loss (revised after K3 check) | R2 item 6 |
=======
| T1.14, sharp form | PROVED after repair (K9, 2026-10-22): along one D-winning strategy of the D-winner; (V2) at terminals reached, (V3) strong at loser's nodes, (V1a) split, (V1b) at loser's nodes; conclusion is a strategy win in P (revised after K9, 2026-10-22) | R2 item 6 |
>>>>>>> NEW

### EDIT 2: section 0 table row T1.14 sharp-form clause
<<<<<<< OLD
| T1.14 | Validity: (V1)–(V3) give P = D (no draws), (V4) gives o(S) = P, and (A_Q)(X) gives C = P | (i) PROVED; (ii), (iii) PROVED after repair; the sharp form is a GAP. The C part is the per-position hypothesis (A_Q)(X) |
=======
| T1.14 | Validity: (V1)–(V3) give P = D (no draws), (V4) gives o(S) = P, and (A_Q)(X) gives C = P | (i) PROVED; (ii), (iii) PROVED after repair; the sharp form is PROVED after repair (K9, 2026-10-22). The C part is the per-position hypothesis (A_Q)(X) |
>>>>>>> NEW

### EDIT 3: Sharp form paragraph
<<<<<<< OLD
**Sharp form (GAP (proof incomplete): R2 item 6).** (revised after K3 check)
- (V2) is needed only for the terminals reached under *one* D-winning strategy of the D-winner.
- (V3) is needed in the stronger form: at every loser-to-move node of that strategy, **every** legal Z-move of
  the loser is a P-loss for the loser. The earlier wording ("needed only for terminals") was false as stated: a
  loser's Z-move that is not punished is not a terminal, and then the Lemma 1.7 reduction and the shortness of
  D both fail.
- (V1a) splits into two halves:
  - the winner's prescribed D-moves must be legal chess moves;
  - every legal chess move of the loser must be a D-option.

  The winner may have extra legal moves (Lemma 1.6).
- The conclusion of the sharp form is the result of the strategy itself, not a normal-play result: the D-winner
  σ wins P(X) by that strategy. The claim "the result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z deleted)"
  belongs to (i), not to the sharp form.
=======
**Sharp form (PROVED after repair (K9, 2026-10-22)).** (revised after K3 check; (revised after K9, 2026-10-22))
- Let σ be the D-winner of D(X) with a D-winning strategy Σ. Assume that along every play consistent with Σ:
  - (V2') every terminal reached is a P-win for σ;
  - (V3') at every loser-to-move node of Σ, every legal Z-move of σ̄ is a P-loss for σ̄;
  - (V1a'-i) every move prescribed by Σ is a legal chess move;
  - (V1a'-ii) at every loser-to-move node of Σ, every legal chess move of σ̄ is a D-option of D(X);
  - (V1b') at every loser-to-move node of Σ that is not a terminal, σ̄ has a legal chess move.
- Then σ wins P(X) by following Σ. The conclusion is a strategy win, not a normal-play result: the claim "the
  result is the normal-play result of G₁ ⊞ … ⊞ G_k (Z deleted)" belongs to (i), not to the sharp form.
- (V3') must hold for *all* legal Z-moves at the node, not just those played: an unpunished loser Z-move is
  not a terminal in the P-relevant sense, the D-to-P mapping collapses, and σ̄ could loop in Z, defeating the
  finite-time win. Lemma 1.7 (suicide deletion) is therefore not used; Z is not deleted and the conclusion is
  not the normal-play result. Lemma 1.6 is used to ignore σ's extra legal chess moves. (revised after K9,
  2026-10-22)
>>>>>>> NEW