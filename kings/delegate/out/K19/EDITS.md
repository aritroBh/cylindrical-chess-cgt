# K19 edits to kings/theory/LOOPY.md

Labels changed: CONJECTURE to CHECKED-2 where K19's independent code and the original scratch result agree; (L3) is COMPUTED-1 (never checked before, one implementation); two statements are corrected (Black's king moves in 5.1, and "only if Black has no spare move" in 5.5). Apply in order; OLD occurs exactly once in the current LOOPY.md (the script `scripts/make_edits.py` asserts it).

### EDIT labels-checked2
<<<<<<< OLD
- **KNOWN**: from the literature, with a citation.
=======
- **KNOWN**: from the literature, with a citation.
- **COMPUTED-1** and **CHECKED-2** (revised after K19, 2026-10-27): labels for a finite computation, never for a
  theorem. COMPUTED-1: one implementation produced the numbers. CHECKED-2: two independently written
  implementations agree on the exact numbers (for example the scratch run and a second program, or two solvers).
  Neither label is a proof, and neither replaces PROVED for a statement over all contexts.
>>>>>>> NEW

### EDIT status-5.1-L1
<<<<<<< OLD
| §5.1, (L1) | CONJECTURE (scratch, k ≤ 4 and k = ∞ only; (L3) not checked). The k = ∞ case was re-run in K7 against the local game of Definition 2.6 ((L1_P): T = 5 to 6; (L1) with the queen clause: T = 6 to 7), same label (revised after K7, 2026-10-22) | R1 items 3 and 10, R4 item 9; K7 |
=======
| §5.1, (L1) | CHECKED-2 (revised after K19, 2026-10-27). K19 wrote the local game again from Definition 2.6 and agrees with the K7 numbers: after the reply Kxa4, with k = ∞ and the king confined to {h, a, b}, T = 6, 6, 6, 7, 7 with the queen clause and T = 6, 6, 5, 6, 6 for (L1_P) (Kg4, Kg5, Kg6, Kh6, Ka6). With the pre-K7 rules and every budget k = 0, …, 8 and ∞ the least T is 5 to 7, as the scratch run said. The budgets k = 5, 6 (not checked before) equal k = ∞, and so does every k ≥ 7, because the window holds at most T ≤ 7 moves of s. The five Black sorties give the mirrored numbers. (L3): COMPUTED-1 (K19 only): in the bare group it holds for the five sorties at T and at T + 1, T + 2, with and without the queen clause | R1 items 3 and 10, R4 item 9; K7; K19 |
>>>>>>> NEW

### EDIT status-5.2
<<<<<<< OLD
"Not punished": CONJECTURE (scratch); in C, kpsolve confirms the 6-rank analogue (P5) | R4 item 9 |
=======
"Not punished": CHECKED-2 (revised after K19, 2026-10-27): after Kd5, Ke5 or Kf5 Black has no forced promotion, in the local game after ...Kxd7 (with or without passes, confined or not) and in the exact P-model after the sortie with every Black reply (result D, two solvers). Only Kf7 loses, with T = 10. In C, kpsolve agrees on both boards and on the 6-rank analogue (P5) | R4 item 9; K19 |
>>>>>>> NEW

### EDIT status-5.5
<<<<<<< OLD
| §5.5 | CONJECTURE (scratch); Kd3 added | R1 items 10 and 11, R4 item 9 |
=======
| §5.5 | CHECKED-2 (revised after K19, 2026-10-27), with one correction. Confirmed: Black's moves are exactly Kc5, Kd3, Kd4, Kd5; after Kc5 Kxb3 White has no win with any number of passes; after Kd3 White wins with T = 5 for every budget, unlimited passes included. Corrected: after Kd4 and Kd5 White wins the local game against every finite budget of passes (T = 6 + k) and not against unlimited passes, so "only if Black has no spare move" holds for an unlimited supply only. kpsolve and the P-model agree on all four sorties | R1 items 10 and 11, R4 item 9; K19 |
>>>>>>> NEW

### EDIT status-5.6
<<<<<<< OLD
μ_W = 5: PROVED by count. T = 5 and "(L2) fails by one tempo": CONJECTURE (scratch; R4 re-derived both) | R1 item 11 |
=======
μ_W = 5: PROVED by count (K19's breadth-first search agrees). T = 5 and "(L2) fails by one tempo": CHECKED-2 (revised after K19, 2026-10-27: T = 5 for every budget, with or without the queen clause and the confinement; μ_W = 5 < T + 1 = 6; the scratch run, R4 and K19 agree) | R1 item 11; K19 |
>>>>>>> NEW

### EDIT status-P5
<<<<<<< OLD
bare w-entry CONJECTURE; kpsolve agrees on all four entries | — |
=======
bare w-entry CHECKED-2 (revised after K19, 2026-10-27: the P-value D from two independent solvers, and D in C from kpsolve); kpsolve agrees on all four entries | K19 |
>>>>>>> NEW

### EDIT status-P6P7
<<<<<<< OLD
| P6, P7 | CONJECTURE, and partly PROVED in P. kpsolve (exact, 8×8):
=======
| P6, P7 | CHECKED-2 (revised after K19, 2026-10-27: P6 = (L, W) and P7 = (D, W) in P from two independent solvers, on the cylinder and on the flat board; P7's w-entry is the draw that was a CONJECTURE), and partly PROVED in P. kpsolve (exact, 8×8):
>>>>>>> NEW

### EDIT 5.1-black-moves
<<<<<<< OLD
BK's five legal moves are Ka3, Kc3,
  Kc4, Kc5 and Kb5; the first four abandon BP a5, which White's king then captures on a5, giving White a
  passer, and the fifth (Kb5) puts Black's king on the square that guards both a4 and a5, so that White is in
  zugzwang with only pawn-blocked moves left. So every king move in the group is decisively punished, and the
  group is frozen. The enumeration agrees with `notes/diagram_audit.md` §C.3.
=======
BK's five legal moves are Ka3, Kb3,
  Kc3, Kc4 and Kc5 (Kb5 is illegal: the pawn a4 attacks b5); each of them abandons BP a5, which White's king
  then captures on a5, giving White a passer. (They are the mirror images of the White list: g4 ↔ c5, g5 ↔ c4,
  g6 ↔ c3, h6 ↔ b3, a6 ↔ a3.) So every king move in the group is decisively punished, and the group is frozen.
  (Corrected after K19, 2026-10-27: the earlier list had Kb5 for Kb3 and a zugzwang argument for a move that is
  not legal. The conclusion stands. K19's move generator, checked against `kpsolve --moves`, gives the list above.
  The agreement with `notes/diagram_audit.md` §C.3 claimed earlier refers to the earlier list; K19 did not re-read
  the audit.)
>>>>>>> NEW

### EDIT 5.1-L1-bullet
<<<<<<< OLD
  - (L1) holds for all five White sorties with T ≤ 7 (5 to 7, depending on the sortie and the budget), for
    pass budgets **k ≤ 4 and k = ∞**, with the punisher's king confined to {h, a, b}. Budgets k = 5, 6 were
    not checked; they differ from ∞ when T ≥ 6. This is scratch evidence (Appendix A) (revised after review:
    R1 item 10, R4 item 9).
=======
  - (L1) holds for all five White sorties with T ≤ 7 (5 to 7, depending on the sortie and the budget), for
    every pass budget **k = 0, 1, …, 8 and k = ∞**, with the punisher's king confined to {h, a, b}: **CHECKED-2**
    (revised after K19, 2026-10-27: the scratch run and K19's code agree. The budgets k = 5, 6, 7, 8 equal k = ∞,
    and every k ≥ 7 equals k = ∞, because the window contains at most T ≤ 7 moves of s, so no budget is used up.)
    (L3) holds in the bare group for the five sorties: **COMPUTED-1** (K19 only; Appendix A).
>>>>>>> NEW

### EDIT 5.1-K7-sub
<<<<<<< OLD
This is still scratch evidence: the label stays CONJECTURE (revised after K7, 2026-10-22).
=======
K19's code reproduces both lists, so this is now CHECKED-2 (revised after K19, 2026-10-27).
>>>>>>> NEW

### EDIT 5.1-prediction
<<<<<<< OLD
- **Prediction.** The bare 5.1 is a real mutual zugzwang, (L, W) (P6 in §6). In the bare position the local
  game is the whole game, so the scratch run is a full P-model computation. It is still one throwaway
  implementation, hence a CONJECTURE.
=======
- **Prediction.** The bare 5.1 is a real mutual zugzwang, (L, W) (P6 in §6). **CHECKED-2** (revised after K19,
  2026-10-27): K19's own P-model solver and the P-model build of kpsolve both give (L, W) in P, and kpsolve gives
  (L, W) in C. After each of the five White sorties (Black to move) White is lost in P, and after each of the five
  Black sorties (White to move) Black is lost, in P and in C.
>>>>>>> NEW

### EDIT 5.2-not-punished
<<<<<<< OLD
  - That the three sorties are *not punished* in P (no forced promotion for Black) rests on scratch evidence
    only, and is a CONJECTURE (revised after review: R4 item 9, R1 item 11): even without passes, Black cannot
    force promotion after Kd5, Ke5 or Kf5. Only Kf7 loses, in 10 moves. In chess, kpsolve gives (D, W) for the
    6-rank analogue Z_72 bare, so White to move draws (P5).
=======
  - That the three sorties are *not punished* in P (no forced promotion for Black) is **CHECKED-2** (revised after
    K19, 2026-10-27): even without passes, Black cannot force promotion after Kd5, Ke5 or Kf5. K19: in the local
    game after ...Kxd7 Black has no win at any T, with or without passes, with the king confined to {d, e, f} or
    not; in the exact P-model after the sortie, against every Black reply, the result is a draw (own solver and the
    P build of kpsolve), and kpsolve gives a draw in C on the cylinder and on the flat board. Only Kf7 loses, in 10
    moves (T = 10 in the local game without the queen clause, with or without passes; with the queen clause T = 10
    without passes and 11 with unlimited passes). In chess, kpsolve gives (D, W) for the 6-rank analogue Z_72 bare,
    so White to move draws (P5). In the analogue Kb3, Kc3 and Kd3 are not punished and Kd5 loses (T = 6).
>>>>>>> NEW

### EDIT 5.5-escape
<<<<<<< OLD
- **But Black has an escape. CONJECTURE (scratch evidence; kpsolve agrees).** After the sortie Kc5 and Kxb3,
  White cannot force promotion even without passes; after Kd4 and Kd5, White wins only if Black has no spare
  move. Black's legal moves
=======
- **But Black has an escape. CHECKED-2 (revised after K19, 2026-10-27; kpsolve agrees).** After the sortie Kc5
  and Kxb3, White cannot force promotion even without passes, and not with unlimited passes either (no win at any
  T, confined or not). After Kd4 and Kd5, White wins the local game against every finite budget of Black's passes
  (T = 6 + k with the queen clause, k = 0, …, 8) and does not win against unlimited passes: "wins only if Black
  has no spare move" is right for an unlimited supply of passes and was too strong as written for a finite one.
  After Kd3 White wins with T = 5 for every budget, unlimited passes included. So (L1) holds for Kd3 and fails
  at k = ∞ for Kd4 and Kd5, which are nevertheless punished in P and in C, because the real supply is finite.
  Black's legal moves
>>>>>>> NEW

### EDIT 5.6-T-mu
<<<<<<< OLD
  - Black's local win after Ke6 Kxg4 takes T = 5 (scratch). **CONJECTURE** (scratch evidence).
  - So μ = T, and (L2) fails by one tempo. **CONJECTURE** (scratch evidence; Review 4 re-derived both
    numbers independently: μ = 5 = T, so (L2) does fail by one tempo — R4 item 10).
=======
  - Black's local win after Ke6 Kxg4 takes T = 5. **CHECKED-2** (revised after K19, 2026-10-27: the scratch run and
    K19's code agree. T = 5 for every pass budget 0, …, 4 and ∞, with or without the queen clause and the
    confinement to {f, g, h}. Here Q_Z = `Ke6 kg4 pg5`: the context pawns c3 and d6 are deleted.)
  - So μ = T, and (L2) fails by one tempo. **CHECKED-2** (Review 4 re-derived both numbers, and K19's breadth-first
    search gives μ_W = 5 with the same Q°, so μ_W = 5 < T + 1 = 6). The sortie nevertheless loses in P: the P build
    of kpsolve gives Black the win after Ke6 (`Ke6 Pg4 Pc3 kh4 pg5 pd6 b -` is L from White's side;
    COMPUTED-1, K19), so the documented draw is an (A_Q) failure, not a failure in P.
>>>>>>> NEW

### EDIT 6-P5
<<<<<<< OLD
all entries PROVED in P except the bare w-entry, which is a CONJECTURE (scratch: no forced promotion); kpsolve agrees on all four entries |
=======
all entries PROVED in P except the bare w-entry, which is CHECKED-2 (K19, 2026-10-27: the P-value D from an own solver and from the P build of kpsolve, and D in C from kpsolve); kpsolve agrees on all four entries |
>>>>>>> NEW

### EDIT 6-P6
<<<<<<< OLD
| Thm 2.4 + Thm 2.7 ((L1) scratch, T ≤ 7) + self-duality | CONJECTURE; kpsolve agrees |
=======
| Thm 2.4 + Thm 2.7 ((L1): CHECKED-2, T ≤ 7; (L2) is vacuous in the bare group; (L3): COMPUTED-1) + self-duality (also checked numerically by K19) | CHECKED-2 (K19, 2026-10-27: (L, W) in P from two solvers); kpsolve agrees |
>>>>>>> NEW

### EDIT 6-P7
<<<<<<< OLD
| Prop 2.10(a) for Black; Lemma 2.9 for White | b PROVED in P; w CONJECTURE; kpsolve and Lichess agree |
=======
| Prop 2.10(a) for Black; Lemma 2.9 for White | b PROVED in P; w CHECKED-2 (K19, 2026-10-27: D in P from two solvers, on both boards); kpsolve and Lichess agree |
>>>>>>> NEW

### EDIT appendix-K19
<<<<<<< OLD
    - sharpness examples of the text above: I re-ran them myself with the private builds, and they agree.
=======
    - sharpness examples of the text above: I re-ran them myself with the private builds, and they agree.
- **K19 re-computation (2026-10-27; scripts, logs and `summary.json` in `kings/delegate/out/K19/`).** One new
  implementation, written from Definition 2.6 and `kings/SPEC.md` without reading `kings/ref/` or the K7 scripts:
  - a move generator (kings, pawns, e.p., promotion), which agrees with `kpsolve --moves` on 980 random
    positions (4802 moves, 6 boards, with e.p. rights);
  - the local game of Definition 2.6: bounded recursion with a pass budget k (0, …, 8, ∞), the queen clause and the
    mate rule as switches, so that the pre-K7 and the K7 versions both run; the unbounded least fixed point; (L3) as
    a search over guided strategies against a real s without passes; and μ_s as a breadth-first search;
  - a full-board solver of the model P, which agrees with the P-model build of kpsolve on 350 random positions;
  - the local game with no passes, no confinement and no queen clause is exactly P, and agrees with the P build of
    kpsolve on 110 random positions (38 of them won by the attacker; bounded recursion and fixed point agree).
  Results: §5.1 (L1) and (L3) (five White and five Black sorties), §5.2 (not punished), §5.5, §5.6, P5, P6, P7 as
  recorded in the status table and in those sections. Every kpsolve run used a private build
  (`cc -O2 -o kp kings/kpsolve.c -lpthread`; the P build is K7's `kp_p.c`).
>>>>>>> NEW

