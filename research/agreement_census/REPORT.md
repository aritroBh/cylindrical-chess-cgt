# Agreement census: model (cylcgt, e.p.-aware, count rule) vs exact kpsolve, beside a frozen trebuchet

Run 2026-10-28. All numbers are COMPUTED-1 (one program, kpsolve, plus cylcgt; no second solver was run here). Nothing under kings/, cylcgt/, realchess/, paper/ was edited.

## Summary (5 lines)

1. Enumerated class, queen-only promotion, cap 2, e.p. on, both sides to move, 1-2 pawns a side: **326 placements** on 4 boards (cyl:4x4 2, cyl:5x5 240, cyl:6x6 42, flat:5x6 42). Of these 137 start as a promotion race (model gives no value), 65 have one side to move illegal (a pawn attacks a king), leaving **124 testable placements, of which the model is right on 85 = 68.5%, Wilson 95% CI [59.9, 76.1]**. Counting races and illegal rows as non-predictions the figure is 85/326 = 26.1%.
2. Per board (testable): cyl:6x6 13/26 = 50.0% [32.1, 67.9]; flat:5x6 23/26 = 88.5% [71.0, 96.0]; cyl:5x5 (compact layout) 49/71 = 69.0% [57.5, 78.6]; cyl:4x4 0/1. The 6x6 and 5x6 figures **reproduce the published 13/26 and 23/26** at row level (0 verdict differences in 84 rows).
3. By model class (pooled, testable): L 33/40 = 82.5%, R 29/34 = 85.3%, N 14/24 = 58.3%, P 9/26 = 34.6%. The model fails mostly where it says the mover loses (P) or wins (N), i.e. where the trebuchet's zugzwang must hold.
4. All 39 mismatches are classified: **37 king effects** (frozen kpsolve = model, real chess differs; 23 of the 39 have a real draw, which the model never predicts) and **2 conventions** (frozen kpsolve differs from the model; both on cyl:5x5, both with a passer value +W/-W where the model says "wins at once" and the real/frozen result is N).
5. Promotion set: where QRBN is exactly determined it equals the queen-only result in 92 of 92 placements (cap 1 on 5x5/6x6/5x6, cap 2 on 4x4), but cap 1 leaves 234 of 324 undetermined, so this is a weak check. Cap-2 QRBN on 5x5 and flat:5x6, and cap-2 Q on 6x6, exceeded the 3.9 GB guard and were stopped (not completed). The 3-pawn extension is only a pilot.

## Important design caveats (read before quoting the numbers)

- **cyl:4x4 and cyl:5x5 have no room under the published layout** (`kings/experiment.py`: P lives on W-5 files, which is 0 or 0 for W=4, 5). I used a **compact layout with no buffer files**: P on file c (4x4) or files c,d (5x5); trebuchet Z as in `layout()` (Pa{r} pa{r+1} K{last}{r+1} kb{r}, r=H//2). Both Z were verified as mutual zugzwangs by kpsolve (w: L, b: W). Because P now stands next to the kings (b and the last file), P and Z are no longer separated by Lemma 2.2's empty buffers: pawn attacks on a king make 65 of the 240 5x5 rows illegal for one side, and the king-effect rate is higher. The 5x5 and 4x4 numbers answer "what happens with no buffer", not the published sweep design. 6x6 and 5x6 use the published layout.
- cyl:4x4 has only 2 placements (1 pawn each, on c2/c3), so it carries no statistical weight.
- Races are counted as their own class (kept in every table); "one side illegal" is a second non-testable class (a race row with an illegal side is counted as illegal). Side-level accuracy (each legal side separately) is given as a supplement.
- cyl:6x6 Q cap 2: my own re-run was stopped at 3.90 GB RSS sampled (4.03 GB max RSS) after 506 s. The cap-2 Q results for 6x6 used here are **imported** from `kings/results/exp_cyl6x6_epon_Q.jsonl` (kept in `work/cyl_6x6/out_Q2.txt`, status file says IMPORTED). My own frozen 6x6 run matches the published frozen values on all 84 positions.
- The memory guard (`guard.py`) polls every 2 s and kills only its own child; maxrss at kill was 4.03-4.15 GB decimal (3.76-3.86 GiB), a small overshoot of "4 GB" if read as decimal.
- The model side uses cylcgt's default e.p.-aware passed test (`PASSED_RESPECTS_EP = True`), not the textbook test the published sweeps were scored with; on 6x6/5x6 both give identical verdicts.

## Method (exact commands)

All from `/Users/aritro/Downloads/Research/Chessendgames/research/agreement_census/`. One kpsolve at a time, `nice -n 15`, `--threads 2`, PID in `work/*/kpsolve_*.pid`, RSS watchdog `guard.py` (kills own child above 3.9 GB).

1. Step 1, diff of 6x6 Q vs QRBN files (inline python, results in `qvsqrbn.py` / `qvsqrbn.txt`). The published QRBN file is cap 1: 13 determined, 13 undetermined, 16 race rows. Where the QRBN bounds agree it equals the Q cap-2 value (15 of 15 in the full-row comparison below).
2. Step 2, `python3 -I reagg_existing.py` -> `reagg_existing.json` (896 components = 42+42+812). Reproduces the published 341/500 (textbook test: 107 king effects, 52 convention) and gives 346/500 with the e.p.-aware test (120 king, 34 convention; 7x6 only changes: 143 -> 138 mismatches).
3. Generation: `python3 -I gen.py cyl:4x4 compact work/cyl_4x4 le2`; `gen.py cyl:5x5 compact work/cyl_5x5 le2`; `gen.py flat:5x6 orig work/flat_5x6 le2`; `gen.py cyl:6x6 orig work/cyl_6x6 le2`; and `ext3` variants (`work/*_x3`: 3 pawns on a side, where they fit). Counts (nW,nB) in {(1,1),(2,1),(1,2),(2,2)} for `le2`.
4. Solving (`chain1.sh`, `chain2.sh`, each line `python3 -I guard.py DIR BOARD PROMOTE CAP TAG [--frozen]`, i.e. `kings/kpsolve --board B --ep on --promote P --cap C --threads 2 [--frozen]`):
   - Q cap 2: cyl:4x4, cyl:5x5 (peak 1.85 GB, 145 s), flat:5x6 (peak 2.0 GB, 181 s), flat:5x6 ext3 (peak 3.07 GB, 254 s).
   - Frozen: every board (all fast).
   - QRBN cap 2: cyl:4x4 done; cyl:5x5 and flat:5x6 stopped at the memory guard (322 s and 257 s); fell back to QRBN cap 1 (bounds).
   - Q cap 2 for cyl:6x6 and cyl:6x6 ext3: stopped at the guard (506 s, 199 s). cyl:5x5 ext3: Q cap 1 only (peak 1.17 GB).
   - A first attempt on cyl:5x5 with all pawn counts incl. 3/3 (1000 positions) was stopped at 3.98 GB; its files are in `work/old_unused/` (empty of results).
5. Analysis: `python3 -I analyze.py` -> `census.tsv` (one row per placement and configuration, 920 rows), `summary.md`, `summary.json`; `mismatches.tsv` (the 42 mismatching rows in Q-cap-2 le2 plus ext3 sets).
   - Wilson 95% CI, z = 1.96. Prediction map: L -> (W,W), R -> (L,L), N -> (W,L), P -> (L,W) for (White to move, Black to move), White's view.
   - A row is "match" only if both sides' kpsolve values are exact (bounds equal) and equal the prediction; a real draw (D) is always a mismatch.
   - Mismatch label: pred = model prediction, fz = frozen kpsolve result. fz = pred -> **king effect**; fz != pred -> **convention** (suffix "+king" if also fz != real).

## Results

### Headline (testable = not a race, neither side illegal, bounds agree)

| board | pawns | promo/cap | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cyl:4x4 (compact) | le2 | Q/2 | 2 | 1 | 0 | 0 | 0/1 | 0.0% | [0.0, 79.3] | 1 | 0 |
| cyl:5x5 (compact) | le2 | Q/2 | 240 | 104 | 65 | 0 | 49/71 | 69.0% | [57.5, 78.6] | 20 | 2 |
| cyl:6x6 | le2 | Q/2 (imported) | 42 | 16 | 0 | 0 | 13/26 | 50.0% | [32.1, 67.9] | 13 | 0 |
| flat:5x6 | le2 | Q/2 | 42 | 16 | 0 | 0 | 23/26 | 88.5% | [71.0, 96.0] | 3 | 0 |
| **pooled** | le2 | Q/2 | 326 | 137 | 65 | 0 | **85/124** | **68.5%** | **[59.9, 76.1]** | 37 | 2 |
| flat:5x6 | ext3 | Q/2 | 8 | 2 | 0 | 0 | 5/6 | 83.3% | [43.6, 97.0] | 1 | 0 |

Pooled by model class (le2, Q cap 2):

| class | rows | one side illegal | match/testable | accuracy | Wilson 95% CI | king | conv | mismatches with real draw |
|---|---|---|---|---|---|---|---|---|
| L | 52 | 12 | 33/40 | 82.5% | [68.0, 91.3] | 6 | 1 | 3 |
| R | 52 | 18 | 29/34 | 85.3% | [69.9, 93.6] | 4 | 1 | 2 |
| N | 40 | 16 | 14/24 | 58.3% | [38.8, 75.5] | 10 | 0 | 8 |
| P | 32 | 6 | 9/26 | 34.6% | [19.4, 53.8] | 17 | 0 | 10 |
| race | 150 | 13 | n/a | n/a | n/a | n/a | n/a | n/a |

Race rows (137 plus 13 hidden under "illegal") have no model value. Real outcomes of the races at start are listed per configuration in `summary.md`.

By pawn count, by class and per configuration: `summary.md` ("by model class", "by pawns (W/B)" tables for each configuration). Side-level supplement (every legal exactly-valued side, non-race, Q cap 2): cyl:5x5 152/194 = 78.4% [72.0, 83.6]; cyl:6x6 32/52 = 61.5% [48.0, 73.5]; flat:5x6 49/52 = 94.2% [84.4, 98.0].

### Reproduction of published figures

| item | published | here |
|---|---|---|
| 6x6 cylinder testable | 13/26 | 13/26 (row-level verdicts identical, 42/42) |
| 5x6 flat testable | 23/26 | 23/26 (identical, 42/42; my own kpsolve run) |
| step 2 total (textbook test) | 341/500, 107 king, 52 convention | same |
| step 2 total (e.p.-aware test) | not stated | 346/500, 120 king, 34 convention |

### Promotion set (Q vs QRBN)

| board | QRBN run | exact | equals Q cap 2 | differs | undetermined |
|---|---|---|---|---|---|
| cyl:4x4 | cap 2 | 2 | 2 | 0 | 0 |
| cyl:5x5 | cap 1 | 58 | 58 | 0 | 182 |
| cyl:6x6 | cap 1 (published) | 15 | 15 | 0 | 27 |
| flat:5x6 | cap 1 | 17 | 17 | 0 | 25 |

Cap-1 QRBN model accuracy on its determined rows (selection-biased, not comparable to the Q cap-2 headline): 5x5 35/39, 6x6 13/13, 5x6 15/15. The determined rows are exactly those where promotion choice does not matter. Cap-2 QRBN was not achieved on the boards where it matters (memory).

### Three-pawn extension (pilot, not a headline)

- cyl:5x5 with 3 pawns on a side, Q cap 1: 260 rows, 95 races, 100 with an illegal side, 26 undetermined, 38/39 testable match (97.4%, CI [86.8, 99.5]); 1 king effect. Selection-biased by cap 1; most rows are not testable.
- flat:5x6, 3W+1B / 1W+3B, Q cap 2: 5/6 match (1 king effect). cyl:6x6 same set: not completed (memory guard).

### Mismatches (all 39 in the le2 Q cap-2 set, plus the 2 in the ext3 sets)

Full rows in `mismatches.tsv`. Breakdown of the 39 (board: cause, real outcome class):
- cyl:5x5: king effect 20 (11 real draws, 5 N, 3 L, 1 R); convention 2 (both real N).
- cyl:6x6: king effect 13 (10 draws, 1 L, 1 R, 1 N).
- flat:5x6: king effect 3 (1 draw, 2 L).
- cyl:4x4: king effect 1 (W c2 / B c3, model P (L,W), real draws on both sides).
The two convention failures (cyl:5x5, Q cap 2): `W: c2 c3 / B: d3` (model +W, class L, real and frozen both (W,L) = N) and `W: d3 / B: c3 c4` (model -W, class R, real and frozen both (W,L)). Both have a passer value (+-W) at the start, so they are "a passed pawn wins at once" failures of the V2 type (frozen kpsolve = real, so the kings are not the cause). Whether these two are the V2 mechanism is not tested here.
ext3 mismatches: cyl:5x5 `W: c2 c3 d3 / B: c4 d2` (Q cap 1, king effect: model -W class R, real (W,W)); flat:5x6 `W: a2 a3 a4 / B: a5` (king effect: model P, real (W,W)).

Reading of the king-effect rate (INFERENCE, not tested): the model's weakest classes are P and N, where the result relies on the zugzwang; a king leaving the trebuchet explains most failures, and 23 of the 39 mismatches have a real draw.

## Limits

- Only one pawn file (6x6, 5x6) or two files (5x5) per board; 4x4 has 2 placements. The class is "1-2 pawns a side beside this specific trebuchet", not all positions of the board.
- The 5x5/4x4 class uses a layout the earlier sweeps did not (no buffer); do not merge it with the published sweeps without saying so.
- Wilson intervals treat placements as independent; related placements (same pawns, other ranks) are not, so intervals are optimistic.
- Both sides of one placement are scored together, so a "mismatch" can be one side wrong.
- kpsolve is the only solver used (CHECKED-2 against the independent reference by earlier work on small boards: `kings/results/crosscheck.txt`; not re-checked here on these exact positions).
- Not done: cap-2 Q on 6x6 (reused), cap-2 QRBN on the boards that matter, the full 3/3 sets, and cyl:7x6 (skipped by brief).

## Files (all in this folder)

`gen.py`, `guard.py`, `run.sh`, `chain1.sh`, `chain2.sh`, `analyze.py`, `reagg_existing.py`, `qvsqrbn.py`; outputs `census.tsv`, `mismatches.tsv`, `summary.md`, `summary.json`, `reagg_existing.json`, `qvsqrbn.txt`; raw per-board outputs, status and PID files in `work/`; logs in `logs/`. No raw file exceeds 5 MB (largest directory 168 KB), so nothing was compressed.
