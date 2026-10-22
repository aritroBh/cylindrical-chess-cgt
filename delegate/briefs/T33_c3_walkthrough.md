# T33: move-by-move explanation of the six-pawn \*2 on the 3-file cylinder (light compute)

**Output directory:** `research/c3_star2/`.

**Position:** `W a2 a3 b2 / B b7 c6 c7` on C3 (files a, b, c; a and c adjacent). Default setting: count rule,
e.p. on, e.p.-aware test.

Compute its value with cylcgt (`PYTHONPATH=.`, `pawns.Board(3, 8, True, True)`, `pawns.RACE_RULE="count"`,
`pawns.PASSED_RESPECTS_EP=True`). It should be \*2.

**Task.**
1. List every move for each side, the resulting position and its canonical value.
2. Explain why the value is \*2 = {0, \* | 0, \*}, in the paper's walk-through style (see
   `paper/ieee/sections/08_star2.tex`, positions A and B):
   - which moves lead to 0 and to \*;
   - which are reversible and how they reverse;
   - which are dominated.
3. Show why it is 0 with e.p. off: which en passant capture matters.
4. Show its value under the mover and opponent rules.
5. Check the same for `W a4 b2 c2 / B b6 c5 d6 d7` on C4 (7 pawns).
6. Can either position arise in a game on a cylinder with 3 or 4 files, starting from pawns on ranks 2 and 7?
   Give capture histories.

**Deliverable:**
- `REPORT.md` with the walk-throughs, each about 120 words, ready to adapt;
- every value recomputed and printed in an appendix.
