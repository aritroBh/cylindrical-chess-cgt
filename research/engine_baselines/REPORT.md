# Engine baselines for Section XII (COMPUTED-1)

All numbers COMPUTED-1: recomputed offline from files on disk, no engine rerun.

## Summary
1. (B) On the 200 ChessSums positions a uniformly random legal move is a model-winning move with expected accuracy 23.7% (random pawn move 49.0%); Stockfish 26.5-28.0% is 1.12-1.18x random legal, 0.56-0.59x random pawn; Lc0 32.5-33.5% is 1.37-1.41x and 0.69-0.71x.
2. (B) The paper's engine percentages reproduce exactly. Caveat: in 72 positions some listed winning moves are not legal on the 8x8 board; in 16 all are (plus 45 with none), so 61 of 200 have no legal winning move.
3. (A) The 233-position table reproduces cell for cell. On the 180 agree-only positions (181 minus 1 decided) infinitesimals are still weakest at depth 1 and 2 (30%, 26%, n=27); all 27 infinitesimals and all 20 other-tame are in the agree set, so the 52 disagreements lie in hot, number, decided.

## Table B1: random baselines (200 positions, `subset_ids.json`)
Legal moves via python-chess 1.11.2 (`.venv`; positions with more than 8 pawns accepted, only that status flag ignored). Hand check of 5 positions by listing moves from the FEN: `train-14899` 5 (Ke3 Ke4 Ke5 Kg5 d5; Kf3, Kf5 and Kxg4 are illegal, g3 is blocked), and the program counts `train-00714` 4, `train-17371` 4, `test_heldout-00568` 6, `train-05427` 6, which agree.

| quantity | value |
|---|---|
| legal moves per position min / median / max | 2 / 6 / 12 |
| pawn moves per position min / median / max | 0 / 3 / 7 (7 positions have no pawn move) |
| listed winning moves (`solutions_uci`) min / median / max | 0 / 1 / 7 (155 positions with >=1; 45 with 0, all outcome P) |
| legal winning moves min / median / max | 0 / 1 / 6 (139 positions with >=1) |
| positions where a listed winning move is illegal | 72 (85 illegal listed moves; 82 land on an occupied square, 3 do not); all winning moves illegal in 16 |
| winning moves that are non-pawn moves | 0 |
| random legal move, expected accuracy, all 200 | 23.7% (47.4 expected correct) |
| random pawn mover, all 200 (0 when no pawn move) | 49.0% (94.6 expected correct) |
| same, only the 155 positions with a listed winning move | legal 30.6%, pawn 61.0% |
| same, only the 139 positions with a legal winning move | legal 34.1%, pawn 68.1% |

Scoring of the 45 outcome-P positions: `solved` is false for every engine (0 of 45 solved in every file), so they count as errors in the paper's 200 denominator, as do the 16 all-illegal ones.

## Table B2: engine accuracy (solved = best move in `solutions_uci`; recomputed equals stored flag)
| engine, budget (file) | solved/200 | % | % of 155 | ratio to random legal (47.4) | ratio to random pawn (94.6) |
|---|---|---|---|---|---|
| Stockfish 1e3 (`sf_results.json`) | 55 | 27.5 | 35.5 | 1.16 | 0.58 |
| Stockfish 1e4 | 53 | 26.5 | 34.2 | 1.12 | 0.56 |
| Stockfish 1e5 | 55 | 27.5 | 35.5 | 1.16 | 0.58 |
| Stockfish 1e6 | 56 | 28.0 | 36.1 | 1.18 | 0.59 |
| Lc0 1e3 (`lc0_1k_merged.json`) | 65 | 32.5 | 41.9 | 1.37 | 0.69 |
| Lc0 1e4 (`lc0_10k_merged.json`) | 67 | 33.5 | 43.2 | 1.41 | 0.71 |

Paper: Stockfish 26.5-28.0% (1e4 low, 1e6 high) confirmed; Lc0 32.5-33.5% at 1e3 and 1e4 confirmed; "34-36% and 42-43% without the 45" confirmed (34.2-36.1, 41.9-43.2). Lc0 was run on 200 only at 1e3 and 1e4.

## Table A1: Stockfish 19, eval matches tablebase (%), by class (n), 226 positions excluding 7 decided
Same metric as `engine/runs/analyze_sf.py` (score verdict, thresholds +-150 cp or mate, vs tablebase root; file `engine/runs/sf19_depth.json`, classes from `c5` in the two EPD files). Full table equals Table I of `12_engines.tex` in every cell; no difference. Full and agree-only tables with counts and Wilson 95% intervals for depth 1 and 2 are in `baseline_a_tables.md`.

Agree-only (the 181 positions of `cgt_verified.epd`, 1 decided removed; the 52 of `cgt_disagree.epd` are 24 hot, 20 number, 6 decided, 1 switch, 1 nimber):

| class | n | d1 | d2 | d4 | d6 | d8 | d12 | Wilson d1 | Wilson d2 |
|---|---|---|---|---|---|---|---|---|---|
| hot | 44 | 80 | 77 | 86 | 98 | 100 | 100 | 65-89 | 63-87 |
| number | 37 | 84 | 86 | 89 | 97 | 97 | 97 | 69-92 | 72-94 |
| switch | 36 | 72 | 78 | 89 | 100 | 100 | 100 | 56-84 | 62-88 |
| other | 20 | 60 | 50 | 75 | 95 | 100 | 100 | 39-78 | 30-70 |
| nimber | 16 | 50 | 62 | 88 | 100 | 100 | 100 | 28-72 | 39-82 |
| infinitesimal | 27 | 30 | 26 | 59 | 85 | 100 | 100 | 16-48 | 13-45 |
| all | 180 | 67 | 67 | 82 | 96 | 99 | 99 | 59-73 | 60-74 |

Does "weakest on infinitesimals at low depth" hold? Yes. Infinitesimal at d1/d2 sits below number and switch (intervals for number 69-92 and 72-94 do not overlap infinitesimal's 16-48 and 13-45) and below hot. Overlaps remain with other (39-78, 30-70) and nimber (28-72, 39-82), as the paper already says. Nimber falls from 53 to 50 at d1 and 65 to 62 at d2 (one position lost); the paper's "nimbers 53%" is the full-suite figure.

Other Section XII checks: Stockfish solves 233 at 1e5 and 232 at 1e3 and 1e4 (and 233 at 1e6) confirmed; Lc0 solves 233/233 at 1e3 to 1e6 confirmed (draw subset not separately checked). Not reproduced: none of the numbers in the section. Not checked: the 26,000, 418, 37, 4,887 and node-ratio claims (other data).

## Commands (repo root)
```
.venv/bin/python research/engine_baselines/baseline_b.py   # writes baseline_b.json
python3 research/engine_baselines/baseline_a.py            # writes baseline_a_tables.md
```

## Candidate sentences (at most 25 words)
1. B: "Random legal play scores 23.7% on these 200 positions and random pawn play 49.0%, so neither engine is far above chance." (21 words)
2. A: "On the 180 positions where model and tablebase agree, infinitesimals are still hardest at depth 1 and 2 (30% and 26%, n=27)." (22 words)
