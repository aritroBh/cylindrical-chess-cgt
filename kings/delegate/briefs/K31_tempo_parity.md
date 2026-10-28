# K31: the parity of finite king tempi, and two-tempo leads (LOOPY §8 open question 3, the K20 conjectures)

**Output directory:** `kings/delegate/out/K31/` (create it). Write only there; your report goes in `FINDINGS.md`.
Do not edit any existing file. Do not run git.

## Background (read these)

- `kings/theory/LOOPY.md` §8 item 3 (K20): the local game LK, the batteries B34 and B4553, "A finite tempo exists",
  and three CONJECTUREs:
  - (C1) the parity: single blocked pairs give roots of value +1 and −1 on cylinders of even width (6, 8, 10 with
    six ranks) and none on odd widths (5, 7, 9 with six ranks). The conjecture is that this holds for other heights
    and widths.
  - (C2) the tempo is a one-tempo race lead between two kings that reply inside Z, not a reservoir.
  - (C3) a lead of two tempi is already decisive, which would explain why ±2 and ±3 never occur.
- `kings/delegate/out/K20/` (`summary.json`, `VERIFY.md`, `REVIEW.md`, `scripts/kg.cpp`, `verify/` with the
  referee's `lk.cpp`).

## Task

1. (C1) Run K20's `kg.cpp` and the referee's `lk.cpp` on single-pair configurations of cylinders with widths 5..12
   and heights 5..8, as far as fits in 3 GB and 20 minutes per run. Tabulate the number of +1 and −1 roots per
   (width, height, pawn rank). Report whether parity of the width decides existence, or what does. Two solvers must
   agree for CHECKED-2.
2. If a pattern holds, try to prove it: for example a colouring or distance argument for even width. A proof needs
   every step. Otherwise state the observed rule as a CONJECTURE with the exact boundary.
3. (C3) Test "two tempi are decisive": for each ±1 root found, test the sum of two copies, and of a root with the
   integer 1 from the battery. Check whether the sum is decisive (a forced event) in LK. Explain why ±2 cannot occur
   as a single root if you can prove it; otherwise report the evidence.
4. (C2) Optional: give one concrete line showing the race-lead mechanism for the flat:6×6 +1 root
   `Kc3 ka4 Pa2 pa3 Pc4 pc5`, checked against the solver.

## Output

`FINDINGS.md` (5-line summary; tables; exact commands), `EDITS.md` in the EDITS format (`### EDIT <title>`,
`<<<<<<< OLD`, `=======`, `>>>>>>> NEW`; each OLD copied from the current LOOPY.md, occurring exactly once),
`summary.json`.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Every solver run over about one CPU-minute goes through
`kings/delegate/heavy.sh` (nice 15). Under 3 GB RSS (check a small case first) and under 20 minutes per run. No file
over 50 MB. No installs, no network. Never use pkill, killall, `kill -- -1` or any pattern kill. Kill only PIDs you
started and recorded in `pids.log`. Delete binaries and bulk outputs at the end.
