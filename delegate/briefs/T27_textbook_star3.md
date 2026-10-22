# T27: check T24's \*3 positions on six files under the count and mover rules

**Output directory:** `research/star27_textbook3/`. Create it.

**Claim to check.** T24 scanned the ordinary 6-file board with 8 pawns (`research/star3_hunt/flat_w6p8_*.tsv`,
from frontier_split `--flat`). Its table reports these \*3 or higher counts:

| Setting | \*3+ positions |
|---|---|
| count / e.p. on / textbook test | 16 |
| count / e.p. off | 16 |
| mover / e.p. on / textbook test | 14 |
| mover / e.p. off | 22 |
| either rule, e.p.-aware test | none |

With e.p. off, the textbook and e.p.-aware tests coincide. So a \*3 with e.p. off would not be a passed-pawn-test
artifact; it would be a \*3 of chess without en passant.

**Task.**
1. Extract every row whose nimber is ≥ 3 in any count or mover column. The TSV columns are position, width,
   npawns, then C/T, C/off, C/aware, M/T, M/off, M/aware, O/T, O/off, O/aware, each as outcome,nimber.
   - The files are large: stream them with awk.
   - Keep one hits file.
2. For each hit, compute its value with `cylcgt` in all 9 settings (`PYTHONPATH=.`):
   - `pawns.Board(6, 8, False, ep)`;
   - `pawns.RACE_RULE` set to count, mover or opponent;
   - `pawns.PASSED_RESPECTS_EP` set per setting;
   - clear the caches between settings (any function with `cache_clear`).

   Record whether cylcgt agrees with the scanner.
3. Take the 3 cheapest e.p.-off \*3 hits and check them with the independent whole-board solver:
   - `verify_ext/codex/solver.py`, with `PawnGame(6, "count", False, "aware")`,
     `parse_position(text.replace(":", ""), 6)` and `show(value(w, b))`;
   - it ends the game at the first passed pawn, and can be slow (about 10 minutes per position at width 5);
   - run at most 3 processes, under `nice -n 10`.
4. For one confirmed e.p.-off \*3, explain the value: its options, and which are reversible or dominated.

**REPORT.md:**
- the hit table, with both programs' values;
- the verdict: is there a \*3 under the count rule with e.p. off on six files (CHECKED-2 or not)?
- why the e.p.-aware test removes them;
- reproduce commands.

Never commit a file over 50 MB.
