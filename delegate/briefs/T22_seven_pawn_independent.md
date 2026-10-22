# T22: independent census of 7-pawn positions (no code from the C scanners)

**Output directory:** `research/star2_seven_check/`.

**Background.**
- The claim "on flat boards of width ≤ 4, exactly two 7-pawn positions are \*2 under count / e.p.-aware" rests
  on one C scanner (`research/star2_frontier/frontier.c`, COMPUTED-1).
- The two are `W a4 b3 d2 d3 / B a7 b7 c5` and `W b4 c2 d2 / B a6 a7 c6 d5`.
- Make it CHECKED-2 with a different program.

**Task.**
1. Write your own enumerator. Do NOT read `frontier.c` or `nimscan.c`. Enumerate:
   - flat widths 1–4, 8 ranks, exactly 7 pawns, pawns on ranks 2–7, at least one pawn per side;
   - no passed pawn at the root (e.p.-aware test);
   - both edge files occupied; one of each mirror pair.
2. Evaluate each with `cylcgt` (`RACE_RULE = "count"`, `PASSED_RESPECTS_EP = True`, `Board(w, 8, False, True)`)
   and record the positions whose value is a nimber \*k with k ≥ 2.
3. Use `multiprocessing` with **at most 3 processes**. Other heavy jobs are running. Keep each job under
   45 minutes, and split the work and checkpoint to disk.
4. Report:
   - the root count;
   - the list of \*k hits;
   - whether it is exactly the two positions above.
   If it is not, give the differences.

**Deliverable:** REPORT.md, with labels and reproduce commands.
