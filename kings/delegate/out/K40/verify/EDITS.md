### EDIT 8.5 Gafni's K+P vs K values without edges answered (K40, replacement after the K40 referee)
<<<<<<< OLD
5. Gafni's K+P vs K values without edges (plan item A8): the cylinder KPK table in `atlas/cylinder/kpk` is the
   starting point.
=======
5. **Gafni's K+P vs K values without edges** (plan item A8). **Answered for cyl:W×H, 3 ≤ W ≤ 8, H ∈ {6, 7, 8}**
   (new, K40, 2026-10-29; revised after the K40 referee, 2026-10-29; `kings/delegate/out/K40/findings.txt`, hand proofs in
   `PROOF.md`, referee in `VERIFY.md`). Gafni's thesis was not located, and his values (on\*, {on | 0}, 1\*) are known only
   second-hand. So K40 computed the object itself, on larger cylinders than K4, K6 and K8 (boards up to 5×5 and 4–6
   ranks; `kings/REPORT.md`), and its results agree with theirs where the boards overlap in kind.
   - **The object.** In D(X) of §1.2 a lone pawn is a passer, so the component is scored ⊕ at once (BIG). That is wrong
     wherever Black holds. The meaningful component is x in P:
     - a promotion is ⊕;
     - Kxp leaves K v K, after which no decisive event can occur and neither king is ever without a move (PROVED,
       `PROOF.md` Lemma 1; no K v K position without a king move on cyl:3–8×4–8, COMPUTED).

     Its value is read off its results in x ⊞ T (Definition 1.3, plus the chess rule that a side in check may not move
     in T). T ranges over the integers −12…12, on, off, dud, over, under, \*, ↑, ↓, ±1 and on + \*, with White to move and
     with Black to move. Two conventions for a side with no move: **(N)** it loses (the D-semantics), or **(C)** stalemate
     draws (chess, which is P itself).
   - **Checks.** The bare P result of every legal position (T = 0; 1,056,504 positions on cyl:3–8×6 and cyl:3–8×8) agrees in
     K40's `kpsum`, `kp_p --pmodel`, `ref3m` and the referee's own solver, with 0 differences (CHECKED-2). The sum
     results agree position by position between K40's `kpsum.c` and the referee's own solver (`verify/src/vsum.c`,
     written from SPEC.md and Definitions 1.2, 1.3 and 1.5 only): 71,842,272 results (both conventions, all 34 tests,
     integers ±12 on every board), 0 differences (CHECKED-2). The referee also ran H = 7 with the same solver (COMPUTED-1).
   - **Under (N), on 3 and 5–8 files, every (x, s) has one of three signatures** (CHECKED-2 for H = 6, 8; COMPUTED-1 for H = 7):
     - **DEC:** W against every test, which is P_L = W(x ⊞ dud) = W(x ⊞ off);
     - **ON:** the signature of on (also that of on + \*);
     - **DUD:** D against every test.

     The class is fixed by two bits: r(x ⊞ 0) under (N), and r(x ⊞ dud). On cyl:8×8, White to move gives
     110,672 / 35,032 / 14,952 and Black to move gives 82,296 / 36,664 / 47,024. Per placement (White to move / Black to
     move), only DEC/DEC, DEC/ON, DEC/DUD, ON/ON, ON/DUD and DUD/DUD occur.
   - **What is proved by hand** (`PROOF.md`; one AI proof, every step re-checked by one referee of the same model family).
     - Black never wins x ⊞ T: under (C) on every cylinder, and under (N) when W ≠ 4, because White is never stalemated
       there (Lemma 2, Corollary 3). So {on | 0}, the negative numbers and off never occur.
     - DEC = P_L, by Theorem 3.11. Its proof survives the check rule (Proposition 4).
   - **What is computed only.** That an ON position needs no spare tempo and is not hurt by up to 12 Black spares.
     No number and no infinitesimal occurs, so Gafni's on\* and {on | 0} do not appear, and neither does 1\* (against a
     second-hand summary; the source was not located). A tie of on with on + \* cannot be split by these tests.
   - **DUD is "Black can force Kxp against a White who may pass at will".** This holds on every cyl:W×H with W ∈ {3, 6, 8}
     and H ∈ {6, 7, 8}, and on cyl:7×6. On cyl:5×H (30, 100 and 170 positions for H = 6, 7, 8) and cyl:7×H (H = 7: 182,
     H = 8: 378) Black draws instead by a fortress: each king stands on one of the two files at cyclic distance (W−1)/2
     from the pawn's file, the two kings on the same file or on different ones (COMPUTED; the referee reproduced every
     count and the geometry).
   - **The 4-file cylinders are different.** Under (N) they have finite tempo thresholds n ∈ {−4, …, 1} and 28 Black wins
     per board (White stalemated in front of the pawn), as in K6.
   - **Under (C), K+P vs K has no CGT value at many positions.** DEC and DUD are the same sets as under (N) on 3 and
     5–8 files. Almost all of ON (8×8: 33,176 of 35,032 with White to move) becomes tempo-sensitive: the result
     against n is W iff n ≥ θ with θ ∈ {−1, 0, 1} (θ = −1 only for H ∈ {7, 8}), or follows a parity pattern in which W
     depends on whether n is even or odd. A parity pattern is not monotone in n, and r(G + n) is monotone in n for every
     loopy normal-play game G (KNOWN; the strategy argument of Lemma 1.6), so no such G has it.
     - PROVED (Proposition 5): for `Ka6 Pa7 ka8`, Black to move on cyl:W×8 with W ≥ 4 (any H ≥ 4 after a shift of ranks),
       x ⊞ n is a White win iff n < 0 and n is odd. On every board run with W ≥ 4 and H ∈ {6, 7, 8}, the positions with
       this pattern are exactly the W file translates of this one (COMPUTED by K40 and again by the referee).
     - Why: a stalemated Black must spend the spare moves he has. White's three pawn-guarding king squares form a path,
       so White cannot lose a tempo.
     - On the 3-file cylinders all of ON becomes D.

     This is Remark 1.8 seen from the tempo side: Gafni-style values exist only when stalemate loses.
   - **Relation to the KPK table.**
     - Under (N), the table's W set is DEC ∪ ON and its D set is DUD.
     - Under (C), the P table does not determine the class: on cyl:8×8 an ON position with White to move is a P win at
       19,504 positions and a P draw at 15,528.
     - The atlas code `atlas/cylinder/kpk` (8 ranks; for 6 ranks the same code was recompiled with RANKS = 6) differs
       from P at 0.75–3.4% of the positions of the 12 boards (2.5–3.4% on the four boards below). Every difference is
       P = W, atlas = D: 3,440 + 4,824 on cyl:8×8, and 504 + 810, 910 + 1,652, 1,440 + 2,512 on cyl:6×6, 7×6, 8×6
       (White to move + Black to move).
     - All of them come from the atlas scoring a promotion as a draw: when Black's king takes the new queen (Kxq), and on
       4 files also when the new queen stalemates (8 positions per board). With P's promotion rule substituted, the
       atlas code reproduces P at every position, with 0 differences (CHECKED-2: K40's copy and the referee's copy, and
       the referee's own implementation of the atlas rule).
     - Against chess (`kpsolve --cap 1`, exact at every position, COMPUTED-1), the atlas is right everywhere except 24
       positions per board on cyl:4×6 and cyl:4×8, which are chess wins by a rook promotion that the queen-only atlas
       does not credit. So on 3 and 5–8 files every difference is an exact chess draw and a P win: an (A_Q) failure. On
       4 files 24 of the differences are not (A_Q) failures but atlas errors.
     - Every difference is listed in `data/atlas_disagreements.tsv.xz` (27,490 rows; the referee's list is the same set).
   - **Open:** a hand proof of the ON claims (no tempo needed under (N)); a rule for the parity classes beyond the
     family of Proposition 5; and flat boards with Gafni's exact conventions.
>>>>>>> NEW
