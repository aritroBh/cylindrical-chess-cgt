# K8: does stalemate explain when spare tempo matters? Predictions and a rule switch

**Output directory:** `kings/delegate/out/K8/` (create it). Write only there; never modify K4/ or K6/.

## Background (read first)

- `kings/delegate/out/K4/REPORT.md` §1 and §4 and `kings/delegate/out/K6/REPORT.md` give the setup.
  - K+P vs K is summed with 16 test games, under normal play: a side with no move in the sum loses, so a
    stalemate is a loss, and infinite play is a draw.
  - A quiet placement is **tempo-sensitive** if its (White starts, Black starts) result is not constant
    over the 11 finite test games and over x ⊞ n for n = −10 … 10.
- **K6 finding (CHECKED-2).** Cylinders with 3 or 5–8 files are tempo-insensitive. 4-file cylinders and every
  flat board are sensitive.
- **K6 conjecture.** A board has tempo-sensitive placements exactly when White can be stalemated in front of
  its own pawn, that is, when the off/off+\* class is non-empty.
- **Mechanism suggested.** Under normal play a stalemate is a loss, so Black can win tempo battles that run
  White out of moves.

## Task 1: prediction tests (normal play, as in K6)

Copy K6's pipeline into `kings/delegate/out/K8/` and run the copies there: `graph.py`, `testgames.py`,
`product.py`, `checks.py`, `check1.py`, `gafni.py`, `tempo_scan.py`, `tempo_detail.py`, `run_all.sh`,
`runlim.py`, `summarize.py`, and whatever they import. Build kpsolve with
`nice -n 10 cc -O2 -o kings/delegate/out/K8/kp kings/kpsolve.c`, and make sure `check1.py` uses that binary.

Boards, smallest first. For each, first record whether the off/off+\* class is non-empty, which is the
conjecture's prediction, then the tempo-sensitive count.
- `cyl:5x4`, `cyl:3x7`, `cyl:5x7`, `cyl:3x8`: predicted insensitive.
- `cyl:4x7`, `cyl:4x8`, `flat:4x6`, `flat:3x7`: predicted sensitive.
- If time allows: `cyl:2x6` and `cyl:2x8`, the 2-file cylinder (no prediction; report what happens),
  and `cyl:6x7`.

Check 1 (against kpsolve) and check 2 must pass on every board, as in K4.

## Task 2: the same scan under the chess stalemate rule

Add a variant to your copy of the product solver; leave the original behaviour as the default.
- **Chess stalemate rule:** a side with no legal move in the whole sum that is **not** in check draws. One that
  is in check, which is checkmate, loses as before.
- Everything else is unchanged: in-check rule for test-game moves, infinite play a draw.
- Test the variant first. With T = 0 it must equal kpsolve on every K+P vs K position, which is K4's check 1.

Under this rule, run the tempo scan (11 finite test games and n = −10 … 10) on these boards:
- `flat:3x4`, `flat:4x4`, `cyl:4x4`, `cyl:4x6`, `flat:5x6`;
- the K6-insensitive cylinders `cyl:3x6`, `cyl:5x6`, `cyl:6x5`, `cyl:7x5`.

Report per board the number of tempo-sensitive placements, the thresholds and examples.

**Cross-check with mutual zugzwangs.** kpsolve gives the chess result with each side to move. A **mutual
zugzwang** is a placement where the side to move does worse than if the other side moved: for example, White
to move draws and Black to move loses.
- Count mutual zugzwangs per board from kpsolve.
- Compare them with the placements that are tempo-sensitive at n = ±1 under the chess rule.
- Explain any placement that is in one set but not the other. Concretely, check whether every mutual zugzwang is
  sensitive to one spare move, and whether every sensitive placement is a zugzwang.
- Background: `research/odd_cylinders_verify/REPORT.md` says `Ka3 Pa2 ka5` is a mutual zugzwang on every
  cylinder.

## Deliverables

- `REPORT.md`, starting with a 5-line summary. Then:
  - a table per task, with board, off class empty or non-empty, tempo-sensitive count, thresholds, and kpsolve
    check;
  - for each prediction: confirmed or refuted;
  - the chess-rule results and the zugzwang comparison;
  - a statement of what the data say about the mechanism.

  Label everything COMPUTED-1, since this is one implementation; a separate verifier will re-check it.
- `run.sh` with the exact commands, `summary.json`, and per-board `tempo_detail_<board>.json`.
- Keep the per-placement `.jsonl` files. Gzip the kpsolve inputs and outputs under `check1/`.

## Limits (rule 7 of `delegate/COMMON.md`)

- One heavy process at a time, under `nice -n 10`, under 3 GB RSS. `runlim.py` enforces this for your own jobs.
- At most 20 minutes per board, and at most 2 hours in total.
- No file over 50 MB. No git, no installs, no network.
- Never kill or signal a process you did not start.
