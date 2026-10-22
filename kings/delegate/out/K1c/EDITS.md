### EDIT 1: R4 item 7
<<<<<<< OLD
**Chess bridge** (PROVED, by the proof of Theorem 1.14). Suppose r(G ⊞ on_D) = W, White plays that strategy
(shuttling for its passes), and along it:
- every Black Z-move is decisively punished in P;
- every decisive event of G that is reached is a P-win for its beneficiary;
- Black always has a legal move.

Then White wins in P. The mirror statement holds for Black wins.
=======
**Chess bridge** (PROVED after repair, by the proof of Theorem 1.14 with (V1a) added).
Suppose r(G ⊞ on_D) = W, White plays that strategy (shuttling for its passes), and along it:
- (V1a) every legal chess move of the side to move is one of the D-options of the D-model, and leads to the
  matching position;
- every Black Z-move is decisively punished in P;
- every decisive event of G that is reached is a P-win for its beneficiary;
- Black always has a legal move.

Then White wins in P. *Proof:* the proof of Theorem 1.14(i), with (V1a) among the hypotheses — (V1a) makes
the D-play a chess play, the shuttling strategy supplies White's passes, and the last two bullets make every
deviation decisive for Black. The mirror statement holds for Black wins.
(Revised after review: R4 item 7: the bridge needs (V1a). It fails in P2 + H\* if White plays e3–e4, which
stalemates Black, so the bridge may only be used along a strategy that avoids that move; kpsolve gives (W, W)
for P2 + H\*.)
>>>>>>> NEW

### EDIT 2: R4 item 6
<<<<<<< OLD
**What loopy kings do to the convention (PROVED by Theorem 3.4).**
- **With a White shuttle:** the components' values (numbers, infinitesimals, nimbers) are irrelevant except
  for Black's forcing threats. White cannot be zugzwanged, and Black loses as soon as its context tempo runs
  out.
- **With shuttles on both sides:** all tempo content disappears. Positions without threats are draws, even
  where the convention predicts a clear winner. The 7.3 group would be of this type if its pawn could not
  promote (§5.3).
=======
**What loopy kings do to the convention.**
- **With a White shuttle (PROVED by Theorem 3.4(b)):** the components' values (numbers, infinitesimals, nimbers)
  are irrelevant except for Black's forcing threats. White cannot be zugzwanged, and Black loses as soon as its
  context tempo runs out.
- **With shuttles on both sides (CONJECTURE):** all tempo content should disappear. Positions without threats
  should be draws, even where the convention predicts a clear winner. The 7.3 group would be of this type if
  its pawn could not promote (§5.3). *To settle:* a two-sided Proposition 3.2 — a bisimulation on the four
  combined king states, in each of which each side's shuttle is legal and each side is frozen — followed by
  Theorem 3.4(a). (Revised after review: R4 item 6: Theorem 3.4 is stated for one reservoir, so this bullet
  was not proved by it.)
>>>>>>> NEW

### EDIT 3: R4 item 3
<<<<<<< OLD
**Theorem 4.2 (finite versus loopy tempo). PROVED.**
- **(a)** For a short G, G ⊞ R_n^W behaves as "White has n one-shot passes". Its BIG translation G^B + n
  gives the right outcome when G ⊞ R_n^W is first-event dominant. A sufficient condition is pairwise safety
  in G together with B > n + max(M_L(G), M_R(G)).
  *Proof:* Theorem 1.11, with R_n counted as a component without threats; its n Left moves enter M_L.
=======
**Theorem 4.2 (finite versus loopy tempo). PROVED after repair** (each part is proved
below).
- **(a)** Let G be short, and let R_n^W have no Black options (Black's suicides are deleted first; see (b)).
  Then G ⊞ R_n^W behaves as "White has n one-shot passes", and its BIG translation G^B + n gives the right
  outcome when G ⊞ R_n^W is first-event dominant. A sufficient condition is pairwise safety in G ⊞ R_n^W
  together with B > n + max(M_L(G), M_R(G)), with the threats counted by the corrected τ of Definition 1.10
  (revised: τ counts moves into ⊕ or ⊖ by *either* player).
  *Proof:* Theorem 1.11(a) and (b), with the corrected τ. R_n has no Black options, so it carries no threat at
  all, τ(R_n) = ∅, and pairwise safety in G ⊞ R_n^W follows from pairwise safety in G. Its n Left moves
  enter M_L, so max(M_L(G ⊞ R_n^W), M_R(G ⊞ R_n^W)) ≤ max(M_L(G), M_R(G)) + n < B, which is the bound (b)
  needs, and Theorem 1.11(b) then gives first-event dominance. (Revised after review: R4 item 3: Definition
  4.1 allowed Black suicides inside R_n, and then the stated hypothesis does *not* give first-event
  dominance — take a context whose only option is Black's move to ⊖, whose translation is −B−1, with n = 1 and
  a Black suicide at ρ₁: the frontier is B + (−B−1) = −1 ∈ 𝓡, so dominance fails for every B. The corrected
  τ counts that suicide, so the hypothesis correctly fails there; with no Black options the proof above is
  complete.)
>>>>>>> NEW

### EDIT 4: R4 item 4
<<<<<<< OLD
- **(b)** If White's safe Z-moves form an acyclic graph and all Black Z-moves are suicides, then Z, with
  Black's suicides deleted (Lemma 1.7), equals the integer ℓ: the length of the longest path of safe White
  moves.
  *Proof:* induction, using {m₁, …, m_k | } = max m_i + 1. Dominated options can be deleted (KNOWN, [WW]
  ch. 2, [S] ch. II).
=======
- **(b)** If White's safe Z-moves form an acyclic graph and all Black Z-moves are suicides, then
  Z, with Black's suicides deleted, is equivalent in the D-model to R_ℓ^W, where ℓ is the length of the
  longest path of safe White moves; and in CGT, for B > ℓ, its BIG translation is the integer ℓ.
  *Proof:* induction on the number of White options, using {m₁, …, m_k | } = max m_i + 1: the value of a
  White-only option set is 1 plus the maximum of the values of its options, and dominated options can be
  deleted (KNOWN, [WW] ch. 2, [S] ch. II). In the D-model the deletion of Black's suicides is Lemma 1.7, a
  statement about results; the CGT statement needs the extra hypothesis B > ℓ, because {i−1 | B} = i holds
  only for B > i. (Revised after review: R4 item 4: Lemma 1.7 alone does not give the CGT equality, and the
  D-model equivalence to R_ℓ was not proved; both are now proved, and the CGT form carries B > ℓ.)
>>>>>>> NEW

### EDIT 5: R4 item 5
<<<<<<< OLD
- **(c)** A reservoir with a White 2-cycle is on_D and equals no integer. *Proof:* take G = R_{n+1}^B, n + 1
  Black tempi with no threats.
  - G ⊞ R_n^W with White to move is L: the tempi run out on White first.
  - G ⊞ on_D with White to move is W: Black runs out.

So a group's tempo is *finite* (a stopper equal to an integer) exactly when its spare moves are
non-reversible, and *unbounded* (on or off) when they contain a cycle.
=======
- **(c)** A reservoir with a White 2-cycle is on_D and equals no integer. *Proof:* take G = R_{n+1}^B, n + 1
  Black tempi with no threats.
  - G ⊞ R_n^W with White to move is L: the tempi run out on White first.
  - G ⊞ on_D with White to move is W: Black runs out.
  - on_D is not a number at all, so it differs from every integer, negative ones included.
  - The identification needs the hypotheses of Proposition 3.2 — the cycle must be reachable, and in each of
    its two states every Black Z-move must be a suicide — not merely the existence of a cycle.
  (Revised after review: R4 item 5: separating on_D from the integers has to cover the negative integers as
  well, and "is on_D" needs Proposition 3.2's hypotheses.)

So a group's tempo is *finite* (a stopper equal to an integer) exactly when its safe spare moves form an
**acyclic** graph, and *unbounded* (on or off) when they contain a cycle. The word is "acyclic", not
"non-reversible": a 3-cycle has no immediately reversible move and is still unbounded.
(Revised after review: R4 item 5: the old sentence conflated acyclicity with the absence of a 2-cycle.)
>>>>>>> NEW

### EDIT 6: R4 items 1 and 2
<<<<<<< OLD
**Proposition 4.3 (no finite king tempo in isolated K+P groups). PROVED.** Let Z be a king group in a
position without officers, with a buffer. Suppose side s plays a non-capturing king move u → v inside F_Z,
and the opponent replies outside Z. Then v → u is legal at s's next turn and restores Z exactly.

=======
**Proposition 4.3 (no finite king tempo in isolated K+P groups). FALSE as originally stated →
repaired.** Let Z be a king group in a position without officers, with a buffer. Suppose side s plays a
non-capturing king move u → v inside F_Z, and the opponent replies outside Z. **As stated this is false:** the
step back fails if s was in check on u, or if the reply promotes. The repaired statement adds two hypotheses:
- (H1) s is not in check on u;
- (H2) the reply is not a promotion, and does not attack u.

Then v → u is legal at s's next turn and restores Z exactly.
>>>>>>> NEW

### EDIT 7: R4 item 2, R1 item 11
<<<<<<< OLD
Consequently, if the opponent is frozen (all its Z-moves are suicides), any one safe king step of s gives s
an unlimited supply of passes. A king group's king tempo is therefore 0 (frozen) or ∞ (shuttle), never a
finite n ≥ 1.
=======
**Consequences, with the scope narrowed (revised after review: R4 item 2, R1 item 11).** Call a king step
u → v inside F_Z *safe* if (H1) and (H2) hold and the opponent is frozen — all its Z-moves are suicides — at
both u and v. Then one safe step gives s an unlimited supply of passes: s returns to u on its next turn, the
Z-state is exactly as before, and the step can be repeated. So, among king steps *inside* F_Z, the tempo of a
pure reservoir is 0 (the opponent is frozen and s has no safe step) or ∞ (s has a safe step); it is never a
finite n ≥ 1. Three caveats, which the original wording hid:
- the dichotomy covers king steps inside F_Z only. A step onto a buffer file can be taken away later by a
  context pawn (Lemma 2.2 lets context pawns attack buffer squares), so such a supply depends on the context
  and is neither 0 nor ∞;
- a king move can be neither a suicide nor a pass: it can unfreeze the opponent without losing (§5.5 shows
  this), so the dichotomy is about pure reservoirs only;
- "safe" is not "any legal step": the opponent must be frozen at the new state v as well as at u.
>>>>>>> NEW

### EDIT 8: R4 items 1 and 2
<<<<<<< OLD
*Proof.*
- u is empty, since s's king just left it and the opponent did not move in Z.
- u is not adjacent to the opponent's king: that king has not moved since s's king stood on u legally.
- u is not attacked by an opponent Z-pawn, since none has moved. It is not attacked by a context pawn
  either: context pawns attack only context and buffer squares (Lemma 2.2), and u ∈ F_Z.
- With no sliders, the move exposes nothing. ∎
=======
*Proof.*
- u is empty, since s's king just left it and the opponent did not move in Z.
- u is not adjacent to the opponent's king: by (H1) the opponent's king was not adjacent to u when s's king
  stood there (kings may never be adjacent), and by (H2) the reply did not move it next to u.
- u is not attacked by an opponent Z-pawn, since none has moved (by (H2) the reply is not a promotion), and by
  (H1) none attacked u before. It is not attacked by a context pawn either: context pawns attack only context
  and buffer squares (Lemma 2.2), and u ∈ F_Z.
- With no sliders, the move exposes nothing. ∎

*Counterexample to the original statement (revised after review: R4 item 1).* `Kb2 Pc2 kc4 pc3`, White to
move, on flat:4x4: White is in check from pc3 and plays Kb2–a1; when Black then moves outside Z, Kb2 is
illegal, because pc3 still attacks it. The position is hand-checkable; kpsolve confirms the move lists:
only Ka1a2 and Ka1b1 are legal for `Ka1 Pc2 kc4 pc3 w -`. The step back fails because u was attacked, not
because the opponent moved.
  - Reproduce: `printf 'Kb2 Pc2 kc4 pc3 w -\nKa1 Pc2 kc4 pc3 w -\n'
    | kings/kpsolve --board flat:4x4 --ep on --promote QRBN --cap 1 --moves`.
>>>>>>> NEW

### EDIT 9: R4 item 2, R1 item 11
<<<<<<< OLD
**What this means for the "n safe spare moves" picture.** In king-and-pawn chess, a king with exactly n safe
spare moves cannot occur in an isolated group: one safe step and the step back already give infinitely
many.
=======
**What this means for the "n safe spare moves" picture.** In king-and-pawn chess, a king with exactly n safe
spare moves cannot occur in an isolated group *for steps inside F_Z*: one safe step and the step back already
give infinitely many (Proposition 4.3, repaired). Steps out of F_Z are the exception, and their supply depends
on the context. (Revised after review: R4 item 2, R1 item 11: the original sentence claimed more than
Proposition 4.3 proves.)
>>>>>>> NEW

### EDIT 10: R1 item 11
<<<<<<< OLD
**Over.** over = {0 | over} (KNOWN, [WW] ch. 11, [S] ch. VI). Right can pass forever (over → over), and Left
has one move, to 0, that ends Right's passing.
=======
**Definition 4.4 (over).** over = {0 | over} (KNOWN, [WW] ch. 11, [S] ch. VI). Right can pass forever
(over → over), and Left has one move, to 0, that ends Right's passing. (Revised after review: R1 item 11: the
note had no item 4.4, so the numbering jumped from 4.3 to 4.5; this paragraph is now Definition 4.4.)
>>>>>>> NEW

### EDIT 11: R4 item 8
<<<<<<< OLD
**Chess reading of over.**
- Black has a safe king shuttle (endless passes), and White has exactly one move, typically a pawn move by
  Proposition 4.3, that takes away a shuttle square and leaves a mutual zugzwang.
=======
**Chess reading of over.**
- Black has a safe king shuttle (endless passes), and White has exactly one move that takes away a shuttle
  square and leaves a mutual zugzwang. That move is typically a pawn move, but not by Proposition 4.3:
  Proposition 4.3 assumes a frozen opponent that replies outside Z, and in an over-group the opponent
  shuttles inside Z. (Revised after review: R4 item 8.)
>>>>>>> NEW

### EDIT 12: R1 item 10, R4 item 8
<<<<<<< OLD
- **CONJECTURE 4.7:** no over-type group with ≤ 3 + 2 pawns fits on 3 files of the 8×6 cylinder, but over is
  realisable on the cylinder with wider groups. *Scratch evidence:* the first half; a geometric search found
  none. *To settle:* a wider search, then kpsolve.
=======
- **CONJECTURE 4.7:** no over-type group with ≤ 2 + 2 pawns fits on 3 files of the 8×6 cylinder, but over
  is realisable on the cylinder with wider groups. *Scratch evidence:* the first half; a geometric search over
  placements of ≤ 2 + 2 pawns on 3 (or 4) files found none (Appendix A). *To settle:* a wider search, then
  kpsolve. (Revised after review: R1 item 10, R4 item 8: the search described in Appendix A covered ≤ 2 + 2
  pawns, not the ≤ 3 + 2 claimed here; the conjecture is restated for what was actually searched.)
>>>>>>> NEW

### EDIT 13: R1 item 11, R4 item 9
<<<<<<< OLD
- **Frozen in the convention. PROVED** (diagram audit). Each king has five moves, and each drops its pawn.
=======
- **Frozen in the convention. PROVED by enumeration** (revised after review: R1 item 11, R4 item 9: the
  proof is written out here, instead of being left to the diagram audit). The group is WK h5, WP a4, BK b4,
  BP a5 on the 8-file cylinder. WK's five legal moves are Kg4, Kg5, Kg6, Kh6 and Ka6; each of them abandons
  WP a4, which Black's king then captures on a4, giving Black a passer. BK's five legal moves are Ka3, Kc3,
  Kc4, Kc5 and Kb5; the first four abandon BP a5, which White's king then captures on a5, giving White a
  passer, and the fifth (Kb5) puts Black's king on the square that guards both a4 and a5, so that White is in
  zugzwang with only pawn-blocked moves left. So every king move in the group is decisively punished, and the
  group is frozen. The enumeration agrees with `notes/diagram_audit.md` §C.3.
>>>>>>> NEW

### EDIT 14: R4 item 9, R1 item 11
<<<<<<< OLD
- **White's sorties are not punished.**
  - Ke5 already stands on the e-pawn's path. Kd5 and Kf5 reach e5 next move: after ...Kxd7, e5 is not
    adjacent to d7 and not attacked by e7.
  - By Lemma 2.9, (L1) fails for these three sorties. PROVED.
  - Scratch evidence: even without passes, Black cannot force promotion after Kd5, Ke5 or Kf5. Only Kf7
    loses, in 10 moves.
=======
- **White's sorties: the certificate fails. PROVED by Lemma 2.9.** (The heading "White's sorties are not
  punished" stated as fact what is proved only as the failure of the certificate.)
  - Ke5 already stands on the e-pawn's path. Kd5 and Kf5 reach e5 next move: after ...Kxd7, e5 is not
    adjacent to d7 and not attacked by e7.
  - By Lemma 2.9, (L1) fails for these three sorties. PROVED.
  - That the three sorties are *not punished* in P (no forced promotion for Black) rests on scratch evidence
    only, and is a CONJECTURE (revised after review: R4 item 9, R1 item 11): even without passes, Black cannot
    force promotion after Kd5, Ke5 or Kf5. Only Kf7 loses, in 10 moves. In chess, kpsolve gives (D, W) for the
    6-rank analogue Z_72 bare, so White to move draws (P5).
>>>>>>> NEW

### EDIT 15: R4 item 6
<<<<<<< OLD
- **Without the pawn break.** If f8 were unavailable, the group would be a both-sides shuttle (dud-type), and
  Theorem 3.4(a) would make every threat-free sum a draw.
  - *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. dud may not occur in small K+P groups (CONJECTURE).
=======
- **Without the pawn break. CONJECTURE** (revised after review: R4 item 6): if f8 were unavailable, the
  group would be a both-sides shuttle (dud-type), and Theorem 3.4(a) would make every threat-free sum a draw —
  but that needs a two-sided Proposition 3.2, which is not proved: the bisimulation must hold on the four
  combined king states, in each of which each side's shuttle is legal and each side is frozen.
  - *Scratch evidence:* no both-sides-shuttle group without a pawn break exists among 3-file groups with
    ≤ 2 + 2 pawns and no passer on the 8×6 cylinder. dud may not occur in small K+P groups (CONJECTURE).
>>>>>>> NEW

### EDIT 16: R1 item 11
<<<<<<< OLD
- **So Z_onT1 realises `on`.** By Proposition 3.2, its chess bridge and Proposition 2.10(a), Theorem 3.4(b)
  applies in every non-terminal context that leaves d5 legal and leaves Black a legal move after Kxb5. Black
  loses unless it has a forced decisive event against a passing White. Predictions P2 and P10.
=======
- **So Z_onT1 realises `on`. PROVED in P** (revised after review: R1 item 11: the claim carried no label).
  By Proposition 3.2, its chess bridge and Proposition 2.10(a), Theorem 3.4(b) applies in every non-terminal
  context that leaves d5 legal and leaves Black a legal move after Kxb5. Black loses unless it has a forced
  decisive event against a passing White. Predictions P2 and P10; in chess the conclusion needs (A_Q), which
  is checked position by position (kpsolve: (W, W) for all ten P2 and P10 positions).
>>>>>>> NEW

### EDIT 17: R1 items 10 and 11, R4 item 9
<<<<<<< OLD
- **It passes the convention's test.** Every Black king move drops b3, after which White has a passer and
  Black none, and White's king shuttles a3 ↔ a4.
- **But Black has an escape.** *Scratch evidence:* after the sortie Kc5 and Kxb3, White cannot force
  promotion even without passes. After Kd4 and Kd5, White wins only if Black has no spare move.
=======
- **It passes the convention's test. PROVED by enumeration.** Every Black king move drops b3, after which
  White has a passer and Black none, and White's king shuttles a3 ↔ a4.
- **But Black has an escape. CONJECTURE (scratch evidence; kpsolve agrees).** After the sortie Kc5 and Kxb3,
  White cannot force promotion even without passes; after Kd4 and Kd5, White wins only if Black has no spare
  move. Black's legal moves in the group are Kc5, Kd4, Kd5 and Kd3 (revised after review: R1 item 10 — Kd3
  was missing from the original list; Kc3 is illegal because White's pawn b2 attacks c3), and kpsolve confirms
  that the escape is exactly Kc5: `Ka4 Pb2 kc5 pb3 w -` is (D, D) — a draw, with or without the passes — while
  `Ka4 Pb2 kd3 pb3 w -`, `Ka4 Pb2 kd4 pb3 w -` and `Ka4 Pb2 kd5 pb3 w -` are (W, W).
  - Reproduce: `printf 'Ka4 Pb2 kc5 pb3 w -\nKa4 Pb2 kd3 pb3 w -\nKa4 Pb2 kd4 pb3 w -\nKa4 Pb2 kd5 pb3 w -\n'
    | kings/kpsolve --board cyl:8x6 --ep on --promote QRBN --cap 1 --moves`.
>>>>>>> NEW

### EDIT 18: R1 item 11
<<<<<<< OLD
  - Our count gives μ_W = 5: the c-pawn walks c4–c8 while Black is busy.
  - Black's local win after Ke6 Kxg4 takes T = 5 (scratch).
  - So μ = T, and (L2) fails by one tempo.
=======
  - Our count gives μ_W = 5: the c-pawn walks c4–c8 while Black is busy. **PROVED by count** (revised after
    review: R1 item 11: this chain carried no labels).
  - Black's local win after Ke6 Kxg4 takes T = 5 (scratch). **CONJECTURE** (scratch evidence).
  - So μ = T, and (L2) fails by one tempo. **CONJECTURE** (scratch evidence; Review 4 re-derived both
    numbers independently: μ = 5 = T, so (L2) does fail by one tempo — R4 item 10).
>>>>>>> NEW

### EDIT 19: R1 item 5, PREDICTIONS.md
<<<<<<< OLD
kpsolve options: `--ep on --promote QRBN --cap 1`. Positions use the format of `kings/SPEC.md`; append
` w -` or ` b -`. Each row gives:
- the predicted result pair (w, b), W/D/L from White's view;
- the naive-convention pair (king group read as 0, H valued by `cylcgt` on its strip);
- the theorem behind the prediction, and its label.
=======
kpsolve options: `--ep on --promote QRBN --cap 1`, and `--cap 2` for the three P4 rows whose cap-1 bounds
differed. Positions use the format of `kings/SPEC.md`; append ` w -` or ` b -`. Each row gives:
- the predicted result pair (w, b), W/D/L from White's view;
- the Z = 0 convention pair (king group read as 0, H valued by `cylcgt` on its strip);
- the pair kpsolve computes in chess (C), from `kings/results/PREDICTIONS.md`;
- the theorem behind the prediction, and its label.

Reproduce the kpsolve column with `kings/kpsolve --board cyl:7x6 --ep on --promote QRBN --cap 1` on the
positions of the rows (and `--board cyl:8x6` for P10, `--cap 2` for the three P4 rows); the raw runs are in
`kings/results/theory_predictions_raw.txt` and `kings/results/theory_P4_cap2.txt`.
>>>>>>> NEW

### EDIT 20: PREDICTIONS.md (kpsolve column)
<<<<<<< OLD
| # | Board | Position family | Predicted (w, b) | Naive convention | Basis | Label |
|---|---|---|---|---|---|---|
=======
| # | Board | Position family | Predicted (w, b) | Z = 0 convention | kpsolve (C) | Basis | Label |
|---|---|---|---|---|---|---|---|
>>>>>>> NEW

### EDIT 21: PREDICTIONS.md (kpsolve column)
<<<<<<< OLD
| P1a | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` | (D, D) | (W, W) | (V1b) fails: stalemate (§5.4) | PROVED |
| P1b | cyl:7x6 | `Kc1 Pb2 Pe2 ka2 pb3 pc2 pe3 pe5` | (D, D) | (L, L) | mirror of P1a | PROVED |
| P2 | cyl:7x6 | Z_onT1 `Ka5 Pb4 Pc5 kc6 pb5` + each of {nothing, Hm1, H\*, H\*2, H0} | (W, W) in all five | (L,W), (L,L), (W,L), (W,L), (L,W) | Thm 3.4(b) + Prop 3.2 + Prop 2.10(a) | PROVED in P; C modulo (A_Q) |
| P3 | cyl:7x6 | Z_offT1 `Kc1 Pb2 ka2 pb3 pc2` + each of {nothing, Hp1, H\*, H\*2, H0} | (L, L) in all five | (L,W), (W,W), (W,L), (W,L), (L,W) | mirror of P2 | PROVED in P; C modulo (A_Q) |
| P4 | cyl:7x6 | Z_T `Ka4 Pb3 kc3 pb4` + each of {nothing, Hm1, Hp1, H\*, H\*2, H0} | equal to the convention: (L,W), (L,L), (W,W), (W,L), (W,L), (L,W) | same | Thm 2.4(b) + Thm 2.7. (L1) holds: scratch, T ≤ 5, all budgets, confined king. (L2) holds at every loser-to-move node: scratch. (L3) not checked | CONJECTURE |
=======
| P1a | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 Pe4 kc6 pb5 pe5` | (D, D) | (W, W) | (D, D) | (V1b) fails: stalemate (§5.4) | PROVED; kpsolve agrees |
| P1b | cyl:7x6 | `Kc1 Pb2 Pe2 ka2 pb3 pc2 pe3 pe5` | (D, D) | (L, L) | (D, D) | mirror of P1a | PROVED; kpsolve agrees |
| P2 | cyl:7x6 | Z_onT1 `Ka5 Pb4 Pc5 kc6 pb5` + each of {nothing, Hm1, H\*, H\*2, H0} | (W, W) in all five | (L,W), (L,L), (W,L), (W,L), (L,W) | (W, W) in all five | Thm 3.4(b) + Prop 3.2 + Prop 2.10(a) | PROVED in P; C modulo (A_Q); kpsolve agrees on all ten |
| P3 | cyl:7x6 | Z_offT1 `Kc1 Pb2 ka2 pb3 pc2` + each of {nothing, Hp1, H\*, H\*2, H0} | (L, L) in all five | (L,W), (W,W), (W,L), (W,L), (L,W) | (L, L) in all five | mirror of P2 | PROVED in P; C modulo (A_Q); kpsolve agrees on all ten |
| P4 | cyl:7x6 | Z_T `Ka4 Pb3 kc3 pb4` + each of {nothing, Hm1, Hp1, H\*, H\*2, H0} | equal to the convention: (L,W), (L,L), (W,W), (W,L), (W,L), (L,W) | same | (L,W), (L,L), (W,W), (D,L), (D,L), (L,D) | Thm 2.4(b) + Thm 2.7. (L1) holds: scratch, T ≤ 5, all budgets, confined king. (L2) holds at every loser-to-move node: scratch. (L3) not checked | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H\*, H\*2, H0) |
>>>>>>> NEW

### EDIT 22: PREDICTIONS.md (kpsolve column)
<<<<<<< OLD
| P5 | cyl:7x6 | Z_72 `Kc4 Pb5 kb6 pc5`, bare; and + Hp1 | bare (D, W); + Hp1 (W, W) | bare (L, W); (W, W) | Black side: Prop 2.10(a) with T = 1 (PROVED in P). White side: Lemma 2.9 (escape by blockade) | all entries PROVED in P except the bare w-entry, which is a CONJECTURE (scratch: no forced promotion) |
| P6 | cyl:8x8 | 5.1 `Kh5 Pa4 kb4 pa5` | (L, W): a real mutual zugzwang | (L, W) | Thm 2.4 + Thm 2.7 ((L1) scratch, T ≤ 7) + self-duality | CONJECTURE |
| P7 | cyl:8x8 and flat:8x8 | 7.2 group `Ke6 Pd7 kd8 pe7` | (D, W) | (L, W) | Prop 2.10(a) for Black; Lemma 2.9 for White | b PROVED in P; w CONJECTURE |
| P8 | cyl:8x8; cyl:7x6 | 7.3 group `Kg8 Pf7 kf6 pg7`; 6-rank analogue `Kc6 Pb5 kb4 pc5` | (W, W) | (L, W) (read as 0) | unparriable safe promotion (§5.3) | PROVED in P |
=======
| P5 | cyl:7x6 | Z_72 `Kc4 Pb5 kb6 pc5`, bare; and + Hp1 | bare (D, W); + Hp1 (W, W) | bare (L, W); (W, W) | bare (D, W); + Hp1 (W, W) | Black side: Prop 2.10(a) with T = 1 (PROVED in P). White side: Lemma 2.9 (escape by blockade) | all entries PROVED in P except the bare w-entry, which is a CONJECTURE (scratch: no forced promotion); kpsolve agrees on all four entries |
| P6 | cyl:8x8 | 5.1 `Kh5 Pa4 kb4 pa5` | (L, W): a real mutual zugzwang | (L, W) | not run | Thm 2.4 + Thm 2.7 ((L1) scratch, T ≤ 7) + self-duality | CONJECTURE (not run on 8×8) |
| P7 | cyl:8x8 and flat:8x8 | 7.2 group `Ke6 Pd7 kd8 pe7` | (D, W) | (L, W) | not run | Prop 2.10(a) for Black; Lemma 2.9 for White | b PROVED in P; w CONJECTURE (not run on 8×8) |
| P8 | cyl:8x8; cyl:7x6 | 7.3 group `Kg8 Pf7 kf6 pg7`; 6-rank analogue `Kc6 Pb5 kb4 pc5` | (W, W) | (L, W) (read as 0) | 6-rank analogue (W, W); 8×8 not run | unparriable safe promotion (§5.3) | PROVED in P |
>>>>>>> NEW

### EDIT 23: PREDICTIONS.md (kpsolve column)
<<<<<<< OLD
| P9 | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 kc6 pb5 pf3` | (W, L): class 𝓝 | BIG with Z as `on`: (W, W) | Thm 3.3 versus Thm 3.4(b). Black: fxe2 and e1=Q; White: exf3, then zugzwang (Kd5 forced) | PROVED in P |
| P10 | cyl:8x6 | Z_onT1 + k Black tempo units: k = 0 nothing; k = 1 `Pe2 pe3 pe5`; k = 2 also `Pg2 pg3 pg5` | (W, W) for k = 0, 1, 2 | (L,W), (L,L), (L,L) | Prop 4.3 + Thm 3.4(b): the result does not depend on k, and there is no integer threshold | PROVED in P |
| P11 | cyl:8x6, `--frozen` | Kings parked on the a-file (`Ka1 ka6`, b- and h-files empty); pawn components on c–g; every passer and race node speed-certified (Remark 2.11 with frozen kings); condition (E) | kpsolve `--frozen` = o(W(X)); also = o(S(X)) when hereditarily sum-safe. Where o(S) ≠ o(W) (opposite threats, Prop 1.12), `--frozen` sides with W | — | Thm 1.11 + Thm 1.14 (frozen kings satisfy V1 and V3 by fiat) | PROVED (as an implication; the harness checks the hypotheses) |
| P12 | cyl:7x6 | Z_T + any context on e–f | Every disagreement between kpsolve (real) and `kpsolve --frozen` is witnessed, at some loser-to-move node, by a king move that violates (L1), (L2) or (L3), or by an (A_Q) or (V2) failure | — | Thm 2.4(b) + Thm 2.7 (contrapositive) | PROVED (implication) |
=======
| P9 | cyl:7x6 | `Ka5 Pb4 Pc5 Pe2 kc6 pb5 pf3` | (W, L): class 𝓝 | BIG with Z as `on`: (W, W) | (W, L) | Thm 3.3 versus Thm 3.4(b). Black: fxe2 and e1=Q; White: exf3, then zugzwang (Kd5 forced) | PROVED in P; kpsolve agrees |
| P10 | cyl:8x6 | Z_onT1 + k Black tempo units: k = 0 nothing; k = 1 `Pe2 pe3 pe5`; k = 2 also `Pg2 pg3 pg5` | (W, W) for k = 0, 1, 2 | (L,W), (L,L), (L,L) | (W, W) for k = 0, 1, 2 | Prop 4.3 + Thm 3.4(b): the result does not depend on k, and there is no integer threshold | PROVED in P; kpsolve agrees for k = 0, 1, 2 |
| P11 | cyl:8x6, `--frozen` | Kings parked on the a-file (`Ka1 ka6`, b- and h-files empty); pawn components on c–g; every passer and race node speed-certified (Remark 2.11 with frozen kings); condition (E). Here W(X) is the D-game of X with its own winning side, and "hereditarily sum-safe" (HSS) means that every component of X is itself sum-safe in the sense of Theorem 1.14(ii) | kpsolve `--frozen` = o(W(X)); also = o(S(X)) when hereditarily sum-safe. Where o(S) ≠ o(W) (opposite threats, Prop 1.12), `--frozen` sides with W | — | — (a harness check, not one position) | Thm 1.11 + Thm 1.14 (frozen kings satisfy V1 and V3 by fiat) | PROVED (as an implication; the harness checks the hypotheses) |
| P12 | cyl:7x6 | Z_T + any context on e–f | Every disagreement between kpsolve (real) and `kpsolve --frozen` is witnessed, at some loser-to-move node, by a king move that violates (L1), (L2) or (L3), or by an (A_Q) or (V2) failure | — | — (a harness check, not one position) | Thm 2.4(b) + Thm 2.7 (contrapositive) | PROVED (implication), restricted to the nodes where `--frozen` reports a win |
>>>>>>> NEW

### EDIT 24: R4 item 7
<<<<<<< OLD
- **What P2, P3 and P10 prove.** The derivations use only enumerated move lists (§5.4) and Theorem 3.4(b).
  The one-move punishment holds in every context listed: none of them puts a pawn on e4 (respectively e3)
  that would cover d5 (respectively d2).
  - In H\*2, White's double step e2–e4 *would* stalemate Black. In P3's H\*2, Black's double step e5–e3 would
    stalemate White. The winner simply never plays it.
=======
- **What P2, P3 and P10 prove.** The derivations use only enumerated move lists (§5.4) and Theorem 3.4(b).
  The one-move punishment holds in every context listed, except where a context pawn covers the king's escape
  square d5 (respectively d2) — and that happens only after the *winning* side has moved its own pawn there:
  - In H\*, White's single step e3–e4 covers d5 and **stalemates Black**: kpsolve scores it a draw, so White
    must avoid it and play the shuttle (Ka6). (Revised after review: R4 item 7: the old sentence "none of them
    puts a pawn on e4 … that would cover d5" was wrong for H\*, where the pawn moves there during the window.)
  - In H\*2, White's double step e2–e4 *would* stalemate Black. In P3's H\*2, Black's double step e5–e3 would
    stalemate White. The winner simply never plays it.
>>>>>>> NEW

### EDIT 25: R1 item 6
<<<<<<< OLD
- **Scratch confirmation in P.** A scratch P-model solver (no e.p.; queen safety required) reproduced every
  P-level entry of P1, P2, P3, P5, P9 and P10 that it finished:
=======
- **Scratch confirmation in P.** A scratch P-model solver (no e.p.; queen safety required — a stricter P
  than Definition 1.5's, which counts any promotion as a win) reproduced every P-level entry of P1, P2, P3,
  P5, P9 and P10 that it finished:
>>>>>>> NEW

### EDIT 26: R1 item 5, PREDICTIONS.md
<<<<<<< OLD
- **Where the naive convention fails.** P2, P3 and P10 are the decisive tests of the loopy theory. In every
  one of their 13 positions, the naive convention gets at least one of the two results wrong (17 of the 26
  entries). P1 is the decisive test of (V1b).
- **What P4 tests.** P4 is the positive control: the theory predicts that the convention is *right* there.
=======
- **What separates the theory from the conventions (revised after review: R1 item 5).** The old headline — "P2,
  P3 and P10 are the decisive tests of the loopy theory" — did not say which baseline it used. Against the
  note's own "Z = 0" reading (king group = 0, the context valued by cylcgt on its strip) it is right: that
  reading gets 17 of the 26 P2/P3/P10 entries wrong, and at least one of the two results in every one of the
  13 positions. Against the *literal* convention it is not: on the actual pawn sets, `cylcgt.pawns.value`
  returns +BIG for every P2 and P10 position and −BIG for every P3 position, so literal cylcgt gets all 26
  entries right and does **not** separate the theory from cylcgt. The positions that do separate them are P1
  (the stalemate trap: both readings say (W, W) and (L, L), the truth is (D, D)), P5 and P7 (the literal
  reading has no answer — it scores a race at move 0 on the 6-rank analogue — while kpsolve settles P5 bare as
  (D, W)), P9 (both readings predict (W, W), the truth is (W, L)) and P4 (below). Over the 25 exactly
  determined predictions of `kings/results/PREDICTIONS.md`, the theory holds in 22 and literal cylcgt in 16;
  the three positions literal cylcgt scores as a race (P5 bare, P5 + Hp1, P8 6-rank) have no answer from it
  at all.
- **What P4 tests, and how it failed.** P4 was the positive control: the theory predicts that the convention
  is *right* there. kpsolve refutes it in 3 of the 6 contexts.
  - H\* and H\*2 with White to move are draws, not (W, L). In H\* every White king move loses (Ka5, Kb5, Kg3,
    Kg4, Kg5) and White's only drawing move is e3–e4; in H\*2 the position is a draw as well.
  - H0 with Black to move is a draw, not (L, W): Black's king draws by Kd3 or Kd2.
  - The mechanism: the defending king walks to the locked context pawns and attacks the stuck pawn there
    (…Kd3, …Kd2, …Kd4). In H0 after …Kd3 the white king is confined to the a- and b-files: Kg4, Kg5 and Kg3
    all lose, while Ka5, Kb4 and Kb5 draw. This is what Proposition 2.10(b) predicts — the zero of the group is
    context-dependent, a CONJECTURE after Proposition 2.10(b), now supported in C by P4 — and the (L2) margin
    the theory assumed does not survive the context.
  - The same three contexts are exactly the ones in which the Z = 0 convention and literal cylcgt are wrong
    too, so the refutation is a fact about the positions, not about the convention.
>>>>>>> NEW

### EDIT 27: R1 item 10, R4 item 8
<<<<<<< OLD
- **Group search.** On the 8×6 and 7×6 cylinders: all placements of the kings and of ≤ 2 + 2 pawns on 3 (or 4)
  files, with no passer at the root. Each placement was classified as frozen, on, off, dud or over by one-ply
  tests. It found:
=======
- **Group search.** On the 8×6 and 7×6 cylinders: all placements of the kings and of ≤ 2 + 2 pawns on 3 (or 4)
  files, with no passer at the root. Each placement was classified as frozen, on, off, dud or over by one-ply
  tests. It found: (revised after review: R1 item 10, R4 item 8: the search covered ≤ 2 + 2 pawns, so every
  claim that depends on it is stated for ≤ 2 + 2 — Conjecture 4.7's "≤ 3 + 2" was wrong. The "no passer at the
  root" test is the note's own, not cylcgt's: cylcgt's passed test calls Z_onT1's c5 passed, so the search
  would have rejected Z_onT1.)
>>>>>>> NEW

## STATUS ROWS

| result | final label | one-line note with review item |
|---|---|---|
| T4.2(a) | PROVED after repair (through the corrected T1.11(b)) | R4 item 3: Black suicides inside R_n break the hypothesis; R_n must have no Black options |
| T4.2(b) | PROVED after repair (needs B > ℓ; the D-model equivalence is now proved) | R4 item 4: Lemma 1.7 is a D-result, not a CGT equality |
| T4.2(c) | PROVED after repair (negative integers; reachable cycle; "acyclic", not "non-reversible") | R4 item 5 |
| P4.3 | FALSE as originally stated (a king in check) → s not in check on u, reply not a promotion: PROVED after repair. The dichotomy "0 or ∞" is narrowed to steps inside F_Z with the opponent frozen at both ends | R4 items 1 and 2, R1 item 11 |
| D4.4 (over) | the numbering gap is filled | R1 item 11 |
| P4.5, P4.6 | PROVED | R4: sound |
| C4.7 | CONJECTURE, restated for ≤ 2 + 2 pawns (what was searched) | R1 item 10, R4 item 8 |
| §3, shuttles on both sides | CONJECTURE: needs a two-sided Proposition 3.2 | R4 item 6 |
| §3, Prop 3.2 chess bridge | PROVED after repair (adds (V1a)) | R4 item 7 |
| §4, "over" chess reading | the "typically a pawn move by Proposition 4.3" is withdrawn | R4 item 8 |
| §5.1, frozen | PROVED by enumeration, now written out | R1 item 11, R4 item 9 |
| §5.2, White's sorties | the certificate fails: PROVED (L2.9). "Not punished": CONJECTURE (scratch); in C, kpsolve confirms the 6-rank analogue (P5) | R4 item 9 |
| §5.4, Z_onT1 realises `on` | PROVED in P (label added) | R1 item 11 |
| §5.5 | CONJECTURE (scratch; kpsolve agrees): the escape is exactly Kc5 — (D, D) after …Kc5, (W, W) after …Kd3, …Kd4 and …Kd5. Kd3 added to the move list | R1 items 10 and 11, R4 item 9 |
| §5.6 | μ_W = 5: PROVED by count. T = 5 and "(L2) fails by one tempo": CONJECTURE (scratch; R4 re-derived both) | R1 item 11 |
| P1a, P1b (§6) | PROVED; kpsolve (D, D) | PREDICTIONS.md, as for every P-row |
| P2, P3 | PROVED in P; kpsolve agrees in C on all 10 positions; literal cylcgt also gets them right | R1 item 5 |
| P4 | CONJECTURE → **refuted** by kpsolve in 3 of 6 contexts (H*, H*2, H0) | PREDICTIONS.md, theory_P4_cap2_moves.txt |
| P5 | PROVED in P (b entries, + Hp1); bare w-entry CONJECTURE; kpsolve agrees on all four entries | — |
| P6, P7 | CONJECTURE, and partly PROVED in P; not run | — |
| P8 | PROVED in P; kpsolve (W, W) on the 6-rank analogue; 8×8 not run | — |
| P9 | PROVED in P; kpsolve (W, L) | — |
| P10 | PROVED in P; kpsolve (W, W) for k = 0, 1, 2 | R1; PREDICTIONS.md lists all three rows (the draft row said "not run") |
| P11 | PROVED (implication) after repair: W(X) and HSS defined; (V1b) checked from the layout | R1 item 11 |
| P12 | PROVED (implication) after repair: restricted to nodes where `--frozen` reports a win | knock-on of R2 item 4 |
