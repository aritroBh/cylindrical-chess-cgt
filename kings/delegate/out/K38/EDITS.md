# EDITS for kings/theory/LOOPY.md (K38). Each OLD occurs exactly once in the LOOPY.md of 2026-10-29; `kings/delegate/apply_edits.py kings/theory/LOOPY.md <copy> kings/delegate/out/K38/EDITS.md` checks it.

### EDIT status row P5: bare w-entry has a hand proof
<<<<<<< OLD
| P5 | PROVED in P (b entries, + Hp1); bare w-entry CHECKED-2 (revised after K19 and K24, 2026-10-27: the P-value D from K19's solver and `kp_p --pmodel` (K7's P-model build of kpsolve), and from K24's `mine.c` and the referee's `psolve.py`, each written from `kings/SPEC.md`; D in C by Lemma 2.7a, with EPW and EPB both D for White to move in two implementations, and by kpsolve exact; no hand proof); kpsolve agrees on all four entries | K19; K24 |
=======
| P5 | PROVED in P (b entries, + Hp1). Bare w-entry: PROVED by hand, in P and in C directly (new, K38, 2026-10-29; `kings/delegate/out/K38/PROOF.md`; not yet re-derived by a referee), on cyl:7x6 and flat:7x6. It is K30's proof for 7.2 moved two files left and two ranks down: after any of White's four moves Black plays ...Kxb5; after Kb3, Kc3 or Kd3 White follows the blockade rule of Lemma D with an invariant of 296 positions per board (checked by an own move generator, all Black moves, 0 failures), and ...Ka5 is met by Kc4, ...c4 and ...c3 by taking the pawn; Kd5 loses in P (...c3 at once, T = 6). The earlier evidence agrees (revised after K19 and K24, 2026-10-27: the P-value D from K19's solver and `kp_p --pmodel` (K7's P-model build of kpsolve), and from K24's `mine.c` and the referee's `psolve.py`, each written from `kings/SPEC.md`; D in C by Lemma 2.7a, with EPW and EPB both D for White to move in two implementations, and by kpsolve exact; K38: the own solver, `kp_p --pmodel` and `ref3` agree in P on all 27,688 (cyl) and 28,373 (flat) positions reachable from the group, and kpsolve cap 2 exact gives D in C on both boards); kpsolve agrees on all four entries | K19; K24; K38 |
>>>>>>> NEW

### EDIT status row L2.7a: P5 w no longer needs the lemma
<<<<<<< OLD
The values it is applied to (P5 w, P7 w) are CHECKED-2 (revised after K30, 2026-10-27: the P7 w value is also PROVED by hand directly in chess, so for P7 w the lemma is not needed) | K24; `kings/delegate/out/K24/VERIFY.md` |
=======
The values it is applied to (P5 w, P7 w) are CHECKED-2 (revised after K30, 2026-10-27: the P7 w value is also PROVED by hand directly in chess, so for P7 w the lemma is not needed; revised after K38, 2026-10-29: the same holds for P5 w, `kings/delegate/out/K38/PROOF.md`, not yet re-derived by a referee) | K24; `kings/delegate/out/K24/VERIFY.md` |
>>>>>>> NEW

### EDIT Lemma 2.7a application: P5 w route to chess
<<<<<<< OLD
for P5 w this application is still the route to chess.)
=======
for P5 w the same holds since K38, 2026-10-29, `kings/delegate/out/K38/PROOF.md`, not yet re-derived by a referee, so the lemma is now an agreeing check for both.)
>>>>>>> NEW

### EDIT section 5.2 predictions: P5
<<<<<<< OLD
  analogue (P5), CHECKED-2 (K30's proof does not cover it).
=======
  analogue (P5): the w-entry D is PROVED by hand in P and in C on cyl:7x6 and flat:7x6 (new, K38, 2026-10-29; `kings/delegate/out/K38/PROOF.md`, K30's proof translated by two files and two ranks, with an invariant of 296 positions per board; not yet re-derived by a referee); the b-entry as for 7.2.
>>>>>>> NEW

### EDIT section 6 row P5
<<<<<<< OLD
| all entries PROVED in P except the bare w-entry, which is CHECKED-2 (K19, 2026-10-27: the P-value D from an own solver and from `kp_p --pmodel` (K7's P-model build of kpsolve), and D in C from kpsolve; K24, 2026-10-27: the P-value D also from `mine.c` and the referee's `psolve.py`, and D in C by Lemma 2.7a with EPW = EPB = D for White to move, which agrees with kpsolve exact; no hand proof) (revised after K24, 2026-10-27); kpsolve agrees on all four entries |
=======
| all entries PROVED in P; the bare w-entry D is PROVED by hand in P and in C (new, K38, 2026-10-29; `kings/delegate/out/K38/PROOF.md`; not yet re-derived by a referee; White cannot win because ...Kxb5 follows every White move, and after Kb3, Kc3, Kd3 White holds by the blockade rule of Lemma D, invariant 296 positions per board, checked by an own move generator; Kd5 loses, T = 6). Earlier evidence, which agrees: K19, 2026-10-27: the P-value D from an own solver and from `kp_p --pmodel` (K7's P-model build of kpsolve), and D in C from kpsolve; K24, 2026-10-27: the P-value D also from `mine.c` and the referee's `psolve.py`, and D in C by Lemma 2.7a with EPW = EPB = D for White to move, which agrees with kpsolve exact (revised after K24, 2026-10-27); K38: kpsolve cap 2 exact D in C, and three implementations agree in P on every position reachable from the group; kpsolve agrees on all four entries |
>>>>>>> NEW

### EDIT section 8 item 7: P5 done
<<<<<<< OLD
7. **A hand proof that White cannot win in 7.2** (PROVED for 7.2, new, K30, 2026-10-27; re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`; still open for P5). The w-entry of P7 is D in P and
=======
7. **A hand proof that White cannot win in 7.2** (PROVED for 7.2, new, K30, 2026-10-27; re-derived by the K30 referee, `kings/delegate/out/K30/VERIFY.md`; PROVED for P5, new, K38, 2026-10-29, `kings/delegate/out/K38/PROOF.md`, not yet re-derived by a referee). The w-entry of P7 is D in P and
>>>>>>> NEW

### EDIT section 8 item 7: what is still open
<<<<<<< OLD
Kf7 loses in P (...e5 and the pawn runs). Still open: the same proof for the 6-rank analogue P5 (the method should carry over; nothing was run), and for other board sizes.
=======
Kf7 loses in P (...e5 and the pawn runs). For the 6-rank analogue P5 (`Kc4 Pb5 kb6 pc5`) the same proof, moved two files left and two ranks down, gives D in P and in C on cyl:7x6 and flat:7x6 (K38): ...Kxb5 after every White move; after Kb3, Kc3, Kd3 the blockade rule with an invariant of 296 positions per board (the pawn ranks are 5..2 instead of 7..2), checked by an own move generator; ...Ka5 is met by Kc4; Kd5 loses in P with ...c3 at once (T = 6). Only Lemma K needed a change on flat:7x6 (a corner must be allowed, since the pawns b5 and c5 stand next to squares beside the corner a6); nothing broke. Still open: other board sizes.
>>>>>>> NEW
