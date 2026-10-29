### EDIT chess bullet header: decided, not exactly two-shuttle
<<<<<<< OLD
  - *Chess. OPEN (revised after K27 and its referee, 2026-10-27).* In chess with cap 1 the bounds at the 8 roots of Z_B
    alone are (W, L): the capped promotions are met and cap 1 does not decide. Whether Z_B is exactly two-shuttle in chess
    is open, and so is every chess result beside contexts. Of the 26 deviations (the pushes and king moves of the P lists
    above):
=======
  - *Chess. DECIDED: Z_B is **not** exactly two-shuttle in chess (K28, 2026-10-28; CHECKED-2).* In chess with cap 1 the bounds at the 8 roots of Z_B
    alone are (W, L): the capped promotions are met and cap 1 does not decide. K28 solved the five open children at cap 2
    and with the capture refinement; 25 of the 26 deviations lose in chess, and **Kc3–d2 from (c3, b5) draws**. Of the 26 deviations (the pushes and king moves of the P lists
    above):
>>>>>>> NEW

### EDIT five open deviations decided
<<<<<<< OLD
    - *Five are not settled at cap 1. CHECKED-2* (kpsolve and `ownchess`, both bounds). Four have bounds (W, L):
      - the children of c4–c3 from (b2, a4) and of a3–a4 from (c3, b5) (solved by the integrator,
        `kings/delegate/out/K27/logs/integrator/`);
      - the children of the two king captures at (c3, a4), Kc3xc4 (White to move) and Ka4xa3 (Black to move), with
        3 pawns each.

      The fifth is Kc3–d2 from (c3, b5): its child `Kd2 Pa3 Pb4 kb5 pb3 pc4 b -` has bounds (D, L). So White does not
      win after it, and cap 1 cannot say whether it draws. If any of the five does not lose for the side that plays it,
      Z_B is **not** exactly two-shuttle in chess.
=======
    - *Four more lose and one draws (K28, 2026-10-28). CHECKED-2* (on the 3-pawn positions kpsolve and K28's own solver `kq3.cpp`, written from SPEC.md, agree
      at cap 2 on bounds and on every move value; for the 4-pawn row-5 child kq3 gives (D, D) and kpsolve with a per-colour cap patch the lower bound D; for the capture refinement at cap 1 the K27 referee's `ownchess.cpp` extended
      to `ownref.cpp` gives the same five values). The cap-1 bounds were (W, L) for four and (D, L) for the fifth; at cap 2
      (A = B, so exact) the values from White's view are:
      - c4–c3 from (b2, a4): child `Kb2 Pa3 Pb4 ka4 pb3 pc3 w -` is **W**; Black's push loses (White plays Kxc3 to
        `Kc3 Pa3 Pb4 ka4 pb3 b -`, exactly W);
      - a3–a4 from (c3, b5): child `Kc3 Pa4 Pb4 kb5 pb3 pc4 b -` is **L**; White's push loses (Black plays Kxa4 to
        `Kc3 Pb4 ka4 pb3 pc4 w -`, exactly L);
      - Kc3xc4 from (c3, a4): child `Kc4 Pa3 Pb4 ka4 pb3 b -` is **L**; it loses for White;
      - Ka4xa3 from (c3, a4): child `Kc3 Pb4 ka3 pb3 pc4 w -` is **W**; it loses for Black;
      - **Kc3–d2 from (c3, b5): child `Kd2 Pa3 Pb4 kb5 pb3 pc4 b -` is D, exactly** (kq3 at cap 2 gives (D, D); the restricted runs
        give B' = D with White held to one queen, in kpsolve with a per-colour cap patch and in kq3, and A' = D with Black held
        to one queen; `ownref` with the refinement gives A = B = D). Black's moves from it are Kb5–a4, a6, b6, c6 and b3–b2, all D,
        and c4–c3, which loses. So Kd2 does not lose for White.

      So 25 of the 26 deviations lose in chess and Kc3–d2 from (c3, b5) draws: Z_B is **not** exactly two-shuttle in chess.
      The mirror group follows by τ (colours and bounds exchanged), by symmetry only. Not computed: a hand proof of the drawing
      plan after Kd2 (the label stays CHECKED-2); the effect of the draw on chess contexts. Report:
      `kings/delegate/out/K28/FINDINGS.md`.
>>>>>>> NEW

### EDIT cap 2 now run
<<<<<<< OLD
    - *Cap 2 was not run.* One probe (the Kxc4 child) was stopped at its 20-minute wall limit without finishing; the timing block of its wrapper, which also covers a stopped calibration run, shows 618 CPU-s and a peak RSS of 151 MB (COMPUTED-1, not re-run). That is
      all that is known about its cost. The layer counts of the over-approximation reproduce (33,561,864 upper-bound states
      at cap 1 and 1,041,751,368 at cap 2 for that child, COMPUTED-1); any byte figure derived from them (K27 guessed
      2–3 GB for a 3-pawn child and over 20 GB for the 4-pawn children) scales the cap-1 ratio of real to counted states and
      is a CONJECTURE, not a measurement.
=======
    - *Cap 2 was run (K28, 2026-10-28; COMPUTED-1 for the costs).* kpsolve on the four 3-pawn positions behind the rows: 3,710 s, peak RSS
      1.58 GB (1,504,628,496 states; K27's guess of 2–3 GB was too high); `kq3` on the same: 402 s, 0.54 GB. The 4-pawn row-5 child: `kq3`
      1,308 s, 1.94 GB (5.59e9 slots); kpsolve with the per-colour cap patch (White held to one queen): 1,426 s, 1.88 GB. K27's estimate
      of over 20 GB for the 4-pawn children was not borne out for `kq3` (1.94 GB for the one 4-pawn child run); it was an estimate for kpsolve,
      which was not run unrestricted on a 4-pawn child at cap 2.
>>>>>>> NEW

### EDIT status paragraph in 3.2
<<<<<<< OLD
  CONJECTURE that this holds in every context. Whether Z_B is exactly two-shuttle in chess is OPEN (cap 1 gives
  the bounds (W, L); 21 of the 26 deviations lose in chess, CHECKED-2, and five are not settled: §5.7); open: chess
  (cap 2), the cylinder, other boards (§8, item 2). Z_A (§5.7) has one White break.
=======
  CONJECTURE that this holds in every context. Z_B is **not** exactly two-shuttle in chess (K28, 2026-10-28, CHECKED-2: 25 of
  the 26 deviations lose, Kc3–d2 from (c3, b5) draws: §5.7); open: chess contexts of Z_B, the cylinder, other boards (§8,
  item 2). Z_A (§5.7) has one White break.
>>>>>>> NEW

### EDIT status paragraph in section 8
<<<<<<< OLD
  equals dud_D beside every context tested, COMPUTED-1; Z_A is dud-type up to one White break. In chess Z_B is undecided
  (§5.7: 21 of the 26 deviations lose, five are not settled at cap 1), and the cylinder and other boards are open.)
=======
  equals dud_D beside every context tested, COMPUTED-1; Z_A is dud-type up to one White break. In chess Z_B is not exactly
  two-shuttle (§5.7: K28, CHECKED-2: 25 of the 26 deviations lose, Kc3–d2 from (c3, b5) draws), and the cylinder and other boards are open.)
>>>>>>> NEW

### EDIT table row P3.2' (line 89)
<<<<<<< OLD
In chess Z_B is OPEN (revised after K27 and its referee, 2026-10-27): with cap 1 the bounds at the 8 roots are (W, L); 21 of the 26 deviations lose in chess (CHECKED-2: kpsolve and the K27 referee's own chess solver); five are not settled at cap 1, four with bounds (W, L) and Kc3–d2 from (c3, b5) with bounds (D, L); if any of the five does not lose, Z_B is not two-shuttle in chess; cap 2 was not run. Open: chess (those five deviations, cap 2), the cylinder, other boards.
=======
In chess Z_B is **not** exactly two-shuttle (K28 and its referee, 2026-10-28, CHECKED-2): with cap 1 the bounds at the 8 roots are (W, L); 25 of the 26 deviations lose in chess (21 by K27, four by K28 at cap 2), and Kc3–d2 from (c3, b5) draws (child exactly D at cap 2). Open: chess contexts of Z_B, the cylinder, other boards.
>>>>>>> NEW

### EDIT section 8 item 2 (the open-chess sentence)
<<<<<<< OLD
so its negative statements are withdrawn. Open: chess (cap 1 gives bounds (W, L); 21 of the 26 deviations lose,
   CHECKED-2; five are not settled at cap 1, among them Kc3–d2 with bounds (D, L); cap 2 not run), the cylinder, other boards.)
=======
so its negative statements are withdrawn. In chess Z_B is not exactly two-shuttle (K28 and its referee, 2026-10-28, CHECKED-2: 25 of the 26
   deviations lose, Kc3–d2 from (c3, b5) draws). Open: chess contexts of Z_B, the cylinder, other boards.)
>>>>>>> NEW
