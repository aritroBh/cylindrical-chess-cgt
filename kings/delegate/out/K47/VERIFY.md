# K47 VERIFY: independent referee report

Referee task date 2026-11-23. AI work, no human re-derivation. Files written by the referee: this file and `verify/`
(own solver `verify/rz.cpp`, test generator `verify/mktests.py`, small-game solver `verify/small.py`, candidate checks
`verify/cands.py`, `verify/cands275.py`, context predictor `verify/ctxD.py`, comparison `verify/compare.py`, run scripts
`verify/run_*.sh`, logs in `verify/logs/`, replacement edits `verify/EDITS.md`, PIDs `verify/pids.log`). The referee wrote
`rz.cpp` from `kings/SPEC.md` and LOOPY Definitions 1.2, 1.3, 1.5 before opening `src/za.cpp` or `src/zb.cpp`; `za.cpp`
was read afterwards only to explain a difference in node counts (§2.4).

## 0. Verdict

| claim | verdict | label after referee |
|---|---|---|
| 1. Hand proof that q_A is a mutual zugzwang of P ((O3), (O4) at root A) | **GAP, repaired by the referee** (Proposition 2 misses White's reply Kxe5; Black still wins by Kc2, checked by hand and by solver) | PROVED (one AI proof, repaired and re-derived move by move by the referee) |
| "every cyl:Wx6 with W >= 8" | justified (with the repair; one remark about h3) | as stated |
| 2. Model: Z_O as a D-sum component, comparison object over | **right reading, right orientation**, consistent with K40; needs one sentence of caveat | – |
| 2. Z_O != over in D-sums, 38 of 1,100 differences, always for Black | **CONFIRMED**: own solver agrees on all 108 results of the 27 tests run (every kind of difference included); 1...e5-e4 beside * verified with a full line | CHECKED-2 (three implementations on the subset) |
| 3. P contexts, exception `Ph2 pi3 pi5` on cyl:10x6 | **CONFIRMED**: fresh ref3m and kp_p agree on the exception (L L L W) and on 20 more sampled contexts (84 positions, 0 differences); the referee's own over + C predictor agrees with the investigator's | CHECKED-2 |
| 4. EDITS.md | applies cleanly (6 applied, 0 rejected, C4.7 row keeps 4 pipes); content needs the proof repair, a count correction and the model caveat: replacement set in `verify/EDITS.md` | – |

## 1. Hand proof (PROOF.md), re-derived move by move

Board cyl:8x6, White promotes on rank 6, Black on rank 1, Black double steps from rank 5.

**Move lists (§1 of PROOF.md).** Re-derived by hand for q_A (Black: Kc4, Kd3, Ke3, a3; White: Ke6, Kf6, Kg4, Kg5, Kg6,
b3; Kxe4 illegal next to Kf5, c3/c5/d5 covered by b2/b4/e4, Kxe5 next to kd4, Kf4 attacked by e5) and checked for all
eight positions with the referee's solver (`verify/logs/t0_C.out`, P alone): the counts 6, 7, 4, 5 (Black) and 8, 7, 6,
6 (White) and every value and every depth of PROOF.md §5 are reproduced ply for ply (for example root A Black: Kc4 11,
Kd5 15, Ke3 15, a3 11, e4 25, e3 23; q_B White: Kf6 15, Kg4/g5/g6 11, b3 7, e4 13). SOUND.

**Lemma E (White's e-pawn runs).** SOUND. Two Black moves against two White pawn moves; d5/d6 guard e5 and e6; Black
pawns on rank >= 4 need three moves (also b5 with a double step); no Black pawn on the a/b-files attacks the d-file;
no stalemate (king steps back, or a3-a2).

**Lemma F.** SOUND WITH A NOTE. In case (i) with x = c4 Black may also play **Kxb4** (b4 is not guarded in case (i):
b2 covers a3, c3 only). The text "pb5 is blocked by b4" is then false, but the proof goes through unchanged: y = b4 has
dist(b4, d5) = 2, White plays Kd5, and Lemma E's (a), (d) still hold (Black pawns a4, b5). In case (ii) a3 guards b4.
Other replies checked: x = e3 gives y in {d2, d3, e2, f2, f3} (d4, f4 touch e5, e4 guarded); x = c3 (case ii) gives
y in {b2, b3, c2, d2, d3, c4}; only y = c4 touches d5, answered by Kd6.

**Proposition 1** ((O3) at A). SOUND. Kc4/Kd3/Ke3 met by Kxe5 (legal for each), a3 by bxa3 and then Kxe5 (c3 is free
after bxa3, legal too).

**Lemma G (king d3, pawn e3).** SOUND. White's king must reach e1 by its second move via d1, d2, e2, f1, f2: d2, e2
touch d3, f2 (and d2) are attacked by e3, d1/f1 excluded by the hypothesis.

**Lemma G' (king d2, pawn e5).** SOUND, with one remark: if White's third move is Kg2-f2, then e5-e3 gives check; the
check only forces a king move and changes nothing (e3, e2, e1 touch d2).

**Lemma H (after b2-b3).** SOUND. The distance conditions are the right ones: capture a3 at once needs dist(K, a3) <= 1,
block a2 needs dist(K, a2) <= 1, capture a2 needs dist(K, a2) <= 2, block a1 needs dist(K, a1) <= 2; the b3 pawn
attacks a4/c4, not a3; White has no pawn able to promote and gives no check. Distances re-checked: dist(f5, b2) =
dist(f5, b1) = 4; s = e6, f6, g6, g5 give dist to a2 = 4, 4, 4, 3 and to a1 = 5, 5, 5, 4; s = g4 gives dist(g4, a2) = 2
(so the second line), dist(g4, b2) = dist(g4, b1) = 3.

**Proposition 2** ((O4) at A). **GAP, repaired.** After a White king move to s, Black's Kxe4 and White's king move to
w1, the proof plays Kd3 and then always the double step e5-e3 (or Kd2 first). But after Kd3 the pawn e5 is **unguarded**
(d3 does not touch e5, no Black pawn guards it), and if w1 touches e5 White can play **W2 = Kxe5**, a king move of
rank 5 for which the proof says "Black plays e5-e3": impossible, the pawn is gone. This happens for w1 in {d6, e6, f6},
i.e. for s = e6 (w1 = d6, f6), s = f6 (w1 = e6), s = g5 and s = g6 (w1 = f6); only s = g4 is unaffected.

*Repair (referee).* Position: White Ke5, Pb2, Pb4; Black Kd3, pa4, pb5; Black to move. Black plays **Kc2** (c2 is not
covered: b2 covers a3, c3). (i) If White plays b2-b3, then a4xb3, b2, b1: the pawn is guarded by Kc2 on b2 and b1, White's
king (two moves from e5) cannot reach a square next to b2 in time, b4 is blocked by b5, White gives no check. (ii) If
White makes a king move, Black plays Kxb2 and a4-a3, a2, a1: a3, a2, a1 all touch b2, so the king can neither take the
pawn nor stand in front of it (a3 is next to b2, so it cannot be occupied in time either); White's only pawn b4 is blocked
by b5, and from any square next to e5 the king cannot take b5 before its third move after Kc2 (b5's neighbours are on the
a- to c-files), and after Kxb5 it would still need to step aside and play b5, b6, so Black promotes first. White gives
no check (no White pawn can reach a square attacking b2). The referee's solver confirms every step (`verify/logs/gap_C.out`):
`Ke5 kd3 Pb2 Pb4 pa4 pb5` Black to move is a Black win, Kc2 wins in 8 plies (also Kc4, Kd2), and `Kd6 kd3 ...` /
`Kf6 kd3 ...` / `Ke6 kd3 ...` with White to move are lost for White after every move, Kxe5 included (9 plies). With
this case added, Proposition 2 is SOUND, and Corollary 3 follows.

The over-inclusion "w1 = g3 or h3" for s = g4 is harmless: on cyl:8x6 h3 is attacked by a4 (wrap) and illegal, on
W >= 9 it is legal and then needed; its rank-2 successors (g2, h2, and i2 or a2) are covered by Lemma G or by Kd2.

**Remark (no stalemate).** SOUND.

**Widths (§4).** Justified. Every lower bound on a distance (Lemma H, the "not next to d1, e1, f1" conditions, the
repair's race) uses cyclic file distances that do not decrease as W grows, and every upper bound (Kxe5, Kd5/Kd6, Kd3,
Kd2, Kc2) uses squares on files b to f, which do not wrap. The only W-dependent attack is a4's second capture square (h3
on W = 8, the last file on W >= 9); the proof never relies on it. So the hand proof of (O3), (O4) at root A holds on
every cyl:Wx6, W >= 8. (This is not a claim that Z_O is exact on those widths; K45 computed W = 8..12, 14, 16.)

**Labels.** "PROVED" for q_A is right after the repair (one AI proof, repaired and re-derived by the referee). Everything
else in exactness stays CHECKED-2, as PROOF.md says.

## 2. Value in sums

### 2.1 Model and orientation (checked first)

- *Orientation.* over = {0 | over} (Definition 4.4): Left = White has one move to 0, Right = Black passes for ever.
  In Z_O Black's king shuttles d4-d5 (Black's endless passes) and White has the freeze to the mutual zugzwang q (0_D).
  So the comparison object is over, not under, with Left/Right the right way round; the investigator's test game
  "over | 2 | 0: L=1 R=0" is exactly {0 | over} (Black's option loops to the root). Proposition 4.6's over_D (L(omega) =
  {0_D}, R(omega) = {omega}) is the same game. under = {under | 0} would be the group with White shuttling (the colour
  mirror). Comparing with over + G for a further G is not what the claim says; I tested some such G (§2.5).
  ("{0 | over}" in the brief is identical to over by definition, so it is not a separate candidate.)
- *Reading of "Z_O as a D-sum component".* Definition 1.3 needs D-games; Definition 1.5 gives D(X) of a K+P position by
  making the punished moves of the king group terminals. Under that reading Z_O is over_D by construction (its
  non-shuttle, non-freeze moves are suicides, deleted by Lemma 1.7; q has only suicides, i.e. 0_D), and the test would
  be empty. The only non-trivial reading is the investigator's: the P game of the group's own pieces as a loopy D-game,
  with K40's conventions (promotion = terminal for the promoter, a side in check may not move in T, a move in T clears
  the e.p. right, no move at all = loss under N). This is K40's convention verbatim (`K40/findings.txt` §0: "a test-game
  move is illegal while in check", conventions N and C) and is compatible with K44, whose LK sums are D-sums of a game
  in which both kings move. So the model is right, but the result must be read as "the P game of Z_O is not over", and
  LOOPY should say so: a move that "loses at once" in Definition 4.8's sense (the position after it is lost in P alone)
  is a real move in a sum and can win there (1...e5-e4). The replacement edits add this sentence.
- *Comparison of the over tables.* The investigator's r(over + T) equals the referee's `verify/small.py` on all 108
  results of the 27 tests (§2.2).

### 2.2 Referee's re-run (own solver)

`verify/rz.cpp` (mailbox board, open-addressing hash of placements, e.p. target stored only when a capture is
possible, forward and reverse CSR lists, one counting retrograde pass per test game over (node, T-node, side to move);
predecessors through T moves include the e.p. variants of a node). Validation: with T = 0 and convention C (P alone) it
reproduces the eight positions of Definition 4.8 move for move with K45's/K47's values and depths (§1).
Runs (all through `heavy.sh`, nice 15): `verify/logs/main_N.out` (27 tests, 31 s, 1.25 GB), `pv_star.out`,
`pv_under.out`, `pv_down.out`, `t0_C.out`, `gap_C.out`.

Tests (own definitions, `verify/tests_ref.txt`): 0, *, up, down, pm1, over, under, on, off, dud, -3..3, and the sums
*+down, *+up, *+under, up+under, down+under, under+under, down+down, 1+pm1, *+*, over+*, over+under. Both roots, both
sides: **108 results; Z agrees with the investigator's table (`logs/full_A_N.out` = `full_B_N.out`) at all 108; over
agrees at all 108; 0 disagreements** (`verify/logs/compare.out`). Z differs from over at 30 of the 108, exactly the
investigator's differences restricted to these tests: (*, A, b); down at (A, w), (A, b), (B, b); under and the five
sums with under, all four results each (Z = L, over = D); *+down (A, b); *+up (A, b); down+down (A, w), (A, b),
(B, b); 1+pm1 (A, b). Together with 0+*, 0+down, 0+under (the same games as *, down, under) this covers all 38
differences of findings.txt §2. In every difference Z = L, over = W or D. The two roots differ from each other on the
subset at (*, b), (down, w), (*+down, b), (*+up, b), (down+down, w), (1+pm1, b), consistent with the investigator's 8
(the other two are 0+* and 0+down).

### 2.3 The example 1...e5-e4 beside * (verified)

Root A, Black to move, T = *: Black wins only by 1...e5-e4 (all other Z moves and the move * -> 0 lose for Black;
`pv_star.out`). A longest line (White resists longest, Black wins fastest):
1...e5-e4 2.Kf4 (the move that wins in P alone) **Black plays * -> 0** 3.Kf5 Ke3 4.Ke5 Kxe2 5.Kxe4 Kd2 6.Kd4 Kc2
7.Kc5 Kxb2 8.Kxb5 a3 9.Ka4 a2 10.K any a1 (promotion). In P alone the same 1...e4 loses in 25 plies; the spare tempo
puts White in zugzwang after 2.Kf4. Beside under the line is the same with under -> 0 as Black's tempo (`pv_under.out`;
taking under -> 0 also removes White's passes), and beside down Black spends down -> 0 (`pv_down.out`).

### 2.4 Node counts

The referee's component has 2,931,946 nodes = **2,853,540 placements** + 78,406 nodes with a capturable e.p. target
(19,789,873 White and 20,246,969 Black non-promoting moves; 834,750 and 930,471 promotion moves; `verify/logs/stats.err`).
The investigator's "3,914,687 placements" is the number of za's nodes, in which every double step keeps its e.p. target
whether or not a capture is possible (za.cpp `build`, read after the referee's runs), so 1,061,147 of them are e.p.
variants; it is not a count of placements. Values do not depend on this. The bisimulation figure (3,397,278 classes) is
of za's node graph. The replacement edits state the placement count.

### 2.5 What is Z_O? (candidates, COMPUTED-1, referee)

`verify/cands.py`, `verify/cands275.py` (`verify/logs/cands.out`, `cands275.out`) compare candidate short or loopy games
G (results of G + T by `small.py`) with the Z column. Against the investigator's full 275-game table (550 results per
root): root A has the results of **tiny-2 = {0 || 0 | -2}** at 550 of 550 (also tiny-3 and tiny-4; tiny-1 differs once,
1+pm1 with Black to move; up^2 differs at 9, up^2* at 8). On the referee's 27 tests root A differs from over, over + *,
over + down, over + up, {0 | over + *}, over + down + * and over + tiny-1 at 11 tests each, and from 0, *, up, down,
up* at 2 to 8. Root B has the results of **up^2* = {0 | up*} + *** at 550 of 550 (up^2 differs at 5, up* at 13, tiny-2
at 8); on the 27 tests it differs from over and its variants at 7. These are signatures on a finite battery, not
values; the battery cannot tell tiny-2 from tiny-3 or tiny-4. No claim is made beyond the tables.

## 3. P contexts

Re-check on cyl:10x6 of the exception and of 20 other contexts drawn (seed 4747) from the investigator's 199 agreeing
ones (`verify/ctx_ref.pos`, 84 positions), with ref3m compiled freshly from `K23/verify/ref3m.cpp`
(`verify/logs/ctx_ref.ref3m`), and an independent predictor of r(over + C) written by the referee (`verify/ctxD.py`: C
as a pawn-only D-game, e.p. on, promotion terminal, product with over_D; `verify/logs/ctx_ref_compare.out`).
- ref3m: all 84 values equal the investigator's ref3m and kp_p values (0 differences).
- `Ph2 pi3 pi5`: P = L L L W at (d4, b), (d4, w), (d5, b), (d5, w); the referee's predictor gives r(over + C) = W with
  White to move, L with Black to move (the investigator's prediction). So the exception is real: at the d4 root with
  White to move P is a Black win where over predicts a White win; at the d5 root P follows over. CONFIRMED.
- The 20 other contexts: P = r(over + C) in all 20 (by the referee's predictor; patterns W W W W 7, L L L L 8,
  L W L W 5).
- kp_p --pmodel (freshly compiled from `K44/scripts/kp_p10.c`, `--moves`, `verify/logs/ctx_exc.kpp`; 146 s, 0.81 GB):
  the exception gives L L L W as well. At the d4 root with White to move all 11 White moves lose (the six group moves,
  the freezes e2-e4 and e2-e3, and h2-h3, h2-h4, h2xi3); at the d5 root only h2xi3 wins. With Black to move Black wins
  at both roots (d4: Kc4, Ke3, i2, ixh2, a3, e4, e3; d5: Kd4, Kc4, i2, ixh2, a3, e4, e3). CONFIRMED by two solvers.
- kp_p --pmodel on all 84 positions (`verify/logs/ctx_ref.kpp`; 712 s, 1.38 GB peak, bounds exact): equal to the
  referee's ref3m at all 84 (0 differences).
The investigator's D-sum column r(Z_O + C) (COMPUTED-1) was not re-run; the edits keep its label.

## 4. EDITS.md

Applies cleanly to the current LOOPY.md (copy in a temp dir outside the repository; `apply_edits.py`: 6 applied, 0
rejected; the C4.7 row keeps 4 pipes; 118 table lines before and after). LOOPY.md changed during the review (a K54
paragraph near line 34); both the investigator's set and the referee's replacement set were re-applied to the new copy:
6 applied, 0 rejected each, cell counts unchanged. Every OLD anchor occurs exactly once. Numbers
checked against §§1-3: 275 tests, 1,100 results, 38 differences, 1,062 agreements, 8 of 550 root pairs, 63 and 200
contexts, 199 agreeing, 4 and 5 D-sum separations (the last two COMPUTED-1, not re-run by the referee). Needed changes
(full replacement set in `verify/EDITS.md`, same anchors, all short):
1. the hand-proof sentence of the K47 bullet: add the Kxe5 case (Kc2, Kxb2 and the a-pawn) and say the proof was repaired
   and re-derived by the referee; the status row and §8 item 2 say "PROVED by hand after a referee repair" / keep
   "PROVED by hand";
2. "3,914,687 placements (bisimulation quotient ...)" replaced by "2,853,540 placements (3,914,687 nodes when every e.p.
   target is kept)"; the quotient figure dropped from LOOPY (it stays in findings.txt);
3. one sentence on the reading: the non-freeze moves are real moves, not terminals; in the D-model of Definition 1.5
   the group would be over_D by construction;
4. the referee's third solver (108 results) and the candidate signatures (tiny-2 at the d4 root, up^2* at the d5 root,
   COMPUTED-1) added; "the d4 root with Black to move is a Black win only by 1...e5-e4 ... when Black spends * after
   2.Kf4" made precise; VERIFY.md added to the file list.
No other number changes. K48 will edit the same passages; all anchors were kept as in the investigator's set.

## 5. Process

- Heavy runs only through `kings/delegate/heavy.sh` (nice 15). Peaks: rz 1.25 GB. **ref3m on the 84 cyl:10x6 context
  positions peaked at 4.75 GB** (813 s), above the 3 GB limit; the referee had not measured it beforehand. On seeing it,
  the referee stopped its own run (the following `ref3m --moves` step) and ran kp_p alone under a wrapper that kills it
  (own PID only) above 2.9 GB (peaks 0.81 GB and 1.38 GB, never killed). The investigator ran the same ref3m binary on 800 positions of the same board
  (`run_ctx.sh`, no memory log); that run very probably exceeded 3 GB as well.
- PIDs in `verify/pids.log`. The referee killed only its own processes, by recorded PID: the context run once to let the
  short main run go first (54353, 54604, 54606, 54607; restarted), and once after the memory overrun (63964, 70272, 77224,
  77225). Nothing else was killed, no pattern kill.
- Binaries built by the referee (`verify/rz_k47ref`, `verify/rzs_k47ref`, `verify/kpp_k47ref`, `verify/ref3m_k47ref`) were
  deleted by exact name at the end; no output file exceeds 256 KB.
- No git.
