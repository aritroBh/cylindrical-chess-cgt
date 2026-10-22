# K2: non-Claude referee of the A8 report

**Output directory:** `kings/delegate/out/K2/` (create it). Write only there.

## Inputs

You are refereeing `kings/REPORT.md`. Every claim and table in it was produced by Claude models. You are
the first non-Claude reviewer. Check its numbers and claims against the raw files it cites:
- `kings/results/*.jsonl` and `*_summary.json`: the sweeps;
- `kings/results/crosscheck.txt`;
- `kings/results/lichess_check_2-4_cap1.txt`;
- `kings/results/king_groups_8x8.txt`;
- `kings/results/king_groups_lichess.txt`;
- `kings/results/PREDICTIONS.md`;
- `kings/results/FAILURES.md`;
- `kings/results/*_diagnosis.jsonl`;
- `kings/theory/REVIEWS.md`;
- `kings/data/DATA.md`.

## Task

1. **Recompute every number in the report from the raw files**, with your own short scripts kept in your
   output directory. Report each number as confirmed or wrong.
2. **Re-run four checks yourself.** Build the solver with
   `cc -O2 -o kings/delegate/out/K2/kp kings/kpsolve.c`, then run:
   - a cross-check: copy `kings/crosscheck.py` into your output directory, change its two output paths to
     point there, and run the copy with `--board cyl:4x4 --material KPK KPKP --cap 1 --kpsolve kings/delegate/out/K2/kp`
     from the project root (it runs the reference solver `kings.ref.solve` too). Quote its summary line;
   - the 8×8 king groups:
     `kings/delegate/out/K2/kp --board cyl:8x8 --cap 1 < kings/positions/king_groups_8x8.txt`;
   - three positions of your choice from `kings/results/FAILURES.md` §1, solved with `--moves`. Check by
     reasoning that the "real best moves" make sense.
3. **Write an independent mini-solver** in Python (stdlib only), from `kings/SPEC.md` alone, without reading
   `kings/kpsolve.c` or `kings/ref/`. It needs to handle only kings and at most 2 pawns, on boards up to 5×5,
   with promotion scored as a win for the promoter unless the new queen can be captured at once.
   - Use it to check the "frozen" versus "real" distinction on the 6 positions of `FAILURES.md` §1 for the
     6×6 cylinder, if your solver can reach that size. Otherwise check 20 random 4×5 cylinder positions
     against `kp`, run with `--promote Q --cap 1`.
   - State exactly what you compared and where the models differ.
4. **Flag overclaims:** any claim whose label (PROVED / CHECKED-2 / COMPUTED-1 / INFERENCE) is stronger than
   its evidence.

## Deliverable

`kings/delegate/out/K2/REPORT.md`:
- a 5-line summary;
- a table of every checked number (confirmed or wrong);
- your re-run results;
- the mini-solver comparison;
- the overclaims, most severe first.

Be blunt.
