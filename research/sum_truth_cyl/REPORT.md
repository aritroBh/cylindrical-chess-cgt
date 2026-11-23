# Avenue 5: explicit-king sum test on cyl:8x6, and the 56,402 K12 e.p. roots

## 5-line summary
(Note added 2026-11-23: the first bullet describes the first attempt under a 3.6 GB limit and is superseded. The completed test, 19 pairs at up to 12 GB, is in the section "12 GB runs (2026-11-22)" below.)
- **Real-king pair test: NOT COMPLETED.** Of 50 sampled pairs, 4 were attempted with `kpsolve --board cyl:8x6 --cap 1` (pair00, pair01, pair13, pair29); all 4 hit the 3.6 GB watchdog after 7 to 11 min with no answer (peaks 3.5 to 3.7 GB). So 0 of 50 pairs have a real-king outcome and there is no real-chess evidence for additivity yet. A 5th, all-active 10-pawn pilot was killed at 3.8 GB.
- **Frozen-king stand-in (not real chess): the cylcgt sum matches `kpsolve --frozen` on 50/50 pairs**, under both the textbook and the e.p.-aware passed test, with `sum_safe` True on 50/50 and 0 sum (interaction) errors. This is weak: 41/50 pairs contain a passer component (decided by the passer) and the other 9 contain a locked component of value 0 (so the sum is just G + 0).
- **Components alone, real kings, cap 1:** of the 100 component slots, 46 are exact and all 46 match the model; 54 are "undetermined" (cap-1 bounds differ). Frozen: 100/100 match.
- **K12 e.p. roots: 56,402 regenerated** (5,630 on 6x6, 46,896 on 7x6, 3,876 on 8x6, same as K12 REVIEW). **51,050 certified, 0 certified roots disagree with `--frozen`** (pass); 5,352 uncertified, of which 1,752 disagree and 3,600 agree. Label COMPUTED-1.
- Labels: pair test PILOT (no real result); frozen-pair agreement COMPUTED-1; e.p. roots COMPUTED-1 (a second independent implementation was not run).

## Method (exact commands)
Everything ran from `/Users/aritro/Downloads/Research/Chessendgames`, under `nice -n 15`, at most 2 heavy processes, PIDs in `*.pid` files (no pkill). Memory watchdog (`watch.sh`, `worker.py`, `planB/runner.py`) kills only its own kpsolve PID above 3.6 to 3.8 GB.

**Pair selection (`gen.py`).** Source rows: `kings/results/exp_cyl7x6_epon_Q_conv.jsonl` with `verdict == match` and `verdict_ep-aware == match` and `exact` (305 rows). Only one-file components can be embedded (cyl:8x6 has free files d, e, f; two components need d and f with e empty). That leaves 30 rows (15 on d, 15 on e), every one with 3 or 4 pawns. Component A is placed on file d, B on file f (rows moved to the target file). Trebuchet Z: `Pa3 pa4 Kh4 kb3`. 50 pairs were drawn with `random.seed(20261029)`.

**Why only a restricted population.** In the first draw over all 900 ordered pairs, every pair had 8 to 10 pawns. A pilot with the smallest of those (10 pawns incl. Z) was killed at 3.8 GB after 9 min. To get any chance of fitting, pairs were restricted to those with at least one "locked" component (no pawn move for either side): 224 of 900 ordered pairs, which then have 8 or 9 pawns incl. Z. Locked shapes: `d2 d3/d4`, `e3/e4 e5`, `d2 d3/d4 d5`, `e2 e3/e4 e5`. Even these did not fit (see Results).

**Model sum.** `cylcgt.pawns.value` on `Board(8,6,wrap,ep)` for both components together, `pawns.sum_safe`, with `PASSED_RESPECTS_EP` False (textbook) and True (e.p.-aware). The two conventions give identical outcomes on all 50 pairs. Prediction map as in `kings/experiment.py`: L -> (W,W), R -> (L,L), N -> (W,L), P -> (L,W), White's view for (wtm, btm).

**Real kings.** `kings/kpsolve --board cyl:8x6 --ep on --promote Q --cap 1 --threads 2`, one process per job (`worker.py K N 1`), first-run memory measured with `/usr/bin/time -l`. Components alone and Z alone: 33 jobs, all finished (16 to 60 s, 36 to 375 MB). Cap 2 was not attempted for pairs, since cap 1 already exceeded the 4 GB limit. Cap 0 was tried on pair13: it finishes in 4 s (45 MB) but gives differing bounds (`W L`), so it decides nothing; for Z alone it gives `D L`.

**Frozen stand-in.** `runner.py ../jobs_frozen.json ../frozen_out 0 1 1 frozen`: all 154 distinct positions (Z, 64 solo lines, 100 pair lines) in one process, 1 s, 4 MB. Analysis: `analyze.py` -> `pair_table.json`.

**Plan B (kept for the record).** `planB/`: all 72 one-file components with 2 or 3 pawns on d and f, solved alone at cap 1 (`planB/small_comps_real.json`): 22 match (all 3-pawn, mostly decided passer positions), 22 undetermined, 28 race. Any pair of them has 8 pawns incl. Z, the same size that exceeded 4 GB, so no pair run was made.

**e.p. roots.** `k12ep/gen.py`, `checker.py`, `process.py` are unmodified copies of `kings/delegate/out/K12/` (only run from my folder; the originals were not touched). `k12ep/run_ep.py W H K` calls `gen.process_board`, keeps roots with an e.p. right, computes the credited side with `process.beta_for_root`, certifies with `checker.check_certified(..., ep, ...)` (e.p. mode), and self-tests cylcgt's e.p.-aware `passed` against the checker's per-pawn passed list. Then `kpsolve --board cyl:WxH --frozen --cap 1 --threads 2` (`k12ep/chain2.sh`; peak 627 MB) and `k12ep/analyze_ep.py` (output `k12ep/ep_analysis.txt`). A root agrees if frozen = W when beta = W, or L when beta = B.

## Results
**Pair level (real kings).**
| pair | pawns incl. Z | outcome |
|---|---|---|
| pair00 | 9 | killed at 3,524 MB, 420 s |
| pair01 | 8 | killed at 3,542 MB, 426 s |
| pair13 | 8 | killed at 3,712 MB, 500 s |
| pair29 | 8 | killed at 3,692 MB, 681 s |
| 46 other pairs | 8 to 10 | not attempted |

**Pair level (frozen kings, model = cylcgt sum), n = 50.** Model outcomes: L 24, R 20, N 4, P 2. 50 match, 0 mismatch, 0 race. Both passed tests: identical. Stratification: 41 pairs have a passer component, 9 have none (all 9 are locked (0) + a number or switch such as 0, 1, 1/2 pm 1/2), so only the 6 N/P pairs test more than "the passer side wins". Every component alone also matches under frozen play (100/100).

**Components alone with real kings, cap 1:** 46 exact, 46 match, 0 mismatch; 54 undetermined (bounds differ).

**K12 e.p. roots (frozen vs credit).**
| board | roots | single cert agree | race cert agree | uncert agree | uncert disagree | cert disagree |
|---|---|---|---|---|---|---|
| 6x6 | 5,630 | 1,830 | 3,458 | 230 | 112 | 0 |
| 7x6 | 46,896 | 10,372 | 32,528 | 2,440 | 1,556 | 0 |
| 8x6 | 3,876 | 500 | 2,362 | 930 | 84 | 0 |
| total | 56,402 | 12,702 | 38,348 | 3,600 | 1,752 | 0 |

Self-test of the e.p.-aware passed test: 0 mismatches on all 56,402 roots. The 1,752 uncertified disagreements are the root-clause cases already seen without e.p. in K12 (e.g. the P11 root clause); they are not violations because no hypothesis-certified root disagrees.

## Every mismatch, classified
- Pair level: none (frozen), none observed (real: no pair finished).
- Components: none among exact results. 54 real-king component results are inconclusive, not mismatches.
- e.p. roots: 0 violations; 1,752 uncertified-and-disagreeing roots are the expected uncovered class (sum/king effects are not involved: these are single positions).

## Honest limits
- The headline question (does the CGT sum match real-king chess on 8x6) is **unanswered**: every attempted pair needs more than 4 GB at cap 1. Next steps that would need user approval: a memory-lean solver mode, a machine with more RAM for the same commands, or smaller components that survive cap 1 (none exist in the 7x6 matching set; the smallest has 3 pawns).
- Embedding is restricted to one-file components on d and f; the 7x6 "matches" were measured on 7x6, so each component's solo match was re-measured on 8x6 (frozen 100/100, real 46/46 exact, 54 undetermined).
- The frozen result is a test of the sum rule against the frozen-king model, not of real chess. It cannot show king effects.
- e.p. roots: one implementation of the check (K12's own copied code); K12's brute-force variant was not rerun, so COMPUTED-1.

## Labels
- Real-king pair agreement: no result (pilot, infeasible at 4 GB).
- Frozen pair agreement 50/50: COMPUTED-1 (one solver, one model implementation; weak population).
- e.p. roots 51,050 certified with 0 disagreements: COMPUTED-1.

## Files
`gen.py`, `pairs.json`, `in_all.txt`, `worker.py`, `watch.sh`, `jobs/` (real-king job outputs, incl. killed pair13/pair29 and cap-0 pilot), `frozen_out/`, `analyze.py`, `pair_table.json`, `planB/`, `k12ep/` (e.p. roots: `ep_*_in.txt`, `ep_*_out.txt`, `ep_*.json`, `ep_analysis.txt`).

## Note on files from an earlier session in this folder
The folder already held files from an earlier session today (13:32 to 15:07): `items.json`, `shapes.py`, `ep_check.py`, `ep_{6x6,7x6,8x6}.json` (top level), `pilot_*`, `guard.sh`, `pids.txt`, `logs/`. I did not use them for any number above and did not edit them. Two observations, not verified by me beyond reading them:
- `ep_*.json` there classify the same 56,402 e.p. roots with two hypothesis checkers (`checker.py` and the K10r2 `chk.py`, labelled cert12 / cert10) and give class counts identical to my table (single cert agree 1,830 / 10,372 / 500; race cert agree 3,458 / 32,528 / 2,362; uncertified-disagree 112 / 1,556 / 84 on 6x6 / 7x6 / 8x6). If `ep_check.py` really is an independent second implementation, the e.p. clause would qualify for CHECKED-2; I leave it at COMPUTED-1 until that is reviewed.
- `logs/pilot_p_dnf.txt` records an np=7 pair (9 pawns incl. Z) stopped after 36 min with no result, consistent with my finding that real-king pair runs do not finish at cap 1 within 4 GB.
My own stray processes: none left running (all PIDs recorded in `*.pid`, `planB/*/runner*.pid`).


## 12 GB runs (2026-11-22)

All results COMPUTED-1 (single run of `kpsolve --board cyl:8x6 --ep on --promote Q --cap 1`, one implementation, no independent re-run). Machine: at most 2 kpsolve at once, `nice -n 15`, each stopped by its own PID at 12 GB RSS (workers `worker12.py`, `worker12b.py`, `worker2.py`, `worker12c.py`, `worker12d.py`; raw JSON in `jobs12/`; table regenerated by `report12.py`, per-pair judging in `analysis12.py`). Wall time about 5 h 50 min (12:05 to 17:53, 2026-11-22). No process was killed over the limit at cap 1; the only over-limit stops are the cap-2 attempts listed below. One duplicate run (pair 26 started by two workers) was stopped by PID before it produced output; the other worker's result is the one used.

**How to read the output.** kpsolve prints two tokens per side to move, `upper lower` over W > D > L for the mover (cap 1 treats promotions as capped, so a pair of equal tokens is exact and unequal tokens are bounds). The model class is mapped as in `analyze.py` (`PRED`): L = (W,W), R = (L,L), N = (W,L), P = (L,W) for (white to move, black to move). That mapping is validated by the base position Z (anchors only), which solved exactly as `L L` / `W W`, the P pattern. A side is "consistent" when the model's result lies inside the bounds, "agree (exact)" when both sides are exact and equal to the model, and a disagreement would be an exact side that differs or a model result outside the bounds.

### Pairs (P = the 9 priority pairs of `pairs.json`, no passer component; N = 10 new pairs of `pairs2.json`, both components live, non-passer, nonzero value; "pawns" counts the two anchor pawns Pa3/pa4)

| pair | components (model value) | pawns+anchors | model sum (ep-aware) value = outcome (W-to-move, B-to-move) | real cap-1 (W-to-move / B-to-move; first token = upper bound, second = lower) | status | peak GB | secs | verdict | cap 2 |
|---|---|---|---|---|---|---|---|---|---|
| P1 | W: d3 / B: d4 d5 (0) + W: f2 f4 / B: f5 (1) | 8 | 1 = L ('W', 'W') | W D / W D | bounds | 3.1 | 892 | no contradiction cap2 killed at 12 GB after 3985s, no answer |
| P9 | W: d2 d3 / B: d4 d5 (0) + W: f2 f3 / B: f4 f5 (0) | 10 | 0 = P ('L', 'W') | D L / W D | bounds | 6.8 | 4036 | no contradiction |
| P21 | W: d2 d4 / B: d5 (1) + W: f3 / B: f4 f5 (0) | 8 | 1 = L ('W', 'W') | W W / W W | exact | 4.7 | 1022 | agree (exact) |
| P22 | W: d3 / B: d4 d5 (0) + W: f2 / B: f4 f5 (-1/2±1/2) | 8 | -1/2±1/2 = N ('W', 'L') | W D / L L | exact on one side, bounds on other | 4.2 | 982 | no contradiction |
| P26 | W: d2 d3 / B: d4 d5 (0) + W: f2 f3 / B: f5 (1/2±1/2) | 9 | 1/2±1/2 = N ('W', 'L') | W W / D L | exact on one side, bounds on other | 7.6 | 2300 | no contradiction |
| P29 | W: d2 d3 / B: d4 (0) + W: f3 / B: f4 f5 (0) | 8 | 0 = P ('L', 'W') | D L / W D | bounds | 4.2 | 918 | no contradiction |
| P35 | W: d2 / B: d4 d5 (-1/2±1/2) + W: f2 f3 / B: f4 f5 (0) | 9 | -1/2±1/2 = N ('W', 'L') | W D / L L | exact on one side, bounds on other | 6.0 | 2216 | no contradiction |
| P40 | W: d2 d3 / B: d5 (1/2±1/2) + W: f3 / B: f4 f5 (0) | 8 | 1/2±1/2 = N ('W', 'L') | W W / D L | exact on one side, bounds on other | 2.6 | 982 | no contradiction cap2 killed at 12 GB after 3291s, no answer |
| P48 | W: d2 / B: d3 d5 (-1) + W: f2 f3 / B: f4 (0) | 8 | -1 = R ('L', 'L') | D L / D L | bounds | 3.2 | 915 | no contradiction |
| N0 | W: d2 d4 / B: d5 (1) + W: f2 / B: f3 f5 (-1) | 8 | 0 = P ('L', 'W') | D L / W D | bounds | 4.3 | 1129 | no contradiction |
| N1 | W: d2 d4 / B: d5 (1) + W: f2 f3 / B: f5 (1/2±1/2) | 8 | 3/2±1/2 = L ('W', 'W') | W W / W W | exact | 5.1 | 1040 | agree (exact) |
| N2 | W: d2 d4 / B: d5 (1) + W: f2 / B: f4 f5 (-1/2±1/2) | 8 | 1/2±1/2 = N ('W', 'L') | W W / D L | exact on one side, bounds on other | 5.5 | 1085 | no contradiction |
| N3 | W: d2 / B: d3 d5 (-1) + W: f2 f3 / B: f5 (1/2±1/2) | 8 | -1/2±1/2 = N ('W', 'L') | W L / D L | bounds | 4.5 | 1187 | no contradiction |
| N4 | W: d2 / B: d3 d5 (-1) + W: f2 / B: f4 f5 (-1/2±1/2) | 8 | -3/2±1/2 = R ('L', 'L') | L L / L L | exact | 5.0 | 1000 | agree (exact) |
| N5 | W: d2 d3 / B: d5 (1/2±1/2) + W: f2 / B: f4 f5 (-1/2±1/2) | 8 | 0 = P ('L', 'W') | D L / W D | bounds | 5.9 | 1135 | no contradiction |
| N6 | W: d2 d3 / B: d5 (1/2±1/2) + W: f2 f3 / B: f5 (1/2±1/2) | 8 | 1 = L ('W', 'W') | W W / W W | exact | 5.5 | 1057 | agree (exact) |
| N7 | W: d2 / B: d4 d5 (-1/2±1/2) + W: f2 / B: f4 f5 (-1/2±1/2) | 8 | -1 = R ('L', 'L') | L L / L L | exact | 5.3 | 1041 | agree (exact) |
| N8 | W: d2 d4 / B: d5 (1) + W: f2 f4 / B: f5 (1) | 8 | 2 = L ('W', 'W') | W W / W W | exact | 5.0 | 944 | agree (exact) |
| N9 | W: d2 / B: d3 d5 (-1) + W: f2 / B: f3 f5 (-1) | 8 | -2 = R ('L', 'L') | L L / L L | exact | 5.0 | 962 | agree (exact) |

### Totals (19 pairs, 38 sides to move: 18 for P, 20 for N)

- Priority pairs P (9 pairs, 18 sides): 6 sides exact, all 6 match the model; 12 sides are bounds, all 12 contain the model result. 1 of 9 pairs fully exact (pair 21, value 1 = L, W W / W W). 0 contradictions.
- New live-pair test N (10 pairs, 20 sides): 13 sides exact, all 13 match the model; 7 sides are bounds, all 7 contain the model result. 6 of 10 pairs fully exact (N1, N4, N6, N7, N8, N9), N2 exact on one side. 0 contradictions.
- Combined: 19 of 19 pairs have no disagreement with the model sum (0 interaction errors, 0 sum errors); 19 of 38 sides are exact, all 19 match; the other 19 sides are bounds consistent with the model. The 7 fully or half exact sums that involve two nonzero live games (N1, N2, N4, N6, N7, N8, N9) include sums of 1+1/2±1/2, 1+(-1/2±1/2), -1+(-1/2±1/2), 1/2±1/2+1/2±1/2, -1/2±1/2+-1/2±1/2, 1+1, -1+-1, so the model sum is confirmed in real chess for those cases (cap 1, king and anchor setup of this board).
- Cap 2 (tried where the cap-1 run peaked under 6 GB): pair 40 (3290 s) and pair 1 (3985 s) were each stopped at the 12 GB limit with no answer; pair 48 (stopped at the time limit after 86 min, 5.0 GB at last poll) and pair 29 (stopped at the time limit after 56 min, 4.5 GB at last poll) did not finish. So no cap-2 result exists; the bounds above stay bounds. Pairs 22, 35 and N0, N3, N5 were not tried at cap 2.

### Disagreements and their classes

There are no pair-level disagreements, so there is nothing to class as an interaction error or a sum error.

**Components alone (corrected 2026-11-22 by the planner).** The first version of this section reported four exact
mismatches for the negative-valued components played alone. That was a lookup error: `analysis12.solo()` builds the
file name from the position, and on this case-insensitive file system `solo_..._Pd2_pd4_pd5` opens
`solo_..._Pd2_Pd4_pd5` (a different position, value 1). Matching on the position stored inside each JSON file gives:

| component (model value, class) | real, white to move / black to move | verdict |
|---|---|---|
| d3/d4 d5, d2 d3/d4 d5, d2 d3/d4 (value 0, P) | L L / W D | exact match / bounds contain the model |
| f3/f4 f5, f2 f3/f4 f5, f2 f3/f4 (value 0, P) | D L / W W | bounds contain the model / exact match |
| d2 d4/d5 and f2 f4/f5 (value 1, L) | W W / W W | exact match |
| d2 d3/d5 (1/2±1/2, N) | W W / L L | exact match |
| f2 f3/f5 (1/2±1/2, N) | W W / D L | exact match / bounds |
| f2/f4 f5 (-1/2±1/2, N) | W W / L L | exact match (`soloX_0`) |
| d2/d4 d5 (-1/2±1/2, N) | W D / L L | bounds / exact match (`soloX_1`) |
| d2/d3 d5 (-1, R) | L L / L L | exact match (`soloX_2`) |
| f2/f3 f5 (-1, R) | not run (its file name collides with f2 f3/f5) | |

So 13 of the 14 solo positions were run; 19 of their 26 sides are exact and all 19 match the model, 7 are bounds
that contain it, 0 mismatches. The results also respect the board symmetry (colour swap with the mirror d <-> f and
rank flip maps the anchors to themselves): d2 d3/d5 and f2/f4 f5 are images of each other and both give W W / L L.

### Caveats (COMPUTED-1)

- 19 of 38 sides are bounds, so they confirm nothing beyond "not contradicted". Any hidden disagreement would sit in those sides.
- All 19 pairs share the same anchors (Pa3, pa4, Kh4, kb3) and place the components on files d and f with file e empty; the d and f copies of the same component do not have identical real results (the 0 shapes differ on which side is exact), so the king and anchor placement matters at the bound level.
- The 9 P pairs each contain a locked value-0 component and so test the sum only weakly; the 10 N pairs are the informative ones.
- Wall-clock times in the table are `time -l`-style seconds of the whole kpsolve process; peak GB is `maxrss` from `/usr/bin/time -l`.
