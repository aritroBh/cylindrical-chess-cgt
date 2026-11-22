This section defines the square-rule passer test S used for the repair in the main text, says what was computed with it, and shows that S is not a sound certificate in general. No proof is claimed.

## 1. Definitions

**Board and game.** `k` files (cyclic on a cylinder, linear otherwise), `H` ranks. White pawns move up, towards rank `H`; Black pawns move down, towards rank 1. This is the frozen-king pawn game: a king move loses at once, a pawn that reaches its last rank wins at once, and a side with no legal pawn move loses.

**Passed (e.p.-aware).** A pawn of X on `(f, r)` is passed iff no enemy pawn lies on files `f-1, f, f+1` at a rank strictly beyond `r` in X's direction, and the pawn cannot be captured en passant.

**Runner.** A passed pawn is a runner iff no own pawn lies on the same file strictly beyond it.

**Distances.** For a White pawn on rank `r` let `sdist_W(r) = H - r - (1 if r = 2 else 0)`, and for a Black pawn `sdist_B(r) = r - 1 - (1 if r = H-1 else 0)`: the number of moves to promote if nothing is in the way, with one double step from the start rank. Let `n` be the least `sdist` over the runners of X, and `d` the least `sdist` over all pawns of the opponent Y (`d = ∞` if Y has none).

**The test S.** S certifies X iff X has a runner and `n ≤ d` when X is to move, or `n < d` when Y is to move.

## 2. What was computed

- **The repair of the main text.** In the sweep on the seven-file and six-file cylinders and the flat five-file board, all with 6 ranks, the game is ended only at a passed pawn that S certifies. This removes all 52 failures of the passer convention and leaves 128 mismatches, all from the kings (COMPUTED-1, `research/v2_mechanisms/cc.py`). This is a comparison with the real results and does not depend on S being sound.
- **Exhaustive check on small boards.** S never certifies a side that loses the frozen game in 158,544 cases (position, side to move, e.p. state): 1 and 2 files with 8 ranks and 2 files with 6 ranks, up to three pawns a side, and 3 files with 6 ranks, up to two pawns a side (COMPUTED-1, the same program).

## 3. S is not sound in general

**Counterexample** (checked by hand and with the solver of `research/v2_mechanisms/pawngame.py`)**.** Flat board, 3 files and 8 ranks, `W: a4 b6 / B: c7`, Black to move. The pawn a4 is a runner with `n = 4`; Black's only pawn has `d = 5`; Black is to move and `4 < 5`, so S certifies White. But Black wins: 1... cxb6, 2. a5 (White's only pawn move), 2... bxa5, and White has no pawn move.

The reason is that an enemy pawn two files away from the runner can capture another pawn of X and land on a file next to the runner, ahead of it. The same position with 9 ranks (`W: a5 b7 / B: c8`) fails in the same way. The pattern needs a runner on rank `r`, a pawn of X on the next file at rank `r + 2` and an enemy pawn at rank `r + 3` on the file beyond, with `n < d` and Y to move. It needs three files and at least 8 ranks, and the exhaustive check above has at most 2 files at 8 ranks, so it does not meet it.

**Status.** S is a heuristic certificate. It is sound on the boards of the exhaustive check (COMPUTED-1). Whether it is sound on all boards with 6 ranks, and which extra condition makes it sound in general, is open. A sufficient extra condition must at least exclude enemy pawns that can reach a file next to the runner by capturing.
