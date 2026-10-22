# T26: does the first ring \*2 on Cn always have n+3 pawns? And is there a \*3 on narrow cylinders?

**Output directory:** `research/star26_rings/`. Create it. Do not edit `research/star3_hunt*`.

**Known** (default setting: count rule, e.p. on, e.p.-aware test; see `delegate/REVIEW.md` T24):
- The first ring \*2 (every file occupied) on C3 has 6 pawns (`W a2 a3 b2 / B b7 c6 c7`).
- On C4 it has 7 pawns (`W a4 b2 c2 / B b6 c5 d6 d7`).
- On C5 it has 8 pawns (the 14 known rings).
- On C6 there is none with 8 pawns or fewer.
- The pattern is n+3 pawns.

**Tool.**
- `research/star3_hunt/frontier_split`: copy it in, and pass `--cylinder --width n --min p --max p --nw a --nb b`.
- Its stderr line always prints "flat". That is a known cosmetic bug; check that you passed `--cylinder`.
- The TSV columns are position, width, npawns, then the 9 settings. Column 6 is count/epon/aware, as
  outcome,nimber.
- Pilot every split first with `--pilot 2000`, and skip any split projected at over 4 CPU-hours (say so).
- Run every split under `nice -n 10`, at most 3 processes at once.
- Do not keep TSVs over 50 MB. Keep only the hit rows (`grep` the nimber ≥ 2 rows) plus the log.

**Scans** (every split nw+nb=p that has roots):
1. C6 with 9 pawns. This is the pattern's prediction.
2. C7 with 10 pawns, if the pilot allows. Otherwise C7 with 9 pawns, to confirm there is none below.
3. Narrow cylinders, looking for the first \*3: C3 with 7–10 pawns, and C4 with 8–9 pawns.

**Verify** every new minimum-pawn \*2 and every \*k (k ≥ 3) in the default setting with `cylcgt`:
- set `PYTHONPATH=.`, `pawns.RACE_RULE="count"` and `pawns.PASSED_RESPECTS_EP=True`;
- call `pawns.value(pawns.Board(n, 8, True, True), pawns.Pos.parse(text))`;
- clear the caches between race rules (any function with `cache_clear`).

**REPORT.md:**
- a table of cylinder × pawns × split, with roots, \*2 count and \*k≥3 count in the default setting;
- the n+3 verdict for C6 and C7;
- the first \*3 on any cylinder, if any;
- labels: COMPUTED-1 for scan-only results, CHECKED-2 when cylcgt agrees;
- reproduce commands.
