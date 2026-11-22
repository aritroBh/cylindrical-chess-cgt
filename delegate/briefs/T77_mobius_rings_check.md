# T77: independent check of pawn rings on the Moebius strip

Output directory: `research/mobius_rings_check/`. Write your own program from the rules below.
**Do not read anything under `research/mobius_rings/` or `research/mobius/`** (that is the work being checked) until
your own numbers are final; you may read `research/c9_rings/rg_copy.c` or `cylcgt/pawns.py` for the cylinder game,
which is the same game without the twist.

## The game (whole-board pawn game with a nim-heap)

- Board: n files (1..n), 8 ranks. Files i and i+1 are neighbours; file n and file 1 are neighbours across the
  **seam**, with the rank flipped: square (n, r) is beside (1, 9 - r). (Cylinder = same without the flip.)
- Every pawn has a colour and a direction d (+1 = towards rank 8, -1 = towards rank 1). At the start White pawns
  have d = +1 and Black pawns d = -1. Home rank (double step allowed from it), and promotion edge follow d, not the
  colour: d = +1 double-steps from rank 2, d = -1 from rank 7.
- Moves: one step forward (in direction d) to an empty square; a double step from the home rank over an empty
  square to an empty square; a capture of an enemy pawn one step diagonally forward. Only captures change file.
  A capture that crosses the seam lands on the flipped rank and flips the capturing pawn's d. Example with n = 3:
  a White pawn (d = +1) on (3, 4) attacks (2, 5) and, across the seam, the square beside (3, 5), which is
  (1, 9 - 5) = (1, 4); after capturing there it stands on (1, 4) with d = -1.
- En passant as in chess: after a double step, an enemy pawn that attacks the skipped square may capture there
  on the very next pawn move of its side (across the seam with the same flip rules). As in `rg_copy.c`, an e.p. flag is
  recorded only if an enemy pawn can use it, and the right survives a move in the nim-heap.
- Passed: a pawn is passed if no enemy pawn (of either direction) stands strictly ahead of it, in its own
  direction, on its own file or a neighbouring file; for the seam neighbour "ahead" is read in the flipped
  coordinates. A pawn that can still be captured en passant is not passed.
- The pawn game ends as soon as a position has a passed pawn: the side that has one wins. If both sides have one
  after a move, the race rule "count" of `rg_copy.c` / `cylcgt.pawns` (RACE_RULE = "count") decides, with promotion
  distance counted in the pawn's own direction. A side with no pawn move (and an empty heap) loses.
- Signature of a position G: the outcome class (N, P, L, R) of G + *h for h = 0, 1, 2, 3, where *h is a nim-heap;
  either player may move in the heap instead of moving a pawn; a passed pawn ends the whole game at once.
  *2 means signature NNPN, *3 means NNNP.
- Root ring: pawns on ranks 2..7 with default directions, at least one pawn on every file, no passed pawn, no
  e.p. right.

## Tasks

1. Validate your program with the twist switched off against `research/c9_rings` data: the cylinder ring
   `B4 W2 B6 W2 W3 B6 B7 W3 B7 W5` on 10 files must be *2 (ring notation: one entry per file, left to right;
   `W23B4` = White pawns on ranks 2 and 3 and a Black pawn on rank 4 of that file), and on the 3-file cylinder
   `W a2 a3 b2 / B b7 c6 c7` must be *2. Also compare a few hundred random small cylinder positions with
   `cylcgt` outcomes if you can.
2. With the twist on, compute the signature of each ring below (seam between the last entry and the first):
   - n = 3: `W3B6 W2B7 W4B5`
   - n = 5: `B6 W3 B5 W2 W3B7`
   - n = 4: `B5 W23 W2B67 W4B7`
   - n = 6: `B4 W2 W2 W2B6 B5 W3B7`
   - n = 7: `B6 W2 W3 B6 B7 W3 W6B7`
   - n = 8: `B7 W3 W3 B6 W3 B6 B6 W2`
   - n = 5: `B67 W4 W2B6 W2B5 W5B7`
   - n = 6: `B7 W4 W23 B5 W3B7 W4B7`
3. Exhaustive: enumerate ALL root rings (count them without any symmetry reduction, and also up to the left-right
   mirror) and report how many are *2 and how many *3, for as many of these (n, pawns) as you can within the
   limits, in this order: (3,3) (3,4) (3,5) (3,6); (5,5) (5,6); (4,4) (4,5) (4,6) (4,7); (7,7); (8,8); (4,8);
   (6,6) (6,7). Report the ring counts so they can be compared.
4. REPORT.md: first your signatures for task 2 and your table for task 3, written BEFORE you open
   `research/mobius_rings/REPORT.md`; then a section comparing with that report (its claim: least pawns in a
   Moebius ring *2 is 6, 8, 6, 8, 8, 8 for n = 3..8; the eight rings above are *2, the last two *3). If anything
   disagrees, find the smallest position where the two programs differ and say which rule reading causes it.

Limits: at most 2 processes, nice 10, under 4 GB each, no job over 45 minutes, no pkill/killall (see the shared
rules), no git, write only in your output directory.
