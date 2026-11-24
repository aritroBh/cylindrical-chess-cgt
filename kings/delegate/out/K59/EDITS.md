### EDIT Corollary 4.16: the four cyl:8×7 groups, (B1) now CHECKED-2
<<<<<<< OLD
The four exact groups of cyl:8×7 (K48) satisfy (B1) by one program (pr56/pr57, COMPUTED-1), so for them the same conclusion is conditional on a COMPUTED-1 fact.
=======
The four exact groups of cyl:8×7 (K48) also have the results of over beside every finite D-game, PROVED given CHECKED-2 computations (K59, 2026-11-23; `kings/delegate/out/K59/findings.txt`): `Kd4 kf4/kf5 Pa4 Pb5 Pe2 pa5 pb6 pe6`, `Kd4 kf4/kf5 Pb3 Pb5 Pe2 pb4 pb6 pe6` and `Kd4 kf4/kf5 Pb3 Pb5 Pe2 pa5 pb6 pe6` (Black shuttles f4–f5, freezes e2–e4 at f4 and e2–e3 at f5), and `Kc4 ka4/ka5 Pb2 Pe3 Pe5 pb6 pe4 pe6` (shuttle a4–a5, freezes b2–b4 and b2–b3). Definition 4.8 is CHECKED-2 for them (K48). (B1) is now CHECKED-2: after each of their 11, 11, 13 and 11 non-shuttle Black root moves the position is a White win beside −1 under the sum's rule (`vgsum59`, a copy of the K57 referee's `vgsum` changed only in memory layout, which reproduces its H10 and Z_O outputs line for line), and the move is lost against one Black pass (K56's pr56, K57's pr57); the two programs list the same moves. A direct check of three of them (not the largest, for memory) beside the K57 referee's 63 finite D-games: 0 of 1,215 results each differ from over (COMPUTED-1, `vgsum59`).
>>>>>>> NEW

### EDIT Corollary 4.17 (new): groups with the results of over on flat boards
<<<<<<< OLD
and for Z_O this is where it differs from over (K47).
=======
and for Z_O this is where it differs from over (K47).

**Corollary 4.17 (groups with the results of over on a flat board). PROVED, given CHECKED-2 computations** (new, K59, 2026-11-23; `kings/delegate/out/K59/findings.txt`, `search_table.txt`; AI work, not yet refereed; no human re-derivation). On flat 8×7 (no wrap) the following five exact over groups of Definition 4.8, each as the P game of its own pieces in a D-sum, have the results of over beside every finite D-game (both roots, either side to move; each q has the results of 0_D), by Lemma 4.15: F1 `Ka4 kc4/kc5 Pb2 Pe4 Pe5 pb6 pe6` (3 + 2 pawns), F2 `Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6` (2 + 2 pawns, the smallest found), F3 `Ke4 kc4/kc5 Pb2 Pb5 Pf5 pb6 pf6` and F5 `Ka4 kc4/kc5 Pb2 Pe5 Pf4 pb6 pe6 pf5`, in each of which Black shuttles c4–c5 and the freezes are b2–b4 at c4 and b2–b3 at c5; and F4 `Kc4 ke4/ke5 Pb5 Pf2 Pf5 pb6 pf6`, Black shuttling e4–e5, freezes f2–f4 at e4 and f2–f3 at e5. The two computed facts, for each group: (i) Definition 4.8, CHECKED-2 (found by the exhaustive search of K45's implementation A on flat 8×7, ranks 2 to 6, at most 3 + 3 pawns, every king placement, in the four file classes {a,b,e}, {a,d,e}, {b,c,f}, {b,e,f}, one per left-right reflection, with the same counters and the same exact groups from the K45 referee's implementation R; and confirmed group by group from the move values of ref3m and of `kp_p --pmodel`, which agree on every value); (ii) (B1), CHECKED-2 (every non-shuttle Black root move, 8, 11, 6, 10 and 6 of them, is a White win beside −1 under the sum's rule by `vgsum59` and lost against one Black pass by pr57; same move lists). Direct check: beside the K57 referee's 63 finite D-games (`vgsum59`) and K56's 600 random D-games (pr57) each group has the results of over at all 1,215 and 2,400 results compared (COMPUTED-1 for each program). The search finds no other exact over group in these four classes, and none of the cyl:8×7 groups of K48 or their translates is exact on flat 8×7, 9×7 or 8×8. Larger flat boards: F1 is exact also on flat 9×7 and flat 8×8 as placed (not translated), with (B1) and the two direct checks as on 8×7; F2, F3, F4, F5 placed as on 8×7 are exact on flat 9×7, and F2, F3, F4 on flat 8×8, as are some translates of F3 and F4 (ref3m and kp_p), and (B1) holds for each of these placements by `vgsum59` and pr57, so the same conclusion holds for them (direct sums not run). "Has the results of over beside every finite D-game" is the statement proved; it says nothing about P contexts or chess, and other file classes of flat 8×7 were not searched.
>>>>>>> NEW

### EDIT C4.7 status row: K59
<<<<<<< OLD
by Lemma 4.15, PROVED and refereed): exact over groups and their mirror
=======
by Lemma 4.15, PROVED and refereed; K59, 2026-11-23: so do the four exact groups of cyl:8×7, (B1) now CHECKED-2, and **five exact over groups found on flat 8×7, without the wrap**, Corollary 4.17, PROVED given CHECKED-2 computations, not yet refereed; the smallest has 2 + 2 pawns, `Ka4 kc4 Pb2 Pf5 pb6 pf6`, Black shuttling c4–c5, freezes b2–b4 and b2–b3): exact over groups and their mirror
>>>>>>> NEW

### EDIT To settle: the cyl:8×7 item is done; flat groups added
<<<<<<< OLD
a second program for (B1) on the four cyl:8×7 groups; 
=======
a referee check of K59 (Corollary 4.17, the flat 8×7 groups); the flat groups beside P contexts and in chess; other file classes of flat 8×7, and full searches of flat 9×7 and 8×8; 
>>>>>>> NEW
