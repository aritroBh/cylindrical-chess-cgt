# K32: reserves (λ, ρ) against Siegel's stops (LOOPY §8 open question 4(d))

**Output directory:** `kings/delegate/out/K32/` (create it). Write only there; your report goes in `FINDINGS.md`.
Do not edit any existing file. Do not run git.

## Background (read these)

- `kings/theory/LOOPY.md` §3 from Theorem 3.7 to Theorem 3.11 (the reserves λ and ρ, Theorem 3.8, Corollary 3.8b,
  Proposition 3.9) and §8 item 4. Open question 4(d) is the CONJECTURE (untested): for a terminal-free stopper S with
  finite reserve, λ(S) = ⌈−RS(S)⌉ or one more, where RS is the right stop. ρ is the mirror statement with the left stop.
- `kings/delegate/out/K21/` (`summary.json`, `VERIFY.md`, `scripts/sumsolve.c`, `scripts/dsum.py`, `verify/`): the
  K21 solvers that compute the reserves.
- Siegel, *Combinatorial Game Theory* (2013), chapter on loopy games and stoppers, for the stops of a stopper
  (KNOWN; cite the definitions you use).

## Task

1. Fix the definitions: λ and ρ as LOOPY defines them; the left and right stops of a stopper as in Siegel. Write both
   down precisely in `FINDINGS.md`.
2. Write code that computes the stops of a finite stopper given as a game graph, and the reserves λ, ρ (reuse K21's
   code, or write your own from LOOPY's definition; say which).
3. Test the conjecture on all terminal-free stoppers with at most N nodes, for the largest N that runs in 20 minutes
   (at least N = 4), and on the named games (on, off, over, under, and the finite-reserve stoppers in K21's
   examples). Tabulate λ against ⌈−RS⌉ and ρ against ⌈LS⌉.
4. Report a counterexample if one exists (smallest first), or the exact boundary of the verified range. Try to prove
   whichever relation holds. A proof needs every step written out.
5. Use two independent implementations for any count or counterexample you report (CHECKED-2), or label it
   COMPUTED-1.

## Output

`FINDINGS.md` (5-line summary; definitions; tables; exact commands), `EDITS.md` in the EDITS format (`### EDIT
<title>`, `<<<<<<< OLD`, `=======`, `>>>>>>> NEW`; each OLD copied from the current LOOPY.md, occurring exactly
once), `summary.json`.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Runs over about one CPU-minute go through `kings/delegate/heavy.sh` (nice 15).
Under 3 GB RSS and under 20 minutes per run. No file over 50 MB. No installs, no network. Never use pkill, killall,
`kill -- -1` or any pattern kill. Kill only PIDs you started and recorded in `pids.log`. Delete binaries and bulk
outputs at the end.
