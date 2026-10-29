# K31 referee report, second referee (VERIFY)

Verdict: ACCEPT_WITH_FIXES. Every number I recomputed matches K31. I found no refuted claim.
The fixes are wording and evidence: the old spot-check line was imprecise, the "lead of exactly 1" sentence was loose,
and two labels can now be raised. Replacement edits: `verify/EDITS.md`.

## What I reused and what I built
An earlier referee had already finished (`K31/VERIFY.md`, `verify/src`, `verify/mine_*.txt`). I moved its report to
`verify/VERIFY_first_referee.md` and its edits to `verify/EDITS_first_referee.md`. I did not run or read its code. I used its
`mine_*.txt` only as comparison data (item 1). I did not read `mini.h`, `lk.cpp`, `kg.cpp` or `tempo.cpp`.
My own code is in `verify/r2/` and was written from the definition text in `K20/summary.json`:
`lk3.cpp` (LK for any number of pairs with passed-pawn terminals, a generic K-component retrograde sum solver, the 34 games of
B34, the signature classifier) and `lk3b.cpp` (lead profiles, sums with contexts, `allpairs`, line plies by value iteration).
First checks: cyl:6x6 a3 gives 794 roots, +1/-1 = 3/3, and class counts +1 3, -1 3, 0 2, off 57, on 57, tis 6, tisn 6, as K31's log.
ref3 does not apply (P/frozen solver; K31 makes no P claim): NOT_CHECKED.

## Claim by claim

1. C1, counts of +1/-1 roots over the whole grid H = 4..12, W = 3..26: CONFIRMED, and now CHECKED-2 for all 1,080 cases.
   My solver ran all 1,080 cases (through `heavy.sh`, 7 chunks, largest case 92,270 roots, 83 MB). Differences against K31's
   logs: 0 in 934 of 934 cases. Differences against the first referee's `mine_*.txt`: 0 in 541 of 541 cases (all 146 gap cases
   among them). Root sets (positions) equal K31's dumped sets in 452 of 452 cases, 10,514 roots (`r2/cmproots.py`).
   Totals: 495 cases with W even and 6 <= W <= 26, every one has both signs; 585 cases (W = 3, 4, odd W) have none;
   11,914 roots of value +-1 (+1: 5,957, -1: 5,957, my count from the sweep files, `r2/summarize.py`). K31's numbers 934 + 146 = 1,080,
   470 two-solver cases, 464 lk-only (460 with W*H > 127 plus four with W*H <= 127), 474 cases with W*H <= 127: all recomputed from K31's
   logs and correct. Rule for all H, W: CONJECTURE (correctly labelled).
   Reproduce: `verify/r2/sweep.sh Hmin Hmax Wmin Wmax out`, `python3 verify/r2/cmpall.py`, `lk3 cls cyl 8 6 a3 dump`.
2. Structure (both kings on file W/2, same colour): CONFIRMED on all 11,914 roots (counters "not on file W/2" and "odd rank
   difference" are 0; `r2/out/s_h*.txt`). CHECKED-2 for the 10,514 roots whose sets equal K31's.
3. Colour symmetry and saturation: CONFIRMED. +1 count at r equals -1 count at H - r in all 1,080 cases. First W with the last row
   is exactly 2H - 2 for H = 4..12 and the 2H - 4 row differs. For H = 12 only W = 22, 24, 26 are in the grid, so the evidence
   there is thin; the edit says so.
4. Flat boards, one pair: CONFIRMED. 405 cases (W = 5..10, H = 5..7, every file and rank, no mirror reduction), 0 roots
   (`r2/out/flat1.txt`). My solver does find +1 at `Kc3 ka4 Pa2 pa3 Pc4 pc5` (two pairs), so the flat code is not blind.
5. Spot checks outside the grid: K31's edit text was imprecise. The first referee's file holds 12 chosen cases (H = 13 with W = 6, 7, 8, 9; H = 14 with W = 5, 10;
   W = 28..31 with H = 4, 5, 6, 6), not "W = 5..10". I ran 237 cases (every rank, H = 13 and 14 with W = 4..12; every rank, H = 4..6 with
   W = 27..34, `r2/ext.sh`): all agree with the rule, 0 exceptions. COMPUTED-1.
6. C3 sums with integer contexts: CONFIRMED, 0 mismatches. K31's totals 8,166 and 2,308 are the sums of its 13 lines (12 in `pairs.out`,
   cyl:8x7 a4 in `pairs_8x7_a4.out`); "outcomes" counts the two movers separately. My solver, own graph: cyl:6x6 a2, a3, a4 (N = 4),
   cyl:8x6 a2, a3 and cyl:8x5 a2 (N = 3): 0 mismatches (`r2/out/pairs_*.txt`), same root counts. CHECKED-2 on these six, as raised
   in the edit. Beyond the claim, with all 34 B34 games as the context (x + y + K against the integer sum + K): 5,712 outcomes on
   cyl:6x6 a2, a3, a4 and cyl:6x5 a2, 0 mismatches (`pairsbat`).
7. `lk allpairs`: CONFIRMED and upgraded. My solver with its own graph, all 14 configurations: the same numbers of named roots in each, total 2,706,185
   ordered pairs, 0 mismatches (`r2/out/allpairs_all14.txt`). K31 said "the game graph is the same for both solvers"; for me it is not, so this is
   CHECKED-2 for the graph and the sum.
8. Single-root lead profiles: CONFIRMED, upgraded. N = 12: for all 571 configurations I reproduced the joint histogram of (Lw, Fw, Lb, Fb), not only the
   marginals: 8,839 distinct (configuration, lead tuple) cells, 764,312 root entries, 0 differences, 0 races (`profbatch`). Lead values are only -1, 0, 1, 12.
   N = 30: all eight lines equal K31's; the entries sum to 16,575; values only -1, 0, 1, 30. The sentence in K31's edit "a lead of exactly 1 occurs on
   even-width cylinders and on two-pair configurations, and on no faithful odd-width cylinder" is true but loose. By count: all 56 single-pair even-width
   cylinder configurations, 2 of 63 faithful two-pair even-width cylinder ones, 16 faithful two-pair flat ones, 6 non-faithful odd-width two-pair cylinder ones;
   none of 92 faithful odd-width cylinder configurations, none of 63 single-pair flat ones. The edit gives these counts.
9. C2 line: CONFIRMED with plies by value iteration. `Kc3 ka4`, c = -2..2: White to move L6 L6 W13 W5 W5; Black to move L7 W14 W4 W4 W4.
   So 4 plies (Black to move), 13 plies (White to move), Black wins in 6 with one spare Black move (c = -1). `Kd3 kb4`: White to move L2, Black to move W10 at c = 0
   (the mover loses). B34 names: `Kc3 ka4` +1, `Kd3 ka4` {1|0}, `Kd3 kb4` 0, as LOOPY says. "Using files d and e" is true for the
   principal variation (Kd3, Ke4, Ke5, Kd6, Kd5); the edit now says "principal variation". Mechanism: CONJECTURE (correct).
10. "C3 is false for sums": correct as scoped (x + x acts as the integer 2). It does not test a single group with lead two. K31's edit says exactly that.
11. Proof claim: none is made. The reduction "odd W follows from kings on file W/2" is trivial and its premise is a CONJECTURE. No PROVED label used. CONFIRMED.

## Edits
Both OLD blocks of `K31/EDITS.md` occur exactly once in the current LOOPY.md (3,361 lines); so do the OLD blocks of `verify/EDITS.md`
(same text, checked by program). K31's NEW numbers are accurate. My replacements change: the spot-check sentence (item 5); the labels (items 1, 6, 7, 8);
the "principal variation" wording (item 9); the "lead of exactly 1" counts (item 8); the names "first referee" and "second referee", since two referees now exist.
The tag dates follow the task text (2026-10-27), with "2026-10-28" for the referee revision; the author may adjust.

## Process notes
Runs: one-off runs under one CPU-minute at nice 15; the grid sweep through `heavy.sh` (7 queued chunks, I waited about 15 minutes for the slots). Largest RSS 880 MB
(`pairs`, cyl:8x6). I killed nothing; no pattern kills; no git. First attempts crashed only because zsh does not word-split `$s` (my shell slip, fixed with `${=s}`) and one
return-code collision in my own code (found by the first output, fixed before any reported run). Writes only inside `K31/verify/` and this file.
Large sweep outputs are kept (about 1 MB); binaries in `verify/r2/bin` are deleted.
