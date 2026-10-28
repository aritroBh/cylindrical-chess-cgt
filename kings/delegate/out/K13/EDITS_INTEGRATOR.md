### EDIT preamble caveat for the K9 repair
<<<<<<< OLD
(an induction on the rank of the D-win), and the integrator read the rewrite. It has not been re-checked by
another reviewer (revised after K9, 2026-10-22).
=======
(an induction on the rank of the D-win), and the integrator read the rewrite (revised after K9, 2026-10-22). K13
(Codex, outside the Claude family) then re-derived it in its own words, by an induction on the stage at which a
D-state enters σ's winning region, and marked every step of the proof SOUND. It found one wording gap, in the
hypotheses of the one-sided chess bridge after Proposition 3.2, which is repaired there (`kings/delegate/out/K13/REPORT.md`;
revised after K13, 2026-10-27).
>>>>>>> NEW

### EDIT status row T1.14 sharp form
<<<<<<< OLD
The winner may move in Z. Not yet independently re-checked (revised after K9, 2026-10-22) | R2 item 6; K3, K9 |
=======
The winner may move in Z (revised after K9, 2026-10-22). Re-derived independently by K13 (Codex, outside the Claude family): no false step. ρ is the stage of a least fixed point on the finite game D, so the induction does not need D to be short (revised after K13, 2026-10-27) | R2 item 6; K3, K9, K13 |
>>>>>>> NEW

### EDIT status row C2.7′
<<<<<<< OLD
then σ wins P. The chess form adds (A_Q) | K7 |
=======
then σ wins P. The chess form adds (A_Q). K13 (Codex) re-derived it independently as an instance of the sharp form of Theorem 1.14 (revised after K13, 2026-10-27) | K7, K13 |
>>>>>>> NEW

### EDIT status row P3.2
<<<<<<< OLD
| P3.2 | PROVED; chess bridge PROVED after repair (adds (V1a)) | R4 item 7 |
=======
| P3.2 | PROVED; chess bridge PROVED after repair (adds (V1a)). After K13 the bridge's (V1a) covers only White's strategy moves and Black's context moves, and its proof cites the sharp form of Theorem 1.14 (revised after K13, 2026-10-27) | R4 item 7; K13 |
>>>>>>> NEW

### EDIT status row T1.14 (second table)
<<<<<<< OLD
the sharp form is PROVED after repair (simulation form on a certified set; revised after K9, 2026-10-22).
=======
the sharp form is PROVED after repair (simulation form on a certified set; revised after K9, 2026-10-22; re-derived independently by K13, 2026-10-27).
>>>>>>> NEW

### EDIT sharp form label paragraph
<<<<<<< OLD
*Label.* PROVED after repair: the proof above is complete for the abstract statement. It has not yet been
independently re-checked, because K3 saw only the earlier draft.
=======
*Label.* PROVED after repair: the proof above is complete for the abstract statement. K3 saw only the earlier
draft. K13 (Codex, outside the Claude family) re-derived the statement independently and marked every step of the
proof above SOUND (revised after K13, 2026-10-27; `kings/delegate/out/K13/REPORT.md`).
>>>>>>> NEW

### EDIT one-sided chess bridge: hypotheses scoped, proof by the sharp form
<<<<<<< OLD
Suppose r(G ⊞ on_D) = W, White plays that strategy (shuttling for its passes), and along it:
- (V1a) every legal chess move of the side to move is one of the D-options of the D-model, and leads to the
  matching position;
- every Black Z-move is decisively punished in P;
- every decisive event of G that is reached is a P-win for its beneficiary;
- Black always has a legal move.

Then White wins in P. *Proof:* the proof of Theorem 1.14(i), with (V1a) among the hypotheses — (V1a) makes
the D-play a chess play, the shuttling strategy supplies White's passes, and the last two bullets make every
deviation decisive for Black. The mirror statement holds for Black wins.
=======
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
>>>>>>> NEW
