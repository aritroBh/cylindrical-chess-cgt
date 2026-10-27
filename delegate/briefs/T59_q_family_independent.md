# T59: independent (non-Claude) computation for the *3 ring family Q_n

Output directory: `research/q_family_check/`. Create it and write nothing anywhere else.

## Rules of the game (implement these yourself)

Pawns only, on the n-file cylinder C_n with 8 ranks. File n-1 is adjacent to file 0.

**Moves:**
- White pawns move up the ranks and black pawns move down.
- A pawn steps one square forward if that square is empty.
- From its start rank (2 for white, 7 for black) it may double-step if both squares are empty.
- It captures diagonally forward onto an enemy pawn on an adjacent file. Adjacency wraps around.
- **En passant:** after a double step that lands beside an enemy pawn, that enemy may capture it e.p. on the very next
  move only.

**Passed pawns:**
- A pawn is *passed* if no enemy pawn stands ahead of it on its own file or on either adjacent file.
- A pawn that can be captured e.p. right now is NOT passed.

**Game end:**
- The game ends as soon as a move leaves exactly one side with a passed pawn. That side wins.
- If both sides have passed pawns, the race rule "count" decides:
  - the side whose passed pawn needs fewer moves to promote wins;
  - on a tie, the side that did NOT just move wins.
- A side with no legal move loses.

**Sum with a nim heap.** G+*h means: on each turn the mover either moves in G or reduces the heap *h to any smaller
heap. A player who cannot move loses. A position that makes a passed pawn ends the whole game as above. Compute the
outcome class of G+*h (N = first player wins, P = second player wins) for both movers; the signature is the outcome
for h = 0, 1, 2, 3, 4.

You may use the project's `cylcgt.pawns.passed` only to cross-check your passed test. Run with
`PYTHONPATH=. .venv/bin/python` from the project root. Do NOT read `rg.c`, `cylcgt`'s value code, or any `verify*`,
`check3` or `research/ring_n_plus_2*` directories.

## Positions

Q_n = W4 B7 (B4 W2)^((n-8)/2) W3B6 W3 W2B5 B5 W2 B4, for n even ≥ 8. Notation: one token per file, file 0 first.
`W3B6` is a white pawn on rank 3 and a black pawn on rank 6 of that file. White is "N"-first when white moves first.

## What to do

1. Implement the solver, in any language.
2. Compute the signature of Q_n for n = 8, 10, 12, 14, 16, 18, 20. The claim to test is that Q_n is *3, i.e. G+*h is
   N for h = 0, 1, 2, 4 and P for h = 3.
3. Controls:
   - Q_8 with the black pawn on file 1 moved from rank 7 to rank 6;
   - P_8 = W5 B7 W4 W4B7 B6 W3B6 W2 B4, which should be *2.
4. Write `REPORT.md`:
   - begin with a 5-line summary;
   - give each signature and its time;
   - give the command to reproduce;
   - state any disagreement plainly.

## Process rules

- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS.
- No git.
