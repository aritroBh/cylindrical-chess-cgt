### EDIT status row C4.7: Z_O is exact but not over in sums (K47, 2026-11-23)
<<<<<<< OLD
(K45, 2026-11-23; CHECKED-2; equality with over in sums not tested)
=======
(K45, 2026-11-23; CHECKED-2), **but the cyl:8×6 group is not equal to over in D-sums** (K47, 2026-11-23, CHECKED-2: against 275 test games it differs from over at 38 of 1,100 results, always in Black's favour, from T = \*, ↓, under and sums containing them; its freeze at the d4 root is a mutual zugzwang of P, PROVED by hand; see the K47 bullet in Conjecture 4.7)
>>>>>>> NEW

### EDIT Conjecture 4.7 opening: equality with over now tested (K47, 2026-11-23)
<<<<<<< OLD
Over-type groups of Definition 4.8 are now known (K45, 2026-11-23, CHECKED-2; equality with over in sums not tested; see the K45 bullet below).
=======
Over-type groups of Definition 4.8 are now known (K45, 2026-11-23, CHECKED-2; see the K45 bullet below), but the one tested in sums is not equal to over (K47, 2026-11-23, CHECKED-2; see the K47 bullet below): Definition 4.8 does not force the value over.
>>>>>>> NEW

### EDIT Conjecture 4.7 second half: realised only in the sense of Definition 4.8 (K47, 2026-11-23)
<<<<<<< OLD
that the groups equal over in sums is not tested):*
=======
the cyl:8×6 group is not equal to over in D-sums, K47 bullet below; so over itself is still not realised as a sum value):*
>>>>>>> NEW

### EDIT K45 bullet: the context sample is now superseded (K47, 2026-11-23)
<<<<<<< OLD
is consistent with 0 < over < 1 but does not decide equality with over.
=======
is consistent with 0 < over < 1 but does not decide equality with over (K47, 2026-11-23, decides it in D-sums: not equal; see the next bullet).
>>>>>>> NEW

### EDIT new K47 bullet and revised "To settle" (K47, 2026-11-23)
<<<<<<< OLD
  - *To settle:* more files and pawns, kings off the group files, officers; chess (kpsolve was not run for any over candidate); equality of the K45 groups with `over` in sums (needs a D-sum model of P or contexts of several kinds).
=======
  - *K47 (2026-11-23; `kings/delegate/out/K47/findings.txt`, `PROOF.md`; AI work, no human re-derivation). The cyl:8×6 group Z_O = `Kf5 kd4/kd5 Pb2 Pb4 Pe2 pa4 pb5 pe5` is exact but not over.*
    - *Hand proof, partial (PROVED).* The move lists of the four roots and the two freezes, and: the freeze q_A = `Kf5 kd4 Pb2 Pb4 Pe4 pa4 pb5 pe5` (e2–e4 at the d4 root) is a mutual zugzwang of P. Black to move, its 4 moves lose (after a king move Kxe5 and the e-pawn runs behind a king on d5 or d6; after a3, bxa3 and the same); White to move, its 6 moves lose (b3 is met by a3 or axb3 and a run of the a- or b-pawn; a king move by Kxe4, Kd3 (or Kd2) and the double step e5–e3). So (O3) and (O4) hold at the d4 root, and the d4 root has a freeze. The argument holds on every cyl:W×6 with W ≥ 8. Not proved by hand: (O1) at both roots, (O3) and (O4) at the d5 root (freeze e2–e3), and that the other White moves at the roots lose; those rest on K45's CHECKED-2 computation (the solver's lines are 11 to 25 plies deep). So the exactness of Z_O as a whole stays CHECKED-2.
    - *Value in sums (CHECKED-2).* Z_O as a component of a D-sum is the P game of its own pieces (K40's convention: a promotion is a terminal for the promoter, a side in check may not move elsewhere, a move elsewhere clears the e.p. right, a side with no move loses, Definition 1.2): 3,914,687 placements (bisimulation quotient 3,397,278 classes). Two implementations (`K47/src/za.cpp`, a retrograde pass with counters; `K47/src/zb.cpp`, written separately, reachable product states and two attractors), whose P values agree with ref3m on 66,997 sampled states, compare r(Z_O ⊞ T) with r(over ⊞ T) for 275 test games T (the integers −6…6, on, off, dud, \*, ↑, ↓, ±1, over, under and all 253 sums of two), both roots, both sides to move: A and B agree on all 1,100 results; Z_O equals over at 1,062 and **differs at 38**: T = \* (d4 root, Black to move), ↓, under and sums containing them. In every difference Z_O gives Black the win where over gives White the win or a draw, never the reverse. Example: beside \*, the d4 root with Black to move is a Black win by 1…e5–e4, a move that loses in P alone (25 plies, by zugzwang) but wins with the spare tempo \*; beside under every root is a Black win, while over ⊞ under is a draw. The two roots also differ from each other (8 of 550 test-and-side pairs). So Definition 4.8 does not force the value over: exactness is a property of P alone, while the sum value also depends on the losing moves, which can lose only through zugzwang. The value of Z_O was not identified.
    - *P contexts (CHECKED-2: ref3m and `kp_p --pmodel` agree on every position).* On cyl:8×6 no file is at distance ≥ 2 from the group (pawn files a, b, e; kings on d and f), so the test used cyl:9×6 (context file h, buffers g and i; all 63 contexts of at most 2 + 2 pawns) and cyl:10×6 (files h and i, buffers g and j; 200 of the 885 contexts of at most 2 + 2 pawns, a seeded sample). The P results equal r(over ⊞ C), C the context pawns as a D-game, in all 63 contexts on cyl:9×6 and in 199 of 200 on cyl:10×6; the exception is `Ph2 pi3 pi5`, where the d4 root with White to move is a Black win (over predicts a White win). The D-sum r(Z_O ⊞ C) (implementation A, COMPUTED-1) separates Z_O from over in 4 of the 63 and 5 of the 200 contexts (always the d4 root, a Black win where over gives a White win); P follows it in only one of these nine (`Ph2 pi3 pi5`) and follows over in the other eight, so in P beside these contexts the group does not behave as its D-sum value: the P context test, unlike the D-sums, hardly separates Z_O from over.
  - *To settle:* more files and pawns, kings off the group files, officers; chess (kpsolve was not run for any over candidate); the value of the K45 groups in sums (Z_O is not over, K47) and whether some exact group of Definition 4.8 has the value over; a hand proof of (O1) and of the d5 root of Z_O.
>>>>>>> NEW

### EDIT §8 item 2: K45's groups are not over in sums (K47, 2026-11-23)
<<<<<<< OLD
with 3 + 3 pawns on the non-adjacent files a, b, e (CHECKED-2). The two investigations use different definitions and scopes; where they overlap they agree.
=======
with 3 + 3 pawns on the non-adjacent files a, b, e (CHECKED-2). K47 (2026-11-23, CHECKED-2) found that this group is not equal to over in D-sums (it differs against \*, ↓, under and sums containing them, always in Black's favour), so "an over-group" in the sense of a group with the value over is still not known; its freeze at the d4 root is a mutual zugzwang of P, PROVED by hand (Conjecture 4.7, K47 bullet). The two investigations use different definitions and scopes; where they overlap they agree.
>>>>>>> NEW
