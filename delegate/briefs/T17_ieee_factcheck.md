# T17: adversarial fact-check of the IEEE paper

**Output directory:** `notes/ieee_review/facts/`.

**Input:**
- `paper/ieee/` (main.tex, sections/*.tex, main.pdf), written by T16;
- the fact sheet in `paper/ieee/SPEC.md`;
- `RESULTS.md`, `delegate/REVIEW.md` and `delegate/checks/*.out`.

**Task.**
1. Check every number, value, position, move and claim in the paper against the sources. Where possible,
   recompute it with `cylcgt` (`PYTHONPATH=. .venv/bin/python`): every pawn position the paper gives a value
   for, and every walk-through move.
   - Use the e.p.-aware test (`pawns.PASSED_RESPECTS_EP = True`) and the count rule unless the paper says
     otherwise.
   - Use the board width the paper states, or the 8-file flat board.
2. Check that each theorem's evidence label matches the sources.
3. Flag anything stated more strongly than the sources support.
4. Flag every chess-legality problem in a diagram: pawns on rank 1 or 8, a side in check that is not to move,
   adjacent kings.

**Deliverable: REPORT.md**
- A table with columns location (file:line) | claim | source or recomputation | verdict (OK / WRONG /
  UNSUPPORTED / OVERSTATED) | fix.
- WRONG items first.
- Do not edit the paper.
