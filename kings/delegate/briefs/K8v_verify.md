# K8v: independent check of K8

**Output directory:** `kings/delegate/out/K8v/` (create it). Write only there.

K8 (`kings/delegate/out/K8/REPORT.md`; read it first) ran two things:
- the K4/K6 tempo scan on new boards, under normal play;
- the same scan under a chess stalemate rule (a stalemated side draws, a checkmated side loses), compared with
  kpsolve's mutual zugzwangs.

You re-check it **without reading K8's code**. Do not open any `.py` or `.sh` file in `kings/delegate/out/K8/`.
You may read its `REPORT.md`, `summary.json`, `.jsonl` and `tempo_detail_*.json`.

## How

1. Copy the independent verifier pipeline from `kings/delegate/out/K6/verify/` into
   `kings/delegate/out/K8v/`. It has its own move generator `v_gen.py`, its own test games `v_games.py` and its
   own C solver `v_prod.c`. Read its scripts and `run_verify6.sh` to see how it runs.
2. Run it on every normal-play board K8 reports, and compare per placement: the quiet set, signatures, classes,
   and tempo sensitivity (the 11 finite tests and x ⊞ n for n = −10 … 10).
3. **Chess stalemate rule.** Add that rule to your copy of `v_prod.c` yourself, from this description: a side
   with no legal move in the sum that is not in check draws; one in check loses; infinite play draws.
   - With T = 0 it must match kpsolve on every K+P vs K position. Build kpsolve with
     `nice -n 10 cc -O2 -o kings/delegate/out/K8v/kp kings/kpsolve.c`.
   - Then redo K8's chess-rule tempo scan and its mutual-zugzwang comparison, and compare the counts and
     placements.
4. **Report** placements compared and differences per board, and whether each K8 conclusion follows from your
   numbers.

## Deliverables

`REPORT.md`, starting with a 5-line summary, plus a per-board table and the exact commands. Label agreement
CHECKED-2.

## Limits

Rule 7 of `delegate/COMMON.md`:
- one heavy process at a time, under `nice -n 10`, under 3 GB RSS;
- at most 20 minutes per board;
- no file over 50 MB, no git, no installs, no network;
- never kill or signal a process you did not start.

Delete your own intermediate `work/` files when you are done.
