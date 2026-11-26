# K65 referee's edits for kings/theory/LOOPY.md (replace the investigator's edit in kings/delegate/out/K65/EDITS.md)

### EDIT Corollary 4.17: flat 8×8 census of two file classes (K65, refereed)
<<<<<<< OLD
F5 is not exact on flat 8×8, and no placement one rank up is.
=======
F5 is not exact on flat 8×8, and no placement one rank up is. *Flat 8×8 census (K65, 2026-11-25; refereed (K65 referee), `kings/delegate/out/K65/verify/VERIFY.md`).* On flat 8×8 (ranks 2 to 7, at most 3 + 3 pawns, every king placement) the file classes {b,c,f} and {b,e,f} hold exactly 23 and 25 exact over groups, 38 in all, 26 up to reflection and file translation (CHECKED-2: p45a and r48 agree on every counter and group). Four have 2 + 2 pawns, in three shapes: F2, `Ka5 kc5/kc6 Pb2 Pf6 pb7 pf7`, `Kc5 ka4/ka5 Pb2 Pf3 pb5 pf4` and its reflected translate. (B1) holds for 27 of the 38, which so have the results of ω (Lemma 4.15); it fails for 11 (CHECKED-2 for all 38). Seven of these 11 still have the results of ω, since White wins Aux at every bad move (Corollary 4.19); four fail (C) at one bad move, three with N\* = 2 and one with N\* = 3 (Proposition 4.24). In chess (Syzygy tablebase, KNOWN) five of the 19 groups with at most seven men are exact over groups: `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6`, `Ke5 kc5/kc6 Pb2 Pb6 Pf6 pb7 pf7`, `Kc5 ke5/ke6 Pb6 Pf2 Pf6 pb7 pf7`, `Kg4 ke4/ke5 Pe6 Pf2 Pf5 pe7 pf6`, `Kd4 kf4/kf5 Pe2 Pe5 Pf6 pe6 pf7`; the other 14, F1 to F4 among them, are not. Not searched: {a,b,e}, {a,d,e}, eleven two-file classes, other shapes.
>>>>>>> NEW

### EDIT Corollary 4.19: real groups with the results of ω without (B1) (K65, refereed)
<<<<<<< OLD
No known real group has the results of ω without (B1).
=======
Real groups with the results of ω without (B1) exist (K65, 2026-11-25, refereed, `kings/delegate/out/K65/verify/VERIFY.md`). On flat 8×8, `Kc4 ke4/ke5 Pb5 Pf2 Pf6 pb6 pf7` (Black shuttles e4–e5; freezes f2–f4 at e4, f2–f3 at e5) is an exact over group; (B1) fails exactly at …Ke5–d6 and …Ke5–e6, and White wins Aux at both. After either move the board with Black to move is a zugzwang, but with White to move only Kc4–d4 wins on the bare board (after …Ke6 also f2–f4), and beside −1 Black meets every White move while keeping its token. In Aux White passes instead: if Black spends its freeze, Kc4–d4 wins; if Black moves its king, White passes again or wins on the board, and an endless king walk against White's passes is a White win. So by (c) and (b) the group has the results of ω beside every finite D-game, PROVED given CHECKED-2 computations (Definition 4.8: ref3m, `kp_p`, ax65; (B1) at all eight bad moves: vgsum59, pr57, ax65, `pk_sum`; Aux: aux60, ax65, `pk_sum`). Six more groups of the K65 census do the same (Corollary 4.17).
>>>>>>> NEW

### EDIT Remark after Corollary 4.23: N* ≥ 3 is no longer open
<<<<<<< OLD
Whether a real exact group has N\* ≥ 3 is OPEN; to search for it, compute N\* on each bad Black root move of the known and newly found exact groups with the layer recursion of Theorem 4.20 (one ladder solve per n), looking for a White win beside T_2 with Aux lost.
=======
A real exact group with N\* = 3 exists (Proposition 4.24, found by this search on the K65 census); whether a real exact group has N\* ≥ 4 is OPEN.
>>>>>>> NEW

### EDIT Proposition 4.24: a real exact over group with N* = 3 (new, K65)
<<<<<<< OLD
*Computable test (K43).* `kings/delegate/out/K43/plocalp3.cpp`
=======
**Proposition 4.24 (a real exact over group with ladder length 3). PROVED, given CHECKED-2 computations** (new, K65, 2026-11-25; `kings/delegate/out/K65/verify/VERIFY.md`; refereed (K65 referee)). On flat 8×8, G = `Kg5 ke5/ke6 Pb2 Pf2 Pf6 pc4 pf5 pf7` (3 + 3 pawns; Black shuttles e5–e6; freezes f2–f3 at e5 and f2–f4 at e6) is an exact over group of Definition 4.8 with eleven bad Black root moves. At …Ke5–e4, x_m ⊞ u_0, White to move, is a White win beside T_0, T_1 and T_2 and a draw beside T_3, and White does not win Aux, so N\* = 3. At the other ten bad moves (C) holds: (B1) at six, Aux won at four. The e5 root, Black to move, is a White win beside u_0 of T_2 and a draw beside u_0 of T_3; so G has the results of ω beside T_0, T_1 and T_2 but not beside T_3. *Proof.* Theorem 4.18 (b), (c) and Corollary 4.19 (i), with these computed facts, each CHECKED-2: Definition 4.8 (ref3m, `kp_p`, ax65); the ladder values at x_m and at both roots for T_0 to T_3 and Aux at all eleven bad moves (ax65, and `pk_sum`, the K65 referee's sum and Büchi version of K63's `pk`, which shares no code with ax65).

*Computable test (K43).* `kings/delegate/out/K43/plocalp3.cpp`
>>>>>>> NEW

### EDIT Open questions: the K65 answers
<<<<<<< OLD
no known real group has the results of over without (B1); K62
=======
K65 (2026-11-25, refereed) found real ones: seven exact over groups of a flat 8×8 census, among them `Kc4 ke4/ke5 Pb5 Pf2 Pf6 pb6 pf7`, fail (B1) and have the results of over (Corollary 4.19), and `Kg5 ke5/ke6 Pb2 Pf2 Pf6 pc4 pf5 pf7` has N\* = 3 (Proposition 4.24); K62
>>>>>>> NEW
