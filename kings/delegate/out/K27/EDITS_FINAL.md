### EDIT status row P3.2' Z_B alone
<<<<<<< OLD
and Z_B alone is (D, D) at all 8 roots in P: CHECKED-2 (kp_p and the independent solver ref3). Beside every context tested
=======
and Z_B alone is exactly two-shuttle in P, (D, D) at all 8 roots, every one of the 26 non-shuttle moves losing by force: PROVED by hand (revised after K27 and its referee, 2026-10-27; `kings/delegate/out/K27/PROOF.md`, 26 certificates), CHECKED-3 for the computations (kp_p, ref3, K27's pm.py, the K27 referee's own solver). Beside every context tested
>>>>>>> NEW

### EDIT status row P3.2' chess
<<<<<<< OLD
In chess with cap 1 the bounds at the 8 roots are (W, L): undecided. Open: chess (cap 2), the cylinder, other boards. Z_A (§5.7) is a second group
=======
In chess Z_B is OPEN (revised after K27 and its referee, 2026-10-27): with cap 1 the bounds at the 8 roots are (W, L); six of the 26 deviations lose in chess (CHECKED-2: kpsolve and the referee's own chess solver); of the other 20, four give only bounds (W, L) at cap 1 and 16 were not computed; cap 2 was not run. Open: chess (those 20 deviations, cap 2), the cylinder, other boards. Z_A (§5.7) is a second group
>>>>>>> NEW

### EDIT status row P3.2' sources
<<<<<<< OLD
| R4 item 6; K14 and its referee |
=======
| R4 item 6; K14 and its referee; K27 and its referee |
>>>>>>> NEW

### EDIT section 3 paragraph on Z_B
<<<<<<< OLD
  exists in P on the flat 7×6 board: Z_B of §5.7 has every non-shuttle move losing at once at all 8 roots (CHECKED-2),
  and beside every context tested its P-result equals r(G ⊞ dud_D) (COMPUTED-1; 225 of 885 contexts untested);
  CONJECTURE that this holds in every context. Whether Z_B is exactly two-shuttle in chess is undecided (cap 1 gives
  the bounds (W, L)); open: chess (cap 2), the cylinder, other boards (§8, item 2). Z_A (§5.7) has one White break.
=======
  exists in P on the flat 7×6 board: Z_B of §5.7 has every non-shuttle move losing at once at all 8 roots (PROVED by
  hand, revised after K27 and its referee, 2026-10-27; CHECKED-3 for the computations),
  and beside every context tested its P-result equals r(G ⊞ dud_D) (COMPUTED-1; 225 of 885 contexts untested);
  CONJECTURE that this holds in every context. Whether Z_B is exactly two-shuttle in chess is OPEN (cap 1 gives
  the bounds (W, L); six of the 26 deviations lose in chess, CHECKED-2, the rest are not decided: §5.7); open: chess
  (cap 2), the cylinder, other boards (§8, item 2). Z_A (§5.7) has one White break.
>>>>>>> NEW

### EDIT 5.3 Z_B pointer
<<<<<<< OLD
  this type exists elsewhere on the flat 7×6 board: Z_B of §5.7 (every non-shuttle move loses at once in P, CHECKED-2),
=======
  this type exists elsewhere on the flat 7×6 board: Z_B of §5.7 (every non-shuttle move loses at once in P, PROVED by hand,
  revised after K27, 2026-10-27),
>>>>>>> NEW

### EDIT 5.7 Z_B bullet header
<<<<<<< OLD
- **An exactly frozen two-shuttle group: Z_B (revised after the K14 referee, 2026-10-27). Z_B alone: CHECKED-2 in P; the
  search and the contexts: COMPUTED-1.**
=======
- **An exactly frozen two-shuttle group: Z_B (revised after the K14 referee and after K27 and its referee, 2026-10-27).
  Z_B alone: PROVED in P (K27's hand proof), CHECKED-3 for the computations; the search and the contexts: COMPUTED-1.**
>>>>>>> NEW

### EDIT 5.7 Z_B mirror and tau
<<<<<<< OLD
  - **Z_B:** White king b2, c3 (shuttle), Black king a4, b5 (shuttle), pawns Pa3 Pb4 pb3 pc4. Its mirror (a ↔ c) is
    Ka3, Kb2 / kb5, kc4 / Pb4 Pc3 pa4 pb3. Roots are written like `Kb2 ka4 Pa3 Pb4 pb3 pc4 w -`.
=======
  - **Z_B:** White king b2, c3 (shuttle), Black king a4, b5 (shuttle), pawns Pa3 Pb4 pb3 pc4. Its mirror is
    Ka3, Kb2 / kb5, kc4 / Pb4 Pc3 pa4 pb3 (the file image a ↔ c of Z_B as a set of positions). Roots are written like
    `Kb2 ka4 Pa3 Pb4 pb3 pc4 w -`.
    - *The mirror group (revised after K27 and its referee, 2026-10-27). PROVED by symmetry; the check is CHECKED-2.* The
      mirror is also the image of Z_B under τ = "flip the ranks r → 7 − r, swap the colours, swap the side to move".
      τ **is** a symmetry of the P model and of chess on the flat 7×6 board (pawn directions, promotion ranks 6 ↔ 1, and
      double-step ranks 2 ↔ 5 map to each other), unlike the file reflection a ↔ c taken alone (file a is an edge, file c
      is not). So every statement proved for Z_B holds for the mirror with the colours exchanged: the mirror is exactly
      two-shuttle in P too. Checks: K27's `tau_check.py` (the 8 roots map onto the 8 roots of the mirror, and the legal
      moves correspond on 22,818 positions) and the referee's own solver (`kings/delegate/out/K27/verify/own.cpp`: τ maps
      the value and the distance to promotion of each of the 649,994 positions reachable from the 16 roots onto those of its
      image, 0 mismatches). In chess with the promotion cap τ exchanges the two bounds, so a chess statement for the mirror
      carries over with the bounds swapped; none is claimed here.
>>>>>>> NEW

### EDIT 5.7 Z_B geometry pointer
<<<<<<< OLD
  - *Geometry. PROVED by enumeration.* (K1): pb3 attacks a2, c2; pc4 attacks b3, d3; Pa3 attacks b4; Pb4 attacks a5, c5;
=======
  - *Geometry. PROVED by enumeration (K1; written out with the shuttle lemma in `kings/delegate/out/K27/PROOF.md`, section 3, and re-derived by the K27 referee).* (K1): pb3 attacks a2, c2; pc4 attacks b3, d3; Pa3 attacks b4; Pb4 attacks a5, c5;
>>>>>>> NEW

### EDIT 5.7 Z_B alone proved by hand
<<<<<<< OLD
    mover; the shuttle draws). So (Pun) holds for Z_B alone at all 8 roots, in both colours. **CHECKED-2:**
    the referee's build of kp_p (the K7 P-model solver) and the K23 referee's solver ref3
    (`kings/delegate/out/K23/verify/ref3.cpp`, which shares no code with kpsolve or kp_p; for flat boards pass
    `--board flat7x6`, a parsing quirk) give the same 8 root values and the same move lists, as re-run by the integrator.
=======
    mover; the shuttle draws). So (Pun) holds for Z_B alone at all 8 roots, in both colours. **PROVED** (new, K27;
    revised after the K27 referee, 2026-10-27; hand proof in `kings/delegate/out/K27/PROOF.md`, summary in
    `kings/delegate/out/K27/summary.json`, report in `kings/delegate/out/K27/REPORT.md`, referee report in
    `kings/delegate/out/K27/VERIFY.md`): the shuttle step is legal and safe in both directions at all 8 roots (K1, K2),
    and each of the 26 non-shuttle moves (15 White, 11 Black) has an explicit winning strategy for the opponent: a
    certificate of at most 37 entries (286 in all) in which every legal reply is listed with the reason that the others
    are illegal, winning within at most 11 plies after the move. A player who shuttles until the other deviates never
    loses, and both shuttling forever is a draw, so Z_B alone is exactly two-shuttle in P. No en passant ever arises (no
    pawn stands on its second rank). The referee re-checked the text of all 26 certificates with its own move generator
    (0 problems, and the check fails on five deliberate corruptions of the text). **CHECKED-3 (for the computations):**
    the referee's build of kp_p (the K7 P-model solver), the K23 referee's solver ref3
    (`kings/delegate/out/K23/verify/ref3.cpp`, which shares no code with kpsolve or kp_p; for flat boards pass
    `--board flat7x6`, a parsing quirk), K27's own `scripts/pm.py` and the K27 referee's own solver
    (`kings/delegate/out/K27/verify/own.cpp`) give the same 8 root values and the same move lists (16 roots with the
    mirror), and the referee's solver gives the same distance, at most 11 plies, after each of the 26 deviations.
>>>>>>> NEW

### EDIT 5.7 Z_B chess open
<<<<<<< OLD
  - *Chess. Undecided.* In chess with cap 1 the bounds at the 8 roots of Z_B alone are (W, L): the capped promotions are
    met and cap 1 does not decide. Whether Z_B is exactly two-shuttle in chess is open (cap 2 not run, memory), and so is
    every chess result beside contexts.
=======
  - *Chess. OPEN (revised after K27 and its referee, 2026-10-27).* In chess with cap 1 the bounds at the 8 roots of Z_B
    alone are (W, L): the capped promotions are met and cap 1 does not decide. Whether Z_B is exactly two-shuttle in chess
    is open, and so is every chess result beside contexts. Of the 26 deviations (the pushes and king moves of the P lists
    above):
    - *Six lose in chess. CHECKED-2* (kpsolve at cap 1, and the referee's own chess solver `ownchess.cpp`, which agrees with
      kpsolve on 76 small test positions, 0 differences). After the push the opponent can capture the pushed pawn, and the
      position after that capture is exact at cap 1 (A = B), so the push loses: b4–b5 from (b2, a4) and from (c3, a4) and
      a3–a4 from (b2, b5) lose for White; c4–c3 from (b2, b5) and b3–b2 from (c3, a4) and from (c3, b5) lose for Black.
    - *Four are not settled at cap 1.* The positions after the captures that follow c4–c3 from (b2, a4) and a3–a4 from
      (c3, b5) have bounds (W, L) (kpsolve only, COMPUTED-1); the children of these two deviations themselves were not
      computed. The children after Kc3xc4 and after Ka4xa3 (3 pawns each) have bounds (W, L) (CHECKED-2, kpsolve and
      `ownchess`).
    - *Sixteen were not computed* (the king moves of 4-pawn positions): a cap-1 batch did not obtain a slot under `heavy.sh`.
      So the deviations that decide whether Z_B is two-shuttle in chess are mostly untested.
    - *Cap 2 was not run.* One probe (the Kxc4 child) did not finish in 20 minutes (618 CPU-s, peak RSS 151 MB), which is
      all that is known about its cost. The layer counts of the over-approximation reproduce (33,561,864 upper-bound states
      at cap 1 and 1,041,751,368 at cap 2 for that child, COMPUTED-1); any byte figure derived from them (K27 guessed
      2–3 GB for a 3-pawn child and over 20 GB for the 4-pawn children) scales the cap-1 ratio of real to counted states and
      is a CONJECTURE, not a measurement.
    - *The P certificates do not transfer to chess.* In 22 of the 26 certificates some promotion can be answered by an
      immediate capture of the new piece (the referee's count; for example, in 1.Ka1 c3 2.Kb1 b2 3.Ka2 the P certificate
      promotes, but b1=Q is met by Kxb1). So chess may differ from P, and the P result is no evidence either way for the
      16 king-move deviations.
>>>>>>> NEW

### EDIT 8 item 2 label
<<<<<<< OLD
   need wider searches. (After K14 and its referee, 2026-10-27: on the flat 7×6 board Z_B of §5.7 has every non-shuttle
   move losing at once in P, CHECKED-2; a search of flat 7×6 (F_Z = {a, b, c}, ≤ 2 + 2 pawns, no cut-off) found exactly
=======
   need wider searches. (After K14 and its referee, and after K27 and its referee, 2026-10-27: on the flat 7×6 board Z_B
   of §5.7 has every non-shuttle move losing at once in P, PROVED by hand (K27), CHECKED-3 for the computations; a search
   of flat 7×6 (F_Z = {a, b, c}, ≤ 2 + 2 pawns, no cut-off) found exactly
>>>>>>> NEW

### EDIT 8 item 2 open list
<<<<<<< OLD
so its negative statements are withdrawn. Open: chess (cap 2; cap 1 gives bounds (W, L)), the cylinder, other
   boards.)
=======
so its negative statements are withdrawn. Open: chess (cap 1 gives bounds (W, L); six of the 26 deviations lose,
   CHECKED-2; 16 not computed; cap 2 not run), the cylinder, other boards.)
>>>>>>> NEW

### EDIT conjecture list: dud group
<<<<<<< OLD
has every non-shuttle move losing at once in P, CHECKED-2, and equals dud_D beside every context tested, COMPUTED-1;
  Z_A is dud-type up to one White break. Chess (cap 2), the cylinder and other boards are open.)
=======
has every non-shuttle move losing at once in P, PROVED by hand (K27, 2026-10-27; CHECKED-3 for the computations), and
  equals dud_D beside every context tested, COMPUTED-1; Z_A is dud-type up to one White break. The chess statement stays a
  CONJECTURE: Z_B in chess is open (§5.7), and so are the cylinder and other boards.)
>>>>>>> NEW
