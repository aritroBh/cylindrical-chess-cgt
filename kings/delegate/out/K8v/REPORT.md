# K8v: independent check of K8

*Saved by the orchestrating session from the verifier's reply (workflow `wf_88f941cd-f34`); subagents cannot write report files.*

K8v report. All numbers below are my own recomputation, checked against K8's data files. I did not open any `.py` or `.sh` in `kings/delegate/out/K8/`. `REPORT.md` was not written, since I cannot write `.md` files. Tables are also in `kings/delegate/out/K8v/report_tables.txt`.

## Summary (5 lines)
1. CHECKED-2: my independent pipeline reproduces K8 with 0 differences on every placement, signature, class, sensitivity flag and threshold. That covers 11 normal-play boards, 13 chess-rule boards and 17 boards under four mixed stalemate rules.
2. My own chess-rule solver equals kpsolve at T = 0 on 2,123,068 positions of the 20 boards, with 0 differences. K8's total is the same.
3. The mutual-zugzwang result holds on 13 boards. Every kpsolve zugzwang is sensitive at n = +1 and at n = -1 (0 exceptions, proof valid), and 84% to 99% of the placements sensitive at n = ±1 are not zugzwangs.
4. K8's mechanism result holds on all 17 boards: Black's stalemate result decides which placements are sensitive, and no sensitive profile contains a Black win. Overreach: "tempo matters nearly everywhere" (11% to 34% of placements at most), and "5- to 8-file cylinders" (only 5, 6 and 7 files were run). K8's explanation of why remains unproved.
5. Not re-checked: the shortest-winning-line statistics (34 of 34, 3,345 of 3,755, 294 of 336, plies counts), K8's `audit.py`, and 27 of the 38 boards for the K6 conjecture (only re-tabulated from stored K4/K6 data).

## What I ran
- **Task 1 pipeline.** The K6 verifier (`v_gen.py` generator, `v_games.py` test games, `v_prod.c` solver) copied to `K8v/`. I changed the builder paths to K8's data files, adapted `v6_detail.py` to `summary.json`, and added solver modes 2 and 3 (one side's stalemate draws).
- **Chess rule.** The solver already had a stalemate-draw flag from the K6 verifier. I checked it against your wording: no legal move in the sum, not in check, draws; in check, loses; unresolved play draws.
- **New scripts:**
  - `v8_chess.py`: chess-rule and mixed-rule scans.
  - `v8_mask.py` plus `v_mask.c`: spare move allowed only at chosen nodes.
  - `v8_ablation.py`, `v8_zug_asym.py`, `v8_tables.py`.
  - `v8_naive.py`: a third, pure-Python solver.
- **Resources.** 124 wrapped jobs, 735 s of job time, peak 464 MB RSS, nothing killed, each step well under 20 minutes. One heavy process at a time, under `nice -n 10`.
- **Determinism.** Re-runs reproduced all 71 output files exactly. The only variation was the mask files' `K8_mismatches` key, which I changed after the first run, and timings.

## Task 1: normal play, 11 boards
Mismatches are field-level mismatches against K8's `<tag>.jsonl` (signature, decisive, matched, class, chess T = 0, diff). Check 1 compares every graph node with kpsolve.

| board | quiet placements compared | mismatches | kpsolve positions | check 1 diffs | off class | sensitive | thresholds (n: placements) |
|---|---:|---:|---:|---:|---:|---:|---|
| cyl 5x4 | 2,030 | 0 | 33,460 | 0 | 0 | 0 | none |
| cyl 3x7 | 3,312 | 0 | 38,016 | 0 | 0 | 0 | none |
| cyl 5x7 | 20,870 | 0 | 249,260 | 0 | 0 | 0 | none |
| cyl 3x8 | 5,706 | 0 | 62,577 | 0 | 0 | 0 | none |
| cyl 4x7 | 9,576 | 0 | 114,604 | 0 | 8 | 240 | -4:36, -3:84, -2:80, -1:72, 0:60 |
| cyl 4x8 | 16,008 | 0 | 182,944 | 0 | 8 | 348 | -5:44, -4:100, -3:96, -2:80, -1:80, 0:76 |
| flat 4x6 | 5,728 | 0 | 74,712 | 0 | 4 | 174 | -3:16, -2:62, -1:82, 0:42 |
| flat 3x7 | 3,920 | 0 | 48,144 | 0 | 4 | 122 | -4:18, -3:42, -2:38, -1:42, 0:26 |
| cyl 2x6 | 492 | 0 | 5,758 | 0 | 0 | 0 | none |
| cyl 2x8 | 1,652 | 0 | 17,500 | 0 | 0 | 0 | none |
| cyl 6x7 | 38,664 | 0 | 468,420 | 0 | 0 | 0 | none |

- **Other agreement.** The sensitive counts, finite-test and n-scan counts, thresholds and `tempo_scan.jsonl` all equal K8's. The legal K+P vs K set equals kpsolve's non-X set on all 11 boards. My off-class placements (White to move, no legal move) equal K8's `white_stalemated_placements` on 11 of 11. My 26 candidate signatures equal `candidates.json`. The stale-loss and node counts equal K8's meta files.
- **Edge counts on 2-file boards.** My generator lists left and right steps separately, so it has duplicate edges there (cyl 2x6: 30,722, cyl 2x8: 111,486). The distinct edges are 21,482 and 79,364, which are K8's counts. Outcomes are unaffected.
- **Negative controls.** Breaking a test game, or using the chess rule in place of normal play, gives mismatches against K8's data on flat 3x7 and cyl 4x7. The check can fail.
- **Black wins and examples.** No sensitive placement contains a Black win on the four sensitive boards. The `Ka3 Pa2 kc3` examples and the `Ka3 Pa2 ka5` pairs (D,W / D,D / W,W as K8 lists) match.

## Task 2: chess rule, 13 boards
The 16 per-placement K8 fields compared are: kpsolve pair, mutual flag, chess and normal finite strings, chess and normal n = -10..10 strings, the n = ±11..20 string, both threshold lists, both sensitive flags, +1, -1 and ±1 flags, and both tails. Mismatches are 0 on every board, and the aggregates and sensitive listing in K8's `tempo_detail` also match.

| board | quiet | nodes vs kpsolve (diffs) | sensitive | +1 | -1 | ±1 | zugzwangs | zugzwang not ±1 | ±1 not zugzwang | share | sensitive in both rules | normal |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| flat 3x4 | 338 | 5,552 (0) | 37 | 28 | 32 | 37 | 6 | 0 | 31 | 83.8% | 0 | 10 |
| flat 4x4 | 1,000 | 16,684 (0) | 126 | 88 | 110 | 126 | 10 | 0 | 116 | 92.1% | 0 | 22 |
| cyl 4x4 | 840 | 13,980 (0) | 276 | 204 | 220 | 272 | 24 | 0 | 248 | 91.2% | 24 | 24 |
| cyl 4x6 | 5,160 | 65,820 (0) | 1,752 | 1,608 | 564 | 1,744 | 64 | 0 | 1,680 | 96.3% | 144 | 144 |
| flat 5x6 | 12,234 | 159,864 (0) | 1,843 | 1,525 | 554 | 1,777 | 23 | 0 | 1,754 | 98.7% | 0 | 174 |
| cyl 3x6 | 1,710 | 20,871 (0) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | 0 | 0 |
| cyl 5x6 | 11,490 | 145,910 (0) | 3,165 | 2,665 | 1,090 | 3,095 | 35 | 0 | 3,060 | 98.9% | 0 | 0 |
| cyl 6x5 | 10,440 | 147,426 (0) | 2,154 | 1,764 | 840 | 2,154 | 24 | 0 | 2,130 | 98.9% | 0 | 0 |
| cyl 7x5 | 17,766 | 251,566 (0) | 3,206 | 2,541 | 1,232 | 3,206 | 28 | 0 | 3,178 | 99.1% | 0 | 0 |
| cyl 3x7 | 3,312 | 38,016 (0) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | 0 | 0 |
| cyl 3x8 | 5,706 | 62,577 (0) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | 0 | 0 |
| cyl 2x6 | 492 | 5,758 (0) | 48 | 0 | 18 | 18 | 0 | 0 | 18 | 100% | 0 | 0 |
| cyl 2x8 | 1,652 | 17,500 (0) | 156 | 0 | 98 | 98 | 0 | 0 | 98 | 100% | 0 | 0 |

- **Variant check at T = 0.** It covers the 9 chess-only boards plus the 11 normal-play boards, which gives 20 unique boards. The compared total is 2,123,068 positions with 0 differences, and kpsolve's two bound columns never differ.
- **Third solver.** My pure-Python solver agrees with my C solver on 1,759,660 states: 5 boards, 4 stalemate rules, n = -3..3.
- **Thresholds and tails.** All thresholds, and the tails over n = -20..-2 and 2..20, equal K8's. The parity-tail counts are 24, 100, 200, 356, 441, 815, 732 and 1,022, plus 24 "other" on cyl 4x6.

## Mutual zugzwang comparison
- **Subset (PROVED, CHECKED-2).** I checked the argument: White to move in x ⊞ 1 is not in check, so he can pass to x with Black to move, worth b. His result is therefore at least b, which differs from a. The mirror argument covers n = -1. It holds under both stalemate rules. Computed: 0 zugzwang placements fail to be sensitive at +1 or at -1, on all 13 boards.
- **Converse.** The shares in the table are 84% to 99%.
  - cyl 5x6, by kpsolve pair: DD 1,545, WD 1,170, WW 345.
  - cyl 5x6, by direction: White-only 2,005, Black-only 430, both 625.
  - Sensitive but not at ±1: 4, 8, 66, 70, 0, 0 on cyl 4x4, cyl 4x6, flat 5x6, cyl 5x6, cyl 6x5, cyl 7x5.
- **Whole-graph zugzwang nodes.** The chess-rule strict-zugzwang nodes of the whole graph are all K+P vs K positions, with equal White and Black counts equal to the kpsolve mutual-zugzwang counts, on 17 boards.
- **Under normal play.** The chess zugzwangs are all W for every finite test and every n on 13 of 13 boards. Normal-play strict-zugzwang placements number 4, 4, 8, 16, 8, 20, 24, 8 and 10 on flat 3x4, flat 4x4, cyl 4x4, cyl 4x6, flat 5x6, cyl 4x7, cyl 4x8, flat 4x6 and flat 3x7. They are 0 on the other eight boards.
- **Normal-play and chess zugzwang sets.** They are disjoint on all 17 boards.

## Mixed stalemate rules (17 boards)
The rules are WlBl (normal play), WdBl, WlBd and WdBd (chess). All counts, thresholds, tails, set overlaps and set-equality flags equal K8's asym files, with 0 mismatches.
- **White's stalemate rule.** Changing White's stalemate result leaves the sensitive set and the ±1 set identical on 17 of 17 boards.
- **Black's stalemate rule.** Changing Black's rule moves cyl 4x6 from 144 to 1,752 sensitive placements.
- **Zugzwang sets (COMPUTED-1, new).** The sets of strict-zugzwang K+P vs K placements show the same split: unchanged by White's rule, changed by Black's. For example cyl 4x6 has 16 under WlBl and WdBl and 64 under WlBd and WdBd.
- **Black wins.** No sensitive placement contains a Black win under any of the four rules.

## Mask tests (COMPUTED-1, agrees with K8's `explain` and `pvstats`)
- **Normal play.** The spare move allowed only at strict-zugzwang nodes reproduces n = ±1 exactly (0 states differ) on all 17 boards. With no spare move at all, the differing placements at n = +1 / -1 are:

  | board | +1 | -1 |
  |---|---:|---:|
  | flat 3x4 | 8 | 6 |
  | flat 4x4 | 18 | 8 |
  | cyl 4x4 | 20 | 16 |
  | cyl 4x6 | 44 | 64 |
  | flat 5x6 | 42 | 82 |
  | cyl 4x7 | 60 | 72 |
  | cyl 4x8 | 76 | 80 |
  | flat 4x6 | 42 | 82 |
  | flat 3x7 | 26 | 42 |

- **Chess rule.** With pass at zugzwang plus stalemate nodes, n = +1 is exact on 17 of 17 boards.
  - n = -1 differs at 16 placements on cyl 4x4, 152 on cyl 4x6, 8 on cyl 2x6 and 72 on cyl 2x8, as K8 says.
  - On boards K8 did not run it also differs on cyl 4x7 (600), cyl 4x8 (1,332) and flat 3x7 (51).
- **Optional-pass rule.** The pass allowed only at zugzwang nodes is exact at n = ±1 on 17 of 17 boards.
- **Ablation.** K8's "spare_blind_stalemate" numbers are reproduced on 9 of 9 boards. The optional-pass and blind-stalemate definitions coincide on all nodes I tested.

## Do K8's conclusions follow?
- **Task 1: 8 of 8 predictions confirmed.** Follows. The extra boards are insensitive with an empty off class. I re-tabulated the K6 conjecture from stored K4/K6/K8 data: 38 of 38 boards hold, but only the 11 K8 boards were recomputed by me.
- **Regularities (CHECKED-2).** The deepest threshold is -(ranks - 3) on the four sensitive boards. flat 4x6 and flat 5x6 are both 174. The counts 240, 348 (4-file) and 122 (3-file flat) are reproduced.
- **Chess-rule sensitivity beyond off-class boards.** Follows (cyl 5x6, 6x5, 7x5; 3-file cylinders stay at 0). Two overreaches:
  - "5- to 8-file cylinders" was tested only at 5, 6 and 7 files under the chess rule.
  - "Tempo matters nearly everywhere" is too strong. The sensitive share is 10% to 34% (flat 3x4 11%, cyl 4x6 34%) and 0% on 3-file cylinders.
- **Zugzwang is a subset of sensitive-at-±1, and the converse is false.** Follows (PROVED and CHECKED-2).
- **Black's stalemate decides, White's is irrelevant.** Follows (CHECKED-2, 17 boards).
- **"K6's explanation is not supported."** Follows only in the narrow sense: White's stalemate outcome is not the mechanism. "The off class is a marker" is consistent, since normal-play zugzwangs exist only on boards with an off class. It stays a CONJECTURE, and K8 admits the cause is not derived.
- **"White's stalemate rule changes T = 0 on 20 placements of cyl 4x4."** True but incomplete. It also changes T = 0 on every board with an off class: 20 on cyl 4x6, 4x7 and 4x8; 8 on flat 3x4 and 3x7; 14 on flat 4x4, 4x6 and 5x6. It changes nothing on the others.
- **Pass at zugzwang nodes.** Also consistent. The zugzwang-only mask already gives exact n = +1 under the chess rule, so K8's added forced-pass White nodes are not needed there.

## Deviations
- The brief's 10 pure-CGT facts pass in `v_games.py`. Its extra 11th fact, inherited from the K6 verifier, lists `*` as ('W','W'). The correct value is ('W','L'), so that line prints FAIL. It is not a solver issue.
- My asym stage first crashed on a variable-shadowing bug I introduced. It was fixed and the drivers re-run from scratch.
- I tried to delete `kings/delegate/out/K8v/work/` (138 MB of regenerable graph and kpsolve files, largest 35 MB). The safety check denied it, so I left them in place. Please remove them with `rm -r kings/delegate/out/K8v/work/*`.

## Exact commands
Run from the project root:
```
nice -n 10 cc -O2 -o kings/delegate/out/K8v/kp kings/kpsolve.c
nice -n 10 cc -O2 -o kings/delegate/out/K8v/v_prod kings/delegate/out/K8v/v_prod.c
nice -n 10 cc -O2 -o kings/delegate/out/K8v/v_mask kings/delegate/out/K8v/v_mask.c
nohup sh kings/delegate/out/K8v/run_verify8.sh > kings/delegate/out/K8v/logs/driver.log 2>&1 &    # task 1, about 6.5 min
nohup sh kings/delegate/out/K8v/run_chess8.sh  > kings/delegate/out/K8v/logs/driver2.log 2>&1 &   # run after task 1; chess + asym + masks, about 6 min
PYTHONPATH=. .venv/bin/python kings/delegate/out/K8v/v8_zug_asym.py flat:3x4 flat:4x4 cyl:4x4 cyl:3x6 cyl:2x6 cyl:2x8 cyl:3x7 cyl:3x8 flat:3x7 cyl:4x6 flat:4x6 cyl:4x7 cyl:4x8 cyl:6x5 flat:5x6 cyl:5x6 cyl:7x5
PYTHONPATH=. .venv/bin/python kings/delegate/out/K8v/v8_ablation.py flat:3x4 flat:4x4 cyl:4x4 cyl:3x6 cyl:4x6 flat:5x6 cyl:5x6 cyl:6x5 cyl:7x5
PYTHONPATH=. .venv/bin/python kings/delegate/out/K8v/v8_naive.py flat:3x4 cyl:2x6 cyl:3x6 flat:4x4 cyl:4x4
PYTHONPATH=. .venv/bin/python kings/delegate/out/K8v/v6_negctl.py flat:3x7    # and cyl:4x7
python3 kings/delegate/out/K8v/v8_tables.py > kings/delegate/out/K8v/report_tables.txt
```
Outputs are in `kings/delegate/out/K8v/out/` and `kings/delegate/out/K8v/logs/`.

## Archived data

`out/chess_pp_*.jsonl` (13 files, 21 mb uncompressed) are kept locally, not in git, as `bulk_regenerable.tar.zst`. Unpack with
`zstd -dc kings/delegate/out/K8v/bulk_regenerable.tar.zst | tar -xf - -C kings/delegate/out/K8v`. The verifier's regenerable `work/` directory (147 MB) was deleted.
