# K31 referee report (VERIFY)

Verdict: ACCEPT_WITH_FIXES. Every number I recomputed matches K31. Three statements in K31's wording are inexact
(grid coverage, the "470 cases", the phrase "a zero for the mover"); the replacement edits in `verify/EDITS.md` fix them.
No earlier referee output existed in `verify/`; I reused nothing from one. I read K31's logs only to compare against.

## What I built (all in `verify/src`, written from K20's definition text, not from lk.cpp, kg.cpp or tempo.cpp)
`mini.h`: the game LK (cylinder or flat, any number of blocked pairs, passed-pawn terminals, legality rules of the
definition), the battery B34 (34 games), a K-component sum solver by retrograde analysis with plies-to-end, integer
reservoirs. `cls.cpp` classifies roots by B34 signature and dumps +1/-1 roots. `prof.cpp` gives the lead profile
Lw, Fw, Lb, Fb (same definition as K31's tempo.cpp header). `pairs.cpp` gives x+y+c and x+integer+c. `c2.cpp` gives the
flat:6x6 outcomes and plies. Binaries were deleted at the end; sources, logs and scripts are kept (588 KB).
The only other binary I built was K20's `lk` (privately, to rerun `lk allpairs`); it was deleted too.

## Claim by claim

1. C1, counts of +1/-1 roots per (W, H, r): CONFIRMED.
   My solver gave identical root counts and identical +1/-1 counts in all 383 cases that K31's runs and mine share
   (`verify/cmp_sweep.py`, 0 differences), and identical sets of +1 and -1 roots (positions) in 112 cases, 720 roots
   (`verify/cmp_roots.py`, 0 differences). Table 1 (W = 5, 6, 8, 10, 12; H = 5..8) reproduced cell by cell.
   Reproduce: `verify/sweep_mine.sh`, `verify/src/cls cyl W H a<r> [dump]` (build: c++ -O2 -std=c++17 -o cls cls.cpp).
2. C1, the rule "+1 and -1 roots exist iff W even and W >= 6": CONFIRMED on the searched grid; still a CONJECTURE.
   Hidden gap found: K31's 934 cases are not "H = 4..12, W = 3..26" (1,080 cases). Missing were H = 4 with W = 17..24
   (8 cases); W = 3, 4 for H >= 9 (60); W = 25, 26 for H >= 7 (78). Total 146. I ran all 146 with my solver
   (`mine_gap1/2/3.txt`): the rule holds in all of them (even W >= 6: both signs; odd W and W = 3, 4: none). The
   full grid now has 495 cases with roots and 585 without, and 11,914 roots of value +-1 (10,514 in K31's runs plus 1,400).
   Spot checks outside the grid (12 cases, `mine_extra_direct.txt`): H = 13 (W = 6, 7, 8, 9), H = 14 (W = 5, 10),
   W = 28, 29, 30, 31 with H = 4, 5, 6: all agree with the rule. Label COMPUTED-1 for my 146 (one implementation).
3. The "470 cases with W*H <= 127" ran in both K31 solvers: REFUTED as worded. 474 cases have W*H <= 127; four of them
   (cyl:25x4 a2, 26x4 a2, 25x5 a2, a3) were lk-only (sweep_wide ran with nokg). The two-solver set is 470 cases, the
   lk-only set is 464 (460 with W*H > 127 plus these 4). The 470 are real and all agree (K31 logs: agree_sets and
   agree_classes true in 470 of 470). The label CHECKED-2 stands for those 470; fix the wording only.
4. Structure: every +-1 root has both kings on file W/2 and an even rank difference: CONFIRMED. From K31's logs: 10,514
   of 10,514 (odd rank difference 0, rank difference < 2: 0, +1 5,257 and -1 5,257). In my own runs (541 cases) the counters
   "kings not both on file W/2" and "odd rank difference" were 0 everywhere.
5. Saturation: row at W is constant for even W >= 2H-2 and differs at 2H-4: CONFIRMED from K31's logs for H = 4..12 (first W
   equal to the last row is exactly 2H-2) and by my runs W = 26 for H = 7..12, W = 20 and 22 for H = 12, W = 17..24 for H = 4.
   Caveat in K31's text: for H = 4 K31 ran only W = 6..16, 25, 26, and for H >= 7 only up to 24; the gaps are now filled.
6. Colour symmetry (+1 count at rank r = -1 count at H-r): CONFIRMED in K31's data (+1 and -1 totals equal) and in all rows I computed.
7. Flat boards, one pair, no +-1 root: CONFIRMED. My solver: 405 cases (W = 5..10, H = 5..7, every file, every rank, no mirror
   reduction), 0 roots (`flat_mine.txt`). K31's 216 are the mirror-reduced subset.
8. C3 sums: x+y+c equals the integer sum: CONFIRMED on four configurations by my own solver: cyl:6x6 a2, a3, a4 (N = 4) and
   cyl:8x6 a3 (N = 3), 0 mismatches; per-pair outcomes (+1,+1) (W,W); (+1,-1) (L,W); (-1,-1) (L,L) as K31 reports. The totals
   8,166 and 2,308 equal the sum of K31's per-configuration lines (13 configurations). The other 9 configurations are K31's only
   (tempo.cpp, which shares lk.cpp's graph and its own copy of the solver). `lk allpairs` rerun on cyl:6x6 a3, cyl:7x6 a3,
   cyl:9x6 a3: 105,625 / 145,161 / 219,961 pairs, 0 mismatches (identical to K31's lines); the 2,706,185 total over 14 configurations
   equals the sum of K31's lines. Note: `allpairs` is a two-component sum with no context, so it checks x+y at c = 0 only.
9. C3 interpretation "a lead of two tempi is not decisive": CONFIRMED for sums, but "refuted" is too strong as a statement
   about the conjecture. The test shows that x + x (two separate groups) acts as the integer 2 and has a second-player win at
   c = -2. It says nothing about one group with a lead of two, which is what the conjecture was about. K31's edit text says
   "FALSE for sums", which is accurate; K31's claim line "C3 is refuted as an explanation" is not. My edit keeps the scoped wording
   and adds that the single-root form was not tested.
10. Single-root lead profile, N = 12, 764,312 root entries of 571 configurations: CONFIRMED and upgraded. I ran my solver on all
    571 configurations (`verify/prof_cmp.py`): the marginal counts of Lw, Fw, Lb, Fb equal K31's for every configuration, 0 differences.
    Leads take only -1, 0, 1 and 12 (so none in 2..11). Wording fix: these are root entries (a root is counted once per configuration), the
    571 configurations include two-pair models some of which are not faithful, and the flat boards are 6x6, 7x6, 8x6 only.
    N = 30: my solver reproduced all eight lines of K31's profile (cyl:6x6 a2, a4, cyl:8x6 a3, cyl:10x6 a3, cyl:12x8 a4,
    flat:6x6 a2,c4, cyl:8x6 a2,d3, cyl:7x6 a2,c3), values only -1, 0, 1, 30 (`prof_mine_N30.txt`). K31's remark that the 344 roots with Lw = 1
    split into 271 named +1 and 73 not named +-1 is what the log says (counted from `profile_N12.jsonl`; not recomputed one by one).
    The remark "a finite lead of exactly 1 never occurs on a faithful odd-width cylinder" holds in the log (the 28 odd-width cylinder entries
    with a lead of 1 are all non-faithful two-pair models); COMPUTED-1.
11. C2 line (flat:6x6 `Kc3 ka4 Pa2 pa3 Pc4 pc5`): CONFIRMED with plies. My solver (own outcomes and plies-to-end, last move counted):
    White to move c = -2..2: L(6) L(6) W(13) W(5) W(5); Black to move: L(7) W(14) W(4) W(4) W(4). So Black to move c = 0: 4 plies;
    White to move c = 0: 13 plies; White to move with one spare Black move (c = -1): Black wins in 6. B34 label of the root: +1.
    `Kd3 kb4` (same pawns): label 0; White to move L(2), Black to move W(10) at c = 0: the mover loses. Wording: "a zero for the mover"
    is confusing; "has value 0: the player to move loses" is what was computed.
    The mechanism ("race lead around a zugzwang", not a reservoir) stays a CONJECTURE, as K31 says: one root on one board, and the
    +1 root equals the integer 1 in every sum, so sums cannot distinguish.
12. Proof claim (odd W follows from "all +-1 roots have both kings on file W/2"): the implication is correct (W/2 is not an integer
    for odd W). It is a one-line reduction from an unproved premise, and K31 presents it that way (CONJECTURE for the premise). No PROVED label is
    needed or used in the edit. No proof of C1 or of the absence of a lead of two exists in the report.
13. ref3: not applicable (ref3 is the P/frozen solver; K31's claims are about LK). NOT_CHECKED for any P-model or chess claim; K31 makes none.

## Edits
Both OLD blocks occur exactly once in the current `kings/theory/LOOPY.md` (3,116 lines; checked by program for K31's EDITS.md and for mine).
K31's NEW text is accurate in its numbers but I replace it because of: the grid statement (items 2, 3), the "refuted" scope (item 9), the wording of
"a zero for the mover" (item 11), "roots" versus "root entries" and the model caveat (item 10). `verify/EDITS.md` also adds the referee's checks, each
with its label. The tag date 2026-10-27 follows the task text (K31's second session ran on 2026-10-28; K33 in LOOPY uses 2026-10-28). The author may
change the tag.

## Process notes
K31's FINDINGS.md is absent (the harness refused it); the report exists only in the orchestrator's summary field, plus `summary.json` and `EDITS.md`.
K31 logged one read-only `git log` (rule slip), harmless. My own heavy.sh jobs: I queued a full sweep through `heavy.sh`, waited about 15 minutes in a
queue of 8 waiters without a slot, killed my own waiting processes (PIDs 89837, 1492, 89845, recorded in `verify/verify_pids.txt`; none had started a
solver), and ran short runs instead (each run under 2 CPU-seconds and under 400 MB, nice 15; in total about 3 CPU-minutes in chunks of under one
minute). No pattern kills. Nothing outside `K31/` was written. Largest RSS of mine: 0.72 GB (pairs, cyl:8x6 N = 3).

## Commands (from `K31/verify`, c++ -O2 -std=c++17 for each source in `src`)
`./sweep_mine.sh Wmin Wmax Hmin Hmax out`; `./src/cls cyl 10 6 a3 dump`; `./flat_mine.sh`; `./src/prof cyl 8 6 a3 30`; `python3 prof_cmp.py`;
`./src/pairs cyl 6 6 a3 4`; `./src/c2`; `python3 cmp_sweep.py mine_*.txt`; `python3 cmp_roots.py dump_mine.txt`.
