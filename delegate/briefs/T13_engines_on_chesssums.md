# T13: Stockfish 19 and Lc0 on ChessSums positions beyond the tablebase

Output directory: `engine/runs/chesssums/`.

**Context:** on the 233-position suite (<= 7 men) both engines are near-perfect (`engine/runs/analysis.md`, `engine/runs/lc0/analysis.md`). The CGT contrast needs bigger sums, where only CGT knows the answer. ChessSums is in `bench/`; read its README and REPORT. Its 8-file subsets contain sums that fit on 8 files.

1. **Embed instances.** Turn each 8-file ChessSums test instance into a legal 8×8 chess position.
   - Add a king freeze, the trébuchet W Pg4 / B Pg5, WK f5, BK h4, only if it fits. Otherwise design another legal freeze and justify it.
   - Keep only positions with > 7 men.
   - Ground truth is the CGT outcome and winning-move set from bench. State clearly that it holds under the frozen-king convention.
2. **Run the engines.** Use `engine/run_suite.py` (or write an EPD-like runner) with:
   - Stockfish: `engine/vendor/Stockfish/src/stockfish`, 1 thread, 64 MB hash;
   - Lc0: `/opt/homebrew/bin/lc0`, bundled network.
   Node budgets: 1k, 10k, 100k and 1M for a subset of 200.
3. **Measure:**
   - best-move-in-winning-set accuracy and outcome-eval accuracy, by number of components k and by CGT value class (nimber, infinitesimal, number, switch);
   - nodes needed to reach a correct move.
   The prediction to test is that the k-dependence is strongest for nimber and infinitesimal parts.
4. Report the tables, plus caveats on the frozen-king convention: check some positions with `kings/` or Lichess where possible.

Write `engine/runs/chesssums/REPORT.md`.
