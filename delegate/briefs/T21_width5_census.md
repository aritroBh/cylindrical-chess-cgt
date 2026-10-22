# T21: complete the *2 search on 5-file flat boards with 8 pawns

**Output directory:** `research/star2_width5/`.

**Background.**
- `research/star2_frontier/` (REPORT.md) scanned flat boards with:
  - widths ≤ 4 and 7–8 pawns;
  - width 5 with ≤ 7 pawns;
  - rings C5–C8.
- It did **not** scan flat width 5 with exactly 8 pawns. Its targeted tests found three \*2 positions there.

**Task.**
1. Use `research/star2_frontier/frontier` (or build it from `frontier.c` with `cc -O2`). Run the missing scope:
   flat width 5, exactly 8 pawns, all nine settings, the same root rules.
   - First a pilot to estimate the time. If it is over 45 minutes, split by pawn split (w, b) and run the parts
     in the background, one CPU core each, at most 2 at a time.
2. Re-check every \*k (k ≥ 2) hit at count / e.p.-aware with cylcgt:
   `pawns.RACE_RULE = "count"; pawns.PASSED_RESPECTS_EP = True; Board(5, 8, False, True)`.
3. Report:
   - counts of \*2 and \*3 by setting;
   - the hits at count / e.p.-aware;
   - whether the three known witnesses are found;
   - any \*3 at count / e.p.-aware.

**Deliverable:** REPORT.md, with labels and reproduce commands.
