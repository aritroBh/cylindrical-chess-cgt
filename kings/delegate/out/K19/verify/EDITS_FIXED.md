# Corrected EDIT blocks (K19 referee, VERIFY.md). Use these in place of the K19 blocks with the same label; all other K19 blocks stand. OLD occurs exactly once in the current LOOPY.md.

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
  (Corrected after K19, 2026-10-27: the earlier list had Kb5 in place of Kb3, and a zugzwang argument for a move
  that is not legal. This was a transcription slip in this section: `notes/diagram_audit.md` §C.3 and the scratch
  list of Appendix A both give the correct list a3, b3, c3, c4, c5. The conclusion stands. K19's move generator,
  checked against `kpsolve --moves`, gives the list above, and so does the referee's.)
>>>>>>> NEW

### EDIT status-5.5
<<<<<<< OLD
| §5.5 | CONJECTURE (scratch); Kd3 added | R1 items 10 and 11, R4 item 9 |
=======
| §5.5 | CHECKED-2 (revised after K19, 2026-10-27), with one correction. Confirmed: Black's moves are exactly Kc5, Kd3, Kd4, Kd5; after Kc5 Kxb3 White has no win with any number of passes; after Kd3 White wins with T = 5 for every budget, unlimited passes included. Corrected: after Kd4 and Kd5 White wins the local game against every finite budget of passes (T = 6 + k with the queen clause, T = 5 + k for k ≥ 1 without it) and not against unlimited passes, so "only if Black has no spare move" holds for an unlimited supply only. kpsolve and the P-model agree on all four sorties | R1 items 10 and 11, R4 item 9; K19 |
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
  at k = ∞ for Kd4 and Kd5, which are nevertheless punished in P and in C in the bare group, where Black has no spare move
  (k = 0, T = 6). A context with k spare moves costs k tempi (T = 6 + k), and (L2) then asks for μ ≥ 7 + k.
  Black's legal moves
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
    (revised after K19, 2026-10-27: for k ≤ 4 and k = ∞ the scratch run and K19's code agree. The budgets k = 5, 6, 8 were
    never run before: K19's code and the referee's own code (K19/VERIFY.md) agree that they equal k = ∞. Every
    k ≥ 7 equals k = ∞ for a reason: the window contains at most T ≤ 7 moves of s, so no budget is used up.)
    (L3) holds in the bare group for the five sorties: **CHECKED-2** (K19's code and the referee's own code; Appendix A).
>>>>>>> NEW

### EDIT status-5.1-L1
<<<<<<< OLD
| §5.1, (L1) | CONJECTURE (scratch, k ≤ 4 and k = ∞ only; (L3) not checked). The k = ∞ case was re-run in K7 against the local game of Definition 2.6 ((L1_P): T = 5 to 6; (L1) with the queen clause: T = 6 to 7), same label (revised after K7, 2026-10-22) | R1 items 3 and 10, R4 item 9; K7 |
=======
| §5.1, (L1) | CHECKED-2 (revised after K19, 2026-10-27). K19 wrote the local game again from Definition 2.6 and agrees with the K7 numbers: after the reply Kxa4, with k = ∞ and the king confined to {h, a, b}, T = 6, 6, 6, 7, 7 with the queen clause and T = 6, 6, 5, 6, 6 for (L1_P) (Kg4, Kg5, Kg6, Kh6, Ka6). With the pre-K7 rules and every budget k = 0, …, 8 and ∞ the least T is 5 to 7, as the scratch run said. The budgets k = 5, 6 (not checked before; K19 and the referee agree) equal k = ∞, and so does every k ≥ 7, because the window holds at most T ≤ 7 moves of s. The five Black sorties give the mirrored numbers. (L3): CHECKED-2 (K19 and the referee's own code, each written from the definition): in the bare group it holds for the five sorties at T and at T + 1, T + 2, with and without the queen clause | R1 items 3 and 10, R4 item 9; K7; K19 |
>>>>>>> NEW

### EDIT labels-kpsolve
<<<<<<< OLD
kpsolve results (§6) are data, not proofs: a claim that only a kpsolve run supports keeps the label
CONJECTURE, with "kpsolve agrees" (revised after review: R1 item 6).
=======
kpsolve results (§6) are data, not proofs: a claim that only a kpsolve run supports keeps the label
CONJECTURE (for a statement over all contexts) or COMPUTED-1 (for the finite computation itself), with
"kpsolve agrees" (revised after review: R1 item 6; after K19, 2026-10-27: CHECKED-2 needs a second, independently
written implementation, and a second run of the same code or of a build derived from it does not count).
>>>>>>> NEW
