# T72: draw-aware model with loopy values (research avenue 7)

Output directory: `research/draw_model/` (create it). Write nothing anywhere else.

## Task: Draw-aware model with loopy values → `research/draw_model/`
- **Goal:** replace the three ad-hoc draw treatments with a principled one.
- **Question:** score draws three ways: (i) as 0, (ii) as dud, (iii) as {on|off}, assigned by which side can shuttle (Thm 3.4). Which treatment best reproduces the 13 real-draw nodes, the 3 draw terminals, the 6 proven drawing king moves, and the drawing king moves in the suite? Does it pin the A2 oracle value to a single value?
- **Method:**
  1. Collect the draws from `realchess/results/comp_Wa2c2_Bb7d7_*` and from `engine/suite/results.json`.
  2. Run `kpsolve --moves` on each draw to read off the shuttle structure.
  3. Write a scratch scorer, with `realchess/oracle_value.py` as the base, using loopy sum rules from LOOPY T3.7/T3.8.
  4. For the K4 K+P-vs-K placements, cluster the (onside, offside) pairs.
- **Success:** the reproduction rate of each treatment, and either a single oracle value under (iii) or a proof that (iii) is ill-defined there.
- **Read first:** `kings/theory/LOOPY.md` (Thm 3.4, T3.7, T3.8), `kings/delegate/out/K4`, `realchess/oracle_value.py`, `realchess/REPORT.md` (the draw-treatment section).
- **Agent:** an external CLI agent (OpenCode or Kilo) writing the loopy scorer independently. A Claude agent supplies the data.


## Rules

- Follow `delegate/COMMON.md`. Write your own scorer; read existing code only for data formats.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under 4 GB RSS, under `nice -n 15`. Check memory of one kpsolve run before more.
- No git. Do not edit `kings/`, `realchess/`, `paper/` or any file outside `research/draw_model/`.
- Finish with `research/draw_model/REPORT.md`: 5-line summary, then method, results table, and labels
  (PROVED / CHECKED-2 / COMPUTED-1). Do not overclaim.
