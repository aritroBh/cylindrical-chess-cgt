# Flat 8x8 atlas, rerun with an independent C solver (workstream A2-search)

Saved by the parent session from the workstream's final report (workflow `wf_3dfce063-f42`). Workflow agents may not write report files, so the text below is the agent's, unedited apart from removing that notice. Verification verdicts come from the workflow's adversarial verifiers; "not verified" includes verifiers that were cut off by a usage limit.

WORKSTREAM A2-search, rerun (2026-10-16). All outputs are in /Users/aritro/Downloads/Research/Chessendgames/atlas/flat8/rerun/.

CONVENTION WARNING. The task says to use cylcgt/pawns.py. On disk that file still implements the TEXTBOOK passed test, in which a pawn that can still be taken en passant counts as passed. The e.p.-aware test that RESULTS.md calls adopted exists only in the parent session's worktree: scratchpad/ep-wt/cylcgt/pawns.py with PASSED_RESPECTS_EP = True. So:
- the database uses the textbook test (as instructed);
- every robustness table also reports the e.p.-aware variant, which I ran read-only from that worktree;
- my independent C solver implements both tests.

METHOD
- I wrote a new enumerator, enumerate.py. Values come from cylcgt with count rule, e.p. on.
- I wrote an independent rules implementation in C, nimscan.c, sharing no code with cylcgt, crosscheck/ or indep_scan.py.
  - It decides G = *k (k <= 15) by testing whether G + *k is a second-player win.
  - It tests G = T for an explicit game T by testing whether G + (-T) is a second-player win.
  - It runs 9 settings: {count, mover, opponent} x {e.p. off, e.p. on textbook, e.p. on aware}. Test mode also has all-races-to-White and all-races-to-Black.

SCOPE AND COMPUTE
- Scope: flat boards with 8 ranks, widths 1-4, pawns on ranks 2-7, w,b >= 1, every w+b <= 6 (including the optional w+b = 6 on width 4), no passed pawn at the root, reduced by translation and mirror. That gives 231,071 records standing for 459,443 board positions. This is identical to the prior run's count.
- The pilot cold-cache estimate was 28,288 CPU-s. Actual use was about 24 CPU-min and about 27 min of compute wall time. Load average was 120-205 from other sessions for most of the run.
- Width 4, w+b = 6 was NOT fully recomputed. 140,835 of its 142,335 records were imported from ../values.jsonl, which was computed by the same cylcgt code, after three checks:
  - the position set and multiplicities equal my own enumeration;
  - a random sample of 1,500 recomputed here matched in every field;
  - the C census matches outcome and nimber for all of them.
  These records are labelled source="prior-run import (verified sample)".

VALUE STRINGS ARE NORMALIZED. Raw cgt.show strings list options in internal game-id order, which differs between runs: 1,151 of the 88,736 phase-1 records differed from the prior run in raw strings only. After recursively sorting options, all 88,736 agree in every field. values.jsonl therefore stores the option-sorted show string.

CROSS-CHECKS (C solver against cylcgt)
- Against the cylcgt database, textbook count/e.p. on: 231,071/231,071 outcomes and nimber columns agree.
- Against the parent's e.p.-aware database (../values_aware.jsonl): also 231,071/231,071.
- Setting-level comparisons of exact values for candidates and targets: 215/215 agree.

NIMBERS
- No *k with k >= 3 occurs under any of the 9 settings (k <= 15 tested).
- No *k with k >= 2 has 3 or fewer pawns. So no nimber candidate fits in 7 men.
- No *2 is robust. *2 occurs at exactly 6 positions (4 up to colour reversal):
  - W a2 c2 / B b7 d7: *2 under count and mover with e.p. on and off; 0 under opponent; {2±1 | -2±1} under e.p.-aware count and mover.
  - W a3 b3 c2 / B b5 b7 c6 and its colour reversal W a3 b2 b4 / B a7 b6 c6: *2 only under opponent with e.p. on (textbook and aware).
  - W a3 b2 c2 / B a4 b6 c5 and its reversal W a5 b3 c4 / B a6 b7 c7: *2 only under opponent with e.p. on, aware. These are new relative to the prior run, which had no aware column.
  - W a3 b2 d3 / B a6 c7 d6: *2 only under mover with e.p. off.
- Candidate race counts (count rule, e.p. on, cold cache): 398 race edges, 184 distinct race positions, 224 distinct (position, mover) pairs. Before any capture: 256 edges, 114 positions, 154 pairs. With e.p. off: 224/166/206 overall and 154/96/136 before any capture. The prior report's "224 distinct / 154 pre-capture" are (position, mover) pairs.

ELKIES 8x8 TARGETS (database setting; all confirmed by the C solver)
- *4: none. Other nimbers: only the *2s above.
- Dyadic numbers with denominator >= 8 (BIG-free): ±1/8 at 13 positions each, ±3/8 at 1, ±9/8 at 1, ±1/16 at 3, ±1/32 at 1.
- Up-second family: exact ↑² = {0 | ↓*} at 5 (and ↓² at 5); ↑²* = {0,* | ↓} at 10 (and its negative at 10); ↑+↑² = {↑ | *} at 3; ↑+↑²+* at 2; 2↑+2↑²+* at 1.
- Fractional tinies: tiny(x) for non-integer dyadic x never occurs (odd/2^j, j = 1..4, x < 8), and tiny(1↑) does not occur. tiny(1) occurs at 13 positions, tiny(4) at 1, and tiny(1*) = {0 || 0 | -1*} at 1 (W a2 c2 d5 / B a4 b6 d7; 6/9 settings), with miny(1*) at its reversal.
- Most robust targets (all 9 settings AND every race outcome, C; the 9 settings also in cylcgt):
  - 1/8 at W a2 a3 b2 / B a6 b5 b6;
  - ↑²* at W a2 b2 b6 / B a6 b7 c5.
- Correction to the prior run: it called the 1/8 pawn structure unreachable. That is true only for the stored representative on files a-b. Its mirror image W a2 b2 b3 / B a5 a6 b6 has the same value, 1/8 under all 9 settings and every race outcome (checked in C and cylcgt). It passes the necessary reachability conditions, and I hand-built a capture history: c2xb3; a7-a5 then b7xa6; c7xb6. FEN: 8/8/pp6/p4Kp1/6Pk/1P6/PP6/8 w - - 0 1 (10 men).
- The prior's "best reachable" 1/8 (W a2 b2 d2 / B a5 c4 d7) and best ↑² (W a3 c5 d4 / B a7 b7 d7) both FAIL under the adopted e.p.-aware test: they become -3/2±3/2 and {3/4 | ↓*}.

UP-SECOND DEFINITION. I could not read Siegel's book. I checked his CGSuite source instead: a 2007 copy of CanonicalGame.java in the scratchpad defines G^n = {0 | H - G^{->(n-1)}} and G^{->n} = {G^{->(n-1)} | H} for G = {0 | H}. For G = ↑ this gives ↑² = {0 | ↓*}. In cgt, ↑² > 0; n·↑² < ↑ for n = 1..64; ↑² < 2^-k for k <= 20; ↑ + ↑² = {↑ | *}; ↑² ≠ ⇑; ↑²+* = {0,* | ↓}.

Everything here is in the pawn-only model (one-sided passer = ±256, frozen trébuchet, race rules, no draws). Nothing was checked with real kings.

## Claims

| id | importance | worker status | adversarial verification | statement |
|---|---|---|---|---|
| C1 | headline | checked-two-ways | not verified | In scope (flat, 8 ranks, widths 1-4, w+b <= 6 including width 4, no root passer), under the database setting (count rule, e.p. on, textbook passed test), the only *k with k >= 2 is W a2 c2 / B b7 d7 (plus its mirror image). No *3 or higher occurs under any of the 9 settings (count/mover/opponent x e.p. off / e.p. on textbook / e.p. on aware), testing k <= 15. |
| C2 | headline | checked-two-ways | not verified | No *k (k >= 2) is robust. Exactly 6 positions are *2 under at least one of the 9 settings: W a2 c2 / B b7 d7 (count and mover, e.p. on/off; 0 under opponent; {2±1 \| -2±1} under e.p.-aware count/mover); W a3 b3 c2 / B b5 b7 c6 and its colour reversal W a3 b2 b4 / B a7 b6 c6 (opponent with e.p. on, textbook and aware); W a3 b2 c2 / B a4 b6 c5 and its colour reversal W a5 b3 c4 / B a6 b7 c7 (opponent with e.p. on, aware only); W a3 b2 d3 / B a6 c7 d6 (mover with e.p. off only). |
| C3 | key | computed-once | not verified | Race nodes of W a2 c2 / B b7 d7, count rule, e.p. on, cold cache: 398 race edges (len(pawns.race_hits)), 184 distinct race positions, 224 distinct (position, mover) pairs. Before any capture: 256 edges, 114 positions, 154 pairs. With e.p. off: 224 edges, 166 positions, 206 pairs; before any capture 154, 96, 136. The prior report's '224 distinct, 154 pre-capture' count (position, mover) pairs. Under the e.p.-aware test: 424 edges and 258 pre-capture edges. |
| C4 | key | checked-two-ways | not verified | The independent C solver agrees with cylcgt on outcome class and nimber column for all 231,071 records. This holds both for the textbook database (this rerun's values.jsonl and the prior ../values.jsonl) and for the parent's e.p.-aware database ../values_aware.jsonl. |
| C5 | headline | checked-two-ways | not verified | 1/8 holds at W a2 a3 b2 / B a6 b5 b6 under all 9 settings and, with e.p. on, off or aware, under every assignment of race outcomes. Its mirror image W a2 b2 b3 / B a5 a6 b6 has the same value. The mirror's pawn structure passes the necessary reachability conditions at files a-b (FEN 8/8/pp6/p4Kp1/6Pk/1P6/PP6/8 w - - 0 1, 10 men), with a hand-built capture history: c2xb3; a7-a5 then b7xa6; c7xb6. This corrects the prior run's statement that the structure cannot arise in chess; that statement holds only for the stored representative on files a-b. |
| C6 | headline | checked-two-ways | not verified | Up-second-star ({0,* \| ↓}) holds at W a2 b2 b6 / B a6 b7 c5 under all 9 settings and every race outcome (FEN 8/1p6/pP6/2p2Kp1/6Pk/8/PP6/8 w; 10 men; 13 race edges, none before a capture). Exact up-second {0 \| ↓*} occurs at 5 positions but under at most 3 of the 9 settings. Under the adopted e.p.-aware count rule it holds at W a2 b2 d4 / B a7 c6 d7 and W a2 b2 d5 / B a6 c5 d7. The prior's best up-second, W a3 c5 d4 / B a7 b7 d7, becomes {3/4 \| ↓*} under the e.p.-aware test. |
| C7 | key | checked-two-ways | not verified | Elkies dyadic targets under the database setting (BIG-free exact numbers with denominator >= 8): ±1/8 at 13 positions each, ±3/8 at 1, ±9/8 at 1, ±1/16 at 3, ±1/32 at 1. 1/8 holds at 9 of the 13 under the e.p.-aware count rule; 1/16 at 2 of 3; 1/32 at none. The prior's 'best reachable' 1/8, W a2 b2 d2 / B a5 c4 d7, holds only under the 3 textbook e.p.-on settings and is -3/2±3/2 under the e.p.-aware test. |
| C8 | key | checked-two-ways | not verified | No fractional tiny occurs: tiny(x) for odd/2^j with j = 1..4 and x < 8 never occurs, and tiny(1↑) never occurs. tiny(1) occurs at 13 positions and tiny(4) at 1. tiny(1*) = {0 \|\| 0 \| -1*}, positive, infinitesimal and fuzzy with tiny(1), occurs at W a2 c2 d5 / B a4 b6 d7 under 6/9 settings (count and opponent rules), with miny(1*) at W a2 c3 d5 / B a4 b7 d7. |
| C9 | key | computed-once | not verified | Up-second is {0 \| ↓*}. Checked against Siegel's CGSuite source (CanonicalGame.java v1.42, 2007, scratchpad copy), not against the book, which I could not read: G^n = {0 \| H - G^{->(n-1)}} and G^{->n} = {G^{->(n-1)} \| H} for G = {0\|H}. In cgt: ↑² > 0; n·↑² < ↑ for n = 1..64; ↑² < 2^-k for k = 0..20; ↑ + ↑² = {↑ \| *}; ↑² ≠ ⇑; ↑²+* = {0,* \| ↓}; ↑³ = {0 \| * - ↑^{->2}} lies strictly between 0 and ↑². |
| C10 | key | checked-two-ways | not verified | Database values.jsonl has 231,071 records (459,443 board positions), settings count rule, e.p. on, textbook passed test. 90,236 records were computed in this rerun. 140,835 width-4 w+b=6 records were imported from the prior run after verification: identical position set and multiplicities from an independent enumeration; a 1,500-record random sample recomputed with every field matching; outcome and nimber columns of all of them independently confirmed by the C census. |
| C11 | minor | computed-once | not verified | The full value column (canonical form, temperature, mean) of the database was computed by cylcgt only. Only the outcome and nimber columns and the listed target identities were checked by a second implementation. |
| C12 | minor | checked-two-ways | not verified | No nimber *k (k >= 2) and no Elkies target in scope fits in 7 men with the trébuchet. Every *2 has 4 or 6 pawns, and the smallest target is up-second-star W a2 b2 / B a6 c5 with 4 pawns (8 men; count rule only). |

### How to reproduce each claim

- **C1**:

  ```
  cd /Users/aritro/Downloads/Research/Chessendgames && cc -O2 -o atlas/flat8/rerun/nimscan atlas/flat8/rerun/nimscan.c && atlas/flat8/rerun/nimscan --max 6 > atlas/flat8/rerun/census.tsv && PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py census
  ```
- **C2**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py robust --aware-root /private/tmp/claude-501/-Users-aritro--claude-spares-spare-E0JaXy/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad/ep-wt && PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py nimbers
  ```
- **C3**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py robust --aware-root <ep-wt path>
  ```
- **C4**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py census
  ```
- **C5**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py gtest --robust atlas/flat8/rerun/robust.json atlas/flat8/rerun/robust_targets.json --targets-json atlas/flat8/rerun/targets.json && PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py reach
  ```
- **C6**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py targets && PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py gtest --robust atlas/flat8/rerun/robust.json atlas/flat8/rerun/robust_targets.json --targets-json atlas/flat8/rerun/targets.json
  ```
- **C7**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py targets; PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py gtest --robust atlas/flat8/rerun/robust.json atlas/flat8/rerun/robust_targets.json --targets-json atlas/flat8/rerun/targets.json
  ```
- **C8**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py targets
  ```
- **C9**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py upsecond --nmax 64
  ```
- **C10**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/enumerate.py enum --workers 8 --chunk 200 --six-widths 1,2,3 --out values_phase1.jsonl --log atlas/flat8/rerun/enum_log_phase1.json; PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/enumerate.py import-prior --prior atlas/flat8/values.jsonl --sample 1500 --workers 4 --out values_phase2_w4six.jsonl --log atlas/flat8/rerun/import_log_w4six.json; PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/enumerate.py merge values_phase1.jsonl values_phase2_w4six.jsonl --out atlas/flat8/rerun/values.jsonl
  ```
- **C11**:

  ```
  n/a
  ```
- **C12**:

  ```
  PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py census; PYTHONPATH=. .venv/bin/python atlas/flat8/rerun/analyze.py targets
  ```

## Bugs found

- Convention mismatch: RESULTS.md says the e.p.-aware passed test (PASSED_RESPECTS_EP = True) is adopted in cylcgt, but /Users/aritro/Downloads/Research/Chessendgames/cylcgt/pawns.py on disk still implements the textbook test. The flag exists only in the parent's worktree, scratchpad/ep-wt/cylcgt/pawns.py, which also changes promote_distance. Any workflow agent told to use cylcgt/pawns.py silently gets the textbook convention.
- cgt.show strings are not reproducible identifiers. Options are listed in internal game-id order, which depends on evaluation order. 1,151 of 88,736 records differ in raw value string between two runs of identical code; all agree after recursively sorting options (enumerate.py norm_show).
- The parent's atlas/flat8/compare_ep_aware.py compares raw show strings, so its 'value changed 21441' (textbook vs e.p.-aware) is wrong in both directions. 3,732 of those are option-order artifacts. At least 428 real changes are hidden by the +W display collapse (|x| >= 128 prints as +W). At least 18,137 records truly change. Its 'outcome changed 4068' should be 4070: two records have identical strings ('+W±+W' / '-W±+W') but different outcome and mean, e.g. W a2 a4 c2 / B a3 b5 b6, outcome L -> N, mean 517/4 -> 129. RESULTS.md has an EPAWARE_CENSUS placeholder that may be filled from those numbers.
- Prior run's reachability verdict (atlas/flat8/REPORT.md, C7): it says W a2 a3 b2 / B a6 b5 b6 (1/8) 'cannot arise in chess', but that was evaluated only for the stored representative. The mirror image W a2 b2 b3 / B a5 a6 b6 has the same value and passes the necessary conditions with a concrete capture history. This affects RESULTS.md section 6, which names W a2 b2 d2 / B a5 c4 d7 as the best reachable 1/8. That position is e.p.-on-only and fails under the adopted e.p.-aware test (-3/2±3/2).
- The prior's best exact up-second, W a3 c5 d4 / B a7 b7 d7, and its best reachable 1/8 both fail under the adopted e.p.-aware convention. RESULTS.md section 6 still presents them under the textbook test.
- In my own target list, 'tiny(up)' = {0 || 0 | ↓} is canonically equal to ↑. My first scan therefore mislabelled 751 plain-↑ positions as tiny(up); fixed by removing that target. Similarly, database strings must be compared with order-normalised target strings, or up-second-star is missed.

## Open questions

- Real chess: does the 1/8 component W a2 b2 b3 / B a5 a6 b6, with the trébuchet (FEN 8/8/pp6/p4Kp1/6Pk/1P6/PP6/8 w - - 0 1, 10 men), behave as 1/8 with real kings? It is beyond Syzygy 7-man at the root. Its 23 race edges (count rule, e.p. on) all come after a capture, so race positions are at most 9 men.
- Same question for up-second-star at W a2 b2 b6 / B a6 b7 c5 (FEN 8/1p6/pP6/2p2Kp1/6Pk/8/PP6/8 w): 13 race edges, none before a capture.
- Is a full retrograde proof game possible for these pawn structures? My check is necessary conditions only, plus a hand-built capture order for the 1/8 mirror.
- Non-nimber targets were searched only under count / e.p. on / textbook. A position that is 1/8 or up-second only under the e.p.-aware or another race rule (and not in the parent's aware database) would be missed. The parent's comparison reports no aware-only 1/8, but it did not cover the mover or opponent rules.
- Is tiny(1*), or 2↑+2↑²+* = {0 | {↑ | *}}, already in the literature for chess? Novelty was not checked.
- Do 7-pawn components, or widths 5-7 with a different freezing device, give *3/*4 or a robust *2? Out of scope here.

## Next steps

- Parent session: save the report text from this output as atlas/flat8/rerun/REPORT.md; the harness blocks workflow agents from writing report .md files.
- Decide whether to merge PASSED_RESPECTS_EP into the main checkout's cylcgt/pawns.py. Until then, label every workflow result with which pawns.py it used.
- Fix compare_ep_aware.py to compare order-normalised strings plus outcome/mean/temperature (or game identity) before filling RESULTS.md EPAWARE_CENSUS. True changed count is at least 18,137, and outcome changes are 4,070.
- Update RESULTS.md section 6: the robust reachable 1/8 is W a2 b2 b3 / B a5 a6 b6 (all 9 settings, every race outcome, model level). The old 'best reachable' 1/8 and best up-second fail under the adopted convention.
- Real-chess certification (realchess/ workflow) of the 1/8 and up-second-star embeddings; their race positions are all post-capture.
- Run the C target test (nimscan --test) over the whole scope for 1/8 and the up-second family under the e.p.-aware and other race rules, to find targets missing from the count-rule database. It costs seconds.
