# T75: a complete proof of the square rule S (certified passers) in the frozen-king pawn game

Output: `research/v2_mechanisms_proof/PROOF_S.md` (create the directory). Write nothing anywhere else.

Read `research/v2_mechanisms/REPORT.md` (rule S and its sketch, around lines 100-135) and the referee report
`research/v2_mechanisms_check/REPORT.md`, which lists the missing steps (e.p. after the passer moves, d as a lower bound
when Y's pawns are blocked, double steps, captures, the cylinder wrap, who moves first).

Write a complete hand proof: definitions (frozen-king pawn game, passed pawn under the e.p.-aware test, n, d), the
statement, and a proof that covers every case the referee lists, step by step, with no gaps. If the statement needs a
correction (for example a precise definition of d), state the corrected version and prove that. Keep it under about 150
lines. Label the result PROVED (by hand) only if every step is argued; otherwise say exactly what remains.

## Rules
- Follow `delegate/COMMON.md`. You may run `research/v2_mechanisms/cc.py` read-only to test a claim (nice -n 15).
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Other projects share this machine.
- No git. Edit nothing outside the output directory.
