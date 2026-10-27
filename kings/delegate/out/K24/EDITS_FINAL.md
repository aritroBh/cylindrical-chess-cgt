# EDITS_FINAL for K24 (fix round), rebased onto LOOPY.md after the K19 and K23 edits (commit fb7d4a4)


### EDIT Definition 1.5 frozen line
<<<<<<< OLD
  - `kpsolve --frozen` computes P with frozen kings: a king move loses at once.
=======
  - `kpsolve --frozen` computes the frozen-king model F of Corollary 2.7′ (a king move loses at once for the mover), not P. P itself, with free kings, is computed by K7's build `kings/delegate/out/K7/scripts/draft/kp_p.c` (its flag is `--pmodel`; `kings/kpsolve.c` has no such flag) and by the independent solvers of K19 and K24 (revised after K24, 2026-10-27: this line used to say that `--frozen` computes P).
>>>>>>> NEW

### EDIT Lemma 2.7a (new)
<<<<<<< OLD
**Corollary 2.8 (square-rule form of (L1)). PROVED.** Suppose:
=======
**Lemma 2.7a (transfer from a promotion model to chess). PROVED (new, revised after K24, 2026-10-27).** For a
king-and-pawn position X let EPW(X) be chess in which the first promotion by either side ends the game as a White win,
and EPB(X) the same with a Black win. Everything else is as in chess: a mate wins, stalemate and infinite play are
draws. A promotion move is legal in EPW and EPB exactly when it is legal in chess.
- (a) If White has no winning strategy in EPW(X), White has none in C(X).
- (b) If Black has no winning strategy in EPB(X), Black has none in C(X).
- (c) If both hold, C(X) is a draw.
- *Proof.* (a) By contraposition. Let σ be a winning strategy of White in C(X). Every play consistent with σ is
  finite and ends in a mate of Black. Play σ in EPW(X), against any behaviour of Black. Until the first promotion the
  legal moves, the mate test and the stalemate test are the same in the two games, so the play so far is a prefix of
  a chess play consistent with σ. If a promotion (by either side) occurs before σ's mate, the play ends in EPW as a
  White win. If none occurs, the whole play is a chess play consistent with σ and ends in the mate of Black, which
  is a White win in EPW as well. No play is infinite. So σ wins EPW(X). (b) is the same with the colours exchanged.
  (c) EPW, EPB and C are finite-state reachability games, so "neither side can force a win" is exactly the value D.
  ∎
- The lemma is used only in the direction "cannot win". The converse is not claimed (White may win EPW by a
  promotion that chess does not reward). EPW and EPB do not distinguish the piece promoted to, and the proof needs
  no cap on officers.
- *Application (CHECKED-2: two implementations of the models, K24's `mine.c`, where EPW is `bb` and EPB is `bw`, and the
  referee's `verify/psolve.py`, where EPW is `ww` and EPB is `bb`; logs `kings/delegate/out/K24/logs/models_p_bb_bw.log`
  and `kings/delegate/out/K24/verify/run8.log`).* With White to move, EPW = D and EPB = D for P7 (`Ke6 Pd7 kd8 pe7`, on
  cyl:8×8 and on flat:8×8) and for P5 (`Kc4 Pb5 kb6 pc5`, on cyl:7×6). By the lemma, White cannot win chess and Black
  cannot win chess there, so the chess value of the w-entry is D. kpsolve exact (lower and upper bound equal) gives D
  as well, and the Lichess tablebase agrees on flat:8×8. The lemma gives a chess draw, not a draw in P and not a hand
  proof of the draw in P. For P6 the values are different (EPW = D and EPB = L with White to move on cyl:8×8): the lemma
  is not used there, the chess value comes from the reduction to KPK (§6, P6).
- *Consistency test, not part of the proof.* K24 checked on 423 legal positions of cyl:5×6 (`kings/delegate/out/K24/logs/soundness_bbbw.log`)
  that no position has "White cannot win in EPW" while kpsolve gives a White win in chess, and no mirror case: 0 violations.

**Corollary 2.8 (square-rule form of (L1)). PROVED.** Suppose:
>>>>>>> NEW

### EDIT summary table row for L2.7a
<<<<<<< OLD
| C2.7′ | If `--frozen` reports a win for σ and every king move of σ̄ on the nodes of its winning strategy is a P-loss, σ wins P (content of P12) | PROVED in P (revised after K7, 2026-10-22) |
=======
| C2.7′ | If `--frozen` reports a win for σ and every king move of σ̄ on the nodes of its winning strategy is a P-loss, σ wins P (content of P12) | PROVED in P (revised after K7, 2026-10-22) |
| L2.7a | If White cannot win when every promotion is a White win (EPW), White cannot win chess; the mirror for Black; both together give a chess draw | PROVED (revised after K24, 2026-10-27). The proof is written out in the lemma, and the K24 referee re-derived it independently (`kings/delegate/out/K24/VERIFY.md`, section 5) |
>>>>>>> NEW

### EDIT status row L2.7a
<<<<<<< OLD
| P12 | GAP → PROVED after repair in P (Corollary 2.7′, from the repaired Theorem 2.7), restricted to nodes where `--frozen` reports a win. The chess form adds (A_Q) at the root; the earlier alternative "(V2) failure" is not needed (revised after K7, 2026-10-22) | knock-on of R2 item 4; K3; K7 |
=======
| P12 | GAP → PROVED after repair in P (Corollary 2.7′, from the repaired Theorem 2.7), restricted to nodes where `--frozen` reports a win. The chess form adds (A_Q) at the root; the earlier alternative "(V2) failure" is not needed (revised after K7, 2026-10-22) | knock-on of R2 item 4; K3; K7 |
| L2.7a | New in K24 (2026-10-27): the transfer lemma from the two promotion models EPW and EPB to chess. PROVED; the proof is in the lemma, and the K24 referee re-derived it. The values it is applied to (P5 w, P7 w) are CHECKED-2 | K24; `kings/delegate/out/K24/VERIFY.md` |
>>>>>>> NEW

### EDIT status row 5.1 (L1)
<<<<<<< OLD
in the bare group it holds for all ten sorties (five White, five Black) at T, T + 1 and T + 2, with and without the queen clause | R1 items 3 and 10, R4 item 9; K7; K19 |
=======
in the bare group it holds for all ten sorties (five White, five Black) at T, T + 1 and T + 2, with and without the queen clause. K24 adds two further implementations of the local game, written from Definition 2.6 (the K24 agent's `kings/delegate/out/K24/scripts/lg.py` and the K24 referee's `kings/delegate/out/K24/verify/lg2.py`): the lists are the same, T = 6, 6, 6, 7, 7 with the queen clause and 6, 6, 5, 6, 6 for (L1_P) (Kg4, Kg5, Kg6, Kh6, Ka6), with the same numbers of s-nodes (1025, 1326, 1939, 4273, 3985 with the queen clause). K24 ran the five Black sorties directly: Ka3, Kb3, Kc3, Kc4, Kc5 give T = 7, 7, 6, 6, 6 with the queen clause and 6, 6, 5, 6, 6 without, the mirror of the White lists (the referee did not run the Black sorties separately). The strict sufficient form (L3_F) fails in every case, because s may walk its king off F_Z (for example Kg4–Kf4), after which no king step reaches F_Z; this does not touch the (L3) above, which holds in the bare group with 0 stalemates of s on any line on which s̄ plays only winning moves, in K24's code and in the referee's (revised after K24, 2026-10-27) | R1 items 3 and 10, R4 item 9; K7; K19; K24 |
>>>>>>> NEW

### EDIT status row 5.2 White's sorties
<<<<<<< OLD
In C, kpsolve agrees on both boards and on the 6-rank analogue (P5) | R4 item 9; K19 |
=======
In C, kpsolve agrees on both boards and on the 6-rank analogue (P5). Revised after K24, 2026-10-27: two more implementations of the local game (`kings/delegate/out/K24/scripts/lg.py`, the referee's `verify/lg2.py`) reproduce this on both boards: no T for Ke5, Kd5, Kf5 (with or without the queen clause), T = 11 with the queen clause and 10 without for Kf7, and T = 1 for Black's Kc7. That White cannot win chess either, so that the bare group is D in C, is CHECKED-2 by Lemma 2.7a (EPW and EPB computed by two implementations) and kpsolve exact. There is no hand proof of it: Lemma 2.9 refutes (L1) for a defender who may pass, and White cannot pass (open question 7) | R4 item 9; K19; K24 |
>>>>>>> NEW

### EDIT status row P5
<<<<<<< OLD
| P5 | PROVED in P (b entries, + Hp1); bare w-entry CHECKED-2 (revised after K19, 2026-10-27: the P-value D from two independent solvers, and D in C from kpsolve); kpsolve agrees on all four entries | K19 |
=======
| P5 | PROVED in P (b entries, + Hp1); bare w-entry CHECKED-2 (revised after K19 and K24, 2026-10-27: the P-value D from K19's solver and the P build of kpsolve, and from K24's `mine.c` and the referee's `psolve.py`, each written from `kings/SPEC.md`; D in C by Lemma 2.7a, with EPW and EPB both D for White to move in two implementations, and by kpsolve exact; no hand proof); kpsolve agrees on all four entries | K19; K24 |
>>>>>>> NEW

### EDIT status row P6, P7
<<<<<<< OLD
| P6, P7 | CHECKED-2 (revised after K19, 2026-10-27: P6 = (L, W) in P from two independent solvers on the cylinder, and P7 = (D, W) in P from two independent solvers on the cylinder and on the flat board; P7's w-entry is the draw that was a CONJECTURE), and partly PROVED in P. kpsolve (exact, 8×8): P6 = (L, W) on the cylinder, also confirmed by the main session's `atlas/cylinder/kpk`; P7 = (D, W) on the cylinder and the flat board, confirmed on the flat board by the Lichess tablebase | `kings/results/king_groups_8x8.txt`, `king_groups_lichess.txt` |
=======
| P6, P7 | CHECKED-2 (revised after K19 and K24, 2026-10-27), and partly PROVED in P. **In P:** P6 = (L, W) on cyl:8×8 and (L, L) on flat:8×8 (no zugzwang there); P7 = (D, W) on both boards; in P7 w, Ke5, Kd5 and Kf5 draw and Kf7 loses. The solvers are K19's, the K7 build `kings/delegate/out/K7/scripts/draft/kp_p.c` (its flag is `--pmodel`; `kings/kpsolve.c` has no such flag), K24's `kings/delegate/out/K24/scripts/mine.c`, and the K24 referee's `kings/delegate/out/K24/verify/psolve.py`, the last two written from `kings/SPEC.md`. They agree on every entry and every per-move value (`kings/delegate/out/K24/logs/pmodel_kp_p_8x8.log`, `logs/models_p_bb_bw.log`, `verify/run8.log`). K24 compared `kp_p.c` with `mine.c` on random positions with 0 differences: 11,102 legal positions (cyl:5×6, flat:5×6, cyl:6×6, cyl:7×6) and 769 legal one-pawn positions of the 8×8 boards (`logs/crossval_p.log`; the referee did not repeat these runs). The referee compared `psolve.py` with `kp_p.c` on 1,512 random positions (1,021 legal, seven board and pawn settings) with 0 differences (`verify/xval.py`, `verify/run_xval.log`). **Theorem route for P6, CHECKED-2:** (L1) for the ten sorties with T = 6, 6, 6, 7, 7 (queen clause) and 6, 6, 5, 6, 6 (L1_P) (§5.1); (L2) is vacuous, since the bare group has no context pawn (μ_s = ∞); (L3) holds in the bare group (0 stalemates of s on any line on which s̄ plays only winning moves). The strict form (L3_F) fails in every case, because s may walk its king off F_Z, so the route uses the (L3) of Definition 2.6 only. **In chess:** P6 = (L, W), CHECKED-2 by reduction to KPK: each of the five moves of the side to move is met by the other king capturing the group's pawn (legal in every case; the referee checked this), and the KPK position is won for the capturer in kpsolve exact, in K24's queen-only solver `scripts/kpk2.c` and in `atlas/cylinder/kpk` (the referee re-ran the 12 queries with the atlas binary and with its own kpsolve build). K24 also reports that `kpk2` and atlas agree on all 326,640 cylinder and 331,352 flat KPK positions (the referee checked the table sizes, not the full comparison). P7 b = W in C the same way (Kc7, then Kxe7), on both boards. P7 w = D in C: Lemma 2.7a with EPW and EPB both D for White to move (two implementations), and kpsolve exact agrees; on flat:8×8 the Lichess tablebase agrees too. No hand proof of the P7 w draw exists: Lemma 2.9 refutes (L1) for Ke5, Kd5, Kf5, but (L1) lets White pass, so that failure does not make the sorties safe (open question 7) | `kings/results/king_groups_8x8.txt`, `king_groups_lichess.txt`; K24 (`kings/delegate/out/K24/summary.json`, `logs/`, `VERIFY.md`) |
>>>>>>> NEW

### EDIT 5.1 certificate, K24 sentence
<<<<<<< OLD
K19's code reproduces both lists, so this is now CHECKED-2 (revised after K19, 2026-10-27).
=======
K19's code reproduces both lists, so this is now CHECKED-2 (revised after K19, 2026-10-27). The K24 agent's local-game code and the K24 referee's (each written from Definition 2.6) give the same lists and the same s-node counts, and K24 ran the five Black sorties directly: T = 7, 7, 6, 6, 6 for Ka3, Kb3, Kc3, Kc4, Kc5 with the queen clause and 6, 6, 5, 6, 6 without, the mirror of the White lists (revised after K24, 2026-10-27). The strict form (L3_F) fails in every case, because s may walk its king off F_Z (for example Kg4–Kf4), after which no king step reaches F_Z; the claim above rests on (L3) of Definition 2.6, which holds in the bare group (0 stalemates of s on any line on which s̄ plays only winning moves, in K24's code and the referee's).
>>>>>>> NEW

### EDIT 5.1 prediction bullet
<<<<<<< OLD
  Black sorties (White to move) Black is lost, in P and in C.
=======
  Black sorties (White to move) Black is lost, in P and in C. Revised after K24, 2026-10-27: two more P-model implementations (K24's `mine.c` and the referee's `psolve.py`) give (L, W) in P as well, and in C the value follows from the reduction to KPK, **CHECKED-2**: each of White's five moves is met by Black's king capturing on a4, and each of Black's five moves by White's king capturing on a5, and the KPK position is won for the capturer (kpsolve exact, K24's `kpk2.c`, `atlas/cylinder/kpk`). On flat:8×8 the bare group is (L, L), in P and in C (kpsolve exact and the P-model solvers); there is no zugzwang there.
>>>>>>> NEW

### EDIT 5.2 not-punished bullet, K24 sentence
<<<<<<< OLD
    so White to move draws (P5). In the analogue Kb3, Kc3 and Kd3 are not punished and Kd5 loses (T = 6).
=======
    so White to move draws (P5). In the analogue Kb3, Kc3 and Kd3 are not punished and Kd5 loses (T = 6).
  - Revised after K24, 2026-10-27: K24 and its referee find the same with two more implementations of the local game and of
    the P model: no T for Ke5, Kd5, Kf5, with or without the queen clause, on both boards; Kf7 has T = 11 with the queen
    clause and 10 without; in the analogue Kd5 has T = 6 and Kb3, Kc3, Kd3 have none. That **White cannot win chess either**
    is **CHECKED-2** by Lemma 2.7a: with every promotion a White win, White cannot win, and with every promotion a Black
    win, Black cannot win (two implementations of both models), so the chess value is D, and kpsolve exact agrees (the
    Lichess tablebase also, on the flat board). There is no hand proof of this draw. Lemma 2.9 says only that (L1) fails
    for a defender who may pass, and White cannot pass (open question 7).
>>>>>>> NEW

### EDIT 5.2 predictions bullet
<<<<<<< OLD
- **Predictions.** The bare 7.2 is (D, W), not the mutual zugzwang (L, W) (P7). The same holds for the 6-rank
=======
- **Predictions.** The bare 7.2 is (D, W), not the mutual zugzwang (L, W) (P7): CHECKED-2 in P and in C on both boards (revised after K24, 2026-10-27). The same holds for the 6-rank
>>>>>>> NEW

### EDIT section 6 row P5
<<<<<<< OLD
which is CHECKED-2 (K19, 2026-10-27: the P-value D from an own solver and from the P build of kpsolve, and D in C from kpsolve); kpsolve agrees on all four entries |
=======
which is CHECKED-2 (K19, 2026-10-27: the P-value D from an own solver and from the P build of kpsolve, and D in C from kpsolve; K24, 2026-10-27: the P-value D also from `mine.c` and the referee's `psolve.py`, and D in C by Lemma 2.7a with EPW = EPB = D for White to move, which agrees with kpsolve exact; no hand proof) (revised after K24, 2026-10-27); kpsolve agrees on all four entries |
>>>>>>> NEW

### EDIT section 6 row P6
<<<<<<< OLD
CHECKED-2 (K19, 2026-10-27: (L, W) in P from two solvers); kpsolve agrees.
=======
CHECKED-2 (K19, 2026-10-27: (L, W) in P from two solvers); kpsolve agrees. Revised after K24, 2026-10-27: K24's `mine.c` and the referee's `psolve.py` (two more implementations, written from `kings/SPEC.md`) give (L, W) in P as well, and the Theorem 2.7 route is run for all ten sorties ((L1) T = 6, 6, 6, 7, 7 with the queen clause and 6, 6, 5, 6, 6 without; (L2) vacuous; (L3) 0 stalemates). In C, (L, W) is CHECKED-2 by the reduction to KPK: every move is met by the capture of the group's pawn, and the resulting KPK is won in kpsolve exact, K24's `kpk2.c` and `atlas/cylinder/kpk`. On flat:8×8 the entry is (L, L), in P and in C.
>>>>>>> NEW

### EDIT section 6 row P7
<<<<<<< OLD
b PROVED in P; w CHECKED-2 (K19, 2026-10-27: D in P from two solvers, on both boards); kpsolve and Lichess agree |
=======
b PROVED in P; w CHECKED-2 (K19, 2026-10-27: D in P from two solvers, on both boards); kpsolve and Lichess agree. Revised after K24, 2026-10-27: the w-entry is also D in P from `mine.c` and the referee's `psolve.py`. In C the w-entry is D by Lemma 2.7a (EPW and EPB both D for White to move, two implementations) and kpsolve exact, CHECKED-2, with no hand proof (Lemma 2.9 only refutes (L1) for a passing defender; open question 7). In C the b-entry is W by the reduction to KPK (after Kc7 White's king takes e7, and `Ke7 Pd7 kc7` with Black to move is won, on both boards: kpsolve exact, `kpk2.c`, `atlas/cylinder/kpk`), CHECKED-2 |
>>>>>>> NEW

### EDIT summary row 5
<<<<<<< OLD
| §5 | 5.1 is a frozen trébuchet whose local certificate holds with T ≤ 7 (CHECKED-2, K19); 7.2 is frozen for Black only (T = 1) and White escapes by blockade; 7.3 is not a zugzwang (f7–f8=Q at once). New groups realise `on`, `off` and a stalemate trap | per item, as in the status table: 5.1 frozen PROVED, its certificate (L1) and (L3) CHECKED-2 (K19, 2026-10-27); 7.2 and 7.3 PROVED in P where stated |
=======
| §5 | 5.1 is a frozen trébuchet whose local certificate holds with T ≤ 7 (CHECKED-2, K19 and K24); 7.2 is frozen for Black only (T = 1) and White escapes by blockade; 7.3 is not a zugzwang (f7–f8=Q at once). New groups realise `on`, `off` and a stalemate trap | per item, as in the status table: 5.1 frozen PROVED, its certificate (L1) and (L3) CHECKED-2 (K19, 2026-10-27, and K24, 2026-10-27); 7.2 and 7.3 PROVED in P where stated. The bare values in chess are CHECKED-2 (revised after K24, 2026-10-27): 5.1 is (L, W) by the reduction to KPK, 7.2 is (D, W) with the w-entry by Lemma 2.7a; there is no hand proof of the 7.2 draw (open question 7) |
>>>>>>> NEW

### EDIT open question 7
<<<<<<< OLD
   `kings/delegate/out/K23/verify/`), is feasible in P.
=======
   `kings/delegate/out/K23/verify/`), is feasible in P.
7. **A hand proof that White cannot win in 7.2** (CONJECTURE; revised after K24, 2026-10-27). The w-entry of P7 is D in P and
   in C, and so is the w-entry of P5, each CHECKED-2 by computation (Lemma 2.7a for C). No proof by hand exists. Lemma 2.9
   only refutes (L1) for a defender who may pass, and White cannot pass. A proof would have to show that after Ke5, Kd5
   or Kf5 Black has no forced promotion and no forced mate against any White play (for instance by an explicit drawing
   strategy built from the blockade), and that Kf7 is the only losing sortie (T = 11 with the queen clause and 10
   without).
>>>>>>> NEW

### EDIT K24 changelog bullet
<<<<<<< OLD
  (`cc -O2 -o kp kings/kpsolve.c -lpthread`; the P build is K7's `kp_p.c`).
=======
  (`cc -O2 -o kp kings/kpsolve.c -lpthread`; the P build is K7's `kp_p.c`).
- **K24 re-computation (2026-10-27; scripts and logs in `kings/delegate/out/K24/`, the referee's code and logs in `kings/delegate/out/K24/verify/`, the
  referee's report in `kings/delegate/out/K24/VERIFY.md`).** K24 wrote no report file; the proof of Lemma 2.7a is in §2 of
  this note, and the referee's re-derivation is in VERIFY.md, section 5. New in K24 (revised after K24, 2026-10-27):
  - two further independent solvers of the promotion models, both written from `kings/SPEC.md`: `scripts/mine.c`
    (models P, EPW, EPB; it calls EPW `bb` and EPB `bw`) and the referee's `verify/psolve.py` (the same models, where
    EPW is `ww` and EPB is `bb`: the two programs use the name `bb` for different models);
  - the local game of Definition 2.6 and the (L3) and (L3_F) checks, `scripts/lg.py` and the referee's `verify/lg2.py`;
  - the reduction of P6 and P7 b to KPK: `scripts/reduction.py`, with the queen-only solver `scripts/kpk2.c`, compared by
    K24 with `atlas/cylinder/kpk` (`logs/reduction.log`);
  - Lemma 2.7a, and its application to P5 w and P7 w (`logs/models_p_bb_bw.log`).
  Results: P5, P6, P7 and §5.1, §5.2 as recorded in the status table, in those sections and in §6. No earlier number
  changed. The referee reproduced every number with code of its own and with its own builds of `kings/kpsolve.c`,
  `kp_p.c` and `atlas/cylinder/kpk`.
>>>>>>> NEW
