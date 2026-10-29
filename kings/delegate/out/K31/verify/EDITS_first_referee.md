### EDIT k31-parity-of-the-width
<<<<<<< OLD
CONJECTURE: the same
     parity holds for other heights and for other widths; it is untested.
=======
Parity of the width (new, K31, 2026-10-27; grid and counts corrected after the K31 referee, 2026-10-27). K31 ran one
     blocked pair `Pa<r> pa<r+1>` at every rank r = 2..H-2 on cyl:W×H with the free board. The grid H = 4..12, W = 3..26
     has 1,080 cases (W, H, r). K31's own runs cover 934 of them; the referee ran the other 146 (H = 4 with W = 17..24;
     W = 3, 4 for H ≥ 9; W = 25, 26 for H ≥ 7) with its own solver, so the whole grid is covered. A +1 root and a -1 root
     exist in every case with W even and 6 ≤ W ≤ 26 (495 cases). None exists for W = 3, 4 or any odd W (585 cases). The
     grid holds 11,914 roots of value ±1 (10,514 in K31's runs). For 470 cases with W·H ≤ 127, `kg`/`kgw` and `lk` agree on
     the class counts and on the sets of +1 and -1 roots (CHECKED-2); four further cases with W·H ≤ 127 (W = 25, 26) and
     the 460 cases with W·H > 127 ran in `lk` only (COMPUTED-1). The referee's own solver (a third implementation, written
     from the definition text) gives the same root counts in the 383 cases it shares with K31's runs and the same sets of
     +1 and -1 roots in 112 of them (720 roots; CHECKED-2). All 10,514 roots of K31's runs have both kings on the file W/2,
     opposite the pawn file, on squares of the same colour (COMPUTED-1; CHECKED-2 for the 2,490 roots of the cases that
     both solvers ran); the referee's own runs found no root that breaks this. For fixed H the numbers of roots at each pair
     rank are the same for all even W ≥ 2H - 2 up to W = 26 (H = 4..12), and the row for W = 2H - 4 differs
     (observation, COMPUTED-1). One blocked pair on a flat board (W = 5..10, H = 5..7, every file, every rank) has no +1 or
     -1 root (K31: 216 cases up to mirror, `lk`; the referee's own solver: 405 cases without the mirror reduction; CHECKED-2).
     The rule for all heights and widths is a CONJECTURE. The referee's spot checks outside the grid agree with it
     (H = 13, 14 with W = 5..10, and W = 28..31 with H = 4..6; 12 cases; COMPUTED-1). For odd W it would follow from "every +1
     and -1 root has both kings on file W/2", which is itself a CONJECTURE. No proof was found (K31).
>>>>>>> NEW

### EDIT k31-tempo-race-and-two-tempo-lead
<<<<<<< OLD
Interpretation, CONJECTURE: the tempo is a one-tempo race lead between two kings that reply inside Z, not a
     reservoir (nothing computed distinguishes a race lead from other mechanisms). CONJECTURE: a lead of two
     tempi is already decisive, which would explain why +-2 and +-3 never occur (untested).
=======
Interpretation, CONJECTURE (revised after K31, 2026-10-27): the tempo is a one-tempo lead in a move-order race
     around a mutual zugzwang, between two kings that reply inside Z. One line is checked (new, K31, 2026-10-27; CHECKED-2:
     K31's Python solver finds the lines, `lk` replays every position and step, and the referee's own solver gives the same
     outcomes and ply counts). On flat:6x6 `Kc3 ka4 Pa2 pa3 Pc4 pc5` the position `Kd3 kb4` has value 0: the player to
     move loses. With Black to move White wins in 4 plies. With White to move White needs 13 plies, using files d and e
     outside F_Z. With one spare Black move and White to move, Black wins in 6 plies. Sums cannot tell a race lead from a
     reserve of one spare move, because the +1 root equals the integer 1. So the mechanism is one root on one board.
     The conjecture that a lead of two tempi is decisive is FALSE for sums (revised after K31, 2026-10-27). It was not
     tested for a single root, where it is not needed (see the profiles below). For every ordered pair of +1 and -1 roots
     of 13 single-pair cylinder configurations, and for each such root with the integer +1 or -1, the sum with every
     integer context c in -N..N (N = 2..4) equals the integer sum (8,166 and 2,308 outcomes, 0 mismatches; COMPUTED-1;
     CHECKED-2 on cyl:6x6 a2, a3, a4 and cyl:8x6 a3, where the referee's own solver reproduces them). So x + x acts as the
     integer 2: White wins for c ≥ -1, the second player wins at c = -2, Black wins for c ≤ -3. The referee's `lk allpairs`
     also finds 0 mismatches in 2,706,185 ordered pairs of named roots over 14 configurations (two-root sums without
     context; the game graph is the same for both solvers; CHECKED-2 as a sum check). As single roots, none has a finite
     integer lead k with 2 ≤ k < N (new, K31, 2026-10-27): N = 12 over 764,312 root entries of 571 configurations (single
     pairs on cylinders and flat boards, and two-pair models, some not faithful; COMPUTED-1, and CHECKED-2: the referee's
     own solver reproduces the four lead counts of every one of the 571 configurations); N = 30 over 16,575 root entries
     of 8 configurations (CHECKED-2 in the same way). Only the leads -1, 0, 1 and N occur. A lead of exactly 1 occurs on
     even-width cylinders and on two-pair configurations, and on no faithful odd-width cylinder (COMPUTED-1). Why ±2 and
     ±3 cannot occur as a single root is not proved (CONJECTURE).
>>>>>>> NEW
