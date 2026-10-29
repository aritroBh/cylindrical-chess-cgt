### EDIT k31-parity-of-the-width
<<<<<<< OLD
CONJECTURE: the same
     parity holds for other heights and for other widths; it is untested.
=======
Parity of the width (new, K31, 2026-10-27). K31 ran one blocked pair `Pa<r> pa<r+1>` at every rank
     r = 2..H-2 on cyl:W×H with the free board, for H = 4..12 and W = 3..26 (934 cases; W up to 24 for H ≥ 7). A +1
     root and a -1 root exist in every case with W even and W ≥ 6. None exists for W = 3, 4 or any odd W (482 cases).
     For the 470 cases with W·H ≤ 127, `kg`/`kgw` and `lk` agree on the class counts and on the sets of +1 and -1 roots
     (CHECKED-2). The other 464 cases ran in `lk` only (COMPUTED-1). All 10,514 roots found have both kings on the file
     W/2, opposite the pawn file, on squares of the same colour (COMPUTED-1; CHECKED-2 for the 2,490 roots of the cases
     that both solvers ran). For fixed H the numbers of roots at each pair rank are the same for all even W ≥ 2H - 2
     (H = 4..12; observation, COMPUTED-1). One blocked pair on a flat board (W = 5..10, H = 5..7, every file, every rank:
     216 cases) has no +1 or -1 root (COMPUTED-1). The rule for all heights and widths is a CONJECTURE; the boundary of
     the search is H ≤ 12, W ≤ 26, one pair, free board. For odd W it would follow from "every +1 and -1 root has both
     kings on file W/2", which is itself a CONJECTURE. No proof was found (K31).
>>>>>>> NEW

### EDIT k31-tempo-race-and-two-tempo-lead
<<<<<<< OLD
Interpretation, CONJECTURE: the tempo is a one-tempo race lead between two kings that reply inside Z, not a
     reservoir (nothing computed distinguishes a race lead from other mechanisms). CONJECTURE: a lead of two
     tempi is already decisive, which would explain why +-2 and +-3 never occur (untested).
=======
Interpretation, CONJECTURE (revised after K31, 2026-10-27): the tempo is a one-tempo lead in a move-order race
     around a mutual zugzwang, between two kings that reply inside Z. One line is checked (new, K31, 2026-10-27;
     CHECKED-2: an independent Python solver finds it and the referee's `lk` replays every position and step). On flat:6x6
     `Kc3 ka4 Pa2 pa3 Pc4 pc5` the position `Kd3 kb4` is a zero for the mover. With Black to move White wins in 4
     plies. With White to move White needs 13 plies, using files d and e outside F_Z. With one spare Black move and
     White to move, Black wins in 6 plies. Sums cannot tell a race lead from a reserve of one spare move, because the +1
     root equals the integer 1. The conjecture that a lead of two tempi is decisive is FALSE for sums (revised after
     K31, 2026-10-27). For every ordered pair of +1 and -1 roots of 13 single-pair cylinder configurations, and for
     each such root with the integer +1 or -1, the sum with every integer context c in -N..N (N = 2..4) equals the
     integer sum (8,166 and 2,308 outcomes, 0 mismatches; COMPUTED-1). So x + x acts as the integer 2: White wins
     for c ≥ -1, the second player wins at c = -2, Black wins for c ≤ -3. The referee's `lk allpairs` also finds 0
     mismatches in 2,706,185 ordered pairs of named roots over 14 configurations (CHECKED-2 for two-root sums). As
     single roots, none has a finite integer lead k with 2 ≤ k < N (new, K31, 2026-10-27): N = 12, 764,312 roots of
     571 configurations (COMPUTED-1); N = 30, 16,575 roots of 8 configurations (COMPUTED-1). The C++ profile and an
     independent Python profile agree on 12 configurations at N = 4 (CHECKED-2). Why ±2 and ±3 cannot occur as a
     single root is not proved (CONJECTURE).
>>>>>>> NEW
