# Mechanisms behind the 34 V2 failures, and a corrected passer test (avenue 3)

Output folder: `research/v2_mechanisms/`. All numbers are on the 7x6 cylinder sweep unless a board is named
(`kings/results/exp_cyl7x6_epon_Q_conv.jsonl`, queen-only promotion, e.p. on, trebuchet `Pa3 pa4 Kg4 kb3`, P on files d, e).

## 1. Summary (5 lines)

1. **Mechanism: 34 of 34 (100%) of the "passed pawn does not win at once" failures are one mechanism, a "step-past race".**
   The pawn that the convention calls decisive is not beaten by a capture, a king or a stalemate. The opponent's pawn is
   statically blocked (so it is not "passed"), steps level with its blocker, becomes passed, and promotes first.
   In all 34, Y (the side the convention says loses) is to move at the decisive node, d_Y = 2 and n_X is 2 or 3.
   No other candidate (stalemate, passer captured, blockade, covered promotion square, check, underpromotion) occurs in the frozen game.
2. **A computable local test removes all 52 convention failures relative to the exact frozen game, and 31 of the 52 relative to real chess.**
   Certified-passer convention CC: a passer ends the game only if n <= d (mover is X) or n < d (mover is Y), with
   n = the passer's own distance to promotion and d = the *unobstructed* distance of the fastest enemy pawn; otherwise play on.
   Mismatches with real chess on the 500 testable components fall from **159/500 to 128/500** (7x6: 143/448 to 112/448); with the e.p.-aware baseline 154/500 to 128/500.
   No component that matched before mismatches after (341 matches stay matches).
3. **The other 21 of the 52 are not repaired in real chess, because free kings change the result as well (8 of the 34 rows, 13 of the 18 e.p. rows).**
   After CC every remaining mismatch is a king effect (frozen = CC, real differs): 128 of 128. The real-chess mechanism of the 8 step-past rows with a king overlay is **not diagnosed** (cap 1 bounds are uninformative; cap 2 does not fit, section 6).
4. **The test is sound, checked exhaustively.** The square rule S certified a false passer in 0 of 158,544 (position, side-to-move, e.p.) cases on 2-3 files and 6-8 ranks,
   and in 0 of the 28 false passers of the actual sweep; it certifies 492/536 = 91.8% of the true one-sided passers (the run-the-passer search RP: 524/536 = 97.8%). The e.p.-aware passed test is required: with the textbook test S is wrong at 8 e.p. nodes.
5. **Checks of the tools:** my Python frozen-king game agrees with `kings/kpsolve --frozen` on all 1,792 root values and all 2,932 pawn-move values (3 boards); my re-implementation of the cylcgt convention agrees with the stored cylcgt outcome on 1,792/1,792 rows (2 passed tests x 896). The 90 distinct positions on the 34 refuting lines were re-solved by kpsolve with zero disagreements.

## 2. Definitions

* **FG** (frozen-king game): kings may not move (a king move loses at once), a promotion wins at once, a side with no pawn move loses. This is `kpsolve --frozen`.
* **CG** (the convention): cylcgt's pawn game, a passed pawn is an immediate win, two passed pawns are a race decided by `promote_distance` ("count").
* **Disputed side:** a (component, side to move) where CG and FG give different results. The 34 rows are the 7x6 rows that are `MISMATCH` against real chess, have frozen != convention, and are *not* repaired by the e.p.-aware passed test (52 minus the 18 e.p. rows). Each has exactly one disputed side, so 34 rows = 34 disputed sides.
* **N\*:** the first decisive node on the line where X (the convention's winner) plays CG-winning moves and Y plays FG-winning moves. CG says X wins at N\*, FG says Y wins.
* **n_X, d_Y:** X's passer needs n_X own moves to promote (double step counted); d_Y is the fewest moves any Y pawn would need if nothing stood in its way.
* **S (square rule)** and **RP (run the passer)** are the two certificates; **CC** is CG with "passed" replaced by "certified" (play on when not certified).

## 3. Method (exact commands, project root `/Users/aritro/Downloads/Research/Chessendgames`)

All Python was run as `python3 -I <script>` from `research/v2_mechanisms/` (no bytecode written; `kings/`, `cylcgt/` untouched). Every `kpsolve` call is under `nice -n 15`, one at a time; PIDs are in `logs/kpsolve.pid`.

1. `validate.py`: runs `kings/kpsolve --board <b> --ep on --promote Q --cap 1 --frozen --moves` on every stored root (cyl:7x6, cyl:6x6, flat:5x6) and compares root values and every pawn-move value with `pawngame.py` (FG); also compares `pawngame.cg` with the stored cylcgt outcome for the textbook and e.p.-aware tests. Result in `validate_result.json`.
2. `mechanisms.py`: selects the 52 rows (`verdict_textbook == MISMATCH and not frozen_matches_convention`), splits them 34 / 18 by whether the e.p.-aware prediction equals the frozen result, finds N\* by the rule above, extracts Y's frozen principal line, labels the mechanism by script, and re-solves all 90 distinct positions on the lines with `kpsolve --frozen` (0 disagreements). Output `mechanisms_34.jsonl`, `mechanism_histogram.json`, table in section 4 (`tables_34.md`).
3. `census.py`: every decisive node of the convention's trees (all roots, both sides, both passed tests): CG verdict vs FG truth vs S and RP. Output `census_result.json`.
4. `cc.py`: exhaustive soundness of S and RP (every placement of up to 3 v 3 pawns on 2 files x 6 ranks, 2 x 2 on 3 x 6, 3 v 3 on 2 x 8 and 1 x 8, plus every legal single e.p. right, both sides to move), then CC for all 896 sweep rows with assertions CC = FG. Output `cc_result.json`.
5. `rescore.py`: before/after table on the 500 testable components (+ the race-at-start rows). Output `rescore_result.json`, `rescore_rows.jsonl`.
6. `realking.py 1` (cap 1, 8 roots, then their pawn-move children) and `realking2.py 2 0,2,7 2` (cap 2 pilot, 3 roots) for the real-king overlay (section 6). `fg2.py`: a negative probe (section 6).
7. Memory of the first kpsolve run, `/usr/bin/time -l`: cap 1, one real root, 233 MB maximum resident set, 45 s. Cap 2, same root: 1.10 GB, not finished after 1,561 s (stopped by PID).

## 4. The 34 failures

Histogram (row-level primary mechanism, sums to 34):

| Mechanism | Rows |
|---|---|
| STEP_PAST_RACE (a statically blocked Y pawn steps level with its blocker, is then passed, and wins the race) | **34** |
| NO_MOVE_LOSS, EP_CAPTURE, PASSER_STUCK_BEHIND_OWN_PAWN, CAPTURE_FREES_RUNNER, UNCOUNTED_RACE, OTHER | 0 each |

How the decisive node arises: 28 rows have the passer on the board at the root with Y to move; 4 rows, X creates the passer by a push (d3-d4 type); 2 rows, X creates it by a capture (d2xe3, d5xe4).
Race arithmetic at N\*: Y is to move in all 34, d_Y = 2 in all 34, n_X = 2 in 28 and n_X = 3 in 6. Y wins 3 plies later in every case (pv length 3: step, X move, promote). The square rule S refuses to certify X at N\* in 34 of 34 (and so does RP).
Y never needs a capture (0 of 34). X's passer is the front pawn of its file in 34 of 34.

Manual check: I replayed `W: d2 d3 / B: e3`, Black to move. The convention calls d3 passed (e3 is level, not ahead) and e3 blocked (d2 is below it), so it scores +BIG. Black plays e3-e2: d2 is now level, so e2 is passed and needs one more move. White's d3 needs three. Black promotes first. The same shape underlies all 34 rows (checked by reading the table below and by the kpsolve re-solve).

Why d_Y = 2 everywhere: on 6 ranks with ranks 2..5 populated, a blocked pawn that is one step from unblocking is at rank 3 (Black) or 4 (White), two moves from promotion. The 100% uniformity is therefore partly a property of this small board and of the 2-file component, not a general law. A taller board could give other shapes (not tested).

Real-chess status of the 34 rows (stored exact cap-2 sweep values): real = frozen at both sides in **26 of 34** rows (so for these the step-past race is also the real-chess mechanism); in **8 rows** a king effect adds to it (4 rows at the disputed side itself, 4 at the other side). The overlay table is in section 6.

Per-side table (mover = side to move at the root, convention and exact frozen result are for that mover):

| # | component P (7x6 cylinder) | mover | convention | exact frozen | decisive node N* the convention declares won | n_X | d_Y | Y's winning line | real = frozen at this side? | real = frozen at both sides? |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | W: d2 d3 / B: e3 | B | White wins | Black wins | W: d2 d3 / B: e3 (B to move) | 3 | 2 | B:e3-e2 W:d3-d4 B:e2-e1 | yes | yes |
| 2 | W: d2 d4 / B: e3 | B | White wins | Black wins | W: d2 d4 / B: e3 (B to move) | 2 | 2 | B:e3-e2 W:d4-d5 B:e2-e1 | yes | yes |
| 3 | W: d2 e4 / B: e3 | B | White wins | Black wins | W: d2 e4 / B: e3 (B to move) | 2 | 2 | B:e3-e2 W:e4-e5 B:e2-e1 | yes | yes |
| 4 | W: d4 e2 / B: d3 | B | White wins | Black wins | W: d4 e2 / B: d3 (B to move) | 2 | 2 | B:d3-d2 W:e2-e4 B:d2-d1 | yes | yes |
| 5 | W: e2 e3 / B: d3 | B | White wins | Black wins | W: e2 e3 / B: d3 (B to move) | 3 | 2 | B:d3-d2 W:e3-e4 B:d2-d1 | yes | yes |
| 6 | W: e2 e4 / B: d3 | B | White wins | Black wins | W: e2 e4 / B: d3 (B to move) | 2 | 2 | B:d3-d2 W:e4-e5 B:d2-d1 | yes | yes |
| 7 | W: d4 / B: d3 e5 | W | Black wins | White wins | W: d4 / B: d3 e5 (W to move) | 2 | 2 | W:d4-d5 B:e5-e4 W:d5-d6 | yes | yes |
| 8 | W: d4 / B: e3 e5 | W | Black wins | White wins | W: d4 / B: e3 e5 (W to move) | 2 | 2 | W:d4-d5 B:e5-e4 W:d5-d6 | yes | yes |
| 9 | W: d4 / B: e4 e5 | W | Black wins | White wins | W: d4 / B: e4 e5 (W to move) | 3 | 2 | W:d4-d5 B:e4-e3 W:d5-d6 | yes | yes |
| 10 | W: e4 / B: d3 d5 | W | Black wins | White wins | W: e4 / B: d3 d5 (W to move) | 2 | 2 | W:e4-e5 B:d5-d4 W:e5-e6 | yes | yes |
| 11 | W: e4 / B: d4 d5 | W | Black wins | White wins | W: e4 / B: d4 d5 (W to move) | 3 | 2 | W:e4-e5 B:d4-d3 W:e5-e6 | yes | yes |
| 12 | W: e4 / B: d5 e3 | W | Black wins | White wins | W: e4 / B: d5 e3 (W to move) | 2 | 2 | W:e4-e5 B:e3-e2 W:e5-e6 | yes | yes |
| 13 | W: d2 d3 / B: e3 e4 | W | White wins | Black wins | W: d2 d4 / B: e3 e4 (B to move) | 2 | 2 | B:e3-e2 W:d4-d5 B:e2-e1 | yes | yes |
| 14 | W: d2 d4 / B: d3 e3 | B | White wins | Black wins | W: d2 d4 / B: d3 e3 (B to move) | 2 | 2 | B:e3-e2 W:d4-d5 B:e2-e1 | yes | NO |
| 15 | W: d2 d4 / B: e3 e4 | B | White wins | Black wins | W: d2 d4 / B: e3 e4 (B to move) | 2 | 2 | B:e3-e2 W:d4-d5 B:e2-e1 | yes | yes |
| 16 | W: d2 e2 / B: d3 e3 | W | White wins | Black wins | W: e2 e3 / B: d3 (B to move) | 3 | 2 | B:d3-d2 W:e3-e4 B:d2-d1 | yes | yes |
| 17 | W: d2 e4 / B: d3 e3 | B | White wins | Black wins | W: d2 e4 / B: d3 e3 (B to move) | 2 | 2 | B:e3-e2 W:e4-e5 B:e2-e1 | yes | yes |
| 18 | W: d2 e4 / B: d4 e3 | B | White wins | Black wins | W: d2 e4 / B: d4 e3 (B to move) | 2 | 2 | B:e3-e2 W:e4-e5 B:e2-e1 | yes | yes |
| 19 | W: d3 d4 / B: e3 e5 | W | Black wins | White wins | W: d3 d4 / B: e3 e5 (W to move) | 2 | 2 | W:d4-d5 B:e5-e4 W:d5-d6 | yes | yes |
| 20 | W: d3 d4 / B: e4 e5 | B | Black wins | White wins | W: d3 d4 / B: e3 e5 (W to move) | 2 | 2 | W:d4-d5 B:e5-e4 W:d5-d6 | yes | yes |
| 21 | W: d3 e4 / B: d5 e3 | W | Black wins | White wins | W: d3 e4 / B: d5 e3 (W to move) | 2 | 2 | W:e4-e5 B:e3-e2 W:e5-e6 | yes | yes |
| 22 | W: d4 e2 / B: d3 e3 | B | White wins | Black wins | W: d4 e2 / B: d3 e3 (B to move) | 2 | 2 | B:d3-d2 W:d4-d5 B:d2-d1 | yes | NO |
| 23 | W: d4 e2 / B: d3 e4 | B | White wins | Black wins | W: d4 e2 / B: d3 e4 (B to move) | 2 | 2 | B:d3-d2 W:e2-e3 B:d2-d1 | yes | yes |
| 24 | W: d4 e3 / B: d3 e5 | W | Black wins | White wins | W: d4 e3 / B: d3 e5 (W to move) | 2 | 2 | W:d4-d5 B:e5-e4 W:d5-d6 | yes | yes |
| 25 | W: d4 e4 / B: d3 d5 | W | Black wins | White wins | W: d4 e4 / B: d3 d5 (W to move) | 2 | 2 | W:e4-e5 B:d3-d2 W:e5-e6 | NO | NO |
| 26 | W: d4 e4 / B: d3 e5 | W | Black wins | White wins | W: d4 e4 / B: d3 e5 (W to move) | 2 | 2 | W:d4-d5 B:d3-d2 W:d5-d6 | yes | yes |
| 27 | W: d4 e4 / B: d5 e3 | W | Black wins | White wins | W: d4 e4 / B: d5 e3 (W to move) | 2 | 2 | W:e4-e5 B:e3-e2 W:e5-e6 | yes | NO |
| 28 | W: d4 e4 / B: d5 e5 | B | Black wins | White wins | W: d4 / B: e4 e5 (W to move) | 3 | 2 | W:d4-d5 B:e4-e3 W:d5-d6 | yes | yes |
| 29 | W: d4 e4 / B: e3 e5 | W | Black wins | White wins | W: d4 e4 / B: e3 e5 (W to move) | 2 | 2 | W:d4-d5 B:e3-e2 W:d5-d6 | yes | NO |
| 30 | W: e2 e3 / B: d3 d4 | W | White wins | Black wins | W: e2 e4 / B: d3 d4 (B to move) | 2 | 2 | B:d3-d2 W:e4-e5 B:d2-d1 | NO | NO |
| 31 | W: e2 e4 / B: d3 d4 | B | White wins | Black wins | W: e2 e4 / B: d3 d4 (B to move) | 2 | 2 | B:d3-d2 W:e4-e5 B:d2-d1 | yes | yes |
| 32 | W: e2 e4 / B: d3 e3 | B | White wins | Black wins | W: e2 e4 / B: d3 e3 (B to move) | 2 | 2 | B:d3-d2 W:e4-e5 B:d2-d1 | NO | NO |
| 33 | W: e3 e4 / B: d3 d5 | W | Black wins | White wins | W: e3 e4 / B: d3 d5 (W to move) | 2 | 2 | W:e4-e5 B:d5-d4 W:e5-e6 | yes | yes |
| 34 | W: e3 e4 / B: d4 d5 | B | Black wins | White wins | W: e3 e4 / B: d3 d5 (W to move) | 2 | 2 | W:e4-e5 B:d5-d4 W:e5-e6 | NO | NO |

## 5. The corrected test and the re-score

**Certificates** (X's front, e.p.-aware passed pawn; n = its moves to promote, d = fewest moves any Y pawn would need ignoring obstruction):

* **S:** X wins if n <= d when X is to move, n < d when Y is to move. **PROVED** in the frozen-king pawn game: a passed front pawn can neither be blocked nor captured (no enemy pawn is ahead of it on its file or an adjacent file, enemy pawns only move down, and a pawn that could take it e.p. would be ahead of it, so is excluded), X always has the move of the passer, and Y cannot promote in fewer than d moves. If Y has no pawn move he loses (a king move loses at once). This is a proof sketch written here, not referee-checked. It is false in real chess in general (a king can stop a certified passer), so S certifies only the frozen game.
* **RP:** X only pushes the passer; a full search over every Y pawn reply shows Y cannot promote first. S implies RP (0 of 158,544 exhaustive cases and 0 sweep nodes where S held and RP did not, with the e.p.-aware test).
* Neither is complete: the passer may win without being certified (a Y pawn that is nearer but permanently blocked).

**Exhaustive soundness** (`cc.py`, COMPUTED-1 using the FG engine that kpsolve cross-checks):

| Placements | (position, side, e.p.) cases | S certified | RP certified | S wrong | RP wrong |
|---|---|---|---|---|---|
| 2 files x 6 ranks, <= 3 v 3 pawns | 9,858 | 7,768 | 7,836 | 0 | 0 |
| 3 files x 6 ranks, <= 2 v 2 | 15,350 | 11,922 | 12,240 | 0 | 0 |
| 2 files x 8 ranks, <= 3 v 3 | 131,886 | 96,286 | 97,922 | 0 | 0 |
| 1 file x 8 ranks, <= 3 v 3 | 1,450 | 996 | 1,034 | 0 | 0 |

(Certified counts are per (case, side X): a case can contribute up to two.)

**Census of the decisive nodes of the 7x6 convention trees** (e.p.-aware test; FG is the truth):

| Node type | CG right | CG wrong | S certifies, CG right | RP certifies, CG right | S or RP certifies, CG wrong |
|---|---|---|---|---|---|
| one-sided passer | 536 | 28 | 492 (91.8%) | 524 (97.8%) | 0 and 0 |
| both passed (race, "count" rule) | 16 | 0 | 16 | 16 | n/a |

So all 28 false passers of the sweep are refused by both certificates. With the *textbook* passed test S certifies 4 + 4 false passers (the e.p. nodes); RP does not. This is why the e.p.-aware test must be part of the certificate.
On the 6x6 and 5x6 boards all 20 decisive nodes are right (S certifies 18 of 20).

**CC = exact frozen game.** CC expands every passed pawn that is not certified, so by soundness CC equals FG at every root; asserted on all 896 rows (including the 358+16+16 race-at-start rows that cylcgt cannot score). Cost: on 7x6 the 1,710 CC nodes contain 68 passed-but-uncertified nodes that must be expanded with S (40 with RP).

**Re-score of the 500 testable components** (real = exact cap-2 sweep value; before = stored textbook verdict; the e.p.-aware verdict is the second column):

| Board | Testable | Mismatch, textbook | Mismatch, e.p.-aware | Mismatch with CC | Matches that stay matches | Mismatch -> match | Match -> mismatch |
|---|---|---|---|---|---|---|---|
| 7x6 cylinder | 448 | 143 | 138 | **112** | 305 | 31 | 0 |
| 6x6 cylinder | 26 | 13 | 13 | 13 | 13 | 0 | 0 |
| 5x6 ordinary | 26 | 3 | 3 | 3 | 23 | 0 | 0 |
| **all** | **500** | **159** | **154** | **128** | 341 | 31 | 0 |

Classification of every mismatch.

* Before (159): 107 king effects (frozen = convention), 34 step-past races, 18 e.p.
* After (128): 128 king effects (CC = frozen, real differs): the original 107, plus 21 that were hidden behind a convention failure (8 step-past rows, 13 e.p. rows). Of these 128, 111 have a drawn real result at one or both sides and 17 are decisive at both sides.
* The 52 convention failures: all 52 are removed relative to FG; 31 of them (26 of the 34, 5 of the 18) become real-chess matches, 21 do not.
* Not diagnosed by this task: the real-chess cause of the 112 + 13 + 3 remaining mismatches (the 7x6 per-move diagnosis is deferred in `kings/results/analyze_7x6.log`; the 6x6 and 5x6 ones are in `kings/REPORT.md` section 4).

Extra (not part of the 500): CC scores the race-at-start components, which cylcgt raises `RaceError` on. Against the exact real values it matches 222 of 298 (7x6), 8 of 14 (6x6), 7 of 12 (5x6), 237 of 324 together (73%). There is no baseline to compare with, so this is only a description.

## 6. What was not determined

* **Real-king mechanism of the 8 step-past rows with a king overlay.** The 8 sides (roots where real != frozen) are rows 14, 22, 25, 27, 29, 30, 32, 34 of the table (listed by P: `d2 d4/d3 e3` w, `d4 e2/d3 e3` w, `d4 e4/d3 d5` w, `d4 e4/d5 e3` b, `d4 e4/e3 e5` b, `e2 e3/d3 d4` w, `e2 e4/d3 e3` b, `e3 e4/d4 d5` b; stored real results: L, D, D, D, W, D, D, D against frozen W, W, W, L, L, L, L, W).
  * Cap 1 (`realking_cap1.json`, 456 s + 414 s, 1.56 GB): bounds differ at the root of all 8 sides (A and B disagree, mostly W against L), so the per-move values are mostly "?" and no mechanism can be read. This reproduces the finding in `kings/results/analyze_7x6.log`.
  * Cap 2: a single root did not finish in 1,561 s (1.10 GB, stopped by PID); a 3-root pilot with 2 threads (`realking2.py`) reached the 3.8 GB watchdog after about 22 min and was stopped. The 8-root run would take more than the 3 CPU-hour budget, so I stopped.
  * One cheap observation from cap 1 only, not a result: for `e2 e3/d3 d4`, White to move, the only non-losing root move is the pawn capture e2xd3 (value D), after which Black's only non-losing reply is d4xe3, and the king moves all lose for Black. So in that row the real draw comes from a pawn line, not from a king escape, and is consistent with a second promotion (two queens) rather than with a king interference. This is a CONJECTURE.
* **A crude fix for that second-promotion effect fails.** `fg2.py` scores the frozen game with "a promotion draws if the opponent can promote on his next move". On the 746 exact 7x6 rows it fixes 70 of the 188 rows where FG != real but breaks 223 of the 558 where FG = real (FG2 matches 405, FG matches 558). So this simple rule is wrong; (A_Q) needs a geometric condition (queen attacks, king distance) that was not attempted.
* The certificates are proved only for the frozen-king pawn game with queen-only promotion, one component, and no other component (no sums, nothing about (V4)). I tested boards of 5-8 ranks and at most 3 files; the 34 failures all come from one 2-file, 6-rank board.
* The 6 undetermined 7x6 rows (cap bounds differ) and the 358 race-at-start rows are not scored against the convention.

## 7. Labels

| Claim | Label |
|---|---|
| Python FG = kpsolve --frozen: 1,792 roots, 2,932 pawn-move values, 3 boards | **CHECKED-2** |
| Python CG = stored cylcgt outcome, 1,792 rows (textbook and e.p.-aware) | **CHECKED-2** |
| Frozen values on the 90 positions of the 34 lines | **CHECKED-2** (kpsolve and the scratch engine) |
| 34 of 34 rows are step-past races (labels by script, read by hand) | **COMPUTED-1** |
| S is sound in the frozen-king pawn game | **PROVED** (sketch here, not referee-checked) |
| S and RP are never wrong in 158,544 exhaustive cases and the sweep | **COMPUTED-1** |
| CC = FG on all 896 rows; re-score 159 -> 128 of 500 | **COMPUTED-1** |
| Real = frozen at both sides in 26 of the 34 rows | **COMPUTED-1** (from the stored cap-2 sweep) |
| The 8 overlay rows: real-king mechanism | **not determined** |
| Second promotion (two queens) explains the draws | **CONJECTURE** (one cap-1 observation; a crude rule failed) |

## 8. Files

`pawngame.py` (FG, CG engine), `tests.py` (S, RP), `cc.py`, `census.py`, `mechanisms.py`, `rescore.py`, `validate.py`, `kp.py`, `realking.py`, `realking2.py`, `fg2.py`, `make_tables.py`; results `validate_result.json`, `mechanisms_34.jsonl`, `mechanism_histogram.json`, `tables_34.md`, `census_result.json`, `cc_result.json`, `rescore_result.json`, `rescore_rows.jsonl`, `realking_cap1.json`; logs in `logs/` (including `kpsolve.pid`). No file over 5 MB, nothing to compress.
