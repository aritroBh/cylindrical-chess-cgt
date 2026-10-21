# T1b (free model): independent re-verification of the *2 headline results

Output directory: `verify_ext/omniroute/`.

So far every check in this project was written by Claude models. Your job is to provide a non-Claude implementation.

1. Write your own pawn-endgame game solver and canonical-form CGT code from scratch.
   - Do NOT import or read `cylcgt/`, `sumtest/`, `lemmas/`, `crosscheck/` or `atlas/` code.
   - You may read RESULTS.md and the REPORT.md files for the claims themselves.
2. Implement the rules exactly as described in `delegate/COMMON.md`.
   - Moves: single steps, double steps from the home rank, captures, and en passant.
   - Passed pawns: both the textbook and the e.p.-aware passed test.
   - Races: the three race rules.
3. Check these claims. For each, report AGREE, DISAGREE or COULD-NOT-CHECK, with your numbers.
   - (a) On a 4-file flat 8-rank board, `W a2 c2 / B b7 d7` is *2 under the textbook test (count and mover, e.p. on and off) and 0 under opponent.
   - (b) Under the e.p.-aware test with e.p. on, it is {2±1 | -2±1} under count and mover.
   - (c) Under the e.p.-aware test, count rule, e.p. on, no position in scope has value *k with k >= 2. Scope: flat 8 ranks, widths 1-4, pawns on ranks 2-7, at least one pawn per side, w+b <= 6, no passed pawn at the root. A nimber test (G + *k is a second-player win) is enough.
   - (d) `W a2 a3 b2 / B a6 b5 b6` equals 1/8 under all three race rules, with e.p. off, textbook and aware (test G - 1/8 = 0).
   - (e) `W a2 b2 b6 / B a6 b7 c5` equals {0,* | ↓} in the same nine settings.
4. Write `verify_ext/omniroute/REPORT.md` with a table of claim → verdict → evidence, plus your code.
