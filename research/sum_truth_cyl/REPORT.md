# Avenue 5: explicit-king sum test on cyl:8x6, and the 56,402 K12 e.p. roots

## 5-line summary
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
