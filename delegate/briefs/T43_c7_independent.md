# T43: independent check of the C7 ring results (heavy compute; your own code)

**Output directory:** `research/c7_independent/`. Write everything there.

**Claims to check** (from our C scanner `frontier_split1_fixed2`, still running; do not touch
`research/star26_rings/` or its processes):
1. On the cylinder C7 (7 files that wrap, 8 ranks), these ten-pawn rings have value \*2 in the default setting:
   every line of `research/star26_rings/c7/p10_5_5/*.hits.tsv` (first column), for example
   `W: a2 a3 c3 e3 f2 / B: a4 b5 d5 f5 g5`.
2. No ring on C7 with 9 pawns has value \*2 (rings with at most 8 pawns are already covered by an earlier scan).

A ring has every file occupied. The default setting is: count race rule, e.p. on, e.p.-aware passed test.

**Write your own solver from the rules**, in C (or Python for part 1 only). Do not read or import `cylcgt/`,
`research/star26_rings/*.c`, `research/ring_min_independent/` or any other solver in this repository.
- **Board:** files a..g that wrap (a and g are neighbors), ranks 1..8, pawns only, no kings.
- **Moves:** single step, double step from rank 2 (White) or 7 (Black), diagonal captures (also across the
  seam), en passant. A double step gives the opponent an e.p. right for one move only. No promotion moves are
  ever needed, because a pawn that could promote is already passed (see below).
- **Passed pawn:** no enemy pawn ahead of it on its own file or on either neighboring file (with wrap). Under
  the e.p.-aware test, a pawn that the opponent can capture en passant on its next move is not passed.
- **Values:** a position where exactly one side has a passed pawn is a win for that side (worth ±BIG with
  BIG = 256; for the nimber test it is enough to treat it as a decisive win). If a move creates passed pawns for
  both sides, the count rule decides: the side that did not just move wins if its promotion distance is at most
  the mover's, otherwise the mover wins. Otherwise normal play: a side with no move loses.
- **Nimber test:** G = \*2 exactly when G + \*2 is a second-player win (outcome search on the sum with a nim
  heap of size 2; a decisive win in the pawn game ends the whole sum). Check also that G is not \*0 or \*1.
- **Part 1:** test every claimed ten-pawn hit. Report each as \*2 or not.
- **Part 2:** enumerate every C7 ring with 9 pawns (every file occupied, pawns on ranks 2..7 only, at least one
  pawn per side, no passed pawn for either side at the root, up to rotation and reflection of the files), and
  count those that are \*2. Split the work into chunks; at most 2 processes at a time, nice -n 15, under 4 GB
  each; memoise with a bounded hash table that replaces entries when full (never freeze it).
- **Cross-check your solver first** on the known small results: C3 `W a2 a3 b2 / B b7 c6 c7` is \*2, and C3 has
  no \*2 ring with 5 or fewer pawns; C4 `W a4 b2 c2 / B b6 c5 d6 d7` is \*2.

**Report** (final message): counts of rings by split, the \*2 hits, agreement with the claims (CHECKED-2 if so),
runtime and reproduce commands.
