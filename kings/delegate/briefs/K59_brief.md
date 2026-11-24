# K59: more groups with the results of over (cyl:8×7 twice checked; flat boards)

State: Lemma 4.15 of `kings/theory/LOOPY.md` (PROVED): an exact over group of Definition 4.8, as the P game of its own
pieces, has the results of over beside every finite D-game if (B1) holds: after every non-shuttle Black move at a root
the position (White to move, with the e.p. right after a double step) is a White win beside −1 under the sum's rule
(Black may once move elsewhere, not while in check; a side with no move loses). Corollary 4.16 applies it to the 2 + 3
group of cyl:10×6. Read Definition 4.8, Lemma 4.15, Corollary 4.16, `kings/delegate/out/K57/REVIEW.md`, `VERIFY.md`
and `kings/delegate/out/K48/findings.txt`, `REVIEW.md`.

Tools that exist: exactness of a named group from move values (`kings/delegate/out/K48/verify/scripts/def48.py` with
`ref3m` or `kp_p --pmodel`; board names need a colon: `cyl:8x7`, `pln:8x7`); (B1) under the sum's rule
(`kings/delegate/out/K57/verify/src/vgsum.cpp`, the K57 referee's program) and in the pass game
(`kings/delegate/out/K57/src/pr57.cpp`, the K57 investigator's); the exact-group searchers of K48
(`kings/delegate/out/K48/src/`, p45a and r48, cylinder and flat).

## Part 1: (B1) for the four cyl:8×7 groups with a second program

K48's four exact groups on cyl:8×7 (files a, b, e) meet (B1) by pr56/pr57 only. Run `vgsum` on each (measure memory on
one first; T3 has 14.3 million nodes). If both programs agree on every non-shuttle Black root move, (B1) is CHECKED-2
and Corollary 4.16 extends to those groups; say which.

## Part 2: a group with the results of over on a flat board

1. The cyl:8×7 groups have pawns on files a, b, e and kings near d to f. Test whether each of them, and each translate
   that fits, is exact on flat 8×7 (`pln:8x7`) from move values with two solvers, and then test (B1) with two programs.
2. Search more widely if step 1 fails or time allows: exact groups on flat 8×7 in the file classes of the known
   shapes with p45a and r48 (they must agree), then (B1) for every exact group found. Then flat 9×7 and flat 8×8 for
   the translates and tall versions only.
3. For every group that is exact and meets (B1) by two programs, run a direct sum check beside a few dozen small
   finite D-games (with terminals) against over, as the K57 referee did for H10.

Report each group as a piece list with both roots, the shuttle and the two freezes.

## Output (only inside `kings/delegate/out/K59/`)

`findings.txt` (labels: COMPUTED-1 one program, CHECKED-2 two independent programs that agree; the conclusion "has the
results of over beside every finite D-game" for a group is "PROVED given CHECKED-2 computations" only if both
Definition 4.8 and (B1) are CHECKED-2 for it), `EDITS.md` against `kings/theory/LOOPY.md` in the house format
(`### EDIT title`, `<<<<<<< OLD`, old, `=======`, new, `>>>>>>> NEW`; each OLD block occurs exactly once): Corollary
4.16's sentence on the cyl:8×7 groups, a new sentence or corollary for any flat-board group, the C4.7 status row, the
"To settle" line. `src/`, `logs/`, `pids.log`. xz outputs over 256 KB; delete binaries.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`. Record
  every PID you start in `pids.log` and stop only those.
- Run solvers through `kings/delegate/heavy.sh` (at most 2 heavy processes, nice 15). Design every run for under 2 GB:
  measure the smallest input first with `/usr/bin/time -l`; hard limit 3 GB. If a search cannot fit, do not run it;
  report the estimate instead.
- No git commands that change anything. Edit nothing outside `kings/delegate/out/K59/`.
- Plain, short English. No personal names or home-directory paths in any file.
