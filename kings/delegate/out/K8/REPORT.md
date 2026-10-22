# K8: does stalemate explain when spare tempo matters?

**Verification status (added by the orchestrating session, 2026-10-22).** K8v
([../K8v/REPORT.md](../K8v/REPORT.md)) re-ran everything with the independent K6 verifier pipeline, with its own
chess-rule solver and a third pure-Python solver, and found 0 differences. That covers 11 normal-play boards, 13
chess-rule boards and 17 boards under four mixed stalemate rules. So every count below is **CHECKED-2**, apart
from the items K8v lists as not re-checked: the shortest-line statistics, `audit.py`, and the 27 K4/K6 boards,
which were only re-tabulated.

Two overreaches in the agent's text are corrected here, as K8v found them:
- "tempo matters nearly everywhere" (the share is 10%–34%);
- "5- to 8-file cylinders" under the chess rule (only 5–7 files were run).

Who did what: Codex (gpt-6-luna) started the task and ran out of quota. A Sonnet 5.5 agent was interrupted, and a
second Sonnet agent finished it and wrote this text. Workflow `wf_88f941cd-f34`.

Everything below is COMPUTED-1 unless marked PROVED (a one-line argument, given in section 4). One implementation (a copy of the K4/K6 pipeline), checked against kpsolve (C) at T = 0 and, for the product solver itself, against a naive solver that shares no code with it (section 6). A separate verifier is expected to re-check it.

## Summary (5 lines)

1. **Task 1: 8 of 8 predictions confirmed.** cyl 5x4, 3x7, 5x7, 3x8 have an empty off/off+* class and 0 tempo-sensitive placements; cyl 4x7, 4x8, flat 4x6, 3x7 have a non-empty off class (8, 8, 4, 4 placements) and 240, 348, 174, 122 sensitive placements. The extra boards cyl 2x6, 2x8, 6x7 are insensitive with an empty off class. The K6 conjecture (sensitive exactly when the off class is non-empty) now holds on all 38 boards (27 from K4/K6 plus these 11).
2. **Task 2: the chess-rule variant equals kpsolve at T = 0 on all 2,123,068 positions of 20 boards (0 differences).** Under the chess rule sensitivity is not confined to the off-class boards: cyl 5x6, 6x5, 7x5 have 3,165, 2,154, 3,206 sensitive placements (0 under normal play); only the 3-file cylinders (3x6, 3x7, 3x8) stay insensitive. K6's insensitivity of the 5- to 8-file cylinders is therefore a property of the stalemate-loses convention, not of the cylinder: under the chess rule the 5-, 6- and 7-file cylinders tested are sensitive (8 files was not run under the chess rule).
3. **Zugzwang comparison.** Every kpsolve mutual zugzwang is sensitive to one spare move for White and to one for Black (PROVED; 0 exceptions on 13 boards). The converse is false: 84% to 99% of the placements sensitive at n = +-1 are not zugzwangs themselves. The spare move is spent only at a zugzwang K+P vs K placement later in the game (mask tests, section 5).
4. **Mechanism.** Only Black's stalemate result decides which placements are sensitive: with White's stalemate a loss or a draw the sensitive set is identical on all 17 boards tested, while changing Black's stalemate from loss to draw turns the K6 set into the chess-rule set. No sensitive profile contains a Black win. The K6 explanation (White stalemated in front of its pawn, Black wins tempo battles) is not supported; the off class is a marker that co-occurs with the real cause.
5. **Limits.** One implementation; n = -10..10 and 11 finite tests only; boards up to 8 files and 8 ranks; why normal-play zugzwangs exist exactly when a White stalemate trap exists is observed on 20 boards but not derived.

## 0. Provenance and what was run

- Codex started K8 and ran out of quota; a Sonnet agent continued; this report is by the Sonnet 5.5 agent that finished it.
- Finishing work:
  - Audited every finished board (check 1 with 0 differences, tempo_detail, summary entries all present and consistent). Nothing needed a rerun. One earlier naive cross-check job had been cut by an outside SIGTERM; it was rerun.
  - Read `chess_scan.py` line by line. It is correct and complete (it gates on check 2 and on check 1 before any scan, asserts that its n = 0 column equals kpsolve for every placement, and recomputes the normal-play counts). Kept as is.
  - Added `audit.py` (re-derives all headline numbers from the per-placement files and the gzipped kpsolve files), `offclass.py`, `explain.py`, `asym.py`, `pv_stats.py`, `run_extra.sh`.
  - Re-ran everything from scratch (`run.sh`, then `run_extra.sh`). All 84 per-placement, detail, meta and ablation files are byte-identical (timings aside) to the earlier run, so the pipeline is deterministic.
- Resources: 106 jobs, 1,097 s of job time (run.sh about 17 min wall), peak RSS 481 MB (cyl 6x7), nothing killed. One heavy process at a time, under `nice -n 10`; no file over 12 MB; directory 91 MB.
- Rule: stalemate = the mover has no legal move in the whole sum x (+) T and is not in check. Normal play: it loses. Chess rule: it draws; checkmate loses either way. Moves in T are illegal while the mover is in check; infinite play draws.
- Tempo-sensitive (K6 definition): the (White starts, Black starts) result is not constant over the 11 finite test games and over x (+) n, n = -10..10. "Threshold n" = number of placements whose result at n differs from that at n+1.

## 1. Task 1: normal play (as K6)

| board | quiet | off/off+* class | tempo-sensitive | thresholds (n: placements) | kpsolve positions (diffs) | prediction |
|---|---:|---|---:|---|---:|---|
| cyl 5x4 | 2,030 | empty | 0 | none | 33,460 (0) | insensitive: CONFIRMED |
| cyl 3x7 | 3,312 | empty | 0 | none | 38,016 (0) | insensitive: CONFIRMED |
| cyl 5x7 | 20,870 | empty | 0 | none | 249,260 (0) | insensitive: CONFIRMED |
| cyl 3x8 | 5,706 | empty | 0 | none | 62,577 (0) | insensitive: CONFIRMED |
| cyl 4x7 | 9,576 | 8 placements | 240 | -4:36, -3:84, -2:80, -1:72, 0:60 | 114,604 (0) | sensitive: CONFIRMED |
| cyl 4x8 | 16,008 | 8 | 348 | -5:44, -4:100, -3:96, -2:80, -1:80, 0:76 | 182,944 (0) | sensitive: CONFIRMED |
| flat 4x6 | 5,728 | 4 | 174 | -3:16, -2:62, -1:82, 0:42 | 74,712 (0) | sensitive: CONFIRMED |
| flat 3x7 | 3,920 | 4 | 122 | -4:18, -3:42, -2:38, -1:42, 0:26 | 48,144 (0) | sensitive: CONFIRMED |
| cyl 2x6 | 492 | empty | 0 | none | 5,758 (0) | none; insensitive |
| cyl 2x8 | 1,652 | empty | 0 | none | 17,500 (0) | none; insensitive |
| cyl 6x7 | 38,664 | empty | 0 | none | 468,420 (0) | none (conjecture: insensitive) |

- Check 1 (T = 0 against kpsolve) and check 2 (10 CGT facts) pass on every board.
- The "off class" is read from the 32-letter signatures (matches off and off+*). `offclass.py` counts the same thing directly with the move generator (White to move, not in check, no legal move) and finds the identical placements on all 11 boards.
- Every sensitive profile changes only between draw and White win; none contains a Black win (audit.py).
- Examples: cyl 4x7 and cyl 4x8 `Ka3 Pa2 kc3`: DD for n <= -4 (-5), DW at the next n, WW above it. flat 4x6 `Ka3 Pa2 kc3`: DD for n <= -3, DW at n = -2, WW for n >= -1. All sensitive placements with profiles are in `tempo_detail_<board>.json`.
- New regularities (COMPUTED-1, with K4/K6): the deepest threshold is n = -(ranks - 3) on every sensitive board known (flat 3-file 4..7 ranks: -1..-4; flat width >= 4: -1, -2, -3 on 4, 5, 6 ranks; 4-file cylinders 4..8 ranks: -1..-5). Counts on 4-file cylinders, 4..8 ranks: 24, 68, 144, 240, 348; flat 3-file, 4..7 ranks: 10, 38, 76, 122. Flat width >= 4 depends only on ranks (flat 4x6 = flat 5x6 = 174).
- These close the K6 "not computed" items: cyl 5x4, flat 4x6, 4-file cylinders with 7 and 8 ranks (predicted sensitive, and are).

## 2. Task 2: the chess stalemate rule

**Variant test (done first).** At T = 0 the variant equals kpsolve on every K+P vs K position and on every K+officer / K vs K position reachable from them: 2,123,068 positions, 20 boards, 0 differences (listed in the variant_check_T0 field and in summary.json). `check1/<board>.in.gz` / `.out.gz` hold the kpsolve inputs and outputs. The chess-rule scan also recomputes the normal-play count on the same placements; it reproduces the K4/K6 numbers on all nine shared boards (10, 22, 24, 144, 174, 0, 0, 0, 0).

| board | quiet | tempo-sens. | sens. at n=+1 | at n=-1 | at +-1 | mutual zugzwangs (kpsolve) | zugzwang not sens. at +-1 | sens. at +-1, not zugzwang | sens. under both rules |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| flat 3x4 | 338 | 37 | 28 | 32 | 37 | 6 | 0 | 31 | 0 |
| flat 4x4 | 1,000 | 126 | 88 | 110 | 126 | 10 | 0 | 116 | 0 |
| cyl 4x4 | 840 | 276 | 204 | 220 | 272 | 24 | 0 | 248 | 24 |
| cyl 4x6 | 5,160 | 1,752 | 1,608 | 564 | 1,744 | 64 | 0 | 1,680 | 144 |
| flat 5x6 | 12,234 | 1,843 | 1,525 | 554 | 1,777 | 23 | 0 | 1,754 | 0 |
| cyl 3x6 | 1,710 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cyl 5x6 | 11,490 | 3,165 | 2,665 | 1,090 | 3,095 | 35 | 0 | 3,060 | 0 |
| cyl 6x5 | 10,440 | 2,154 | 1,764 | 840 | 2,154 | 24 | 0 | 2,130 | 0 |
| cyl 7x5 | 17,766 | 3,206 | 2,541 | 1,232 | 3,206 | 28 | 0 | 3,178 | 0 |
| cyl 3x7 (extra) | 3,312 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cyl 3x8 (extra) | 5,706 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| cyl 2x6 (extra) | 492 | 48 | 0 | 18 | 18 | 0 | 0 | 18 | 0 |
| cyl 2x8 (extra) | 1,652 | 156 | 0 | 98 | 98 | 0 | 0 | 98 | 0 |

(the last column is the number of placements sensitive under both the chess rule and normal play; the normal-play counts are 10, 22, 24, 144, 174, 0, 0, 0, 0, 0, 0, 0, 0.)

**Thresholds (chess rule, n: placements with result(n) != result(n+1)).**
- flat 3x4: n = -10..-2: 24 each, -1: 32, 0: 28. flat 4x4: 100 each, -1: 110, 0: 88. cyl 4x4: 200 each, -1: 220, 0: 204, +1: 20.
- cyl 4x6: -10..-4: 356 each, -3: 380, -2: 368, -1: 564, 0: 1,608, +1: 44. flat 5x6: 441 each, -1: 554, 0: 1,525.
- cyl 5x6: 815 each, -1: 1,090, 0: 2,665. cyl 6x5: 732 each, -1: 840, 0: 1,764. cyl 7x5: 1,022 each, -1: 1,232, 0: 2,541.
- cyl 2x6: -4: 4, -3: 12, -2: 30, -1: 18. cyl 2x8: -4: 20, -3: 28, -2: 58, -1: 98. 3-file cylinders: none.
- The constant block at every n from -10 to -2 is a **parity tail**: the result alternates with the parity of Black's number of spare moves. Tails were checked to n = +-20: for n <= -2, 24 / 100 / 200 / 356 / 441 / 815 / 732 / 1,022 placements (flat 3x4, flat 4x4, cyl 4x4, cyl 4x6, flat 5x6, cyl 5x6, 6x5, 7x5) have period 2 (24 more on cyl 4x6 have another tail); for n >= 2 every tail is constant. Real thresholds are only n = -1, 0, +1 (and -2, -3 on cyl 4x6).
- Examples: flat 3x4 `Ka2 Pb2 ka4` (kpsolve D,W, a mutual zugzwang): DW at n = 0, WW for n >= 1, and DW / WD alternating for n <= -1. cyl 5x6 `Ka3 Pa2 ka5` (D,W): DD for n <= -1, DW at 0, WW for n >= 1. flat 3x4 `Ka1 Pb2 kb3` (D,D, not a zugzwang): DD for n <= 0, WW for n >= 1. cyl 4x4 `Ka1 Pa2 kc3` (W,W): WW at even n <= 0, WD at odd n <= -1.
- Explicit lines (one shortest winning line per example type, with the spare move marked PASS) are in `explain_<board>.json` and `pvstats_<board>.json`.
- `Ka3 Pa2 ka5` (the odd_cylinders_verify example): kpsolve (White to move, Black to move) gives D,W on cyl 4x6, 4x7, 4x8, 5x6, 5x7, 6x7, but D,D on cyl 3x6, 3x7, 3x8, 2x6, 2x8 and on flat 5x6, 4x6, 3x7, and W,W on cyl 6x5, 7x5 (5 ranks). So "mutual zugzwang on every cylinder" holds for 4 or more files with 6 or more ranks, not for 3-file or 2-file cylinders.

## 3. Prediction verdicts

- Insensitive predicted, found insensitive with an empty off class: cyl 5x4, 3x7, 5x7, 3x8 (4 of 4).
- Sensitive predicted, found sensitive with a non-empty off class: cyl 4x7, 4x8, flat 4x6, flat 3x7 (4 of 4).
- No prediction: cyl 2x6, 2x8 (2-file): insensitive under normal play with an empty off class, but sensitive under the chess rule (48 and 156 placements), all at n <= -1 and from Black's forced passes (section 5). cyl 6x7: insensitive, as the conjecture says.

## 4. Mutual zugzwang against one spare move

A mutual zugzwang is a quiet placement whose kpsolve result with White to move is worse for White (L < D < W) than with Black to move. On K+P vs K the only such pair is (White to move D, Black to move W). Counts per board are in the table of section 2.

- **Every mutual zugzwang is sensitive at n = +1 and at n = -1 (PROVED; COMPUTED-1: 0 exceptions on 13 boards).** Let the White-to-move result be a, the Black-to-move result b, with b better for White than a. In x (+) 1 with White to move, White is not in check, so he may spend his spare move and reach x with Black to move and T = 0, worth b. A player's result is at least the value of any option he has, so the result is at least b, which differs from a. For n = -1 let Black spend his spare move and reach White to move, worth a; Black's result is at least as good for him as a, so it differs from b. The argument holds under both stalemate rules. Hence zugzwang is a subset of sensitive-at-+-1, which is a subset of tempo-sensitive.
- **Not every sensitive placement is a zugzwang.** Placements sensitive at +-1 that are not zugzwangs: 31 of 37 (flat 3x4), 116 of 126, 248 of 272, 1,680 of 1,744, 1,754 of 1,777, 3,060 of 3,095, 2,130 of 2,154, 3,178 of 3,206 (cyl 7x5): 84% to 99%. By kpsolve pair, for example cyl 5x6: DD 1,545, WD 1,170, WW 345 (never DW, by definition; never an L, which does not occur on K+P vs K). By direction: sensitive to White's spare move only (cyl 5x6: 2,005), to Black's only (430), to both (625).
- **Why.** `explain.py` solves x (+) 1 and x (+) -1 with the pass allowed only at chosen nodes and compares the result at every node of the chess graph (all positions, with officers too):
  - The strict-zugzwang nodes of the whole graph (the mover is not in check and does strictly worse than with the other side to move) are exactly the mutual-zugzwang placements, each with both sides to move, and all are K+P vs K positions (13 boards).
  - Allowing the pass only at these nodes (stalemate staying a draw, a spare move optional) reproduces the full n = +1 and n = -1 solution with 0 differing states on all 13 boards.
  - Under the chess rule a stalemated side with a spare move must pass; with the pass allowed at the zugzwang nodes plus these forced-pass nodes, n = +1 is again exact on all 13 boards. n = -1 is exact except on the 4-file cylinders (cyl 4x4: 16 placements differ, cyl 4x6: 152) and the 2-file cylinders (cyl 2x6: 8, cyl 2x8: 72). There Black also spends the spare move earlier to dodge a later forced pass.
  - In the shortest winning line of every position that White wins only with the spare move, the spare move is spent at a mutual-zugzwang placement (flat 3x4: 34 of 34; cyl 5x6: 3,345 of 3,755 with the rest winning without the pass along the longest-resisting line but needing it against another Black reply; same pattern elsewhere). It is spent 0 to 21 plies after the start, so one zugzwang pulls in many placements in front of it.
  - So the answer to "who is in one set and not the other" is: sensitive non-zugzwangs are placements from which the player with the spare move can steer play into a mutual-zugzwang placement with the opponent to move; zugzwangs are the placements where that is immediate. Sensitive at other tests but not at +-1: 4 (cyl 4x4), 8 (cyl 4x6), 66 (flat 5x6), 70 (cyl 5x6), 0 on cyl 6x5, 7x5.
- Under normal play the chess zugzwangs disappear: on every board the chess-rule mutual zugzwangs are WW for every test game and every n in normal play (`compare_rules.json`).

## 5. What the data say about the mechanism

**Whose stalemate matters (`asym.py`, 17 boards).** Four stalemate rules on the same placements: White's stalemate loses or draws, Black's loses or draws. Tempo-sensitive counts (identical sets, and identical n = +-1 sets, wherever White's rule alone is changed):

| board | normal (W loses, B loses) | W draws, B loses | W loses, B draws | chess (both draw) |
|---|---:|---:|---:|---:|
| flat 3x4 | 10 | 10 | 37 | 37 |
| flat 4x4 | 22 | 22 | 126 | 126 |
| cyl 4x4 | 24 | 24 | 276 | 276 |
| cyl 4x6 | 144 | 144 | 1,752 | 1,752 |
| flat 5x6 | 174 | 174 | 1,843 | 1,843 |
| cyl 4x7 | 240 | 240 | 3,332 | 3,332 |
| cyl 4x8 | 348 | 348 | 5,460 | 5,460 |
| flat 4x6 | 174 | 174 | 778 | 778 |
| flat 3x7 | 122 | 122 | 425 | 425 |
| cyl 5x6 | 0 | 0 | 3,165 | 3,165 |
| cyl 6x5 | 0 | 0 | 2,154 | 2,154 |
| cyl 7x5 | 0 | 0 | 3,206 | 3,206 |
| cyl 3x6, 3x7, 3x8 | 0 | 0 | 0 | 0 |
| cyl 2x6 / 2x8 | 0 / 0 | 0 / 0 | 48 / 156 | 48 / 156 |

- White's stalemate result is irrelevant to which placements are tempo-sensitive. It does change the T = 0 value of 20 placements on cyl 4x4 (the Black-win placements, WL / LL under normal play, which are insensitive either way), so the flag is live.
- Black's stalemate result decides everything. The symmetric rows reproduce `chess_scan.py` and `product.py` (asserted).
- No sensitive profile under any of the four rules contains a Black win. All changes are draw to White win. K6's reading "Black wins tempo battles that run White out of moves" is therefore not what the sensitive placements show.

**Where spare moves matter under normal play (`pv_stats.py`).**
- Strict-zugzwang K+P vs K placements under normal play (T = 0: White to move D, Black to move W; a different set from the chess zugzwangs, disjoint from them because those are WW under normal play): flat 3x4: 4, flat 4x4: 4, cyl 4x4: 8, cyl 4x6: 16, flat 5x6: 8, cyl 4x7: 20, cyl 4x8: 24, flat 4x6: 8, flat 3x7: 10, and 0 on cyl 3x6, 3x7, 3x8, 5x6, 5x7 (not run), 6x5, 7x5, 2x6, 2x8. They exist exactly on the boards whose off class is non-empty. Their number is not the off-class size (cyl 4x6: 16 against 8).
- With the pass allowed only at these nodes the n = +-1 results are reproduced exactly on all 17 boards (0 differing placements); with no pass at all, 8 / 6 (flat 3x4), 18 / 8, 20 / 16, 44 / 64, 42 / 82, 60 / 72, 76 / 80, 42 / 82, 26 / 42 placements differ at n = +1 / -1.
- The shortest winning line with the spare move ends with Black stalemated in 294 of 336 positions and with Black checkmated in 42 (all of flat 4x4, 24 of 42 on flat 4x6). Under the chess rule all such lines end in checkmate.
- Example (normal play, flat 3x4): Black to move at `Ka3 Pa2 kc3` loses (Black is driven to the corner, White queens and Black is stalemated, which loses); White to move at the same placement only draws; one spare move for White turns it into a win.

**Chess rule.** Mutual zugzwangs of the opposition type (D,W placements) exist on every flat board and every cylinder with at least 4 files and at least 6 ranks (also on 6x5, 7x5) and nowhere on 2- or 3-file cylinders, and spare moves matter exactly there (section 4). The parity tails come from forced passes: with a stalemated side forced to spend a spare move (rather than keep the stalemate draw) the result alternates with parity. In the ablation where a stalemated side may, but need not, use a spare move (`ablation.py`), all tails become constant on all 9 boards. The 2-file cylinders have no zugzwang at all and are sensitive only through Black's forced passes, with the direction reversed (more Black spare moves help White, e.g. cyl 2x6 `Ka1 Pa4 ka3`: WD for n <= -2, DD for n >= -1).

**Statement.**
1. Stalemate does decide when spare tempo matters, but through Black's stalemate rule, not White's.
2. With Black's stalemate a loss (normal play), the opposition-type zugzwangs are erased (the chess-rule zugzwangs become WW) and the only zugzwangs left are a small set that exists only on boards with a confined-king geometry. Those boards are the flat boards and the 4-file cylinders, where White can also be stalemated in front of its pawn. That is why the K6 conjecture holds on 38 of 38 boards, but the off class is a marker for this geometry, not a cause: making White's stalemate a draw changes nothing about which placements are sensitive.
3. With Black's stalemate a draw (chess), zugzwangs are plentiful and tempo matters on 10% to 34% of the quiet placements of the boards tested (0% on 3-file cylinders); 3-file cylinders have none under either rule and 2-file cylinders only forced-pass effects. K6's insensitivity of 5- to 8-file cylinders is an artefact of the convention (shown under the chess rule for 5, 6 and 7 files).
4. Not shown: why the normal-play zugzwang set is non-empty exactly when a White stalemate trap exists (observed on 20 boards, CONJECTURE for other geometries); why 3-file cylinders have no zugzwang under either rule.

## 6. Checks

- Check 1 (variant at T = 0 and normal-play graph against kpsolve): 0 differences on 20 boards. `audit.py` re-reads the gzipped kpsolve files and compares every quiet placement's two results with the stored per-placement results (independent of graph.py and product.py).
- Check 2: 10 of 10 pure-CGT facts before every scan.
- Naive solver (`check_naive.py`, no shared code with product.py or testgames.py): x (+) n for n = -4..4 at every node, both rules, flat 3x4, cyl 4x4, flat 4x4, cyl 3x6, cyl 5x4, cyl 4x6: 2,814,606 node results, 0 differences.
- `audit.py`: 381 checks, 0 failures (counts, thresholds, tails, zugzwang flags recomputed from the per-placement strings; summary.json against tempo_detail; off class against direct stalemate counts; asym against chess_scan).
- Determinism: a second complete run reproduced all per-placement, detail, meta and ablation files byte for byte (timings aside).
- `solve_depth` (explain.py), `solve_gen` (pv_stats.py) and `solve_rule` (asym.py) are asserted equal to `product.solve_product` for n = -3..3 before use.

## 7. Limits

- One implementation. The independent parts are kpsolve (T = 0 only) and the naive solver (6 boards, n in -4..4); the test-game scans on the other boards and all n beyond +-4 rest on product.py.
- Tempo sensitivity is defined by 11 finite tests and n = -10..10 only; thresholds or tails beyond that are not seen. The tail classification used n = +-20.
- Boards: up to 8 files and 8 ranks, one White pawn. Width 8 and the ordinary 8x8 board were not run here.
- The winning lines are one shortest line, not all lines; "no pass in the longest line" cases (for example 1,012 of 2,316 on cyl 4x6) win without the pass along that line and need it against another reply.
- Single-spare-move mask tests show where one spare move matters; larger n are only scanned.

## 8. Reproduce

From the project root:

    nohup sh kings/delegate/out/K8/run.sh > kings/delegate/out/K8/run.log 2>&1 &      # about 17 min
    nohup sh kings/delegate/out/K8/run_extra.sh > kings/delegate/out/K8/run_extra.log 2>&1 &   # after run.sh, about 2 min
    .venv/bin/python kings/delegate/out/K8/tables.py     # the tables above
    .venv/bin/python kings/delegate/out/K8/audit.py      # 381 checks

- `run.sh` builds kpsolve (`nice -n 10 cc -O2 -o kings/delegate/out/K8/kp kings/kpsolve.c`), runs Task 1 (`run_all.sh`), the chess scans (`chess_scan.py`), `offclass.py`, `explain.py`, `asym.py`, `ablation.py`, `compare_rules.py`, `check_naive.py`, `summarize.py` and `audit.py`.
- Files: `summary.json`; `tempo_detail_<board>.json` (normal play for the task-1 boards, chess rule for the task-2 boards; the chess runs on the four boards in both tasks are `tempo_detail_chess_<board>.json`); per-placement `<board>.jsonl` (normal) and `chess_tempo_<board>.jsonl` (chess); `check1/*.gz`; `explain_*`, `asym_*`, `pvstats_*`, `offclass_*`, `ablation_*.json`; `runs.jsonl` (time and RSS per job).


## Archived data

The per-placement normal-play and chess-rule `.jsonl` files and `check1/` (65 files, 10 mb) are kept locally, not in git, as `bulk_regenerable.tar.zst`. Unpack with
`zstd -dc kings/delegate/out/K8/bulk_regenerable.tar.zst | tar -xf - -C kings/delegate/out/K8`.
