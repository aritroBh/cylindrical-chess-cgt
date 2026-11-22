# Sum model S vs whole-board game W: exhaustive census

Question: how often does the outcome (P/N/L/R) of the sum model S(X) differ from the whole-board game W(X), for passer-free X? Does it depend on the race rule (count, mover, opponent) and on the passed-pawn test (textbook, e.p.-aware)?
All numbers below are in `analysis_w{3,4,5,all,cyl4,cyl5}.md` (made by `analyze.py` from the compressed raw rows in `data/`). Label: every number here is C1 (computed by programs, cross-checked by a second and a third program on a sample), none is a proof.

## Headline

1. Flat boards of width 3 and 4 (every position up to 6 pawns, 8 ranks): **zero** disagreements in all 6 configurations (width 3: 40,262 orbit reps; width 4: 154,813 reps). Cylinders of 4 and 5 files (up to 6 and 5 pawns): **zero** (60,447 and 14,883 reps).
2. Flat width 5 (up to 6 pawns): S and W differ in outcome for about 1.5% to 2.0% of all classes (table below). All disagreements are at roots with exactly 2 components, except 8 positions under textbook/mover (1 component at the root, see item 5).
3. The disagreement rate is about the same for the three rules. The count rule is in the middle (1.89%), mover is lowest (1.54%), opponent highest (2.02%) with the e.p.-aware test. So this census gives no support to the claim that the count rule is special for S vs W. It only shows that S = W fails for every rule once the position is not hereditarily sum-safe.
4. Theorem check (hereditarily_safe True implies S = W in outcome): **0 violations** in all 6 configurations, over 539,893 (textbook) and 540,503 (e.p.-aware) hereditarily-safe positions per rule. No stop-and-recheck was needed.
5. sum_safe() false positives (sum_safe() True but S != W): count rule 0, opponent rule 0, mover rule 0 with the e.p.-aware test; **8 with textbook/mover**. Smallest: `W: a5 c3 e2 / B: b7 d4 e6` (6 pawns, 1 component at the root; S=N, W=R). All 8 are 1-component roots, where sum_safe() is True by construction (it only looks at the top-level split), and none is hereditarily safe. All 8 were re-checked with cylcgt canonical forms and sumsolver (both modes): same outcomes (`logs/fpcheck.log`).

## Table 1: all flat positions, widths 3+4+5 (N = 599,098 orbit representatives)

Representative = one position per class under left-right mirror and colour swap (with the rank flip). D = outcome(S) != outcome(W). Wilson 95% interval.

| test | rule | D / N | rate [95% CI] |
|---|---|---|---|
| textbook | count | 11595 / 599098 | 1.935% [1.901, 1.971] |
| textbook | mover | 10496 / 599098 | 1.752% [1.719, 1.786] |
| textbook | opponent | 12104 / 599098 | 2.020% [1.985, 2.056] |
| e.p.-aware | count | 11300 / 599098 | 1.886% [1.852, 1.921] |
| e.p.-aware | mover | 9243 / 599098 | 1.543% [1.512, 1.574] |
| e.p.-aware | opponent | 12100 / 599098 | 2.020% [1.984, 2.056] |

All of the disagreements are on width 5. Width 5 alone (N = 404,023 reps) gives 2.87%, 2.60%, 3.00% (textbook: count, mover, opponent) and 2.80%, 2.29%, 2.99% (e.p.-aware); see `analysis_w5.md` (its first table). Weighted by orbit size over the whole set (2,386,432 positions) the rates are 1.93/1.75/2.02% (textbook) and 1.88/1.54/2.02% (e.p.-aware), nearly equal to the unweighted ones (`analysis_wall.md`).

By number of root components (all widths; textbook / e.p.-aware, count rule):
- 1 component (430,665 reps): 0 / 0 disagreements (mover/textbook: 8, see above).
- 2 components (167,515 reps): 11595 (6.92%) / 11300 (6.75%). Mover: 6.26% / 5.52%. Opponent: 7.23% / 7.22%.
- 3 or more (918 reps): 0.

By heredity (count rule, e.p.-aware): hereditarily safe 0 / 540,503; not hereditarily safe 11,300 / 58,595 = 19.3% [19.0, 19.6]. By sum_safe(): True 0 / 581,544; False 11,300 / 17,554 = 64.4%. Other rules are in the files. The cross table (hss x sum_safe) has no cell "hss True, sum_safe False", as expected.

By total pawns (width 5, count, e.p.-aware): n = 2, 3: 0; n = 4: 30 / 5,140 (0.58%); n = 5: 1000 / 46,102 (2.17%); n = 6: 10,270 / 352,274 (2.92%). The rate grows with n; the 6-pawn row is the biggest and the sixth pawn is the cut-off of this study, so rates for larger n are likely higher (not computed).

## Smallest S != W positions

Count rule, both tests (and in fact all rules), 4 pawns, width 5, 5 smallest by (pawns, text):
- `W: a5 d3 / B: b6 e4`, `W: a5 d4 / B: b6 e5`, `W: a5 e4 / B: b6 d5`, `W: a5 e5 / B: b6 d6`, `W: a6 d2 / B: b7 e3`: all S=P, W=N.
- Reason (all five): two separate locked pairs (a/b files and d/e files). In W the first player captures in one pair and has the only passed pawn at once. In S the capture makes +BIG in one component and the second player answers with a capture in the other component, -BIG, which cancels; the rest is zero, so S is P. This is the mechanism of `research/star2_frontier_recheck/REPORT.md`.
- The smallest S != W needs 5 files and 4 pawns (two components of 2 files each need 5 files with a gap). That is why widths 3, 4 and the cylinders of 4 and 5 files show nothing.

The confusion matrices (which outcome pairs occur) are in the "S != W confusion" section of each analysis file. Mostly W = N while S is L, R or P. Severe cases (S = L, W = R and the reverse) exist: for the count rule 428 + 820 (textbook), 416 + 672 (e.p.-aware).

## Cross-check (task 5)

Three programs: (A) census solver `s_exact.py` (outcome minimax over the sum of components, passers banked as integers 64 with pass moves), cylcgt canonical forms (B: `pawns.value` for S, `lemmas.common.W` for W), `sumtest/sumsolver.py` (C: `comp` mode for S, `whole` mode for W). Every sampled position, every rule, both S and W, compared across A, B and C (fixed seeds, `crosscheck.py`, results `data/cc_*.tsv`, logs `logs/cc_*.log`).
- Uniform sample, 2000 positions from the whole census set, per test (e.p.-aware and textbook), all 3 rules: 12,000 / 12,000 comparisons agree per test (2,000 x 3 rules x {S, W}).
- Extra stratum, 1000 positions with at least 2 root components and >= 5 pawns: 6,000 / 6,000 per test.
- Extra stratum, 1000 positions where the census found S != W under some rule: 6,000 / 6,000 per test.
- Zero mismatches in `data/cc_*.tsv`.
The W column of the census is `lemmas.common.alt_outcome` (plain alternating minimax); hereditarily_safe and sum_safe() are the repo's own functions, unchanged.

## A mistake I made and fixed (so you can trust the files)

My first census solver treated a banked +-BIG as a unit with unlimited free passes. That is wrong: in cylcgt a spent pass turns 256 into 255, so a cancelled bank can leave a small integer, and this changes outcomes. The 2,000-position cross-check caught it (about 1.3% of positions mismatched; cylcgt and sumsolver agreed with each other). I replaced S by the exact-integer version (`s_exact.py`), recomputed S for every flat position (`census_fix.py`) and redid the cylinders with it. All tables above use the corrected S. The earlier (wrong) numbers were deleted. `census.py` and `census_lib.py` still contain the old S and are only kept because the raw rows' W, hss and sum_safe columns come from `census.py`; do not use their S.

## Exact coverage

- Flat, 8 ranks, pawns on ranks 2 to 7 for both colours, e.p. on, no e.p. right at the root, no passed pawn at the root (textbook test, which implies no passer under the e.p.-aware test too). Total pawns 2 to 6 on widths 3, 4, 5. All such positions, none sampled.
- Orbit representatives: min over mirror x colour swap (flat) or rotation x mirror x colour swap (cylinder). Reps per width: w3 40,262; w4 154,813; w5 404,023 (n = 2..6: 57, 450, 5,140, 46,102, 352,274 at width 5).
- Cylinders (wrap): 4 files, n = 2..6 (60,447 reps); 5 files, n = 2..5 (14,883 reps). The 5-file cylinder with 6 pawns was not run.
- Not covered: 7 or more pawns; widths 6 and up; positions with e.p. rights at the root; positions with a passer at the root (trivial in S, in W the game is over); pawns on ranks 1 and 8.
- Configurations: race rule x {count, mover, opponent}, test x {textbook, e.p.-aware}, e.p. on in both. Race rules use the repo's `promote_distance` (double step counted).
- "Outcome" is the outcome class of the position alone (vs 0). I did not compare full game values or outcomes of G + other games. S = W in outcome class does not imply equal values.

## Files

- `enum.c`, `enum_cyl.c`: passer-free canonical position generators (binaries `enum`, `enum_cyl`).
- `census.py` (flat, hss, sum_safe, W; its S is superseded), `census_fix.py` (corrected S), `census_cyl.py` (cylinders, corrected S), `s_exact.py` (corrected S solver), `jobs*.txt`, `runjob*.sh`, `fixjob.sh`.
- `analyze.py`; outputs `analysis_w3.md`, `analysis_w4.md`, `analysis_w5.md`, `analysis_wall.md`, `analysis_wcyl4.md`, `analysis_wcyl5.md`.
- `crosscheck.py`, `cc_all.sh`, `fpcheck.py`; `data/cc_*.tsv`, `logs/`.
- `data/raw_*.tsv.zst`: per position: orbit size, position, root components, hss(textbook), 3 x (S, W, sum_safe) textbook, hss(e.p.-aware), 3 x (S, W, sum_safe) e.p.-aware (rule order count, mover, opponent). Tested with `zstd -t`; raw originals removed. The logs' "rss ...GB" label is really MB.

## What was not done

- No proof; no check beyond 6 pawns; no 6-file boards (where a second kind of 2-component split is possible on cylinders).
- sum_safe() was computed only for roots with >= 2 components (for 1-component roots it is True by its definition).
- No comparison of values or of G + R outcomes; no look at whether S != W positions matter for the paper's tables (e.g. 08_star2).
- Did not edit RESULTS.md or paper/.
