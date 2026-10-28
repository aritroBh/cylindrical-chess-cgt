### EDIT one-sided chess bridge: terminal moves, e.p. flag, no stalemate (K13b)
<<<<<<< OLD
Suppose r(G ⊞ on_D) = W. Let Σ be a rank-lowering White strategy in G ⊞ on_D, with its passes played as the
shuttle, and let N be the set of chess positions that arise when White plays Σ as chess moves and Black plays any
legal D-move (π sends both shuttle states to ω). Assume, at the nodes of N:
- (V1a) with White to move, the move Σ prescribes is legal and leads to the matching position (the shuttle is legal
  by Lemma 2.2); with Black to move, every legal Black context move is an option of G and leads to the matching
  position (e.p. obeying condition (E));
- every Black Z-move is decisively punished in P;
- every decisive event of G that is reached is a P-win for its beneficiary;
- Black always has a legal move.

Then White wins in P. *Proof:* N is White-certified for the sharp form of Theorem 1.14.
- (S1): White's move is the one Σ prescribes, legal by (V1a). It lowers ρ, a pass included, because Σ chooses an
  option of smaller rank. A ⊕ that Σ prescribes is closing by the third bullet.
- (S2): a Black context move is a D-move to a node of N, or a decisive event for White, which is closing by the
  third bullet. A Black promotion would be a ⊖ option of a Black node of W_White, and there is none. Black has no
  move in on_D, so a Black Z-move is not a D-option; it is closing by the second bullet.
- (S3) is the last bullet.

The sharp form gives a P-win. The mirror statement holds for Black wins. (Revised after K13, 2026-10-27. Before,
(V1a) read "every legal chess move of the side to move is one of the D-options". That excluded the Black Z-moves
that the second bullet is about, and it asked for White moves that Σ never plays. The proof cited the proof of
Theorem 1.14(i), which the header above had already replaced.)
=======
Here G is the pawn-only D-model of the context, with the e.p. flag as a coordinate. The pass of on_D resets the flag,
as White's shuttle does in chess (a king move ends an e.p. right; Remark on e.p. after Proposition 3.2′). Suppose
r(G ⊞ on_D) = W. Let Σ be a rank-lowering White strategy in G ⊞ on_D, with its passes played as the shuttle, and let
N be the set of chess positions before the first promotion that arise when White plays Σ as chess moves and Black
plays any legal D-move, up to the first closing move (π sends both shuttle states to ω). Assume, at the nodes of N:
- (V1a) with White to move, the move Σ prescribes is legal; if Σ prescribes a position of G ⊞ on_D (not a ⊕), the
  move does not promote and leads to the matching position (the shuttle is legal by Lemma 2.2). With Black to move,
  every legal Black context move is an option of G, and if that option is a position, the move leads to the matching
  position. The context moves of both sides obey condition (E) for e.p.;
- every Black Z-move is decisively punished in P;
- every decisive event of G that is reached is a P-win for its beneficiary;
- Black is not stalemated.

Then White wins in P. *Proof:* N is White-certified for the sharp form of Theorem 1.14.
- (S1): if Σ prescribes a ⊕, White's move is a decisive event of G and is closing by the third bullet. Otherwise
  it is a D-move by (V1a), and it lowers ρ, a pass included, because Σ chooses an option of smaller rank.
- (S2): before the first promotion every Black move is a context move or a Z-move (Definition 2.1, Lemma 2.2). A
  Black context move is a D-move to a node of N, or an option of G to a terminal. A ⊕ is closing by the third
  bullet. A ⊖ (a Black promotion, for instance) would be a ⊖ option of a Black node of W_White, and there is none.
  Black has no move in on_D, so a Black Z-move is not a D-option; it is closing by the second bullet.
- (S3) is the last bullet. Checkmate of Black is a P-win, so only stalemate has to be excluded.

The sharp form gives a P-win. The mirror statement holds for Black wins. (Revised after K13, 2026-10-27. Before,
(V1a) read "every legal chess move of the side to move is one of the D-options". That excluded the Black Z-moves
that the second bullet is about, and it asked for White moves that Σ never plays. The proof cited the proof of
Theorem 1.14(i), which the header above had already replaced. The post-commit check K13b (Codex) then made three
points exact: moves that Σ makes to a ⊕ have no matching position; the shuttle ends an e.p. right, so the pass must
reset the flag; and the last bullet read "Black always has a legal move", which also excluded checkmate, a White win.
`kings/delegate/out/K13/CHECK_774036f.md`.)
>>>>>>> NEW

### EDIT stale citation after the sharp form
<<<<<<< OLD
3.2 is the instance D = G ⊞ on_D; its proof cites the proof of (i), whose "σ never moves in Z" step does not cover
White's shuttle, so the sharp form is the right citation for it.
=======
3.2 is the instance D = G ⊞ on_D. Its earlier proof cited the proof of (i), whose "σ never moves in Z" step does not
cover White's shuttle; since K13 its proof uses the sharp form (revised after K13, 2026-10-27).
>>>>>>> NEW

### EDIT status row P3.2 (K13b)
<<<<<<< OLD
After K13 the bridge's (V1a) covers only White's strategy moves and Black's context moves, and its proof cites the sharp form of Theorem 1.14 (revised after K13, 2026-10-27) | R4 item 7; K13 |
=======
After K13 the bridge's (V1a) covers only White's strategy moves and Black's context moves, and its proof cites the sharp form of Theorem 1.14; after the K13b check its terminal moves, the e.p. flag under the shuttle and the no-stalemate condition are exact (revised after K13, 2026-10-27) | R4 item 7; K13 |
>>>>>>> NEW
