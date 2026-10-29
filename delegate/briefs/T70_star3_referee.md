# T70: referee report on PROOF_S3T3.md (a ring *3 with n+1 pawns on every C_n, n >= 12)

Output: `research/star3_check/REPORT.md` (create the directory). Write nothing anywhere else.

Read `research/star3_proof/PROOF_S3T3.md` and the files it cites. You refereed the same kind of proof three times
(`research/ring_n_plus_2_check/REPORT.md`, `.../Q/`, `.../odd/REPORT.md`). Your solver `research/ring_n_plus_2_check/odd/independent.py`
may be reused or adapted.

## What to do

1. **Verify each hypothesis H1-H7 by hand.** Pay particular attention to:
   - the two ends of the Lemma-3 arc and their windows;
   - the choice of n0 and c, for both families;
   - T_n (wall B4 W2 from file 0) and S_n (wall W2 B4 from file 3, after B4 B6 W3);
   - the meaning of *3 (signature NNNPNN) and the zone of S_n reaching into the wall.
2. **Recompute the finite checks with your own code** (not myeng.py, rg or cylcgt):
   - the base reduced graphs at n0 (nodes, zone, no flag, no passer, signature h = 0..5);
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
