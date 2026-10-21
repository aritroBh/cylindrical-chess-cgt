# T9: chess on the Möbius strip and the Klein bottle (new boards, new theory)

Output directory: `research/mobius/`.

**Boards:**
- **Möbius strip.** Glue file h to file a with the ranks reversed: square (h, r) is adjacent to (a, 9-r).
- **Klein bottle.** The Möbius gluing of files, plus ranks 1 and 8 glued straight, as on a torus.

Write the rules down precisely in `research/mobius/RULES.md` before computing anything:
- how sliders, knights and kings move across the twisted seam;
- that a rook may not use a full loop as a null move (follow `tablebase/replica/REPORT.md`);
- for pawns, that "forward" reverses when a pawn crosses the twisted seam. Decide and justify one convention, e.g. pawns may not cross the seam, or crossing flips the direction.

**Part A: tablebases (no pawns).**
1. Copy `tablebase/replica/replica.c` into your directory, then generalise its adjacency to the Möbius strip and the Klein bottle.
2. Solve 4-man KQK, KRK, KBBK (split by bishop colour; colour classes may merge on the Möbius strip, so check this), KBNK, KNNK, KRBK, KRRK and KQRK.
3. Report, for White to move: legal positions, positions won, share won, maximal DTM and a maximal position.
4. Validate first: on the plane, cylinder and torus your code must reproduce the numbers in `tablebase/replica/REPORT.md` exactly.

**Part B: Elkies' pawn game on the Möbius strip** (pawns only, using the conventions of `delegate/COMMON.md`).
1. Build a small solver, reusing `cylcgt.cgt` for the canonical forms.
2. Enumerate all positions with <= 4 pawns on Möbius strips of width 3-6.
3. List the values that occur on the Möbius strip but not on the cylinder or a flat board of the same width.

Write `research/mobius/REPORT.md`. Novelty matters here: say plainly that no literature check was done, and leave that to T15.
