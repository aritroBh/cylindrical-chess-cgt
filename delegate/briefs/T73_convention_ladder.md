# T73: smallest counterexample per convention (research avenue 2)

Output directory: `research/convention_ladder/` (create it). Write nothing anywhere else.

## Task: Smallest counterexample per convention → `research/convention_ladder/`
- **Goal:** a minimal-counterexample table showing each of (V1)-(V4) is necessary.
- **Question:** for each convention, find the position with fewest men on the smallest board where toggling only that convention flips the real result. The conventions are: C1 passer wins at once; C2 race rule (count / mover / opponent); C3 e.p.-aware test; C4 frozen kings; C5 stalemate = loss. Is the answer the same on flat and on cylinder?
- **Method:**
  1. Enumerate by increasing man count (2-6 pawns plus the trebuchet) on cyl:4x4, cyl:5x5, flat:4x5 and flat:5x5.
  2. For each position compute the cylcgt class under 3 race rules × e.p. on/off, plus `kpsolve --frozen` and plain kpsolve, all at cap 2, Q and QRBN.
  3. Record the first instance per category.
  4. Seed the search with the failure lists in `kings/results/FAILURES.md` and `exp_cyl7x6_epon_Q_conv.jsonl`.
  5. Re-verify every minimal example with `kings/ref/solve.py`.
- **Success:** a table with one row per convention: the minimal position (FEN), board, man count, model value, real value, and confirmation from the second solver. Report it even if some minima coincide with lemma L4.
- **Read first:** `kings/results/FAILURES.md`, `kings/conventions.py`, `kings/ref/solve.py`, `kings/theory/LOOPY.md`.
- **Agent:** an external CLI agent (Codex) writing the enumerator independently. A Claude agent then cross-checks it with kings/ref.


## Rules
- Follow `delegate/COMMON.md`. Write your own enumerator; read existing code only for formats and for calling kpsolve.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under 4 GB RSS, under `nice -n 15`; measure one kpsolve run's memory first.
- No git. Do not edit `kings/`, `cylcgt/`, `paper/` or any file outside `research/convention_ladder/`.
- Finish with `research/convention_ladder/REPORT.md`: 5-line summary, the minimal-counterexample table, method, labels.
