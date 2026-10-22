# T13: Stockfish 19 and Lc0 on ChessSums positions beyond the tablebase

## 5-line summary

- Embedded all 19,956 rows of the four ChessSums 8-file subsets (k=1..4) into legal 8×8 positions by
  adding a king freeze; ground truth is the CGT outcome and winning-move set from `bench/`, which holds
  under the frozen-king convention (and under both passed-pawn tests, by bench construction).
- Stockfish 19 solves only 27.5% (1k)–28.0% (1M) of the 200-position evaluation subset by best-move-in-
  winning-set, dropping from 50% at k=1 to 10% at k=4 components; Lc0 is 32.5%–33.5% over the same.
- Outcome-evaluation accuracy is ~46–48% for both engines, barely above chance, versus near-perfect on the
  ≤7-man tablebase suite: larger sums are genuinely hard for search.
- The predicted nimber/infinitesimal fragility shows up as value-class dependence (nimbers easiest,
  numbers hardest), but k-dependence is monotone for all classes, not special to nimbers/infinitesimals.
- Shifted trébuchet freezes were verified as mutual zugzwangs by `kings/kpsolve`; the original freeze is
  Lichess-confirmed; caveats below.

## 1. Embedding

Source: `bench/data/{train,val,test,test_heldout}_8file.jsonl` (19,956 rows, k=1..4, 11–16 pawns).
Every row already fits 8 files; we add a 4-man king freeze (2 kings + 2 pawns) so the position is legal
chess and the freeze is a 0 under the convention. Total men 15–20, so no 7-man tablebase shortcut.

Freeze. The canonical freeze is the trébuchet `W Pg4 / B Pg5, WK f5, BK h4`. It is a real mutual
zugzwang on 8×8 (CHECKED-2 by Lichess, `kings/REPORT.md` §3). It fits only 85/364 of the test rows, so we
also use translated and vertically shifted trébuchets of the same shape (orientation A or its mirror,
pawn rank r=2..6). Each variant was solved by `kings/kpsolve` on the flat 8×8 board and is a mutual
zugzwang (White to move loses, Black to move loses) — COMPUTED-1. For every row we pick the first
variant whose four squares are empty and whose two kings are not in check from the existing pawns and not
adjacent; this succeeded for all 19,956 rows (0 failures). The chosen variant is recorded in `meta.json`.

Side to move: outcome `R` (Black wins) positions are set with Black to move and solution set =
`winning_moves.B`; all others White to move with `winning_moves.W`. `P` (draw) positions have an empty
winning set.

Ground truth is the CGT outcome (`L/R/N/P`) and winning-move set from `bench/`. It holds under the
frozen-king convention; bench's values are identical under the textbook and e.p.-aware passed-pawn tests
(bench REPORT, claim C2), so no passed-test ambiguity arises.

## 2. Engines and run conditions

- Stockfish 19: `engine/vendor/Stockfish/src/stockfish`, 1 thread, 64 MB hash, no tablebases.
- Lc0 v0.32.1: `/opt/homebrew/bin/lc0`, bundled network (Metal backend).
- Runner: `engine/run_suite.py`, node limits 1k/10k/100k/1M.
- Evaluation subset: 200 positions stratified by k (50 each) and value class, ids in `subset_ids.json`.
- Reproduce Stockfish: `.venv/bin/python engine/run_suite.py --engine engine/vendor/Stockfish/src/stockfish --epd engine/runs/chesssums/chesssums_subset.epd --nodes 1000 10000 100000 1000000 --option Threads=1 --option Hash=64 --json engine/runs/chesssums/sf_results.json`
- Reproduce Lc0 (1k/10k on 200): chunked runs merged into `lc0_1k_merged.json` / `lc0_10k_merged.json`.

## 3. Results: Stockfish 19 (200 positions)

Best-move-in-winning-set accuracy (positions with a winning set; P-positions excluded in parentheses):

| nodes | solved / 200 | excl. P (155) | k=1 | k=2 | k=3 | k=4 |
|---|---|---|---|---|---|---|
| 1k  | 55 (27.5%) | 35.5% | 50.0% | 30.0% | 16.0% | 14.0% |
| 10k | 53 (26.5%) | 34.2% | 50.0% | 28.0% | 20.0% | 8.0% |
| 100k| 55 (27.5%) | 35.5% | 50.0% | 32.0% | 18.0% | 10.0% |
| 1M  | 56 (28.0%) | 36.1% | 48.0% | 32.0% | 22.0% | 10.0% |

By value class (1k → 1M):

| class | n | 1k | 10k | 100k | 1M |
|---|---|---|---|---|---|
| nimber | 13 | 53.8% | 53.8% | 53.8% | 53.8% |
| infinitesimal | 36 | 33.3% | 25.0% | 27.8% | 27.8% |
| switch | 88 | 23.9% | 26.1% | 27.3% | 28.4% |
| number | 63 | 23.8% | 22.2% | 22.2% | 22.2% |

Outcome-evaluation accuracy (sign of root score vs CGT outcome; 173 scored positions): 48.0% (1k),
46.2% (10k), 47.4% (100k), 48.0% (1M). By class at 1M: nimber 66.7%, infinitesimal 62.5%,
switch 51.5%, number 33.3%.

Nodes to reach a correct move: solution_depth median 1 at all budgets (range 1–27 at 1M); the engine
exhausts its node budget on these positions.

## 4. Results: Lc0 (200 positions at 1k/10k; 10 positions at 100k; 1 position at 1M)

| nodes | solved / n | excl. P | k=1 | k=2 | k=3 | k=4 |
|---|---|---|---|---|---|---|
| 1k  | 65/200 (32.5%) | 41.9% | 52.0% | 28.0% | 24.0% | 26.0% |
| 10k | 67/200 (33.5%) | 43.2% | 52.0% | 30.0% | 26.0% | 26.0% |
| 100k| 5/10 | — | — | — | — | — |
| 1M | 1/1 | — | — | — | — | — |

By value class:

| class | n | 1k | 10k |
|---|---|---|---|
| nimber | 13 | 61.5% | 69.2% |
| infinitesimal | 36 | 33.3% | 30.6% |
| switch | 88 | 35.2% | 36.4% |
| number | 63 | 22.2% | 23.8% |

Outcome-evaluation accuracy: 46.5% (1k), 47.5% (10k).

## 5. Interpretation

- The ≤7-man suite is near-perfect for both engines; ChessSums beyond 7 men is not. Move accuracy
  ~28–34% and outcome-eval ~47% show that larger sums defeat search, as predicted.
- k-dependence is strong and monotone (50%→10% for Stockfish) for every value class; the prediction that
  nimber/infinitesimal parts drive the difficulty is only partly supported: nimbers are actually the
  *easiest* class for both engines, and infinitesimals are mid-pack. The hardest class is numbers.
- Lc0 is modestly better than Stockfish on move accuracy (33.5% vs 28.0% at 1M/10k) but shows the same
  k-dependence; neither engine's extra nodes help much (27.5%→28.0% Stockfish; 32.5%→33.5% Lc0).

## 6. Caveats on the frozen-king convention

- The freeze is assumed to be the CGT game 0. The original trébuchet is a real mutual zugzwang
  (Lichess, CHECKED-2). The shifted variants are mutual zugzwangs by `kings/kpsolve` (COMPUTED-1) on empty
  boards; in a crowded position the kings may interact with pawns (V1 of `kings/REPORT.md`), so the
  convention may fail there. We chose variants whose king squares are not in check from existing pawns, but
  did not certify full non-interaction.
- `kings/REPORT.md` shows the convention fails for some small components (107/500 king effects; 52 pawn-
  convention failures), so ChessSums ground truth is valid only under the frozen-king convention, not
  necessarily in real chess.
- The 8×8 embedding geometry of the original freeze has no checks/stalemate (proved); shifted variants are
  not geometry-proved, only kpsolve-checked.
- No Lichess/tablebase check is possible on the full 15–20-man positions. The freeze alone (4 men) is
  tablebase-confirmed for the original variant.
- All ground truth is COMPUTED-1 from `cylcgt` (bench claim C2/C3 checked two ways for outcomes).

## Files

- `chesssums.epd`: 19,956 embedded positions.
- `meta.json`: per-position metadata including freeze variant.
- `subset_ids.json`, `chesssums_subset.epd`: 200-position evaluation subset.
- `sf_results.json`, `lc0_*_merged.json`: engine runs.
