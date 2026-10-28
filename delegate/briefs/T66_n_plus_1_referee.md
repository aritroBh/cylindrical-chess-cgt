# T66: referee report on PROOF_N.md (a ring *2 with exactly n pawns on every C_n, n >= 10)

Output: `research/ring_n_check/REPORT.md` (create the directory). Write nothing anywhere else.

Read `research/ring_n_proof/PROOF_N.md` and the files it cites. You refereed the same kind of proof three times
(`research/ring_n_plus_2_check/REPORT.md`, `.../Q/`, `.../odd/REPORT.md`). Your solver `research/ring_n_plus_2_check/odd/independent.py`
may be reused or adapted.

## What to do

1. **Verify each hypothesis H1-H7 by hand.** Pay particular attention to:
   - the two ends of the Lemma-3 arc and their windows;
   - the choice of n0 and c, for both families;
   - M_n, whose wall starts at file 0 (B4) beside file n-1 (W5);
   - O_n, whose wall (B7 W5) is the colour mirror of W2/B4: check how Lemma 2 is transferred to it.
2. **Recompute the finite checks with your own code** (not myeng.py, rg or cylcgt):
   - the base reduced graphs at n0 (nodes, zone, no flag, no passer, signature);
   - the insertion isomorphism over two steps;
   - the base cases below n0 by direct search.
3. **Write REPORT.md.** Start with a 5-line verdict (SOUND / SOUND WITH FIXES / GAP), then go through it item by item.
   Label claims PROVED, CHECKED-2 or COMPUTED-1.

## Rules

- Follow `delegate/COMMON.md`.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Record the PID of every process you start and stop
  only those, by PID. Other projects share this machine.
- At most 2 processes, each under 4 GB RSS. Use `nice -n 15`; if the sandbox refuses it, run one process at a time
  without it.
- No git. Do not edit `paper/` or any other directory.
