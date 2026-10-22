# T22b: finish the independent 7-pawn census (T22 lost its hits)

**Output directory:** `research/star2_seven_check/`. Add new files. Leave the old ones as they are.

**What happened in T22.**
- `enumerate_fast.py` finished widths 1–3: width 3 had 1,470,576 positions and 0 hits.
- It got through about 3.65M positions of width 4 and found 1 \*k (k ≥ 2). Then the agent's session ended and
  the process died.
- Hits were kept only in memory, so the hit is lost.
- The checkpoint files hold only markers, so the run cannot be resumed.

**Task.** Write `census7.py`, a fresh enumerator. You may reuse the position generator and the evaluation from
`enumerate_fast.py`, because those are T22's own code. Do NOT read `research/star2_frontier/frontier.c` or
`nimscan.c`.

1. **Scope** (unchanged from T22):
   - flat widths 1–4, 8 ranks, exactly 7 pawns, all on ranks 2–7, at least one pawn per side;
   - both edge files occupied;
   - no passed pawn at the root under the e.p.-aware test;
   - one of each mirror pair;
   - `cylcgt` with `RACE_RULE = "count"`, `PASSED_RESPECTS_EP = True`, `Board(w, 8, False, True)`.
2. **Chunks.**
   - Split each width into numbered chunks with a deterministic rule, for example the rank of the white
     pawn set modulo K. Choose K so that each chunk takes under 30 minutes.
   - Run one chunk per process invocation: `census7.py --width W --chunk k --of K`. Run at most 3 at a time.
   - A chunk that already has its `done` line is skipped on rerun.
3. **Write as you go.**
   - Append each hit immediately, flushed, to `census7/w{W}_c{k}.hits.tsv`: position, k, value string.
   - When a chunk finishes, write `census7/w{W}_c{k}.done` with these counts:
     - positions generated;
     - positions with a passed pawn at the root, skipped;
     - positions evaluated;
     - `RaceError` count;
     - every other exception count, with the first 3 tracebacks.
   - Never swallow an exception silently.
4. **Memory.** Keep the `cylcgt` cache between positions in a chunk. If the process RSS passes 4 GB, call
   `pawns._value.cache_clear()`. The machine is short of memory: another job holds 26 GB.
5. **Sanity check before the full run.**
   - Evaluate `W: a4 b3 d2 d3 / B: a7 b7 c5` and `W: b4 c2 d2 / B: a6 a7 c6 d5` directly. Both must print
     `*2`.
   - Confirm that the generator yields each of them, or its mirror image.
   - If either check fails, fix that first.
6. **Merge.** Write `merge7.py`. It checks that every chunk is done and that the per-width counts add up, then
   writes `census7/summary.json`.

**Report** (`REPORT.md`, rewrite it):
- the root count per width;
- the full list of \*k hits;
- whether it is exactly the two positions above, with the differences if not;
- labels and reproduce commands.

A result of "0 hits" without the sanity check passing is not acceptable.
