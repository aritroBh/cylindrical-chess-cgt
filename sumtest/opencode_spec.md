You are writing a small, self-contained Python 3.12 program (standard library only; do not install
anything, do not use the network). Work ONLY inside the current directory
(/Users/aritro/Downloads/Research/Chessendgames/sumtest/opencode_impl/). Do NOT read, list, import or
search any file outside this directory: in particular never look at
/Users/aritro/Downloads/Research/Chessendgames/cylcgt/ or /Users/aritro/Downloads/Research/Chessendgames/crosscheck/.
This must be an independent implementation written only from the specification below.

# Task: brute-force OUTCOME solver for disjunctive sums G + R

Write from scratch a brute-force outcome solver for disjunctive sums G + R (combinatorial game theory,
normal play: players alternate; a move is made in exactly one component; a player with no legal move in
any component loses).

- White = Left, Black = Right.
- G is a pawn-only chess position: any number of files, flat board or cylinder (on a cylinder the first
  and last files are adjacent, so e.g. on 4 files a and d are adjacent and pawns capture across that
  seam), 8 ranks, en passant on or off (a parameter), normal play. Pawns move as in chess: one step
  forward to an empty square, two steps from their starting rank (White rank 2, Black rank 7) if both
  squares are empty, capture diagonally forward, and (if enabled) capture en passant.
- The Elkies convention ("BIG convention"): if the pawn component becomes a position where exactly one
  side has a passed pawn, its value is +BIG (White) or -BIG (Black), BIG = 256. The sum's outcome is then
  decided by that sign, since BIG dominates every R in the reference set.
- If both sides have passed pawns it is a race, resolved by a parametrised race rule:
  - "count": the opponent of the mover (the player who just made the move that created the race) moves
    first in the race, and whoever needs fewer moves to promote wins, with ties going to the opponent;
  - "mover": the mover wins;
  - "opponent": the mover loses.
- Pawns change file only by capturing.
- R is an explicit abstract game tree from this set:
  0, *, *2, *3, up, down, up*, double-up*, 1/2, -1/2, 1, -1, {1|0}, +-1, tiny(1)
  (standard CGT notation; tiny(1) = {0 || 0 | -1}; double-up* = up + up + *).
- The solver returns the outcome class of G + R in {L, R, N, P}
  (L: Left wins whoever starts, R: Right wins whoever starts, N: first player wins, P: second player wins).

Where the specification leaves a choice open (for example exactly what counts as a passed pawn, how a
race "count" is measured, or what happens to an en passant right when the next move is made in R
instead of in G), make a reasonable choice and DOCUMENT it precisely in README.md.

# Required interface

1. `solver.py`, runnable as `python3 solver.py` (no arguments). It reads JSON Lines from stdin, one
   problem per line, e.g.

       {"id": 7, "files": 4, "wrap": false, "ep": true, "race_rule": "count", "white": ["a2", "c2"], "black": ["b7", "d7"]}

   (`wrap` true means cylinder; squares are file letter a,b,c,... plus rank 1-8; the initial position
   has no en passant right and you may assume no initial passed pawns). For each input line it prints
   one JSON line

       {"id": 7, "outcomes": {"0": "N", "*": "N", "*2": "P", ...}}

   with the outcome class of G + R for each of the 15 reference games, using exactly these keys:
   "0", "*", "*2", "*3", "up", "down", "up*", "double-up*", "1/2", "-1/2", "1", "-1", "{1|0}", "+-1", "tiny(1)".
   It must handle a few thousand lines in a few minutes (memoise).
2. `test_solver.py`: a few sanity tests you can run with `python3 -m pytest -q` or plain `python3 test_solver.py`.
3. `README.md`: your conventions and design.

When you are done, run your tests and run the example line above through solver.py, and report the output.
