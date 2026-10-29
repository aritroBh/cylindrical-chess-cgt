# T74: logic referee of the certified-passer test (square rule S)

Output: `research/v2_mechanisms_check/REPORT.md` (create the directory). Write nothing anywhere else. Keep it under
about 120 lines, written in one go at the end.

Read `research/v2_mechanisms/REPORT.md`, especially the rule S and its proof sketch (around lines 100-135), and the code
`research/v2_mechanisms/cc.py` and `pawngame.py`. Game: the frozen-king pawn game on a cylinder or flat board (kings never
move; a king move loses; the first passed pawn decides, unless it is not certified), e.p. on, e.p.-aware passed test.

S: a passed pawn of X at distance n ends the game for X if n <= d when X is to move, or n < d when Y is to move, where
d is the unobstructed promotion distance of Y's fastest pawn.

Check by hand:
1. Is the sketch's argument complete? Can the passer be blocked, captured (including e.p.) or outrun? Can Y's pawn be
   faster than its "unobstructed distance" (double step, captures that shorten the path, promotion with check, a Y pawn
   that becomes passed by capturing)? Is the definition of d precise (which Y pawns, blocked or not, double steps)?
2. Does the claim depend on the cylinder (wrap-around captures) or on the board height?
3. What exactly is NOT claimed (real chess with active kings)? Is the REPORT clear about it?
4. Give a counterexample if the rule is false, or the missing step if the proof is incomplete.

Start with a 5-line verdict: SOUND / SOUND WITH FIXES / FALSE. Label claims PROVED / CHECKED-2 / COMPUTED-1.

## Rules
- Follow `delegate/COMMON.md`. Do not write a solver.
- Never run `pkill`, `killall`, `kill -- -1` or `kill $(pgrep ...)`. Other projects share this machine.
- No git. Edit nothing outside the output directory.
