# K55: do the other exact groups equal over in sums, and what is the value of Z_O?

Read first: `kings/delegate/out/K47/REVIEW.md`, `findings.txt`, `VERIFY.md` (K47: the cyl:8×6 group Z_O of K45 is exact in
the sense of Definition 4.8 but not equal to over in D-sums), `kings/delegate/out/K45/findings.txt` (the list of exact
groups), and in `kings/theory/LOOPY.md` Definitions 1.2, 1.3, 1.5, 4.8, Section 3 (the order on loopy D-games, Theorems
3.7 to 3.11) and the K45 and K47 bullets of Conjecture 4.7. K47's code is in `kings/delegate/out/K47/src/` (za.cpp,
zb.cpp) and `kings/delegate/out/K47/verify/rz.cpp`; reuse it, with the same model reading (the group is the P game of
its own pieces, its moves are real moves, K40's convention).

## Part 1: the other exact groups

K45 found ten exact groups on cyl:8×6, 9×6 and 10×6, among them the 2 + 3 group `Kg4 kf6 Pb3 Pe2 pa5 pb4 pe5` on
cyl:10×6, and the same pawn group as Z_O on wider boards. For each over-type group that is not a colour mirror of
another, run K47's comparison: r(G ⊞ T) against r(over ⊞ T) for the 275 test games, both roots, both sides to move.
Use two of the three existing solvers and require agreement.
Question: does any of them agree with over on the whole battery? List the differences per group.

## Part 2: the value of Z_O

K47's referee found that on the 275 tests the d4 root has the results of tiny-2 = {0 ‖ 0 | −2} (also of tiny-3, tiny-4)
and the d5 root those of ⇑\* = {0 | ↑\*} + \* (a signature, not a value).
1. Enlarge the battery so that it separates the candidates: add tiny-n and miny-n (n = 1…4), ⇑, ⇑\*, ↑², ↑\*, switches
   {n | −n} and {n | 0}, {0 | −n}, and sums of three atoms from a reduced atom list. Report which candidates survive.
2. Test order relations directly, in the sense LOOPY Section 3 uses for loopy games: for each surviving candidate H
   decide G ≥ H and G ≤ H through the sum G ⊞ (−H) (second player survives), once with draws counted for Left and once
   for Right. State exactly which definition you used and quote its place in LOOPY.
3. Is Z_O a stopper (no infinite alternating play from any reachable position)? If not, say what that means for step 2.
4. If a candidate passes every test, say so with the label COMPUTED-1 and say plainly that a finite battery and an order
   test against one game do not prove equality unless Section 3 gives a theorem that does; if it does, name it.

## Output (only inside `kings/delegate/out/K55/`)

- `findings.txt`: results per part, each with a label (COMPUTED-1 for one program, CHECKED-2 for two that agree; never
  PROVED for a solver result), and what was not done.
- `EDITS.md` against `kings/theory/LOOPY.md` in the house format (`### EDIT title`, `<<<<<<< OLD`, old text, `=======`,
  new text, `>>>>>>> NEW`; every OLD block must occur exactly once in the file): a short addition to the K47 bullet or a
  new K55 bullet, and the "To settle" line. Keep table rows' cell counts.
- `src/`, `logs/`, `pids.log`. xz any output over 256 KB. Delete compiled binaries at the end.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`. Record
  the PID of everything you start in `pids.log` and stop only those.
- Run every solver through `kings/delegate/heavy.sh` (at most 2 heavy processes, nice 15). Each process must stay under
  3 GB of memory: measure one position with `/usr/bin/time -l` before any batch, and cap batches. Do not run ref3m
  batches on cyl:10×6 (it reached 4.75 GB in K47); use `kp_p --pmodel` under a cap there.
- Another agent (K48) is running solvers in `kings/delegate/out/K48/`; do not touch its files or processes.
- No git commands that change anything. Edit nothing outside `kings/delegate/out/K55/`.
- Plain, short English in every file. No personal names or home-directory paths in any file.
