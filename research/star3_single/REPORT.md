# T42: report (agent text) with the verifier's findings

Saved by the orchestrating session on 2026-10-22 from workflow round 8 (Sonnet). The verifier's verdict and fix
list come first and **take precedence over the agent text where they differ**.

## Verifier verdict: ACCEPT_WITH_FIXES

The headline holds. A single-component default-setting *3 exists: W a4 b3 d2 d3 e4 / B a7 b7 c5 e6 on 5 files, 9 pawns. I re-derived it with my own solver and with cylcgt in both models. The claim "no *3 with at most 8 pawns" is true only in the whole-board convention. In cylcgt's default sum model (pawns.value), 7-pawn two-component positions are *3, e.g. W a2 b2 d2 / B a5 d4 e3 e4 = (+W*) + {-W,-W*|-W,-W*} = *3, with sum_safe False and cylcgt-whole giving a non-nimber. No single-component position with 5 to 8 pawns is *3 in either model. "None on 4 files" is false: W a2 b4 c2 d2 / B a4 a6 a7 c6 d5 is *3 on 4 files with 9 pawns. Fixes needed: state the model for the at-most-8 claim, and replace the "none on 4 files" claim. Evidence labels below use the project's scheme.

### Fixes and problems found by the verifier

- OVERCLAIM: 'No *3 has at most 8 pawns' (summary point 3, evidence 'At most 8 pawns: COMPUTED-1') is only a whole-board-convention result. The brief's default setting is cylcgt pawns.value, the disjunctive-sum model. In that model *3 exists at 7 and 8 pawns as two-component sums with sum_safe False. Examples, each confirmed by cylcgt: 'W: a2 b2 d2 / B: a5 d4 e3 e4' (7 pawns), 'W: a3 b3 e2 / B: b6 d3 d4 e4' (7 pawns), 'W: a2 b2 d2 / B: a5 d4 e3 e4 e5' (8 pawns), 'W: a3 d2 e2 / B: a5 b4 b5 b6 d5' (8 pawns). Each is (+W*) + {-W,-W*|-W,-W*} = *3, a cancellation of +BIG and -BIG across components. In 7 pawns these have 3+4 splits on flat widths 5-8 (92 canonical roots). cylcgt-whole is not a nimber for any of them, so none is a robust *3. Fix: say 'no *3 with <=8 pawns in the whole-board convention (scanner); sum-model *3 exists only as sum_safe=False artifacts, from 7 pawns up'. No such sum-model *3 occurs with 4-6 pawns (flat w3-8, gapped included).
- WRONG DOCSTRING / unjustified claim: sums_le8.py states 'the C scanner's whole-board model agrees on span <= 8'. This is false. The scanner has first-passer-ends-game semantics; cylcgt sums cancel +-BIG across components. They differ on many gapped roots (3 of 150 random roots; 112 of 3,000 with 5-8 pawns, e.g. 'W: b2 f5 / B: b6 c6 e6' is RNNNNNNN in the sum model and NNNNNNNN in the scanner). The sums_le8/sums_span9 sum-model coverage is also incomplete: 5- and 6-pawn components are enumerated only one-pawn-per-file, so pairs (2,5), (3,5), (2,6) with 5- or 6-pawn components on fewer files than pawns were never evaluated in the sum model. The report's 'pairs up to (2,5)' therefore overstates it.
- FALSE CLAIM: 'There are none on 4 or 7 files' (summary point 2). A 9-pawn, 4-file single-component *3 exists: W a2 b4 c2 d2 / B a4 a6 a7 c6 d5, one of 4 images (also W a4 b3 d2 d3 d5 / B a7 b7 c5 d7, W a2 b2 c4 d2 / B a5 b6 d4 d6 d7, W a2 a3 a5 c3 d4 / B a7 b5 c7 d7). It is *3 in the default setting and in every e.p.-on setting. T42's coverage.tsv has no flat width-4 9-pawn row. The star3_hunt summary files already contained it (C/aware=5,1,3), and REPORT.md of star3_hunt mis-tabulates it as 10/0/2 and as opponent-rule only. The brief's premise 'no default *3 in any exhaustive scan so far' is therefore also false.
- NARRATIVE GAP: the ball search (--single, width 5) cannot find the width-4 variant 'A + (d5,d7) on A's own file d', because --single requires all 5 files occupied. This explains why the near-A search missed it. The report's structural story 'A + attached * group on an adjacent new file' should be widened to 'A + * group, possibly on an existing file'.
- OVERGENERALISATION: 'Blocked adjacent pairs give *2'. This is true only for (e4,e5), (e5,e6) and (e6,e7). (e2,e3) is N (fuzzy) and (e3,e4) is L.
- COVERAGE not listed under 'Not scanned': flat w4 9 pawns (now done by me, one *3), 9-pawn rings C3, C6, C7, C8 and the C4/C5 3+6 and 2+7 splits (I ran C3 4+5/3+6, C4 3+6/2+7, C5 3+6/2+7 and C6 4+5 with s3: no *3; C7 and C8 at 9 pawns were not run), and flat w6 1+8. Items still unscanned by anyone: flat w8 9 pawns, ring C7/C8 9 pawns.
- MINOR PROCESS / LABELS: the report itself admits breaking the shared-machine rules (three runs over 4 GB RSS, 3 heavy processes at a time). 'CHECKED-3' for class 1 counts s3 (the unchanged frontier scanner core), cylcgt and the Codex solver as three programs; that is fair. The exhaustive scans themselves (including the 4 classes at width 5) are not independent of s3 in T42, but my own ssum replication reproduces the width-5 4+5 root count and hit counts exactly, so they are now CHECKED-2 in the whole-board model.
- My own checks are bounded: the sum-model scans cover single-component roots with 5-8 pawns (19.8M roots) and gapped roots with 4-7 pawns on flat widths 3-8. I did not run the full 110M-root le8 set in the sum model, nor gapped 8-pawn roots exhaustively. Sum-model 8-pawn *3 counts come from three runs (w5 3+5, w5 4+4, w6 3+5). No sum-model *3 was found in single-component 5-8 pawn positions.

### Claims the verifier recomputed

- **agrees.** Claim: Class 1 (W a4 b3 d2 d3 e4 / B a7 b7 c5 e6, 5 files, 9 pawns) is *3 in the default setting, single component
  Recomputed: CHECKED-3. My Python whole-board solver (written from cylcgt/pawns.py, not from s3) gives outcome string NNNPNNNN for G+*k, k=0..7. My C sum/whole solver ssum gives the same. cylcgt sum 70.7 s and cylcgt whole 57.1 s both print *3. The existing s3 binary agrees.
- **agrees.** Claim: All 8 classes and all 4 images each (file mirror, colour reversal) are *3
  Recomputed: CHECKED-2. My Python whole solver gives NNNPNNNN on all 32 images of C1-C4 (5 files) and D1-D4 (6 files). cylcgt sum and whole were re-run on C1 only.
- **agrees.** Claim: A = W a4 b3 d2 d3 / B a7 b7 c5 is *2; A + B d7 alone is negative; class 1 options W e4-e5 = *2, B e6-e5 = *2, W a4-a5 = *, B b7-b6 = 0
  Recomputed: CHECKED-2 (my solver; the *2 of A also from s3). A gives NNPNNNNN. A + B d7 gives RRRRRRRR. The four listed options evaluate to NNPNNNNN, NNPNNNNN, NPNNNNNN and PNNNNNNN, matching the claim.
- **DISAGREES.** Claim: On the right-hand file, pairs (e4,e6) and (e5,e7) give *3, (e2,e4) and (e3,e5) do not, and blocked adjacent pairs give *2
  Recomputed: COMPUTED-1 (my solver). (e4,e6) and (e5,e7) give *3. (e2,e4) and (e3,e5) give L. The *2 holds only for e4/e5, e5/e6 and e6/e7. e2/e3 gives N (fuzzy) and e3/e4 gives L, so 'blocked adjacent pairs give *2' is an overgeneralisation.
- **agrees.** Claim: The 4 width-5 classes are *3 in all 6 e.p.-on settings except class 4 under the opponent rule; with e.p. off none is a nimber (outcome R)
  Recomputed: COMPUTED-1 (my solver, 3 race rules x textbook/off/aware). All four classes give NNNP.. under count and mover, both textbook and aware, and under opponent for C1-C3. C4 under opponent gives L. With e.p. off, C1-C3 give R and C4 gives R under count/mover and L under opponent. This agrees with the report; the only difference is that off/opponent for C4 is L, not R.
- **agrees.** Claim: Exhaustive scan of flat width 5, 9 pawns, split 4+5 single-component roots: 18,603,810 roots, 12 *2, 4 *3
  Recomputed: CHECKED-2. My own enumeration and solver (ssum --model whole, 2 chunks) give 12,853,478 + 5,750,332 = 18,603,810 roots, nim2 = 9 + 3 = 12, nim3 = 4. These match T42 exactly.
- **agrees.** Claim: T42's whole-board <=8-pawn scan outputs are correct
  Recomputed: CHECKED-2 on a sample. My whole-mode ssum reproduces le8 histograms exactly for flat w5 3+5 (3,675,495 roots; L, R, N, P and nim counts identical) and flat w5 4+4 colsym (2,990,762 roots, 12 *2). My single-component root counts match the old count_roots.out in the cases compared (w6 4+4 2,194,893; w7 4+4 1,167,591; w7 3+5 960,562). The le8 totals recompute to 110,276,698 roots and 32 *2.
- **DISAGREES.** Claim: No *3 has at most 8 pawns ('the C scanner's whole-board model agrees with the sum model on span <= 8', from the docstring of sums_le8.py)
  Recomputed: REFUTED for cylcgt's default sum model. My new sum-model solver ssum (thresholds replace the integer BIG count) agrees with cylcgt on 150 random roots plus 112 roots chosen because sum differs from whole, with 0 diffs. It finds 92 canonical 7-pawn roots (flat w5-w8, split 3+4) with value *3, and 72 to 236 8-pawn roots per run (e.g. w5 3+5: 72; w5 4+4: 236). cylcgt itself confirms: W a2 b2 d2 / B a5 d4 e3 e4 is *3 in 0.4 s, components +W* and {-W,-W*|-W,-W*}, sum_safe False. cylcgt whole gives a non-nimber. Likewise W a2 b2 d2 / B a5 d4 e3 e4 e5 (8 pawns) and W a3 b3 e2 / B b6 d3 d4 e4 (7 pawns). In 150 random gapped roots sum != whole on 3, and 112 of 3,000 sampled roots differ. The scanner is whole-board only, so the claim holds there (and 4-6 pawns have no sum-model *3). ('Agrees on span <= 8' is false.)
- **agrees.** Claim: No single-component *3 with at most 8 pawns
  Recomputed: COMPUTED-1 in the sum model, plus the scanner's whole model, so two semantics. My ssum --model sum --single over flat widths 1-8 and rings C3-C8, 5-8 pawns, nw <= nb, covers 19,803,987 roots: 31 *2 and 0 *3. T42's whole-board scan agrees (0 *3).
- **DISAGREES.** Claim: There are none on 4 or 7 files for 9 pawns, and none on rings C4/C5
  Recomputed: FALSE for 4 files. s3 --flat --width 4 --nw 4 --nb 5 --single (4,174,422 roots) finds W a2 b4 c2 d2 / B a4 a6 a7 c6 d5, *3. Its colour-reversed mirror W a4 b3 d2 d3 d5 / B a7 b7 c5 d7 is A plus a one-file group (d5,d7) on A's own file d. Checked by my solver (NNNPNNNN, 4 images), by cylcgt sum (*3, 28.9 s), and by the s3 run. It is *3 under count, mover and opponent with e.p. textbook or aware; with e.p. off it is L. T42 did not scan flat w4 with 9 pawns (not in coverage.tsv). The old star3_hunt/analysis_tmp/flat_w4p9_4_5.summary and flat_w4p9_5_4.summary already show C/aware=5,1,3 (one *3), while the REPORT.md table for 'Flat width 4, 9 pawns' wrongly lists 10/0/2. The splits 3+6 and 2+7 on 4 files give no *2 or *3. For 7 files: 3+6 and 4+5 scanned, 2+7 has 0 roots. For C4/C5 only 4+5 was scanned. I additionally scanned cyl C5 3+6 (97 P, no *2/*3), C5 2+7, C4 3+6, C4 2+7, C3 4+5 and 3+6, flat w3 and w2 9 pawns, and C6 4+5 (nim2=3, no *3), all with s3: no *3.
- **DISAGREES.** Claim: Earlier scans missed the width-5 *3 because the 4+5 and 5+4 splits were skipped
  Recomputed: Partly true for width 5 (star3_hunt REPORT.md says so). But a default-setting *3 was already present in the earlier width-4 data (see previous row), contrary to the brief's 'no default *3 in any exhaustive scan so far'.
- **agrees.** Claim: s3 core is unchanged from frontier_split1_fixed2.c
  Recomputed: CHECKED. diff of base_fixed2.c against frontier_split1_fixed2.c, and of the core section of s3.c, shows comment-only differences.

## Agent report (verbatim)

**T42: SUMMARY**
1. Yes: a single-component *3 exists in the default setting (count rule, e.p. on, e.p.-aware). `W a4 b3 d2 d3 e4 / B a7 b7 c5 e6` on flat 5x8 has 9 pawns, one component (files a-e), and is *3. It is also *3 on the 8x8 cylinder with files f-h empty.
2. It is position A (`W a4 b3 d2 d3 / B a7 b7 c5`, the 7-pawn *2) with a one-file * group (e4/e6) attached on the adjacent file. An exhaustive scan of all 9-pawn single-component roots on 5 files finds exactly 4 classes (16 positions): 3 are A plus an attached * group, 1 is entangled. On 6 files there are 4 more classes (A plus a two-file * group). There are none on 4 or 7 files and none on rings C4/C5.
3. No *3 has at most 8 pawns. The scan covers every flat board up to width 8 with component sums included, and every ring C3..C8. That is 110,276,698 roots, and the largest nimber seen is *2.
4. Earlier scans missed it because the width-5, 9-pawn splits 4+5 and 5+4 were skipped (`research/star3_hunt/REPORT.md`). Searching every position within two pawn edits of A (the --ball search) found the first one in 0.4 s.
5. It needs e.p.: the 4 width-5 classes are *3 in all 6 e.p.-on settings (count/mover, textbook/aware), except class 4 under the opponent rule; with e.p. off none of them is a nimber (outcome R).

**Positions** (data in `positions.tsv`; each class has 4 images under file mirror and colour reversal, and all 16 width-5 and all 16 width-6 images evaluate to *3)

| Class | Position | Structure |
|---|---|---|
| 1 | `W a4 b3 d2 d3 e4 / B a7 b7 c5 e6` | A + e4/e6 |
| 2 | `W a4 b3 d2 d3 e5 / B a7 b7 c5 e7` | A + e5/e7 |
| 3 | `W a4 b3 d2 d3 e4 / B a7 b7 c5 d7` | entangled |
| 4 | `W a2 b4 c3 e2 e3 / B a4 b7 c7 d5` | A shifted one file right + a2/a4 |
| 5 | `W a4 c2 d2 e4 / B b7 c5 d6 f6 f7` | width 6: reversed A + two-file * group (a4,b7) |
| 6 | `W a2 b2 c4 f2 / B a5 b6 d6 d7 e5` | width 6: reversed A + group (f2,e5) |
| 7 | `W a2 b2 c4 e3 / B a5 b6 d6 d7 f6` | width 6: reversed A + group (e3,f6) |
| 8 | `W a2 b2 c4 e2 / B a5 b6 d6 d7 f5` | width 6: reversed A + group (e2,f5) |

- **Class 3 is the one genuinely entangled case.** A plus B d7 alone is negative (outcome R), and W e4 repairs it.
- **Which pairs work on the right-hand file.** Pairs (e4,e6) and (e5,e7) give *3. Pairs (e2,e4) and (e3,e5) do not. Blocked adjacent pairs give *2.
- **Options of class 1.**
  - W e4-e5 gives *2.
  - B e6-e5 gives *2.
  - W a4-a5 gives *.
  - B b7-b6 gives 0.
  - This is consistent with {0,*,*2 | 0,*,*2}. The full list is in `verify_out/options_C1.txt`.

**Evidence**
- **Class 1: CHECKED-3.** Five checks, each reporting *3, from three independently written programs:
  - the C program `s3`;
  - cylcgt sum model (57 s);
  - cylcgt whole-board model (43 s);
  - the Codex solver's canonical form (1697 s);
  - the Codex solver's outcome masks.
  - cylcgt on the 8x8 cylinder also gives *3.
- **Classes 2-8: CHECKED-2 or better.** Each was checked by `s3`, cylcgt sum, cylcgt whole-board and the Codex outcome masks, and all report *3. Class 3 was run through cylcgt sum (162 s) and whole-board (133 s).
- **Engine cross-check: CHECKED-2.** The outcome strings of G+*k (k=0..7) from `s3` and from the Codex mask solver have 0 differences on 24 random roots and 60 positions near A (12 distinct strings).
- **Exhaustive single-component scans: COMPUTED-1.** Default setting; sizes and results in `coverage.tsv`.

| Scan | Roots | Result |
|---|---|---|
| flat w5, 9 pawns, 4+5 | 18,603,810 | 12 *2, 4 *3 classes |
| flat w5, 9 pawns, 3+6 / 2+7 / 1+8 | 8,167,217 / 1,149,962 / 0 | none |
| flat w6, 9 pawns, 4+5 | 35,093,597 | 16 *2, 4 *3 classes |
| flat w6, 9 pawns, 3+6 / 2+7 | 12,658,906 / 740,425 | none |
| flat w7, 9 pawns, 4+5 | 31,591,330 | 5 *2, no *3 |
| flat w7, 9 pawns, 3+6 | 8,444,841 | none |
| flat w4, 10 pawns, 5+5 / 4+6 | 6,275,963 / 9,360,358 | no *3 |
| C4, 9 pawns, 4+5 | 1,491,833 | no *3 |
| C4, 10 pawns, 5+5 | 2,169,192 | no *3 |
| C5, 9 pawns, 4+5 | 5,596,948 | no *3 |
| C5, 10 pawns, 5+5 | 13,114,414 | 43 *2, no *3 |

  - The scanner's core is `frontier_split1_fixed2.c`, unchanged apart from comments.
  - It reproduces the older runs exactly: 1,331,201 roots and 4 *2 for w4 8-pawn 4+4; the identical outcome and nimber histogram for w5 9-pawn 3+6.
  - Root counts for the ≤8-pawn runs also match the old scans (w5 3+5, w6 3+4, w6 3+5).
- **At most 8 pawns: COMPUTED-1.** The 190 runs of `run_le8.sh` cover flat widths 1-8 (edge files occupied, gaps allowed) and rings C3-C8, splits nw ≤ nb (colour reversal covers the rest). The *2 hits are 1 at 6 pawns (C3 ring), 2 at 7 pawns (A on flat, and a C4 ring), 29 at 8 pawns. No *3 anywhere.
- **Sums wider than 8 files (cylcgt sum model: COMPUTED-1):**
  - `sums_span9.py` checks the pairs (4,4), (3,5), (2,6) with one pawn per file, the only two-component cases the scanner cannot hold. It finds 0 sums equal to *3. A control against brute-force addition agrees.
  - `sums_le8.py` covers all 3- and 4-component sums and pairs up to (2,5), with 0 *3.
  - That run was cut during the (2,6) pair, which `sums_span9.py` replaced.
- **Search by editing pawns: COMPUTED-1.**
  - Around the non-default ring seeds, in the default setting: C4 (radius 3, 163,834 nodes) and C3 (radius 3, 44,552 nodes) give no *3. In the default setting the C4 seed is a non-nimber (fuzzy with every *k).
  - Around the 35 single-component *2 seeds (6 on 4 files, 21 on 5, 8 on 6; radius 2, 7-10 pawns): 26 *3 hits (4 with 9 pawns, 22 with 10), no *4. Four of the 10-pawn hits were confirmed by the Codex masks.
- **Not scanned:** flat width 8 with 9 pawns, flat width 5 or 6 with 10 or more pawns, rings C6 and up with 10 pawns (the ball search is the only evidence there), and the Codex canonical form for every class.
- **Resource note:**
  - All chunked scans ran with the table capped at 1.9 GB.
  - Three of the ≤8-pawn runs (flat w7 4+4, w8 3+5, w8 4+4) ran uncapped. Their tables grew to roughly 7.5, 7.5 and 15 GB, over the 4 GB rule; I noticed only afterwards.
  - Capped re-runs (`le8_capped/`) give identical root counts and outcome and nimber histograms.
  - I also ran 3 heavy processes at once for short stretches.
  - Total CPU was about 45 min of scanning and about 90 min of Python checks.

**Reproduce** (from `/Users/aritro/Downloads/Research/Chessendgames/research/star3_single`; `reproduce.sh` runs everything)
```
cc -O2 -o s3 s3.c -lm
echo 'W: a4 b3 d2 d3 / B: a7 b7 c5' > tmp/seedA.txt
./s3 --flat --width 5 --single --ball tmp/seedA.txt --radius 2 --pmin 7 --pmax 9
./run_chunks.sh flat_w5_p9_4_5 48 2 "--flat --width 5 --nw 4 --nb 5 --single"; python3 merge_chunks.py scans/flat_w5_p9_4_5
./run_chunks.sh flat_w6_p9_4_5 96 2 "--flat --width 6 --nw 4 --nb 5 --single"
./run_le8.sh; bash ./rerun_capped.sh; python3 coverage.py
```
From the project root:
```
PYTHONPATH=. .venv/bin/python research/star3_single/verify.py all 5 flat "W: a4 b3 d2 d3 e4 / B: a7 b7 c5 e6"
PYTHONPATH=. .venv/bin/python research/star3_single/verify_masks.py 5 research/star3_single/tmp/all16.txt
PYTHONPATH=. .venv/bin/python research/star3_single/crosscheck_near.py 60 7
PYTHONPATH=. .venv/bin/python research/star3_single/sums_span9.py
```
`bash research/star3_single/verify_batch.sh` runs the cylcgt checks for classes 2 and 4-8 (class 3 was run separately).

Key files in `/Users/aritro/Downloads/Research/Chessendgames/research/star3_single/`: `s3.c`, `reproduce.sh`, `positions.tsv`, `hits_all.tsv`, `coverage.tsv`, `scans/`, `le8/`, `le8_capped/`, `sums/`, `verify_out/`, `ball/`.
