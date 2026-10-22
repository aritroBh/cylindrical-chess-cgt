# T23: KPKP and KPPK on the 8×8 cylinder vs the plane

**Output directory:** `research/kpkp/`.

**Background.**
- KPK is done and checked twice (RESULTS.md §2; `delegate/checks/kpk_crosscheck.py`).
- A previous attempt at KPKP timed out because it fed positions in small batches. kpsolve solves the whole
  space once per run, so feed **all** positions in **one** run.

**Task.**
1. Enumerate every legal KPKP position (White K+P vs Black K+P), and separately every KPPK position, on
   flat:8x8 and cyl:8x8. Legal means:
   - no pawn on rank 1 or 8;
   - kings not adjacent (with wrap on the cylinder);
   - the side not to move not in check;
   - e.p. square `-`.
   Copy the enumeration style of `delegate/checks/kpk_crosscheck.py`.
2. Solve with `kings/kpsolve --board <b> --ep on --promote QRBN --cap 1 --threads 2`.
   - Bounds A ≠ B mean a capped second promotion. Report how many there are, then rerun those with `--cap 2`.
3. Report, flat vs cylinder:
   - win / draw / loss rates by side to move;
   - how many results flip;
   - mutual zugzwangs;
   - three instructive positions, with FENs.
4. Spot-check 20 flat positions against Lichess through `realchess/probe.py`, using the cache.

**Deliverable:** REPORT.md, with labels and reproduce commands.
