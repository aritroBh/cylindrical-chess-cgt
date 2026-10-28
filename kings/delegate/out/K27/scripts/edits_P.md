### EDIT status-line Z_B proved
<<<<<<< OLD
exists in P on the flat 7×6 board: Z_B of §5.7 has every non-shuttle move losing at once at all 8 roots (CHECKED-2),
=======
exists in P on the flat 7×6 board: Z_B of §5.7 has every non-shuttle move losing at once at all 8 roots (PROVED by hand, K27; also CHECKED-2),
>>>>>>> NEW

### EDIT Z_B geometry plus mirror
<<<<<<< OLD
Ka3, Kb2 / kb5, kc4 / Pb4 Pc3 pa4 pb3. Roots are written like `Kb2 ka4 Pa3 Pb4 pb3 pc4 w -`.
=======
Ka3, Kb2 / kb5, kc4 / Pb4 Pc3 pa4 pb3. Roots are written like `Kb2 ka4 Pa3 Pb4 pb3 pc4 w -`. (K27: this mirror is also the image of Z_B under τ = "flip the ranks r → 7 − r, swap the colours, swap the side to move", which **is** a symmetry of the P model and of chess on the flat 7×6 board, unlike the file reflection a ↔ c taken alone. So every statement proved or computed for Z_B holds for the mirror with the colours exchanged: PROVED by symmetry; `tau_check.py` confirms that τ maps the 8 roots onto the 8 roots of the mirror and the legal-move sets correspond on 22,818 positions.)
>>>>>>> NEW

### EDIT Z_B alone proved by hand
<<<<<<< OLD
mover; the shuttle draws). So (Pun) holds for Z_B alone at all 8 roots, in both colours. **CHECKED-2:**
=======
mover; the shuttle draws). So (Pun) holds for Z_B alone at all 8 roots, in both colours. **PROVED (K27,
    `kings/delegate/out/K27/PROOF.md`):** the shuttle step is legal and safe in both directions at all 8 roots (K1, K2), and each
    of the 26 non-shuttle moves (15 White, 11 Black; the figure 27 sometimes quoted is a miscount) has an explicit winning
    strategy for the opponent, a certificate of at most 37 entries (286 entries in all) in which every legal reply is listed with the reason
    that the others are illegal, winning within at most 11 plies after the move. Neither side can win against a player who
    shuttles until the other deviates, so Z_B alone is exactly two-shuttle in P. No en passant ever arises (no pawn stands on
    its second rank). Also **CHECKED-2:**
>>>>>>> NEW

### EDIT geometry bullet pointer
<<<<<<< OLD
  - *Geometry. PROVED by enumeration.* (K1): pb3 attacks a2, c2; pc4 attacks b3, d3; Pa3 attacks b4; Pb4 attacks a5, c5;
=======
  - *Geometry. PROVED by enumeration (and written out with the shuttle lemma in K27's PROOF.md, section 3).* (K1): pb3 attacks a2, c2; pc4 attacks b3, d3; Pa3 attacks b4; Pb4 attacks a5, c5;
>>>>>>> NEW

### EDIT chess bullet for Z_B
<<<<<<< OLD
  - *Chess. Undecided.* In chess with cap 1 the bounds at the 8 roots of Z_B alone are (W, L): the capped promotions are
    met and cap 1 does not decide. Whether Z_B is exactly two-shuttle in chess is open (cap 2 not run, memory), and so is
    every chess result beside contexts.
=======
  - *Chess. Undecided (K27: 6 of the 26 deviations settled).* In chess with cap 1 the bounds at the 8 roots of Z_B alone are (W, L): the capped promotions are
    met and cap 1 does not decide. K27 (kpsolve only, COMPUTED-1): the child after the deviation is a win for the opponent in chess, because the
    opponent can capture the pushed pawn and the resulting position is exact at cap 1 (A = B), for six pawn pushes: b4–b5 from (b2, a4)
    and from (c3, a4) (Black wins), a3–a4 from (b2, b5) (Black wins), c4–c3 from (b2, b5) and b3–b2 from (c3, a4) and from (c3, b5) (White wins).
    Not settled at cap 1 (bounds (W, L)): c4–c3 from (b2, a4) and a3–a4 from (c3, b5) (via the capture position), and the children after Kc3xc4 and after Ka4xa3 (3 pawns).
    The other 16 deviations (king moves of 4-pawn positions) were not computed: a cap-1 batch did not obtain a slot under `heavy.sh`. Cap 2 was not run: the one-position probe (the Kxc4 child) did not finish in
    20 minutes (618 CPU-s, peak RSS 151 MB), and a layer count extrapolates cap 2 to about 2–3 GB for a 3-pawn child and over 20 GB for the 4-pawn children.
    The P certificates do not transfer to chess: a promotion that the P model counts as a win can be captured at once (1.Kd2 b2 2.Kc2). So whether Z_B is exactly two-shuttle in chess is open (CONJECTURE that it is),
    and so is every chess result beside contexts.
>>>>>>> NEW

### EDIT open items: item 2 label
<<<<<<< OLD
   need wider searches. (After K14 and its referee, 2026-10-27: on the flat 7×6 board Z_B of §5.7 has every non-shuttle
   move losing at once in P, CHECKED-2; a search of flat 7×6 (F_Z = {a, b, c}, ≤ 2 + 2 pawns, no cut-off) found exactly
=======
   need wider searches. (After K14 and its referee, 2026-10-27, and K27: on the flat 7×6 board Z_B of §5.7 has every non-shuttle
   move losing at once in P, PROVED by hand (K27) and CHECKED-2; a search of flat 7×6 (F_Z = {a, b, c}, ≤ 2 + 2 pawns, no cut-off) found exactly
>>>>>>> NEW
