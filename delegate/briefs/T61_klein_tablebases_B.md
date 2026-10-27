# T61: independent second implementation — 4-man piece endgames on the Möbius strip, the Klein bottle and the projective plane

Output directory: `research/twisted_tablebases/B/`. Create it and write nothing anywhere else.

## Background

`tablebase/replica/replica.c` solves 3- and 4-man piece endings (K+pieces vs K) on an 8×8 board that is:
- a plane;
- a cylinder (files a and h glued);
- a torus (also ranks 1 and 8 glued).

Results are in `tablebase/replica/REPORT.md`. On the cylinder, KRK and KBNK are not forced wins, and opposite-coloured
bishops win 100%. On the torus only KRRK and KQRK win.

## Task

Write your OWN solver from the rules below, in any language. Do NOT read or copy `replica.c`, `egt_prototype.c` or `research/twisted_tablebases/A/`. Another agent writes a separate version, and the two will be compared. You may read `tablebase/replica/REPORT.md` for the numbers to validate against.

The coordinates are files f = 0..7 and ranks r = 0..7. A step that leaves the board:
- **mobius:** across the a/h edge, wraps the file (f → f mod 8) and flips the rank, r → 7 − r. The rank edges stay walls.
- **klein:** across the a/h edge, wraps the file and flips the rank (as in mobius). Across the rank edge it wraps the
  rank (r → r mod 8) with no flip.
- **rp2** (projective plane): across the a/h edge, wraps the file and flips the rank. Across the rank edge, wraps the
  rank and flips the file, f → 7 − f.

Sliders:
- They continue square by square through the gluings.
- They stop at the first occupied square.
- They must not pass the same square twice; a ray that returns to its start or loops stops.
- A king may not step onto a square adjacent to the other king. Adjacency is computed through the gluings.
- Check, checkmate and stalemate are defined as usual.

Symmetry: use only the symmetries that are true for each topology. If unsure, use none. Correctness matters more than
speed.

For each topology, compute KQK, KRK, KBBK (both bishop-colour cases, if colours are still well defined; say what
happens to square colours), KBNK, KNNK, KQRK, KRRK, KQQK, KRBK and KRNK. Report:
- the share of white-to-move positions that are won;
- the longest mate;
- whether the ending is a forced win from every legal position, or not.

Validate first: your plane/cyl/torus modes must reproduce `tablebase/replica/REPORT.md`'s numbers exactly, at least for KQK, KRK and KBNK.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID.
- At most 2 processes, each under `nice -n 15` and under 4 GB RSS.
- No git. Do not edit `paper/` or `tablebase/`.
- Write `REPORT.md`:
  - begin with a 5-line summary;
  - give a table of results per topology;
  - give the validation numbers and the exact commands.
