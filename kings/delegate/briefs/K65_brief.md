# K65: a census of exact over groups on the ordinary 8×8 board, and a search for a ladder longer than 2

Investigator brief, 2026-11-24. Exhaustive searches with two programs, then classification of every hit. Output in
`kings/delegate/out/K65/`.

## Background (read these)

`kings/theory/LOOPY.md`: Definition 4.8, Lemma 4.15, Corollaries 4.16 and 4.17, Theorem 4.18, Corollary 4.19,
Theorem 4.20, Corollary 4.23 and the paragraph on Z_O (N\* = 2). `kings/delegate/out/K59/findings.txt` §3 with
`search_table.txt` (the flat 8×7 search: programs p45a and r48, counters, hits), `kings/delegate/out/K59/REVIEW.md`,
`kings/delegate/out/K59/verify/VERIFY.md`. For the classification: `kings/delegate/out/K60/` (condition (C), the Aux
game, ladders; `verify/src/r60lib.py`), `kings/delegate/out/K62/verify/` (the referee's solver for ladder lengths).

What is known. On flat 8×7 the file classes {f, f+1, f+4} hold five exact over groups (F1 to F5), all with (B1).
F1 to F4 are also exact with (B1) on flat 8×8 when placed as on 8×7 (K59, CHECKED-2), but flat 8×8 was never
searched. Z_O, the 3 + 3 group of cyl:8×6, is the only real group known to fail (C); its ladder length N\* is 2.
No real group with N\* ≥ 3 is known.

## Questions

1. **Census on flat 8×8.** Which exact over groups (Definition 4.8) exist on the flat 8×8 board with pawns on at most
   three files, at most 3 + 3 pawns, pawn ranks 2 to 7, every king placement? Black pawns have a double step from
   rank 7 only, White pawns from rank 2 only, as in chess. Order of work, stop when the time budget below is spent and
   say exactly which classes were and were not searched:
   a. the four classes of the known shape, {a,b,e}, {a,d,e}, {b,c,f}, {b,e,f} and their translates that fit on eight
      files (state the reflection classes);
   b. every class of two files (up to left-right reflection);
   c. the remaining classes of three files, cheapest first.
   Report each hit as a position a reader can set up (both roots, shuttle, freezes, q's), grouped up to reflection
   and file translation, with the number of men.
2. **Classification of every hit.** (B1) at every non-shuttle Black root move (vgsum59 and pr57, as in K59). Where
   (B1) fails: condition (C) for each bad move (Theorem 4.18), and if (C) holds, the smallest N with White winning the
   ladder T_N as in Theorem 4.20, so the group's N\*. A real group with N\* ≥ 3 would answer an open question of the
   note: report it at once with full detail, and check it twice.
3. **Near misses worth a line.** How many placements pass every clause of Definition 4.8 except one, by clause (the
   counters of K59 already give part of this). No analysis beyond the counts.

## Checks

- Two programs for every search class: p45a and r48 (copies inside your folder). Any change you make to a program
  (board size, rank range, the double-step rule on rank 7) must be regression-tested first: reproduce K59's flat 8×7
  counters for the class {b,c,f} exactly (785,481,597 placements, 3 exact over groups) with both programs. Then
  check that on flat 8×8 both programs find F2 placed as in K59.
- Every hit: Definition 4.8 again with ref3m and `kp_p --pmodel` through `def48.py` (K59's copies), so CHECKED-2.
- Labels: COMPUTED-1 or CHECKED-2 for each table. No hand proofs asked for.

## Budget and rules

- Time: about six hours of solver time in all. Measure one class first (time and peak memory under
  `/usr/bin/time -l`) and give your plan with estimates in `findings.txt` before the long runs.
- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: every run goes through `kings/delegate/heavy.sh <cmd>` (at most two heavy processes at once across all
  agents, nice 15; another agent is using it too, so expect to wait) under `/usr/bin/time -l`, with a watchdog of
  your own that kills that recorded PID if its RSS passes 2.2 GB. Start no chain of runs without the watchdog, even
  if the first inputs measured small. Nothing may pass 3 GB: if a class cannot be searched inside the budget, do not
  start it; report the measured size.
- Runs over 2 minutes: background, and wait for them before reporting.
- Write only inside `kings/delegate/out/K65/`. No git commands that change anything. Do not touch `paper/`, `dist/`,
  `cylcgt/`, `realchess/`, `delegate/` or other `kings/delegate/out/` directories (read them freely). No network,
  no downloads.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.

## Deliverables

- `findings.txt`: the short answer first (the census as a table a paper could quote, then the classification), then
  the search table with counters for both programs, then what was not searched or checked.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
- `EDITS.md` for `kings/theory/LOOPY.md` in the format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy. Do not edit LOOPY.md itself.
  At most ten lines of the note, appended to Corollary 4.17's paragraph (another item is editing the sentence that
  starts "Has the results of over beside every finite D-game": do not use it as your OLD text; anchor on a different
  sentence). No new numbered statement unless a group with N\* ≥ 3 is found. Mark everything "not yet refereed".
