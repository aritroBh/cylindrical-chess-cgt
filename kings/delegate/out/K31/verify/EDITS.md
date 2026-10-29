### EDIT k31-parity-of-the-width
<<<<<<< OLD
CONJECTURE: the same
     parity holds for other heights and for other widths; it is untested.
=======
Parity of the width (new, K31, 2026-10-27; revised after the two K31 referees, 2026-10-28). K31 ran one
     blocked pair `Pa<r> pa<r+1>` at every rank r = 2..H-2 on cyl:W×H with the free board. The grid H = 4..12, W = 3..26
     has 1,080 cases (W, H, r). K31's own runs cover 934 of them; the first referee ran the other 146 (H = 4 with W = 17..24;
     W = 3, 4 for H ≥ 9; W = 25, 26 for H ≥ 7). A +1 root and a -1 root exist in every case with W even and 6 ≤ W ≤ 26
     (495 cases). None exists for W = 3, 4 or any odd W (585 cases). The grid holds 11,914 roots of value ±1 (10,514 in
     K31's runs). Counts of roots: CHECKED-2 on the whole grid. For 470 cases with W·H ≤ 127, `kg`/`kgw` and `lk` agree on
     the class counts and on the sets of +1 and -1 roots; four further cases with W·H ≤ 127 (W = 25, 26) and the 460 cases with
     W·H > 127 ran in `lk` only. The first referee's solver (written from the definition text; a third implementation of LK) gives the same root counts in
     the 541 cases it ran (all 146 gap cases among them) and the same sets of +1 and -1 roots in 112 of them (720 roots). The
     second referee's solver (also written from the definition text; a fourth implementation of LK) ran all 1,080
     cases and gives the same counts of +1 and -1 roots in every one of them (0 differences against K31's 934 and against the
     first referee's 541). It gives the same sets of +1 and -1 roots (positions) as K31 in all 452 cases where K31 dumped them
     (10,514 roots). All 11,914 roots of the grid have both kings on the file W/2, opposite the pawn file, on squares of the
     same colour (0 exceptions in the second referee's runs; CHECKED-2 for the 10,514 roots whose sets the two solvers compare).
     For fixed H the numbers of roots at each pair rank are the same for all even W ≥ 2H - 2 up to W = 26 (H = 4..12), and the
     row for W = 2H - 4 differs (observation; for H = 12 only W = 22, 24, 26 are in the grid; CHECKED-2 with the counts). The
     +1 count at rank r equals the -1 count at rank H - r in all 1,080 cases. One blocked pair on a flat board (W = 5..10,
     H = 5..7, every file, every rank) has no +1 or -1 root (K31: 216 cases up to mirror, `lk`; first referee: 405 cases
     without the mirror reduction; second referee: the same 405 cases with its own solver; CHECKED-2). The rule for all heights
     and widths is a CONJECTURE. Cases outside the grid agree with it: the first referee ran 12 chosen cases (H = 13 with
     W = 6, 7, 8, 9; H = 14 with W = 5, 10; W = 28, 29, 30, 31 with H = 4, 5, 6, 6); the second referee ran 237 cases (every rank
     for H = 13, 14 with W = 4..12, and every rank for H = 4..6 with W = 27..34; no case disagrees; COMPUTED-1 for these, one
     implementation each). For odd W the rule would follow from "every +1 and -1 root has both kings on file W/2", which is
     itself a CONJECTURE. No proof was found (K31).
>>>>>>> NEW

### EDIT k31-tempo-race-and-two-tempo-lead
<<<<<<< OLD
Interpretation, CONJECTURE: the tempo is a one-tempo race lead between two kings that reply inside Z, not a
     reservoir (nothing computed distinguishes a race lead from other mechanisms). CONJECTURE: a lead of two
     tempi is already decisive, which would explain why +-2 and +-3 never occur (untested).
=======
Interpretation, CONJECTURE (revised after K31, 2026-10-27): the tempo is a one-tempo lead in a move-order race
     around a mutual zugzwang, between two kings that reply inside Z. One line is checked (new, K31, 2026-10-27; CHECKED-2:
     K31's Python solver finds the lines, `lk` replays every position and step, and the first and second referees' own solvers
     give the same outcomes and ply counts). On flat:6x6 `Kc3 ka4 Pa2 pa3 Pc4 pc5` the position `Kd3 kb4` has value 0: the player
     to move loses (White to move loses in 2 plies, Black to move wins in 10). With Black to move White wins in 4 plies. With
     White to move White needs 13 plies; the principal variation uses files d and e, outside F_Z. With one spare Black move and
     White to move, Black wins in 6 plies. Sums cannot tell a race lead from a reserve of one spare move, because the +1 root
     equals the integer 1. So the mechanism is one root on one board.
     The conjecture that a lead of two tempi is decisive is FALSE for sums (revised after K31, 2026-10-27). It was not
     tested for a single root, where it is not needed (see the profiles below). For every ordered pair of +1 and -1 roots
     of 13 single-pair cylinder configurations, and for each such root with the integer +1 or -1, the sum with every
     integer context c in -N..N (N = 2..4) equals the integer sum (8,166 and 2,308 outcomes, a pair of outcomes counted as two;
     0 mismatches; COMPUTED-1; CHECKED-2 on cyl:6x6 a2, a3, a4, cyl:8x6 a2, a3 and cyl:8x5 a2, where the referees' own solvers
     reproduce them). So x + x acts as the integer 2: White wins for c ≥ -1, the second player wins at c = -2, Black wins for
     c ≤ -3. The second referee also added every one of the 34 games of B34 as the context (x + y + K against the integer
     sum + K, both movers; cyl:6x6 a2, a3, a4 and cyl:6x5 a2; 5,712 outcomes, 0 mismatches; one implementation, COMPUTED-1).
     `lk allpairs` finds 0 mismatches in 2,706,185 ordered pairs of named roots over 14 configurations (two-root sums without
     context). The second referee's solver, with its own game graph, gives the same numbers of named roots and pairs in all 14
     configurations and the same total with 0 mismatches (CHECKED-2). As single roots, none has a finite
     integer lead k with 2 ≤ k < N (new, K31, 2026-10-27): N = 12 over 764,312 root entries of 571 configurations (single
     pairs on cylinders and flat boards, and two-pair models, some not faithful; COMPUTED-1, and CHECKED-2: both referees' solvers
     reproduce the four lead counts of every one of the 571 configurations, and the second referee's solver reproduces the joint
     histogram of the four leads in every configuration, with 0 races); N = 30 over 16,575 root entries
     of 8 configurations (CHECKED-2 in the same way, both referees). Only the leads -1, 0, 1 and N occur. A lead of exactly 1
     occurs in all 56 single-pair even-width cylinder configurations of the profile, in 2 of the 63 faithful two-pair even-width
     cylinder configurations, in 16 faithful two-pair flat configurations and in 6 non-faithful two-pair odd-width cylinder
     configurations. It occurs in none of the 92 faithful odd-width cylinder configurations and in none of the 63 single-pair
     flat configurations (second referee's count, COMPUTED-1). Why ±2 and ±3 cannot occur as a single root is not proved
     (CONJECTURE).
>>>>>>> NEW

