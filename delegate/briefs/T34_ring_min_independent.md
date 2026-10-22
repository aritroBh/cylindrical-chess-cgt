# T34: independent check of the n+3 minimum for ring \*2 on C3 and C4 (moderate compute, your own code)

**Output directory:** `research/ring_min_independent/`.

**Claim:**
- On the cylinder C3, no ring has value \*2 with 5 or fewer pawns, and exactly one six-pawn ring has value
  \*2: `W a2 a3 b2 / B b7 c6 c7`.
- On C4, no ring with 6 or fewer pawns has value \*2; the seven-pawn ones include
  `W a4 b2 c2 / B b6 c5 d6 d7`.
- A ring has every file occupied, and the default setting is count rule, e.p. on, e.p.-aware passed test.

**Write your own solver from the rules**, in Python or C. Do not import cylcgt or frontier_split.
- **Board:** n files that wrap and 8 ranks; pawns only.
- **Moves:** single step, double step from rank 2 or 7, diagonal captures across the seam, and en passant.
  A double step creates an e.p. right for one move.
- **Passed pawn:** no enemy pawn ahead on its file or on an adjacent file (with wrap). Under the e.p.-aware
  test a pawn that can be captured en passant on the opponent's next move is not passed.
- **Values:**
  - a position where exactly one side has a passed pawn is worth ±BIG (BIG = 256);
  - if both sides have one after a move, apply the count rule: the side that did not move wins if its
    promotion distance ≤ the mover's;
  - otherwise normal play: no move loses.
- **Nimber test:** you only need to decide "is G = \*2". G = \*2 iff G + \*2 is a second-player win, which is
  outcome search on the sum with a \*2 heap. Alternatively, compute canonical forms.
- **Enumerate:**
  - every ring on C3 with 2–6 pawns, and on C4 with 2–7 pawns;
  - no pawn on ranks 1 or 8; neither side has a passed pawn at the root;
  - up to rotation and reflection.

**REPORT.md:**
- the counts of rings and of \*2 rings, by pawn count;
- the list of \*2 rings;
- whether this agrees with the claim (CHECKED-2 if so);
- runtime, and a reproduce command.
