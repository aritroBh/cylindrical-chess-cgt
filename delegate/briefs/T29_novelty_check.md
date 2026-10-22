# T29: novelty check for the paper's new results (web reading allowed, light)

**Output directory:** `notes/novelty2/`.

**Claims to check** (from `paper/ieee/sections/08_star2.tex`, `06_atlas.tex`, `10_tablebases.tex` and
`11_dawson.tex`). For each, search for prior work: Google Scholar, arXiv, MathOverflow, chess-variant sites,
and Elkies' and Siegel's papers.
1. A king-and-pawn position of value \*2 exists on the ordinary 8×8 board with seven pawns plus the trébuchet
   (Elkies' model).
   - Elkies 1996 lists no \*2.
   - Elkies 2002, "Higher nimbers in pawn endgames on large chessboards" (arXiv:math/0011253), builds higher
     nimbers on large boards. Read it and state exactly what board sizes and constructions it uses, with
     page numbers.
2. Cylinder chess: first ring \*2 on Cn has n+3 pawns (n = 3, 4, 5).
3. KPK on the 8×8 cylinder: the rook-pawn draw Ka6 Pa5 vs Ka8 becomes a win; 16,538 ordinary-board draws
   become wins.
4. KRK cannot force mate on the cylinder; KQK still can.
5. Dawson's chess on the 3×n cylinder is a first-player win iff g(n−3) = 0.

**Rules.**
- Network reading is allowed for this task: WebFetch or curl of public pages, at most 150 requests.
- Report: for each claim, PRIOR (with exact citation and quote ≤ 15 words), RELATED (what is close), or NOT
  FOUND (with the searches you ran).
- Never overstate novelty.
