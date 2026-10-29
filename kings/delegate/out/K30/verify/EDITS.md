# EDITS for kings/theory/LOOPY.md (K30, second referee round, 2026-10-28; replaces ../EDITS.md). 12 edits: the 11 edits of the K30 EDITS.md with the Appendix A referee bullet extended, plus one note at the Lemma 2.7a application. Each OLD occurs exactly once in the LOOPY.md of 2026-10-28 01:58 (md5 3da46b286b59cee5da28df055df1d1f3); dry run: 12 applied, 0 rejected.

### EDIT status row 5.2 sorties: not punished
<<<<<<< OLD
"Not punished": CHECKED-2 (revised after K19, 2026-10-27): after Kd5, Ke5 or Kf5 Black has no forced promotion.
=======
"Not punished": PROVED by hand (revised after K30, 2026-10-27; re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`; the computations of K19 and K24 agree): after Kd5, Ke5 or Kf5 Black has no forced promotion.
>>>>>>> NEW

### EDIT status row 5.2 sorties: White cannot win chess
<<<<<<< OLD
That White cannot win chess either, so that the bare group is D in C, is CHECKED-2 by Lemma 2.7a (EPW and EPB computed by two implementations) and kpsolve exact. There is no hand proof of it: Lemma 2.9 refutes (L1) for a defender who may pass, and White cannot pass (open question 7) | R4 item 9; K19; K24 |
=======
That White cannot win chess either, so that the bare group is D in C, is PROVED by hand (revised after K30, 2026-10-27; `kings/delegate/out/K30/PROOF.md`; re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`), on cyl:8×8 and flat:8×8, in chess directly, so Lemma 2.7a is not needed. Part A, White cannot win: after any of its four moves Black plays ...Kxd7, and a lone king can neither promote nor mate. Part B, White does not lose: after Ke5, Kd5 or Kf5 White follows a blockade rule that makes a move every turn, with an invariant of 918 positions per board (Lemma D of the proof), and the other Black replies (...Kc7, ...e6, ...e5) are met by Ke6 or by taking the pawn. An own move generator checked all 918 positions, every Black move and the rule's reply, and three implementations agree on about 15.5k positions. The earlier evidence agrees: Lemma 2.7a with EPW and EPB (two implementations) and kpsolve exact | R4 item 9; K19; K24; K30 |
>>>>>>> NEW

### EDIT status row P6, P7: hand proof of P7 w
<<<<<<< OLD
No hand proof of the P7 w draw exists: Lemma 2.9 refutes (L1) for Ke5, Kd5, Kf5, but (L1) lets White pass, so that failure does not make the sorties safe (open question 7) |
=======
Revised after K30, 2026-10-27: the P7 w draw is PROVED by hand, in P and in chess, on both boards (K30, re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`; `kings/delegate/out/K30/PROOF.md`, mechanically checked). White cannot win: after any of its four moves Black plays ...Kxd7, and a lone king can neither promote nor mate. Black cannot win after Ke5, Kd5 or Kf5: White follows a blockade rule that makes a move every turn (Lemma D of the proof), and the other Black replies are met by Ke6 or by taking the pawn. Kf7 loses in P: PROVED (...e5 and the pawn runs, and the White king is too far by the rule of the square). Lemma 2.9 refutes (L1) for Ke5, Kd5, Kf5, but (L1) lets White pass; the K30 rule never passes |
>>>>>>> NEW

### EDIT section 5.2: not punished
<<<<<<< OLD
is **CHECKED-2** (revised after
    K19, 2026-10-27): even without passes, Black cannot force promotion after Kd5, Ke5 or Kf5.
=======
is **PROVED** (revised after K30, 2026-10-27; hand proof in `kings/delegate/out/K30/PROOF.md`, part B, with the K19 and K24 computations agreeing; K19's revision of 2026-10-27 follows): even without passes, Black cannot force promotion after Kd5, Ke5 or Kf5.
>>>>>>> NEW

### EDIT section 5.2: White cannot win chess
<<<<<<< OLD
That **White cannot win chess either**
    is **CHECKED-2** by Lemma 2.7a: with every promotion a White win, White cannot win, and with every promotion a Black
    win, Black cannot win (two implementations of both models), so the chess value is D, and kpsolve exact agrees (the
    Lichess tablebase also, on the flat board). There is no hand proof of this draw. Lemma 2.9 says only that (L1) fails
    for a defender who may pass, and White cannot pass (open question 7).
=======
That **White cannot win chess either**
    is **PROVED** by hand (revised after K30, 2026-10-27; `kings/delegate/out/K30/PROOF.md`; re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`), so the chess value is D, on both 8×8 boards.
    - White cannot win: every White move leaves d7 unprotected, Black plays ...Kxd7, and a lone king can neither promote nor mate.
    - Black cannot win after Ke5, Kd5 or Kf5: White follows an explicit blockade rule with an invariant (Lemma D of the proof), and it never has to pass. ...Kc7 is met by Ke6, and ...e6 and ...e5 by taking the pawn.
    - Kf7 loses in P: ...e5, and the White king is too far by the rule of the square.
    The earlier evidence agrees: Lemma 2.7a with EPW and EPB (two implementations of both models), kpsolve exact, and the Lichess tablebase on the flat board. The proof does not use Lemma 2.7a. Lemma 2.9 says only that (L1) fails for a defender who may pass; the K30 rule is a blockade that makes a move every turn.
>>>>>>> NEW

### EDIT section 5 summary row
<<<<<<< OLD
7.2 is (D, W) with the w-entry by Lemma 2.7a; there is no hand proof of the 7.2 draw (open question 7) |
=======
7.2 is (D, W), and the w-entry is PROVED by hand (new, K30, 2026-10-27; `kings/delegate/out/K30/PROOF.md`; re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`), with Lemma 2.7a and the solvers as agreeing checks |
>>>>>>> NEW

### EDIT section 5.2 predictions
<<<<<<< OLD
- **Predictions.** The bare 7.2 is (D, W), not the mutual zugzwang (L, W) (P7): CHECKED-2 in P and in C on both boards (revised after K24, 2026-10-27). The same holds for the 6-rank
  analogue (P5).
=======
- **Predictions.** The bare 7.2 is (D, W), not the mutual zugzwang (L, W) (P7). The w-entry D is PROVED by hand in P and in C on both boards (new, K30, 2026-10-27); the b-entry is PROVED in P and CHECKED-2 in C (revised after K24, 2026-10-27). The same values hold for the 6-rank
  analogue (P5), CHECKED-2 (K30's proof does not cover it).
>>>>>>> NEW

### EDIT section 6 row P7: w-entry in C
<<<<<<< OLD
In C the w-entry is D by Lemma 2.7a (EPW and EPB both D for White to move, two implementations) and kpsolve exact, CHECKED-2, with no hand proof (Lemma 2.9 only refutes (L1) for a passing defender; open question 7).
=======
In C the w-entry is D: PROVED by hand (new, K30, 2026-10-27; `kings/delegate/out/K30/PROOF.md`; directly in chess, so Lemma 2.7a is not needed; re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`). The computations agree: Lemma 2.7a with EPW and EPB both D for White to move (two implementations), kpsolve exact, and K30's own solver, `mine.c` and `kp_p --pmodel` on about 15.5k positions per board with 0 differences.
>>>>>>> NEW

### EDIT status row L2.7a
<<<<<<< OLD
The values it is applied to (P5 w, P7 w) are CHECKED-2 |
=======
The values it is applied to (P5 w, P7 w) are CHECKED-2 (revised after K30, 2026-10-27: the P7 w value is also PROVED by hand directly in chess, so for P7 w the lemma is not needed) |
>>>>>>> NEW

### EDIT section 8 item 7
<<<<<<< OLD
7. **A hand proof that White cannot win in 7.2** (CONJECTURE; revised after K24, 2026-10-27). The w-entry of P7 is D in P and
   in C, and so is the w-entry of P5, each CHECKED-2 by computation (Lemma 2.7a for C). No proof by hand exists. Lemma 2.9
   only refutes (L1) for a defender who may pass, and White cannot pass. A proof would have to show that after Ke5, Kd5
   or Kf5 Black has no forced promotion and no forced mate against any White play (for instance by an explicit drawing
   strategy built from the blockade), and that Kf7 is the only losing sortie (T = 11 with the queen clause and 10
   without).
=======
7. **A hand proof that White cannot win in 7.2** (PROVED for 7.2, new, K30, 2026-10-27; re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`; still open for P5). The w-entry of P7 is D in P and
   in C on cyl:8×8 and flat:8×8, with the proof in `kings/delegate/out/K30/PROOF.md`. White cannot win: after any of its four moves Black plays ...Kxd7. Black cannot win after Ke5, Kd5 or Kf5: White follows a blockade rule that makes a move every turn, with an invariant of 918 positions per board, checked by an own move generator. Kf7 loses in P (...e5 and the pawn runs). Still open: the same proof for the 6-rank analogue P5 (the method should carry over; nothing was run), and for other board sizes.
>>>>>>> NEW

### EDIT appendix A: K30 bullet
<<<<<<< OLD
  `kp_p.c` and `atlas/cylinder/kpk`.
- **K18 re-computation (2026-10-27;
=======
  `kp_p.c` and `atlas/cylinder/kpk`.
- **K30 hand proof of the P7 w draw (2026-10-27; `kings/delegate/out/K30/PROOF.md`, scripts and logs in `kings/delegate/out/K30/`; re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`).** One new implementation, `scripts/kpm.py`, an own move generator and solver of P, EPW and EPB written from `kings/SPEC.md` only (no solver code was read), and `scripts/k30lib.py`, which codes the strategies of the proof as finite rules.
  - `check_kpk.py`: the invariant S of Lemma D (918 positions per board) is closed under every Black move and the rule. `check_A.py`: the four White moves, ...Kxd7, Black's rule for EPW, the Kf7 line. `check_B.py`: White's strategy against every Black move for each sortie (about 3,700 White-to-move states each).
  - `compare.py`: 15,536 (cyl:8×8) and 15,695 (flat:8×8) positions visited by the checks, valued by the own solver, `mine.c` (P, EPW, EPB) and `kp_p --pmodel` (P): 0 differences. `mutation_tests.py`: damaged invariants are rejected.
  Results: the P7 w draw is PROVED in P, EPW, EPB and chess; Kf7 loses in P (PROVED).
  - K30 referee, first round (revised after K30, 2026-10-27; its report is `kings/delegate/out/K30/verify/r2/VERIFY_earlier_referee.md`): Lemma D and parts A and C re-derived by hand, case by case. Own code, written from `kings/SPEC.md` and the proof text only: an exact solver of the whole P7 game in P, EPW and EPB (`verify/myx.py`), an exact king-pawn-king solver with the check of S and of the rule (918 positions per board; 6,777 and 5,985 pairs; `verify/mykpk.py`), and an own enumeration of the tau, Kf7 and sigma trees (`verify/mysigma.py`). Every count of the proof is reproduced. The own solver, `ref3` and `mine.c` agree on all 15,536 (cyl) and 15,695 (flat) positions of K30's list in P, and the own solver and `mine.c` in EPW and EPB: 0 differences.
  - K30 referee, second round (revised after K30, 2026-10-27; report `kings/delegate/out/K30/VERIFY.md`, new code in `kings/delegate/out/K30/verify/r2/`): ACCEPT. Lemma D, parts A, B and C and the chess argument re-derived by hand, case by case. New code, written from `kings/SPEC.md` and the proof text only: a move generator and solver of the whole game (`r2_lib.py`, `r2_x.py`), an exact king-pawn-king solver with the check of S and of the rule rho (`r2_kpk.py`), the tau, Kf7 and sigma trees (`r2_tree.py`) and an exhaustive check of Lemma K (`r2_lemmaK.py`). S has 918 positions per board and none is a Black win; the closure over 6,777 (cyl) and 5,985 (flat) pairs has 0 failures; a damaged S (one row cut from Z_L, or the d3, f3 exclusion dropped) is rejected. Whole P7 game, 92,598 (cyl) and 93,830 (flat) positions reachable from X: the own solver, `ref3` (P), `mine.c` (P, EPW, EPB) and `kp_p --pmodel` (P) agree on every one (0 differences), and also on K30's own lists of 15,536 and 15,695 positions. kpsolve exact in chess (cap 1, bounds A = B, re-run by the referee): X is D on both boards, Ke5, Kd5, Kf5 are D, and Kf7 is L, so Kf7 loses in chess too (the proof claims it for P only). Not covered: P5 and other board sizes.
- **K18 re-computation (2026-10-27;
>>>>>>> NEW

### EDIT section 2.7a application: P7 w now has a hand proof
<<<<<<< OLD
The lemma gives a chess draw, not a draw in P and not a hand
  proof of the draw in P.
=======
The lemma gives a chess draw, not a draw in P and not a hand
  proof of the draw in P. (Revised after K30, 2026-10-27: for P7 w the draw, in P and in chess directly, now has a hand proof that does not use this lemma, `kings/delegate/out/K30/PROOF.md`; for P5 w this application is still the route to chess.)
>>>>>>> NEW
