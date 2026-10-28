# K28: decide the five open chess deviations of Z_B (flat 7×6)

**Output directory:** `kings/delegate/out/K28/` (create it). Write only there; your report goes in `FINDINGS.md`.
Do not edit any existing file. Do not run git.

## Background (read these)

- `kings/theory/LOOPY.md` §5.7, the bullet "An exactly frozen two-shuttle group: Z_B". Find it with `grep -n "exactly
  frozen two-shuttle group: Z_B" kings/theory/LOOPY.md`. Read it down to the K14 search bullet: the roots, the move
  lists, the P proof, and the chess split.
- `kings/delegate/out/K27/VERIFY.md` §5 and §6, `kings/delegate/out/K27/REVIEW.md`, and
  `kings/delegate/out/K27/logs/run2/` and `logs/integrator/` (the cap-1 results).
- `kings/SPEC.md` and `kings/kpsolve.c`: the header, the `--cap` semantics, and the bounds A and B.
- The K27 referee's independent chess solver is `kings/delegate/out/K27/verify/ownchess.cpp`. Its argument 0 gives
  bound A and 1 gives bound B; it has no double step.

Z_B is exactly two-shuttle in P (PROVED). In chess, 21 of its 26 non-shuttle moves lose (CHECKED-2). The other five are
not settled at cap 1. Each line below gives the deviation, its child, and the cap-1 bounds (A, B) from White's view, with
A ≥ true value ≥ B:

| # | deviation | child (side to move) | cap 1 |
|---|---|---|---|
| 1 | c4–c3 from Kb2/ka4 | `Kb2 Pa3 Pb4 ka4 pb3 pc3 w -` | (W, L) |
| 2 | a3–a4 from Kc3/kb5 | `Kc3 Pa4 Pb4 kb5 pb3 pc4 b -` | (W, L) |
| 3 | Kc3xc4 from Kc3/ka4 | `Kc4 Pa3 Pb4 ka4 pb3 b -` | (W, L) |
| 4 | Ka4xa3 from Kc3/ka4 | `Kc3 Pb4 ka3 pb3 pc4 w -` | (W, L) |
| 5 | Kc3–d2 from Kc3/kb5 | `Kd2 Pa3 Pb4 kb5 pb3 pc4 b -` | (D, L) |

Z_B is exactly two-shuttle in chess if and only if each of the five loses for the side that played it. That means
rows 1, 3 and 5 are Black wins (true value L) and rows 2 and 4 are White wins (W).

## Task

1. Find the true chess value of each child, or the tightest bounds you can, with the evidence.
2. You choose the method. Some options:
   - Run kpsolve at `--cap 2` (or higher), one child per run. Start with the 3-pawn rows 3 and 4.
   - Use a decomposition. The cap-1 bounds differ only where a second promotion happens. Solve the positions just after
     the first promotion exactly (they have fewer pawns), and back the values up.
   - Use chess knowledge to prove the value of the decisive post-promotion positions. Examples: K+Q against K+P on
     7×6, or a queen won at once by a skewer or a capture. Back that up with exact small solves.
   - Find a hand line. For row 5, either a White drawing plan after Kd2, or a forced Black win that ends in a position
     whose value is computed.
3. Any value you claim as decided needs two independent checks: two solvers that agree, or a hand proof plus one
   solver. Use `ownchess`, or a solver you write from SPEC.md, as the second implementation. If you extend ownchess or
   kpsolve, say exactly how and test the change on positions with known values.
4. In `FINDINGS.md`, give:
   - a 5-line summary;
   - a table: row, value or bounds, method, label (PROVED / CHECKED-2 / COMPUTED-1 / open);
   - the verdict: is Z_B exactly two-shuttle in chess, not, or still open;
   - every command needed to reproduce your results;
   - proposed LOOPY edits in `EDITS.md`. Use the EDITS format of earlier items: `### EDIT <title>`, `<<<<<<< OLD`,
     `=======`, `>>>>>>> NEW`. Each OLD text must be copied from the current LOOPY.md and occur exactly once.

## Rules

`delegate/COMMON.md`, rules 5 and 7. In addition:
- Run every solver through `kings/delegate/heavy.sh`, and at most 2 heavy processes at once.
- Use nice 15. Guard each run with `kings/delegate/out/K27/scripts/watch2.sh` (copy it into your directory) at 3 GB RSS
  (3000000 KB) and at most 90 minutes of wall time.
- If a run would need more than 3 GB, stop and report the estimate. Do not run it.
- No file over 50 MB. No installs, no network.
- Never use pkill, killall, `kill -- -1` or any pattern kill. Kill only PIDs you started and recorded, and write them
  to `pids.log`.
- At the end, delete your binaries and bulk outputs. Keep the scripts, logs and summaries.
