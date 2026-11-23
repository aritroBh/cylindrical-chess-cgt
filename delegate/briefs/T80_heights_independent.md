# T80 — Independent check: the pawn game on boards of other heights

Output directory: `delegate/out/T80/` (create it). Write `REPORT.md` there and your programs. Do not edit
anything else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs
you started and recorded yourself. At most 2 processes at once, each under 3 GB, `nice -n 15` if your sandbox
allows it; total compute budget about 90 minutes. Other people's jobs run on this machine: leave them alone.
Do not copy raw terminal transcripts into your report.

## Claim to check

`research/tall_boards/REPORT.md` (one program, `tw.c`, checked against the project's Python engine on samples)
says that in the whole-board pawn game on a board with R ranks:

1. On R = 5 no position of the scanned class has value *2 or *3, on any of: ordinary boards of 3 and 4 files,
   cylinders of 3, 4 and 5 files (236, 2196, 121, 826 and 5847 positions; all solved).
2. On R = 6 the least number of pawns in a *2 is 8, 6, none, 6, 8 on those five boards, and there is no *3
   (7093, 219491, 3259, 72435 and 1786651 positions; all solved).
3. On R = 7: *2 with 4 pawns exists (`W: a2 c2 / B: c3 b6` on the ordinary 3-file board; `W: c2 a3 / B: b5 c5`
   on the 3-file cylinder; `W: a2 c2 / B: d4 b6` on the ordinary 4-file board), and *3 with 6 pawns
   (`W: a2 c2 d3 / B: c3 b6 c6`, ordinary 4 files). The ordinary 3-file board (196918 positions) and the 3-file
   cylinder (86802) are solved completely: 8 and 6 positions of value *2, no *3.
4. On the 3-file cylinder with R = 9, the position with all pawns at home, `W: a2 b2 c2 / B: a8 b8 c8`, is *2.
5. No position anywhere has a nimber above *3.

## The game (write your solver from this text; do NOT read or import `research/tall_boards/tw.c`, `cylcgt/` or
any other solver in the repository)

- Board: F files, R ranks; ordinary (files a.. are a strip) or cylinder (the first and last files are adjacent).
- White pawns move up one empty square; from rank 2 they may move two if both squares are empty. Black pawns move
  down; double step only from rank R-1. Captures are one step diagonally forward onto an enemy pawn (across the
  seam on a cylinder). En passant: right after a double step, an enemy pawn standing beside the pawn (same rank,
  adjacent file) may capture it by moving diagonally forward to the square it skipped; the right lasts for that
  one reply only.
- A pawn is passed if no enemy pawn stands ahead of it on its own file or on an adjacent file (adjacent across the
  seam on a cylinder). Exception (the paper's default test): a pawn that the opponent can capture en passant right
  now is not passed.
- The game ends as soon as a position has a passed pawn. If only one side has passed pawns, that side wins. If
  both have, compare how many moves each side's most advanced passed pawn needs to promote (White promotes on
  rank R, Black on rank 1); the "count" rule: the side to move wins if its count is at most the opponent's count,
  otherwise the opponent wins. (State in your report exactly how you implemented this; if the rule as written is
  ambiguous, read `research/tall_boards/REPORT.md` section "The game" for the intended reading and say so.)
- Otherwise players alternate moves, and a player with no move loses (normal play).
- Value: a position G is the nimber *k if the outcome of G + *h (h = 0..7, *h a nim-heap of size h) is a
  second-player win exactly for h = k. Compute the outcome class (N, P, L, R) of G + *h for each h and report the
  8-letter string.
- Scanned class ("roots"): White pawns on ranks 2..R-2, Black pawns on ranks 3..R-1, at most one pawn per square,
  every file occupied by at least one pawn, no passed pawn in the position, no en passant right pending, counted
  up to left-right mirror and colour reversal (colour reversal = swap colours and flip ranks r -> R+1-r); on a
  cylinder also up to rotation.

## Tasks

1. Solve the named positions in claim 3 and 4 and the three 6-pawn examples the report gives for R = 6. Report the
   8-letter string for each.
2. Enumerate the full class for R = 5 (all five boards), R = 6 (all five boards) and R = 7 (ordinary 3 files and
   3-file cylinder), solve every position, and report per board: number of positions (compare with the counts
   above; if your count differs, find out whether the difference is the symmetry reduction or the class
   definition and say which), and the number of positions of each nimber value *0..*7, and the least pawn count
   of a *2 and of a *3.
3. State agreement or disagreement with each of claims 1 to 5 (claim 5 only for what you enumerated), with the
   smallest counterexample if any.

Report format: a five-line summary first; then one table per task; label each statement RUN (you ran it) or
READ (from reading only). Keep the report under 150 lines.
