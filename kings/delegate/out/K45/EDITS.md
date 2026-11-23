### EDIT C4.7 status row, status words (K45, 2026-11-23)
<<<<<<< OLD
| C4.7 | Over is realisable with wider groups: CONJECTURE, no support. The old first half
=======
| C4.7 | Over is realisable with wider groups: **realised in P (K45, 2026-11-23; CHECKED-2)**: exact over groups and their mirror, exact under groups, of Definition 4.8 exist on cyl:8×6 and every wider cylinder searched (smallest board cyl:8×6, 3 + 3 pawns on the non-adjacent files a, b, e, `Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5`, Black shuttling d4–d5, freezes e2–e4 and e2–e3; smallest by pawns 2 + 3 on cyl:10×6, `Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5`); none in K44's blocked-pair batteries, and K44's over roots are not exact ((O4) fails, see the K45 bullet in Conjecture 4.7). The "none found" statements in the rest of this row hold in their stated ranges only. The old first half
>>>>>>> NEW

### EDIT C4.7 status row, end (K45, 2026-11-23)
<<<<<<< OLD
Lemma 4.10 (a freeze cannot serve both roots) and Lemma 4.11 (every move at a root loses at once, closures reduce to pairs) PROVED | R1 item 10, R4 item 8; K15, K15b; K26 and its referee; K43 and its referee |
=======
Lemma 4.10 (a freeze cannot serve both roots) and Lemma 4.11 (every move at a root loses at once, closures reduce to pairs) PROVED. K45 (2026-11-23): the same exact test over every pawn configuration of at most 3 + 3 pawns on any three files inside a six-file arc (six file classes), every king placement, cyl:6×6 to 12×6 (14×6 and 16×6 for files a, b, e; two seven-file arcs on cyl:10×6), found **exact over and under groups** from cyl:8×6 on (two independent test and solver implementations on 1,199,596 layer lines of cyl:10×6 to 12×6, 0 differences; ref3m and kp_p confirm all ten groups of cyl:8×6 to 10×6; CHECKED-2); none with at most 2 + 2 pawns; none in the K44 batteries of one to three blocked pairs on cyl:10×6, 11×6, 12×6 (F4 = 0) | R1 item 10, R4 item 8; K15, K15b; K26 and its referee; K43 and its referee; K45 |
>>>>>>> NEW

### EDIT Conjecture 4.7, second half status (K45, 2026-11-23)
<<<<<<< OLD
  - *Second half, CONJECTURE, no support:* nothing was found in any search.
=======
  - *Second half, realised by K45 (2026-11-23; CHECKED-2; see the K45 bullet below):* before K45 nothing was found in any search.
>>>>>>> NEW

### EDIT Conjecture 4.7, two readings, note (K45, 2026-11-23)
<<<<<<< OLD
are not the same, and neither search finds a group of its own kind. (Reconciliation:
=======
are not the same, and neither search finds a group of its own kind (K45, 2026-11-23, finds exact groups of Definition 4.8 on three non-adjacent files; see the K45 bullet below). (Reconciliation:
>>>>>>> NEW

### EDIT Conjecture 4.7, K45 bullet (K45, 2026-11-23)
<<<<<<< OLD
  - *To settle:* more files and pawns, kings off the group files, officers; chess (kpsolve was not run for any over candidate).
=======
  - *K45 (2026-11-23; `kings/delegate/out/K45/findings.txt`, with sources, logs and tables; AI work, no human re-derivation; CHECKED-2). Exact over and under groups exist in P.* Domain: every pawn configuration of at most 3 White and 3 Black pawns on the three files {0,x,y} of the six file classes inside an arc of six files ({a,b,c}, {a,b,d}, {a,b,e}, {a,b,f}, {a,c,e}, {a,c,f}; 43,299 layers each), ranks 2 to 5, every placement of both kings, both orientations, cyl:6×6 to 12×6 (also 14×6 and 16×6 for {a,b,e}; on cyl:10×6 also the arcs of seven {a,c,g}, {a,d,g}: no hit). Two implementations of the test and of the P solver: A is K43's `plocalp3.cpp` adapted (pawn-file list, 128-bit masks; `K45/src/p45a.cpp`; its table equals ref3m on 1,500 random states), B is new, written from SPEC.md and Definition 4.8 (`K45/src/b45.cpp`). They agree counter for counter on 1,199,596 layer lines (cyl:10×6, 11×6, 12×6; 6,123,475,980 placements per orientation, 385,499,965 loose groups, 4 exact per orientation) and on the sets of exact groups. ref3m and `kp_p --pmodel` (`verify_hit.py`, which only reads their `--moves` values) confirm all ten exact groups of cyl:8×6, 9×6 and 10×6 and reject K44's root. **Result:** exact over groups (and, by the colour mirror, exact under groups) exist on cyl:8×6 and every wider cylinder searched, with pawns on the non-adjacent files a, b, e (K43's search used four adjacent files). On cyl:8×6: `Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5`, Black to move or White to move, the Black king shuttling d4–d5; Black has 6 (d4) and 7 (d5) moves, all losing at once, the shuttle included; White's only non-losing move is e2–e4 at d4 and e2–e3 at d5; after the freeze Black to move has 4 resp. 5 moves, White to move 6, all lose at once ((O1) to (O4), no promotion; the freezes are pawn moves, as Lemma 4.9 requires, and differ at the two roots, as Lemma 4.10 allows). Same group on cyl:9×6, 10×6, 11×6, 12×6, 14×6, 16×6 (not on cyl:6×6, 7×6); on cyl:10×6 also a 2 + 3 group `Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5` (shuttle f6–g6, freezes e2–e3 and e2–e4), the smallest by pawns, found on no other width searched. Mirror (under) groups: `Kd2 kf2 Pa3 Pb2 Pe2 pb3 pb5 pe5` (White shuttles d2–d3). No exact group has at most 2 + 2 pawns on three files in a six-file arc. In P the group's roots are White wins with either side to move at White's turn and Black losses at Black's turn, so the group is a "White wins either way" position of P alone; a sample of 88 positions beside far pawns (a free White pawn or a blocked pair: all four roots White wins; a free Black pawn: Black wins; two groups, ref3m and kp_p agree on all 88; P is not additive, one race context breaks the pattern) is consistent with 0 < over < 1 but does not decide equality with over. **K44's roots are not exact:** at `Kc3 ka4 Pa2 pa3 Pc4 pc5 Pf2 pf3` (cyl:10×6; also 11×6, 12×6; the mirror under root too) (O1) to (O3) hold and (O4) fails at every freeze: both freezes are the non-capturing king moves Kc3–c2 and Kc3–d2, and after Kc3–c2 White to move still has Kc2–c3 and Kc2–d2, both winning, so q is a White win with either side to move, not 0_D. This is the colour mirror of Lemma 4.9 applied to computed facts (a freeze that is a king move capturing nothing makes (O4) fail). In K44's blocked-pair batteries (all one-, two- and three-pair configurations on files in a six-file arc, pair ranks 2 to 4, all sub-layers, cyl:10×6, 11×6, 12×6) there is no exact over or under group (F4 = 0 on 756 blocked-pair layer lines per width, A and B agree). Not done: more than three pawn files, other numbers of ranks, officers (chess; kpsolve was not run for the groups), contexts that are D-sums, widths 13 and 15 and beyond 16.
  - *To settle:* more files and pawns, kings off the group files, officers; chess (kpsolve was not run for any over candidate); equality of the K45 groups with `over` in sums (needs a D-sum model of P or contexts of several kinds).
>>>>>>> NEW

### EDIT Section 8 item 2, summary line (K45, 2026-11-23)
<<<<<<< OLD
   Over groups: none found (Conjecture 4.7). The two investigations use different definitions and scopes; where they overlap they agree.
=======
   Over groups: none found by K15, K26 and K43 (Conjecture 4.7); K45 (2026-11-23) found exact over and under groups of Definition 4.8 in plain P on cyl:8×6 and wider, with 3 + 3 pawns on the non-adjacent files a, b, e (CHECKED-2). The two investigations use different definitions and scopes; where they overlap they agree.
>>>>>>> NEW

### EDIT Section 8 item 2, K43 bullet heading (K45, 2026-11-23)
<<<<<<< OLD
   - *Over, none found; K43 (2026-11-22) extended the exact search.* 0 exact over and 0 exact under groups with at most 3 + 3 pawns on four files, every king placement,
=======
   - *Over, none found on four adjacent files (K43, 2026-11-22); found on files a, b, e (K45, 2026-11-23, Conjecture 4.7, K45 bullet: cyl:8×6 `Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5`, 3 + 3 pawns, Black shuttles d4–d5, CHECKED-2).* K43: 0 exact over and 0 exact under groups with at most 3 + 3 pawns on four adjacent files, every king placement,
>>>>>>> NEW

### EDIT Section 8 item 2, K44 parenthesis (K45, 2026-11-23)
<<<<<<< OLD
In P the over roots agree with LK "alone" (CHECKED-2), but no context was run beside them in P.)
=======
In P the over roots agree with LK "alone" (CHECKED-2), but no context was run beside them in P. K45, 2026-11-23: K44's roots are not exact over groups, (O4) fails because both freezes are king moves and White can return, so q is a White win with either side to move; no exact group exists in K44's blocked-pair batteries on cyl:10×6 to 12×6, but exact groups with pawns that are not all blocked pairs do exist (CHECKED-2).)
>>>>>>> NEW

### EDIT Section 8 item 3, over and under remark (K45, 2026-11-23)
<<<<<<< OLD
This is a value of the local king game LK, not an exact over group of Definition 4.8 in P (see the bullet "Over, none found").
=======
This is a value of the local king game LK, not an exact over group of Definition 4.8 in P (K45, 2026-11-23: clause (O4) fails at both freezes of every root, because each freeze is a non-capturing king move of the freezing king and the king can step back; exact groups of Definition 4.8 exist in P elsewhere, with pawns on the files a, b, e; see the bullet "Over, none found on four adjacent files" and Conjecture 4.7).
>>>>>>> NEW
