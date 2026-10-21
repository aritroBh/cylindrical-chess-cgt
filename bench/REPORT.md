# ChessSums benchmark (workstream C1)

Saved by the parent session from the workstream's final report (workflow `wf_3dfce063-f42`). Workflow agents may not write report files, so the text below is the agent's, unedited apart from removing that notice. Verification verdicts come from the workflow's adversarial verifiers; "not verified" includes verifiers that were cut off by a usage limit.

ChessSums report (workstream C1). Continuation of the cut-off run at git 28d790f. Output dir: /Users/aritro/Downloads/Research/Chessendgames/bench/. No git commands were run after an initial read-only `git log`/`git status`. Nothing outside bench/ was written, apart from scratch files in the session scratchpad. No installs, no LLM or API calls.

WHAT WAS ALREADY THERE (v1, 28d790f)
The previous run left a complete benchmark: generator, 518-component library, train/val/test/test_heldout = 20k/2k/2k/2k plus 8-file subsets, scorer, prompts, GRPO reward draft, Python and C alpha-beta baselines, verification and README. I kept all of it and changed only what the 2026-10-16 convention change required.

WHAT THE CONVENTION CHANGE BROKE, AND THE FIX
The adopted e.p.-aware passed test (a pawn that can still be taken en passant is not passed) disagrees with the textbook test only about a pawn that has just double-stepped, can be taken e.p., and is textbook-passed. The race-rule promotion distance skips the same pawns, so it changes only there too. v1's filter 5 ("no e.p. capture ever available") skipped every position the textbook test had already ended, so it never saw these cases.

Direct computation with the e.p.-aware cylcgt (worktree flag PASSED_RESPECTS_EP) over all 518 v1 components, in 12 settings (2 passed tests x 3 race rules x e.p. on/off):
- 48 components change the value of the root or of some child; 28 of them change at the root.
- All 20 v1 components of value +-1/2 or +-1/2* are among the 48. Examples (count rule, e.p. on), textbook -> e.p.-aware:
  - W a2 c2 / B a3 b6: 1/2 -> up;
  - W a6 b3 / B a7 c7: -1/2 -> down;
  - W a2 c2 / B a3 b5: 1 -> *;
  - W a2 c2 / B a4 b6: 1/2* -> {*,0|{*|-1}};
  - some become games with +-BIG inside.
- 52 more keep every value but have some position judged differently, and no e.p. capture is ever playable in them under either test.
- With e.p. off the two tests never differ.

New filter 5' (bench/components.py): reject a component if, at any position the textbook test ends, the pawn that has just double-stepped is textbook-passed and capturable e.p. Informal argument (in the docstring, not yet reviewed): with filters 5 and 5', no reachable position is judged differently, so both tests build the same game tree and give identical values; and since no e.p. capture is ever playable, cylcgt's per-component e.p. model is exact under both tests.

Result: library version 2 = v1 minus 100 = 418 components.
- 37 distinct values, 144 orbits.
- Hold-outs: value class (up* and down*) 3 orbits / 12 components; structure 14 orbits / 39 components.
- Consequence: v2 has NO non-integer-number component. Fractions survive only inside switches such as 3/2+-1/2, and the 'number' value kind is gone from every split.
- I chose identical trees (418) over the weaker "identical values" library (470, the intersection of the two single-test libraries). That choice is flagged below.
- build() pins PASSED_RESPECTS_EP=False while it runs, so the output does not depend on which cylcgt is on the path.

Two bugs in my own new code were caught and fixed during this run:
- The first draft of filter 5' was too broad: it flagged any e.p.-capturable pawn at a terminal position and kept only 300 components. I caught this because the count disagreed with the direct computation.
- The first ab.c e.p. counter counted harmless double steps (about 20 million events). I fixed it and re-ran verify and the baseline. The superseded logs are bench/logs/*_v2_counter_overbroad.log; they show no disagreements and identical node counts.

DATASET v2 (bench/data, regenerated; seed 20261015; library_version 2 in manifest.json)
| split | rows | k | 8-file subset |
|---|---|---|---|
| train | 20,000 | 1: 3,000 / 2: 7,000 / 3: 10,000 | 16,324 |
| val | 2,000 | same shares | 1,626 |
| test | 2,000 | 4, 5, 6: about 667 each | 364 (all k=4; outcomes L139 R147 N67 P11) |
| test_heldout | 2,000 | 1: 400 / 2: 800 / 3: 800 | 1,642 |
- The main splits are outcome-balanced per k.
- Train uses 367 non-held-out components.
- Two further runs reproduced all 10 files byte for byte (cmp): one with the main cylcgt, one with the e.p.-aware cylcgt first on sys.path.

Chance baselines (score.py --baseline random-legal --seed 0):
| split | random letter (outcome) | constant "0" (value) | random legal move wins | items with chance <= 1/4 |
|---|---|---|---|---|
| val | 0.24 | 0.25 | 0.65 | 0.22 |
| test | 0.24 | 0.25 | 0.56 | 0.16 (551 items) |
| test_heldout | 0.24 | 0.25 | 0.59 | 0.22 |
Test has 554 unique-winning-move items.

VERIFICATION (bench/results/verify_report.md, 1,273 s; conventions_report.md, 1,304 s). Zero disagreements.
- A1: 836/836. Component outcomes, e.p. on and off, cylcgt vs Codex crosscheck/minimax.py.
- A2: 418/418. c + r(-v) is a second-player win; for 406 of them r is from another orbit.
- A3: 300/300. Random component pairs.
- B: 9,000/9,000 rows. cylcgt whole-board recomputation of value (e.p. on/off) and winning moves.
- B': 2,000/2,000. Race rules mover and opponent.
- C: 4,887/4,887. Outcomes vs Codex minimax, real-chess e.p.
- C': 600/600. Full winning-move sets vs Codex minimax.
- D: 25,995/25,995. Every row vs bench/ab.c with TT; 5 test k=6 rows hit the 3 CPU-second cap.
- D': 0 in every split. The new ab.c counter of double steps that leave a passed pawn the opponent could take e.p. A count of 0 certifies that the e.p.-aware search would visit the same nodes and return the same result, so D confirms the outcomes under both tests without using cylcgt. The C and Python solvers agree exactly on results, node counts and counter over 447 searches. Positive control (bench.conventions --positive-control): the counter fires for 20 of the 100 removed components and for 0 of the 418 kept ones.
- E1: 418/418. Every kept component and every child is identical in all 12 settings.
- E2: 9,000/9,000 rows. Whole-board value and winning moves re-solved under the e.p.-aware test.
- E3: 518/518. Filter 5' (bench code, textbook test only) agrees with exact "judged differently" detection (e.p.-aware cylcgt).
- KEY-FACT W a2 c2 / B b7 d7 on 4 flat files:
  - textbook: *2 under count and mover (e.p. on and off), 0 under opponent;
  - e.p.-aware, e.p. on: {2+-1 | -2+-1} under count and mover;
  - e.p.-aware, e.p. off: *2 under count and mover;
  - 0 under opponent with e.p.-aware.
  This matches the stated known facts. The position is excluded under either test, so ChessSums has no *2 component.

BASELINE: whole-board alpha-beta that ignores the decomposition (bench/results/baseline_scaling_c.md)
Settings: 8 nested chains, k = 1..8, plus 12 benchmark rows per k; caps of 30M nodes / 60 CPU-seconds per search.

Median nodes along the chains:
| method | k=3 | k=8 | log-linear fit (k = 3..8) | unsolved at k=8 |
|---|---|---|---|---|
| plain | 22 | 1,402,298 | about x8.9 per added component | 5 of 16 |
| TT | 22 | 24,837 | about x4.0 per added component | 2 of 16 |

- Step-to-step factors are irregular, x1.7 to x23, and are biased low at large k because unsolved searches drop out.
- CGT: summing cached values takes median <= 0.0005 s (max 0.024 s); computing from scratch takes median <= 0.05 s (max 0.18 s).
- On the test rows with k=6, plain alpha-beta fails on 5 of 24 searches; TT finishes all.
- Two runs gave identical node counts. Times are CPU seconds on a machine at load average 120-180, so they are noisy.
- Growth is milder than v1's (about x16), but the libraries differ, so the two are not directly comparable.

HONESTY LABELS
- Every CGT value, including the e.p.-aware ones, comes from one implementation, cylcgt; the e.p.-aware values are the same code with one flag flipped.
- The parts independent of cylcgt are: filter 5' (bench code), the ab.c search and its counter, and Codex's minimax (textbook test only).
- The filter-5' sufficiency argument is informal and has not been reviewed by a second model or a human.
- Nothing has been embedded in real chess with kings.
- No model or engine has been evaluated.

CODE CHANGES
- components.py: filter 5' and the textbook pin.
- generate.py: library_version 2 and a passed-test note in the manifest.
- New conventions.py: the 12-setting comparison, the v1 rebuild, the instance re-solve, and --positive-control.
- New stats.py.
- ab.c and baseline.py: the e.p. certificate counter (4th output column) and the log-linear fit in the tables.
- verify.py: check D'.
- tests/test_bench.py: 25 tests, all passing; 2 new ones, and the C-vs-Python test now also compares counters.
- README.md: rewritten for v2, with both conventions labelled 'textbook' and 'e.p.-aware'.

REPRODUCE (from /Users/aritro/Downloads/Research/Chessendgames; prefix every Python command with PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.)
- `.venv/bin/python -m bench.generate --seed 20261015`
- `cc -O2 -o bench/ab bench/ab.c`
- `.venv/bin/python -m pytest -q -p no:cacheprovider bench/tests` (add -s to print the 447/17 search counts)
- `.venv/bin/python -m bench.verify`
- `.venv/bin/python -m bench.conventions --cylcgt-root /private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt`
- `.venv/bin/python -m bench.conventions --positive-control`
- `.venv/bin/python -m bench.baseline --engine c --chains 8 --kmax 8 --per-k 12 --node-cap 30000000 --time-cap 60 --seed 1`
- `.venv/bin/python -m bench.score --gold bench/data/{val,test,test_heldout}.jsonl --baseline random-legal --seed 0`
- `.venv/bin/python -m bench.stats`
- The WT-path determinism run was done as: cd <ep-wt> && PYTHONPATH=<ep-wt>:<project> python -c "from bench.generate import main; main(['--seed','20261015','--out',<scratch>])". This is equivalent to the -m form given in the README.

## Claims

| id | importance | worker status | adversarial verification | statement |
|---|---|---|---|---|
| C1 | headline | computed-once | reproduce: confirmed; refute: confirmed; theory: confirmed | Under the e.p.-aware passed test, 48 of the 518 v1 ChessSums components change the value of the root or of some child (28 at the root). All 20 v1 components of value +-1/2 or +-1/2* are among them, e.g. W a2 c2 / B a3 b6 goes from 1/2 to up. With e.p. off the two tests never differ. |
| C2 | headline | checked-two-ways | reproduce: confirmed; refute: confirmed; theory: confirmed | Library v2 (418 components, v1 minus the 100 filter-5' hits) has identical game trees under the textbook and e.p.-aware tests. Every component and every child has the same value in all 12 settings (2 passed tests x 3 race rules x e.p. on/off). |
| C3 | key | checked-two-ways | reproduce: confirmed; refute: confirmed | The ground-truth outcome class of all 26,000 dataset rows except 5 (test, k=6, capped) is confirmed by bench/ab.c whole-board alpha-beta. ab.c met zero double steps leaving an e.p.-capturable passed pawn, which certifies the same outcomes under the e.p.-aware test. |
| C4 | key | computed-once | reproduce: confirmed; refute: confirmed | Value and winning-move sets re-solved on the whole board under the e.p.-aware test match the stored truth on 9,000/9,000 rows (all of val, test and test_heldout plus 3,000 train). The textbook re-solve (check B) also matches on 9,000/9,000. |
| C5 | key | checked-two-ways | not verified | Outcome classes also agree with Codex's independent minimax (textbook test): 4,887/4,887 rows, plus 600/600 full winning-move sets. Component checks A1 836/836, A2 418/418, A3 300/300. |
| C6 | key | computed-once | not verified | Whole-board alpha-beta that ignores the decomposition grows about x8.9 (plain) and x4.0 (TT) in median nodes per added component, k = 3..8 on nested chains. At k=8, 5 of 16 plain searches hit the 30M-node cap. CGT stays at median <= 0.05 s from scratch. |
| C7 | minor | computed-once | not verified | KEY-FACT W a2 c2 / B b7 d7 (4 flat files): under the textbook test, *2 under count and mover (e.p. on and off) and 0 under opponent. Under the e.p.-aware test, {2+-1 \| -2+-1} with e.p. on and *2 with e.p. off, under count and mover; 0 under opponent. So it is excluded from ChessSums. |
| C8 | key | computed-once | not verified | Library v2 contains no component whose value is a non-integer number; fractions occur only inside switches. 37 distinct values, 144 orbits. |
| C9 | minor | computed-once | not verified | The generator is deterministic. Two reruns with seed 20261015, one with the main cylcgt and one with the e.p.-aware cylcgt first on the path, reproduced all 10 data files byte for byte. |

### How to reproduce each claim

- **C1**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.conventions --cylcgt-root /private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt
  ```
- **C2**:

  ```
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.conventions --cylcgt-root <ep-wt>; also pytest bench/tests -k convention_free
  ```
- **C3**:

  ```
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.verify ; PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.conventions --positive-control
  ```
- **C4**:

  ```
  bench.conventions --cylcgt-root <ep-wt>; bench.verify
  ```
- **C5**:

  ```
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.verify
  ```
- **C6**:

  ```
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.baseline --engine c --chains 8 --kmax 8 --per-k 12 --node-cap 30000000 --time-cap 60 --seed 1
  ```
- **C7**:

  ```
  bench.conventions --cylcgt-root <ep-wt>
  ```
- **C8**:

  ```
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.stats
  ```
- **C9**:

  ```
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. .venv/bin/python -m bench.generate --seed 20261015 --out <scratch>; cmp each file
  ```

## Bugs found

- v1 (git 28d790f, my earlier run): filter 5 did not examine positions that the textbook test ends. 100 kept components had game trees that depend on the passed test, and 48 of them change value under the e.p.-aware test, including every +-1/2 and +-1/2* component. Fixed by filter 5' and regenerated as library v2.
- This run, fixed: the first draft of filter 5' flagged any e.p.-capturable pawn at a terminal position. It was over-broad (it kept only 300 components). I caught it because the count disagreed with direct computation, then narrowed it to the exact condition: the double-stepped pawn is textbook-passed and capturable.
- This run, fixed: the first ab.c e.p. counter counted every double step that left an enemy pawn beside the moved pawn, about 20M harmless events. I restricted it to passed pawns and re-ran verify and the baseline. Superseded logs: bench/logs/*_v2_counter_overbroad.log.

## Open questions

- Library choice: 418 components with identical trees (current) or 470 components with identical values (the intersection of the two single-test libraries; adds back +-3 and more hot games, but loses the ab.c certificate for rows that contain them)?
- Under the adopted e.p.-aware test, no small component (width <= 4, <= 4 pawns) has a non-integer number value. Should the candidate set grow (width 5, 5 pawns, other ranks) so that fractions such as 1/2 return?
- The LLM prompt states the textbook passed rule. That is exact here because e.p. never arises. Should it state the adopted e.p.-aware rule instead?
- The filter-5' sufficiency argument is informal and has not been reviewed by a second model or a human.

## Next steps

- Run the planned Stockfish, Lc0 and LLM evaluations on test and test_heldout with bench/prompts.py and bench/score.py (none run yet).
- After ep-aware-passed is merged into main, re-run bench.conventions without --cylcgt-root and keep the generator's textbook pin, or drop it.
- If fractions are wanted under the adopted convention, extend components.candidates() to width 5 / 5 pawns and re-run the filters (expect much longer build times).
- Have a second model or a human review the filter-5' argument in the bench/components.py docstring.
- Optionally re-time the baseline on an idle machine; node counts will not change, times will.
