# T24: the \*3 hunt and the cylinder minimum for \*2 (deeper scans with T21's C scanner)

**Output directory:** `research/star3_hunt/`. Create it.

**Background.**
- Under the paper's main convention (count race rule, e.p.-aware test, e.p. on), \*2 first appears with 7 pawns
  on flat boards of width ≤ 4.
- On the flat 5-file board with 8 pawns, T21 found 21 positions of value \*2 and no \*3 (14,680,983 roots,
  `research/star2_width5/summary.txt`).
- Under the opponent race rule, \*3 does appear.
- Nobody has looked for a \*3 under count or mover beyond 8 pawns.

**Tool.**
- Use `research/star2_width5/frontier_split` (source `frontier_split.c`, flags `--width`, `--min`, `--max`, `--nw`,
  `--nb`, `--flat`/`--cylinder`, `--pilot`) and `run_all.sh` as a template.
- Copy the binary and the script into your directory. Do not edit T21's files.
- Run every job under `nice -n 10`, at most 3 processes at once, each under 40 minutes. Split by (nw, nb), as
  `run_all.sh` does.

**Scans**, in order. Pilot each one first (`--pilot`) and estimate its runtime. Skip any scan estimated at over 6
CPU-hours, and say so.
1. Flat width 4 with 8 pawns, and flat width 4 with 9 pawns.
2. Flat width 5 with 9 pawns.
3. Flat width 6 with 7 and 8 pawns.
4. Cylinder rings (every file occupied):
   - C3 with 6–8 pawns;
   - C4 with 6–8 pawns;
   - C5 with 7–9 pawns;
   - C6 with 7–8 pawns.

**Report, for each scan and each of the 9 settings:**
- the root count;
- the number of \*2 positions;
- the number of \*k positions with k ≥ 3;
- the largest nimber seen.

**Verification** (`cylcgt` with `Board(w, 8, wrap, ep)`, and `RACE_RULE` and `PASSED_RESPECTS_EP` per setting):
- every \*k hit with k ≥ 3 under count or mover;
- the hits that set a new minimum: the fewest pawns for \*2 on each cylinder Cn under count / e.p.-aware, with
  all of them listed;
- a random 20 of the other \*2 hits.

For each \*3 under count or mover, also run `verify_ext/codex/solver.py` (`PawnGame(w, race, ep, test)`, whole
board).

**Deliverable** (`REPORT.md`):
- the scan table;
- the questions answered:
  - Is there a \*3 under count / e.p.-aware in any scope?
  - What is the fewest number of pawns for \*2 on C3, C4, C5 and C6 at count / e.p.-aware?
- labels and reproduce commands.
