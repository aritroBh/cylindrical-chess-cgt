# T8b: push the *2 search past the current frontier (the open problem)

Output directory: `research/star2_frontier_b/`.

**Goal:** Elkies asks whether a *2 made only of kings and pawns exists on 8×8. Under the adopted e.p.-aware convention, no *k (k >= 2) exists on flat boards of width <= 4 with <= 6 pawns. Push that frontier as far as compute allows.

1. **Start from the existing solver.** Use the independent C solver `atlas/flat8/rerun/nimscan.c`. Read its header and `atlas/flat8/rerun/REPORT.md`, and copy it into your directory before changing anything. It decides G = *k by testing whether G + *k is a second-player win.
2. **New scopes, in this order:**
   - (a) flat width 5, w+b <= 6;
   - (b) flat widths 1-4, w+b = 7 and 8;
   - (c) flat width 5, w+b = 7;
   - (d) cylinders C_5 to C_9, ring positions only (every file occupied), w+b <= 8.
   - Conventions throughout: pawns on ranks 2-7; no passed pawn at the root; reduce by symmetry.
   - Estimate each scope's cost with a pilot first, and skip any scope estimated at over 3 CPU-hours.
3. **Settings.** Run all 9 settings: {count, mover, opponent} × {e.p. off, textbook, e.p.-aware}. The headline setting is e.p.-aware with count.
4. **Report:**
   - every *k with k >= 2, its settings, and its pawn count;
   - whether any is robust across all 9 settings;
   - whether it fits on 8×8 beside a trébuchet: component on files a-d or a-e, kings on f-h, at least one empty buffer file;
   - any *3 or *4.
5. **Validate first.** Before reporting new results, show that your code reproduces the known census on the old scope: 6,724 zeros, 4,042 stars and no *2 under e.p.-aware count.

Write `research/star2_frontier_b/REPORT.md`.
