### EDIT Corollary 4.16: the four cyl:8×7 groups, (B1) now CHECKED-2
<<<<<<< OLD
The four exact groups of cyl:8×7 (K48) satisfy (B1) by one program (pr56/pr57, COMPUTED-1), so for them the same conclusion is conditional on a COMPUTED-1 fact.
=======
The four exact groups of cyl:8×7 (K48) have the same results, PROVED given CHECKED-2 computations (K59, 2026-11-23, refereed; `kings/delegate/out/K59/findings.txt`, `verify/VERIFY.md`): `Kd4 kf4/kf5 Pa4 Pb5 Pe2 pa5 pb6 pe6`, `Kd4 kf4/kf5 Pb3 Pb5 Pe2 pb4 pb6 pe6` and `Kd4 kf4/kf5 Pb3 Pb5 Pe2 pa5 pb6 pe6` (Black shuttles f4–f5, freezes e2–e4 at f4 and e2–e3 at f5), and `Kc4 ka4/ka5 Pb2 Pe3 Pe5 pb6 pe4 pe6` (Black shuttles a4–a5, freezes b2–b4 at a4 and b2–b3 at a5). Definition 4.8 is CHECKED-2 for them (K48). (B1) is CHECKED-2: after each of their 11, 11, 13 and 11 non-shuttle Black root moves the position is a White win beside −1 under the sum's rule by `vgsum59` (the K57 referee's `vgsum` with changes to memory layout only, checked by diff; it reproduces vgsum's H10 output line for line, also with `--lowmem`), and the move is lost against one Black pass by K56's pr56, which implies (B1); the two programs list the same moves. A direct check of three of them (not the largest, for memory) beside the K57 referee's 63 finite D-games: 0 of 1,215 results each differ from over (COMPUTED-1, `vgsum59`).
>>>>>>> NEW

### EDIT Corollary 4.17 (new): groups with the results of over on flat boards
<<<<<<< OLD
and for Z_O this is where it differs from over (K47).
=======
and for Z_O this is where it differs from over (K47).

**Corollary 4.17 (groups with the results of over on a flat board). PROVED, given CHECKED-2 computations** (new, K59, 2026-11-23; `kings/delegate/out/K59/findings.txt`, `search_table.txt`; refereed, `kings/delegate/out/K59/verify/VERIFY.md`; no human re-derivation). On flat 8×7 (no wrap) each of the following five exact over groups of Definition 4.8, as the P game of its own pieces in a D-sum, has the results of over beside every finite D-game (both roots, either side to move; each q has the results of 0_D), by Lemma 4.15. Black shuttles c4–c5 with freezes b2–b4 at c4 and b2–b3 at c5 in F1 `Ka4 kc4/kc5 Pb2 Pe4 Pe5 pb6 pe6` (3 + 2 pawns, 8 non-shuttle Black root moves), F2 `Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6` (2 + 2 pawns, the fewest found; 11 moves), F3 `Ke4 kc4/kc5 Pb2 Pb5 Pf5 pb6 pf6` (3 + 2; 6 moves) and F5 `Ka4 kc4/kc5 Pb2 Pe5 Pf4 pb6 pe6 pf5` (3 + 3; 10 moves); Black shuttles e4–e5 with freezes f2–f4 at e4 and f2–f3 at e5 in F4 `Kc4 ke4/ke5 Pb5 Pf2 Pf5 pb6 pf6` (3 + 2; 6 moves). F4 is F3 reflected left to right and moved one file, so the five are four shapes up to reflection and translation; on flat 8×7 the two placements differ. The two computed facts, for each group: (i) Definition 4.8, CHECKED-2 (found by the exhaustive search of K45's implementation A on flat 8×7, ranks 2 to 6, at most 3 + 3 pawns, every king placement, in the four file classes {a,b,e}, {a,d,e}, {b,c,f}, {b,e,f}, one per left-right reflection, with the same counters and the same exact groups from the K45 referee's implementation R; confirmed group by group from the move values of ref3m and of `kp_p --pmodel`, which agree on every value, and by the K59 referee's own solver, which shares no code with any of them); (ii) (B1), CHECKED-2 (every non-shuttle Black root move is a White win beside −1 under the sum's rule by `vgsum59` and by the K59 referee's solver, and is lost against one Black pass by pr57; all three list the same moves). Direct checks: beside the K57 referee's 63 finite D-games and K56's 600 random D-games each group has the results of over at every result compared (`vgsum59`, pr57; for F2 and F4 also the K59 referee's solver; COMPUTED-1 for each program). None of the five is tempo-exact (Definition 4.12; pr57, COMPUTED-1), so Lemma 4.13 does not apply. The search finds no other exact over group in these four classes; none of the cyl:8×7 groups of K48 or their translates is exact on flat 8×7, 9×7 or 8×8 (ref3m and `kp_p`). Larger flat boards (ref3m and `kp_p` for Definition 4.8, `vgsum59` and pr57 for (B1); so PROVED given CHECKED-2 computations; direct sums only for F1): on flat 9×7, F1 to F5 as placed, F3 moved one and two files right and F4 moved one and two files right (six placements of F3 and F4, three up to reflection); on flat 8×8, F1 to F4 as placed, F3 and F4 moved one file right (these two are F4 and F3 reflected); F5 is not exact on flat 8×8, and no placement one rank up is. "Has the results of over beside every finite D-game" is the statement proved; it says nothing about P contexts or chess, and other file classes of flat 8×7 were not searched.
>>>>>>> NEW

### EDIT C4.7 status row: K59
<<<<<<< OLD
by Lemma 4.15, PROVED and refereed): exact over groups and their mirror
=======
by Lemma 4.15, PROVED and refereed; K59, 2026-11-23, refereed: so do the four exact groups of cyl:8×7, now that (B1) is CHECKED-2 for them (Corollary 4.16), and five exact over groups found on flat 8×7, without the wrap (Corollary 4.17, PROVED given CHECKED-2 computations); the one with fewest pawns has 2 + 2, `Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6`, Black shuttling c4–c5, freezes b2–b4 and b2–b3): exact over groups and their mirror
>>>>>>> NEW

### EDIT To settle: the cyl:8×7 item is done; flat groups added
<<<<<<< OLD
a second program for (B1) on the four cyl:8×7 groups; 
=======
the flat groups of Corollary 4.17 beside P contexts and in chess; other file classes of flat 8×7, and full searches of flat 9×7 and 8×8; 
>>>>>>> NEW

### EDIT Lemma 4.13: the flat groups are not tempo-exact either
<<<<<<< OLD
is tempo-exact or pass-robust exact, so **no known group meets the criterion**
=======
is tempo-exact or pass-robust exact, nor is any of the five flat 8×7 groups of Corollary 4.17 (K59, pr57, COMPUTED-1), so **no known group meets the criterion**
>>>>>>> NEW

### EDIT §8 item 2: K59
<<<<<<< OLD
no known real group has the results of over without (B1); the K45 group
=======
no known real group has the results of over without (B1); K59 (2026-11-23) made (B1) CHECKED-2 for the four cyl:8×7 groups of K48, so they have the results of over too (Corollary 4.16), and found five exact over groups with the results of over on flat 8×7, the smallest with 2 + 2 pawns (Corollary 4.17; both PROVED given CHECKED-2 computations, refereed); the K45 group
>>>>>>> NEW
