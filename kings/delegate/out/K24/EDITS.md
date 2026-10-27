### EDIT status row P6, P7
<<<<<<< OLD
| P6, P7 | CONJECTURE, and partly PROVED in P. kpsolve (exact, 8×8): P6 = (L, W) on the cylinder, also confirmed by the main session's `atlas/cylinder/kpk`; P7 = (D, W) on the cylinder and the flat board, confirmed on the flat board by the Lichess tablebase | `kings/results/king_groups_8x8.txt`, `king_groups_lichess.txt` |
=======
| P6, P7 | Closed by K24 (2026-10-27) by finite computation; the draw in P7 w has no hand proof. **P model (free kings, first promotion wins), CHECKED-2:** `kpsolve --pmodel` and an independent solver give the same value after every move; the two agree on 11,102 random legal positions (cyl:5×6, flat:5×6, cyl:6×6, cyl:7×6) and on 769 legal one-pawn positions of the 8×8 boards. P6 = (L, W) on cyl:8×8 (on flat:8×8 it is (L, L): no zugzwang); P7 = (D, W) on cyl:8×8 and flat:8×8; in P7 w, Ke5, Kd5 and Kf5 draw and Kf7 loses. **Theorem route for P6, CHECKED-2:** (L1) holds for all five White sorties and, by duality, all five Black sorties, with T = 6, 6, 6, 7, 7 (queen clause) and 6, 6, 5, 6, 6 (L1_P) for Kg4, Kg5, Kg6, Kh6, Ka6: the lists K7 recorded, now from a third implementation; (L2) holds trivially, since the bare group has no context pawn (μ_s = ∞); (L3) holds in the bare group: s is never stalemated on any line on which s̄ plays only winning moves (the strict context-free sufficient form (L3_F) fails in every case, see §4 of the K24 report). **Chess:** P6 = (L, W), CHECKED-2: every move of the side to move is met by the king capture of the group's pawn and the resulting KPK is won in the exact KQK + KPK tables, which agree with `atlas/cylinder/kpk.c` on all 326,640 cylinder and 331,352 flat positions; kpsolve exact agrees. P7 b = W the same way, on both boards. P7 w = D, CHECKED-2: by the transfer lemma of the K24 report (PROVED: if White cannot force a win when every promotion is a White win, White cannot win chess, and the mirror), with both models computed, and kpsolve exact; flat also by Lichess. **What had been CONJECTURE, and why:** P6: (L1) rested on scratch scripts and (L3) was never checked; (L2) is vacuous. The remark "in the bare position the local game is the whole game" is wrong (s has unlimited passes there and s̄'s king is confined), the local game is only a sufficient condition. P7 w: Lemma 2.9 and Proposition 2.10(a) say nothing about a draw. Lemma 2.9 refutes (L1) for Ke5, Kd5, Kf5, but (L1) lets White pass, so its failure does not make the sortie safe, and nothing in the note addressed "White cannot win". | `kings/results/king_groups_8x8.txt`, `king_groups_lichess.txt`, `kings/delegate/out/K24/REPORT.md` |
>>>>>>> NEW

### EDIT section 6 row P6
<<<<<<< OLD
| P6 | cyl:8x8 | 5.1 `Kh5 Pa4 kb4 pa5` | (L, W): a real mutual zugzwang | (L, W) | (L, W) (kpsolve, exact) | Thm 2.4 + Thm 2.7 ((L1) scratch, T ≤ 7) + self-duality | CONJECTURE; kpsolve agrees |
=======
| P6 | cyl:8x8 | 5.1 `Kh5 Pa4 kb4 pa5` | (L, W): a real mutual zugzwang | (L, W) | (L, W) (kpsolve, exact) | Thm 2.7 for each of the ten sorties: (L1) T = 6, 6, 6, 7, 7 with the queen clause, 6, 6, 5, 6, 6 without; (L2) vacuous; (L3) no stalemate (K24); self-duality (PROVED); the same value from the P-model solvers and by reduction to KPK in chess | P and C: CHECKED-2 (L, W) (K24); kpsolve agrees; flat:8×8 is (L, L) |
>>>>>>> NEW

### EDIT section 6 row P7
<<<<<<< OLD
| P7 | cyl:8x8 and flat:8x8 | 7.2 group `Ke6 Pd7 kd8 pe7` | (D, W) | (L, W) | (D, W) on both boards (kpsolve; Lichess on flat) | Prop 2.10(a) for Black; Lemma 2.9 for White | b PROVED in P; w CONJECTURE; kpsolve and Lichess agree |
=======
| P7 | cyl:8x8 and flat:8x8 | 7.2 group `Ke6 Pd7 kd8 pe7` | (D, W) | (L, W) | (D, W) on both boards (kpsolve; Lichess on flat) | Prop 2.10(a) for Black ((L1) T = 1, (L2) vacuous, (L3): Black has Kb6, Kb7, Kb8, Kc6); for White no certificate can give a draw (Lemma 2.9 only refutes (L1)), so w rests on the P-model computation and the transfer lemma (K24) | P: b PROVED, w CHECKED-2 (computation, no hand proof); C: b CHECKED-2 (KPK reduction), w CHECKED-2 (transfer lemma + kpsolve); Lichess agrees on flat |
>>>>>>> NEW

### EDIT status row P5
<<<<<<< OLD
| P5 | PROVED in P (b entries, + Hp1); bare w-entry CONJECTURE; kpsolve agrees on all four entries | — |
=======
| P5 | PROVED in P (b entries, + Hp1); bare w-entry CHECKED-2 by K24 (the P-model value (D) from two solvers; chess D by the transfer lemma and kpsolve exact; no hand proof); kpsolve agrees on all four entries | — |
>>>>>>> NEW

### EDIT section 6 row P5
<<<<<<< OLD
| P5 | cyl:7x6 | Z_72 `Kc4 Pb5 kb6 pc5`, bare; and + Hp1 | bare (D, W); + Hp1 (W, W) | bare (L, W); (W, W) | bare (D, W); + Hp1 (W, W) | Black side: Prop 2.10(a) with T = 1 (PROVED in P). White side: Lemma 2.9 (escape by blockade) | all entries PROVED in P except the bare w-entry, which is a CONJECTURE (scratch: no forced promotion); kpsolve agrees on all four entries |
=======
| P5 | cyl:7x6 | Z_72 `Kc4 Pb5 kb6 pc5`, bare; and + Hp1 | bare (D, W); + Hp1 (W, W) | bare (L, W); (W, W) | bare (D, W); + Hp1 (W, W) | Black side: Prop 2.10(a) with T = 1 (PROVED in P). White side: Lemma 2.9 (escape by blockade) | all entries PROVED in P except the bare w-entry, which is CHECKED-2 (K24: the P-model value D from two solvers, a computation with no hand proof; chess D by the transfer lemma and kpsolve exact); kpsolve agrees on all four entries |
>>>>>>> NEW

### EDIT status row 5.1 (L1)
<<<<<<< OLD
| §5.1, (L1) | CONJECTURE (scratch, k ≤ 4 and k = ∞ only; (L3) not checked). The k = ∞ case was re-run in K7 against the local game of Definition 2.6 ((L1_P): T = 5 to 6; (L1) with the queen clause: T = 6 to 7), same label (revised after K7, 2026-10-22) | R1 items 3 and 10, R4 item 9; K7 |
=======
| §5.1, (L1) | CHECKED-2 for the bare group (K24, 2026-10-27): the k = ∞ local game of Definition 2.6 on all ten sorties gives T = 6, 6, 6, 7, 7 (queen clause) and 6, 6, 5, 6, 6 (L1_P), the lists K7 recorded, from a third implementation. (L3) holds in the bare group (no stalemate of s on a winning line); in a context it is context-dependent, and the strict context-free form (L3_F) fails. The context claim ("valid in every context with (L2) at μ ≥ 8 and (L3)") is Theorem 2.7 and is untouched; the older scratch result for k ≤ 4 is not repeated (revised after K24) | R1 items 3 and 10, R4 item 9; K7; K24 |
>>>>>>> NEW

### EDIT 5.1 prediction bullet
<<<<<<< OLD
- **Prediction.** The bare 5.1 is a real mutual zugzwang, (L, W) (P6 in §6). In the bare position the local
  game is the whole game, so the scratch run is a full P-model computation. It is still one throwaway
  implementation, hence a CONJECTURE.
=======
- **Prediction.** The bare 5.1 is a real mutual zugzwang, (L, W) (P6 in §6). **CHECKED-2** (K24, 2026-10-27): the P-model value is (L, W) in two independent solvers, and the chess value is (L, W) by the reduction to KPK and in kpsolve. The earlier remark that in the bare position the local game is the whole game was wrong: the local game gives s unlimited passes and confines s̄'s king, so it is only a sufficient condition, and the P-model value had to be computed on its own. The Black sorties have the same T lists, as self-duality predicts.
>>>>>>> NEW

### EDIT 5.2 not-punished bullet
<<<<<<< OLD
  - That the three sorties are *not punished* in P (no forced promotion for Black) rests on scratch evidence
    only, and is a CONJECTURE (revised after review: R4 item 9, R1 item 11): even without passes, Black cannot
    force promotion after Kd5, Ke5 or Kf5. Only Kf7 loses, in 10 moves. In chess, kpsolve gives (D, W) for the
    6-rank analogue Z_72 bare, so White to move draws (P5).
=======
  - That the three sorties are *not punished* in P (no forced promotion for Black), and that White cannot win either, is **CHECKED-2** (K24, 2026-10-27): two independent P-model solvers give (D, W) for the bare group on cyl:8×8 and flat:8×8, with Ke5, Kd5 and Kf5 drawing and Kf7 losing (local game: T = 11 with the queen clause, 10 without). This is a computation, not a proof; Lemma 2.9 cannot give it, because (L1) lets White pass. In chess the value D follows from the transfer lemma of the K24 report and agrees with kpsolve exact (and with Lichess on the flat board); the 6-rank analogue Z_72 bare is (D, W) in the same way (P5).
>>>>>>> NEW

