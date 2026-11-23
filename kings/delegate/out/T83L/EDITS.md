# T83L edits to kings/theory/LOOPY.md (timing clause of Theorem 2.7(a))

Source of the finding: `delegate/out/T83/REPORT.md` §A.16 (Codex re-read), check `delegate/out/T83/check.py`.
Analysis: `kings/delegate/out/T83L/findings.txt`. Apply with
`.venv/bin/python kings/delegate/apply_edits.py kings/theory/LOOPY.md OUT.md kings/delegate/out/T83L/EDITS.md`.

### EDIT 1 Theorem 2.7(a): the timing clause
<<<<<<< OLD
- **(a)** If LC_T(m) holds at Y, with reply r, then s̄ has a forced win in P after m: it plays r and then wins
  with one of its next T moves. So m is decisively punished in P.
=======
- **(a)** If LC_T(m) holds at Y, with reply r, then s̄ has a forced win in P after m: it plays r and wins, by a
  promotion or by a mate of s, no later than its T-th move after r. The reply r itself may already mate s
  (example after the proof). So m is decisively punished in P. (Revised after T83, 2026-11-23: the earlier
  wording "it plays r and then wins with one of its next T moves" was false, because a real mate of s, helped
  by an s̄ context pawn, need not be a mate in the projection; the P-win was not affected.)
>>>>>>> NEW

### EDIT 2 Proof of Theorem 2.7, Step 5: a mate of s may come early
<<<<<<< OLD
  - s̄ is not stalemated (Step 3). s is not stalemated by (L3). There is no infinite play: the window has at
    most T moves of s̄.
=======
  - s̄ is not stalemated (Step 3). s is not stalemated by (L3). There is no infinite play: the window has at
    most T moves of s̄.
  - A mate of s ends the play in s̄'s favour. It may come before the local game is over (Step 6) (revised after
    T83, 2026-11-23).
>>>>>>> NEW

### EDIT 3 Proof of Theorem 2.7, Step 6: treat a real mate before projecting
<<<<<<< OLD
- **Step 6: s̄ wins in time.** The projection is a play of the winning local game, so it ends within s̄'s first T
  moves with a promotion by s̄ or a mate of s. A promotion by s̄ is a legal real move (Step 2) and ends the real
  game in s̄'s favour in P. A mate of s in π(R) is a mate in R: s is in check in R (I4), and every legal real
  move of s is a local move or a pass (Step 1), and no pass exists in check, so s has no legal move in R either.
  Since s moves first after r, s̄'s t-th move comes after s's t-th, and the count is the one used in Step 4. ∎
=======
- **Step 6: s̄ wins in time.** (revised after T83, 2026-11-23) A mate of s is a win for s̄ in P, wherever it
  occurs. Step 1 gives one direction only: every legal real move of s is a legal local move or a pass. The
  converse fails, because an s̄ context pawn may attack a square next to s's king that is free in π(R). So s may
  be mated in the real game, at Q or at a later turn of s, while π(R) is not a local mate (example below); then
  s̄ has already won. Otherwise, at each of its turns s is not mated and, by (L3), not stalemated, so it has a
  legal real move, which is a local move or a pass (Step 1); at each of its turns s̄ has the legal real move of ρ
  (Steps 2 and 3). So, as long as the real play lasts, its projection is a play of the winning local game, and
  such a play ends within s̄'s first T moves with a promotion by s̄ or a mate of s. A promotion by s̄ is a legal
  real move (Step 2) and ends the real game in s̄'s favour in P. A mate of s in π(R) is a mate in R: s is in
  check in R (I4), and every legal real move of s is a local move or a pass (Step 1), and no pass exists in
  check, so s has no legal move in R either. Hence every real play ends in a win for s̄ no later than s̄'s T-th
  move after r: by a real mate of s before the local game is over (possibly at Q, so on r itself), or by the
  local win. Since s moves first after r, s̄'s t-th move comes after s's t-th, and the count is the one used in
  Step 4. ∎
>>>>>>> NEW

### EDIT 4 Example after the proof: the reply itself mates
<<<<<<< OLD
**Remark (K3's objection, answered).** K3 wrote that (L2) counts promotions only
=======
**Example (the reply itself can mate). PROVED. (revised after T83, 2026-11-23)** Flat 8×8, F_Z = {a, b}, buffer
c, context on d–h, s = Black, s̄ = White. Y = White Ka6, Pb6, Pb7, Pd6; Black Ka8, Pa7, Pe7; Black to move.
- *Y is as in Definition 2.1.* Kings and Z-pawns stand on a and b, the context pawns d6 and e7 on files at
  distance 2 and 3 from F_Z, the buffer c is empty, there is no officer. Black is in check from b7, which Definition
  2.6 does not forbid.
- *m and r.* Black's only legal move is m = Kb8 (a7 holds Black's own pawn, b7 is guarded by the White king, and
  in check the e-pawn may not move). After m, White cannot promote (b8 is occupied, a8 and c8 are
  empty). r = b6×a7 is admissible: a non-promoting Z-move that leaves White's king on F_Z.
- *Q is mate.* Q = White Ka6, Pa7, Pb7, Pd6; Black Kb8, Pe7. Black is in check from a7. a8 and c8 are attacked by
  b7, a7 and b7 are guarded by the king, and c7 is attacked by the context pawn d6. So r is checkmate.
- *LC_1(m) holds.* Q_Z = π(Q) = White Ka6, Pa7, Pb7; Black Kb8. There c7 is free and Black, in check, has the
  single move Kc7 (no pass in check); White plays a8=Q, which Black cannot capture. So (L1) holds with T = 1, with
  the queen clause. (L2): Q° = Black Kb8, Pe7; White Pd6. The e-pawn needs 5 moves (e5, e4, e3, e2, e1), so
  μ_s = 5 ≥ T + 1 = 2. (L3) for T = 1 asks only that Black is not stalemated at Q; it is mated.
- So the real game ends on r, while the local game still has a move of each side. The P-win stands; the earlier
  clause "then wins with one of its next T moves" was false. The move lists were also confirmed by python-chess
  (COMPUTED-1: `delegate/out/T83/check.py`, function `mate_on_reply`, and the T83L check).
- *A version with Y not in check.* Y = White Ka6, Pb6, Pb7, Pd6; Black Kb8, Pa7, Pa3; Black to move (not in check;
  python-chess accepts it as a legal position). m = a3–a2 (the Black king has no legal move), r = b6×a7 mate as
  above. Q_Z = White Ka6, Pa7, Pb7; Black Kb8, Pa2: Black must play Kc7, and a8=Q wins (T = 1); μ_s = ∞, since
  Black has no context pawn; (L3) holds at Q. PROVED by hand; the move lists and the local win with T = 1 are
  COMPUTED-1 (T83L's python-chess check, one implementation).
- *The stalemate analogue is excluded by hypothesis.* A context pawn can also take away squares next to s's king
  and so make a real stalemate of s that π(R) does not see. (L3) is stated over real plays, not over the local game,
  so it excludes exactly this, and Step 5 uses it. The (L3) example `Kb5 kd5 Pb4 Pc5 Pe3 Pf3 Pf4 Pf5` in "The
  conditions cannot be dropped" is such a stalemate. (L3_F) is a sufficient condition only because its moves (a
  Z-pawn move or a king move onto F_Z) stay legal in the real game (Lemma 2.2).

**Remark (K3's objection, answered).** K3 wrote that (L2) counts promotions only
>>>>>>> NEW

### EDIT 5 Sharpness remark under (L2): "queens on its T-th move"
<<<<<<< OLD
  - **μ_s ≥ T + 1 is the exact bound for P.** Step 4 shows that s promotes no earlier than its (T + 1)-th turn, and
    s̄ queens on its T-th move, which follows s's T-th turn. With μ_s = T, s promotes first (example below).
=======
  - **μ_s ≥ T + 1 is the exact bound for P.** Step 4 shows that s promotes no earlier than its (T + 1)-th turn, and
    s̄ wins, by a promotion or a mate, no later than its T-th move, which follows s's T-th turn (revised after T83,
    2026-11-23: earlier "s̄ queens on its T-th move"). With μ_s = T, s promotes first (example below).
>>>>>>> NEW

### EDIT 6 Status table, row T2.7
<<<<<<< OLD
A second review round found no false step | R1 item 3, R3 items 2 and 3; K3; K7 |
=======
A second review round found no false step. T83 (Codex, 2026-11-23) found the timing clause of (a), "then wins with one of its next T moves", false: r itself can be a real mate while π(Q) is not a local mate, because an s̄ context pawn covers a square next to s's king (example after the proof). The P-win stands; the statement of (a) and Steps 5 and 6 of the proof are corrected (revised after T83, 2026-11-23) | R1 item 3, R3 items 2 and 3; K3; K7; T83 |
>>>>>>> NEW

### EDIT 7 Status after review: the K36 paragraph
<<<<<<< OLD
Every other step is SOUND (revised after K36, 2026-10-28).
=======
Every other step is SOUND (revised after K36, 2026-10-28). T83 (Codex, 2026-11-23) then found the timing clause of
(a) false: the reply r can already be a real mate, helped by a context pawn, although the projection is not a local
mate. The P-win stands; the statement and Steps 5 and 6 are corrected, with the example after the proof (revised
after T83, 2026-11-23).
>>>>>>> NEW
