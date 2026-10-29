# K39 edits for kings/theory/LOOPY.md (2026-10-29)

Source: `kings/delegate/out/K39/findings.txt`. Every OLD block occurs exactly once in LOOPY.md as of 2026-10-29
(checked with `kings/delegate/apply_edits.py` on a scratch copy).

### EDIT P3.2′ row: chess on the cylinder and chess contexts (K39, 2026-10-29)
<<<<<<< OLD
Open: chess contexts of Z_B, chess on the cylinder (Z_B, Z_C), a hand proof on the cylinder, other boards. On the cylinder
=======
With the capture refinement at cap 1 the 8 roots of Z_B on flat 7×6 are exactly D and the same 25/1 split of the deviations follows (K39, 2026-10-29, CHECKED-2). On the cylinder in chess (K39, 2026-10-29, CHECKED-2; §5.7): Z_B on cyl:7×6 and cyl:8×6 is (D, D) at its 8 roots, 28 of its 30 deviations lose, and two draw (Kc3–d2 from (c3, b5), and the wrap move Ka4–g5, Ka4–h5 on cyl:8×6, from (b2, a4)); Z_C (cyl:8×6) is (D, D) at its 8 roots at cap 2 with one officer a side, 24 of its 32 deviations lose and 8 draw. So neither is exactly two-shuttle in chess. Beside 8 chess contexts of one pawn a side on files e–g of flat 7×6 (64 roots), the chess value of G ⊞ Z_B is exact at 60 roots and equals r(G ⊞ dud_D) at all 60; 4 roots stay undecided at cap 1 (K39, CHECKED-2 per value, COMPUTED-1 as a sample). Open: the other chess contexts of Z_B, a hand proof on the cylinder, other boards. On the cylinder
>>>>>>> NEW

### EDIT §5.7 Z_B chess: the effect of the draw on chess contexts (K39, 2026-10-29)
<<<<<<< OLD
      plan after Kd2 (the label stays CHECKED-2); the effect of the draw on chess contexts. Report:
      `kings/delegate/out/K28/FINDINGS.md`.
=======
      plan after Kd2 (the label stays CHECKED-2). Report:
      `kings/delegate/out/K28/FINDINGS.md`.
    - *The roots, and chess contexts (K39, 2026-10-29).* With the capture refinement at cap 1 (kp39 `--refine`, a kpsolve
      copy, and own39, K28's `ownref.cpp` extended; they agree on every root and move value, and on 450 random test
      positions) the 8 roots of Z_B alone are **exactly D** in chess, and the split above (25 lose, Kc3–d2 draws) is
      reproduced at cap 1: CHECKED-2. Beside contexts: 8 contexts of one pawn a side on files e–g (e2/e3, e2/e4, e2/f2,
      e2/f3, e3/e4, e4/f4, f3/f4, g4/g5; 64 roots), chess at cap 1 with the refinement, both bounds, two solvers (own39p and
      kp39p, the same values at every root and every move). At 60 roots the value is exact and **equals r(G ⊞ dud_D) and
      the P value at all 60** (0 disagreements; the outcome pairs (D, D), (L, L) and (W, L) occur, and W with White to move in a fourth context). The 4 other roots
      (Pe4 / pf4, Black to move, prediction W) stay at bounds (W, L); cap 2 there was not run (over 3 GB). Kc3–d2 from
      (c3, b5) is still exactly D beside the four contexts whose prediction is (D, D), so it changes no root value there.
      Against H alone with parked kings (Ka1, ka6) in chess, 4 of the 60 exact roots differ (Pe2 / pe4, White to move:
      parked W, Z + H D): parked kings are not dud_D in chess. CHECKED-2 for each value, COMPUTED-1 as a sample: the other
      4,413 contexts of 1–2 pawns a side on e–g were not run (about 61 days at two slots). Report:
      `kings/delegate/out/K39/findings.txt`.
>>>>>>> NEW

### EDIT §5.7 Z_B on the cylinder in chess (K39, 2026-10-29)
<<<<<<< OLD
    at cap 1 on cyl:7×6, as on the flat board (cyl:8×6 not run; K15).
=======
    at cap 1 on cyl:7×6, as on the flat board (K15), and on cyl:8×6 (K39). **Chess on the cylinder: Z_B is not exactly
    two-shuttle (K39, 2026-10-29; CHECKED-2: kp39 `--refine` and own39 with the capture refinement agree on every root and
    move value).** With the refinement at cap 1 all 8 roots are exactly D on cyl:7×6 and cyl:8×6; of the 30 deviations 28
    lose and **two draw**: Kc3–d2 from (c3, b5) (child `Kd2 kb5 Pa3 Pb4 pb3 pc4 b -` exactly D, as on the flat board) and
    the wrap move **Ka4–g5 (Ka4–h5 on cyl:8×6) from (b2, a4)** (child `Kb2 kg5 Pa3 Pb4 pb3 pc4 w -`, resp. `kh5`, exactly D;
    White's a3–a4 loses from it, every other White move draws). Both lose at once in P. Report: `kings/delegate/out/K39/findings.txt`.
>>>>>>> NEW

### EDIT §5.7 Z_C in chess (K39, 2026-10-29)
<<<<<<< OLD
In chess with cap 1 the bounds of Z_C alone are (W, L) at all 8 roots (kpsolve, COMPUTED-1), so chess is open for it.
=======
In chess with cap 1 the bounds of Z_C alone are (W, L) at all 8 roots, with or without the capture refinement (kpsolve, kp39, own39). **At cap 2 with one officer a side Z_C is (D, D) at all 8 roots, and it is not exactly two-shuttle in chess** (K39, 2026-10-29; CHECKED-2: kp39 and K39's own2, written from SPEC.md, give the same value at every root and move in the upper-bound run A′, Black held to one queen, and the lower-bound run B′, White held to one queen, so every value is exact): 24 of the 32 deviations lose and **8 draw**, Kc2–d2 and Kc3–d2 for White and the wrap moves Ka4–h5 and Ka5–h5 for Black, each against both king squares of the other side; their four children are exactly D. In P all 32 lose at once.
>>>>>>> NEW

### EDIT §5.7 Z_B conjecture: open items (K39, 2026-10-29)
<<<<<<< OLD
    families and the exhaustive families above; revised after K26, 2026-10-27). Open: a hand proof on the cylinder, chess contexts, other contexts, other boards.
=======
    families and the exhaustive families above; revised after K26, 2026-10-27). Open: a hand proof on the cylinder, chess contexts beyond the 8 one-pawn-a-side contexts of K39 (which agree with dud_D wherever cap 1 decides), other contexts, other boards.
>>>>>>> NEW

### EDIT §8 item 2: chess is not P (K39, 2026-10-29)
<<<<<<< OLD
     lose in P draw in chess (COMPUTED-1, K15), so they are not two-shuttle in chess. Z_C alone has bounds (W, L) at cap 1 (K26). Z_B on the cylinder: bounds (W, L) at
     cap 1 on cyl:7×6 (K15; cyl:8×6 not run).
=======
     lose in P draw in chess (COMPUTED-1, K15), so they are not two-shuttle in chess. Z_C alone has bounds (W, L) at cap 1 (K26); at cap 2 with one officer a
     side it is (D, D) at its 8 roots, and 8 of its 32 deviations draw (Kc2–d2, Kc3–d2, Ka4–h5, Ka5–h5), so Z_C is not two-shuttle in chess (K39, 2026-10-29,
     CHECKED-2). Z_B on the cylinder: bounds (W, L) at cap 1 on cyl:7×6 (K15) and cyl:8×6 (K39); with the capture refinement (D, D) at its 8 roots on both, and
     two of its 30 deviations draw (Kc3–d2 from (c3, b5) and the wrap move Ka4–g5, resp. Ka4–h5, from (b2, a4)), so Z_B is not two-shuttle in chess there either
     (K39, 2026-10-29, CHECKED-2; §5.7).
>>>>>>> NEW

### EDIT §8 item 2: open list (K39, 2026-10-29)
<<<<<<< OLD
     F_Z elsewhere on a flat board, kings off the group files, officers, chess (contexts of Z_B, Z_C; the cylinder groups beyond G8a, G8b), hand proofs on the
=======
     F_Z elsewhere on a flat board, kings off the group files, officers, chess (contexts of Z_B beyond K39's 8 flat-board contexts, contexts of Z_C, the cylinder groups beyond G8a, G8b, Z_B and Z_C), hand proofs on the
>>>>>>> NEW

### EDIT §8 item 2: closing paragraph (K39, 2026-10-29)
<<<<<<< OLD
   deviations lose, Kc3–d2 from (c3, b5) draws). Open: chess contexts of Z_B, chess on the cylinder (Z_B, Z_C), other boards.)
=======
   deviations lose, Kc3–d2 from (c3, b5) draws). On the cylinder in chess neither Z_B nor Z_C is exactly two-shuttle (K39, 2026-10-29, CHECKED-2), and
   beside 8 small flat chess contexts Z_B agrees with dud_D wherever cap 1 decides (60 of 64 roots; K39). Open: the other chess contexts of Z_B, other boards.)
>>>>>>> NEW
