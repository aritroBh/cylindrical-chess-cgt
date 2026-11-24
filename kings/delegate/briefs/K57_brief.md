# K57: is the 2 + 3 group of cyl:10×6 equal to over? A two-sided argument or a checkable certificate

State after K55 and K56: the 2 + 3 group H10 = `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` (cyl:10×6) has the results of over
beside every test game tried (752 games in K55, 600 random D-games in K56). K56 proved a sufficient criterion
(tempo-exact, `kings/delegate/out/K56/PROOF.md`) that H10 fails on White's side only: five White root moves are saved
in the one-sided pass game by one White pass (Kg4–f3 at both roots, e2–e4 at the f6 root, e2–e3 at the g6 root) or by
unlimited passes (Kg4–g3 at the g6 root). The gap named in PROOF.md section 5 is Black's unlimited budget after a bad
White move.

## Goal

Prove or refute: r(H10 ⊞ T) = r(over ⊞ T) for every finite D-game T, both roots, both sides to move. A proof that
needs a finite computed certificate is acceptable if a general lemma, proved by hand, says the certificate suffices
and the certificate is checked by a second program.

## Ideas to weigh (none is checked)

1. The one-sided pass game is too pessimistic: in a sum a White pass is a move in T, which changes T and gives Black a
   reply there. Describe r(over ⊞ t) directly: Black may always wait, and White may at any of its turns cash in, leaving
   t with Black to move. A White tempo in t that over cannot already use may not exist: check whether "White has a
   useful spare move in t" already makes over ⊞ t a White win, and build the comparison on that.
2. Matched passes: test the pass game in which every White pass gives Black one pass to use later (budgets w = b), and
   other relative budgets. Find the weakest condition H10 meets on White's side and try to prove it sufficient.
3. A simulation certificate: a relation between positions of H10's game and positions of a small model game (over, 0,
   "lost for White", "lost for Black", with tempo counters if needed) such that each side's strategy transfers in both
   directions beside any T. Prove the transfer lemma in general, compute the relation for H10, check it by program.
4. If H10 is not equal to over, the proof attempt should show where: build the test game T from the failing case and
   run it (the random batteries may simply not contain it).

## Output (only inside `kings/delegate/out/K57/`)

`findings.txt`, `PROOF.md` (complete, every case; PROVED only if complete, otherwise CONJECTURE with the gap named),
`EDITS.md` against `kings/theory/LOOPY.md` in the house format, `src/`, `logs/`, `pids.log`. xz outputs over 256 KB;
delete binaries.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`. Record
  every PID you start in `pids.log` and stop only those.
- Run solvers through `kings/delegate/heavy.sh` (at most 2 heavy processes, nice 15). Design every run for under 2 GB:
  measure the smallest input first with `/usr/bin/time -l`; the hard limit is 3 GB.
- A referee is checking K56 in `kings/delegate/out/K56/verify/`; do not touch its files or processes.
- No git commands that change anything. Edit nothing outside `kings/delegate/out/K57/`.
- Plain, short English. No personal names or home-directory paths in any file.
