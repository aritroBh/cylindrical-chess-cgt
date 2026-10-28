# K30: a hand proof that White cannot win in 7.2 (LOOPY §8 open question 7)

**Output directory:** `kings/delegate/out/K30/` (create it). Write only there; your report goes in `FINDINGS.md`.
Do not edit any existing file. Do not run git.

## Background (read these)

- `kings/theory/LOOPY.md`: §8 item 7; §5.2 (Position 7.2, `Ke6 Pd7 kd8 pe7`, frozen for Black only); the status
  rows P6, P7 and L2.7a; Lemma 2.7a (the transfer from the promotion models EPW and EPB to chess); Lemma 2.9; the P7
  row of the §6 prediction table.
- `kings/delegate/out/K24/` (`summary.json`, `VERIFY.md`, `scripts/mine.c`, `verify/psolve.py`, `logs/`), and
  `kings/delegate/out/K19/` for the P-model solves.
- `kings/SPEC.md` for P, EPW and EPB.

P7 w (White to move in `Ke6 Pd7 kd8 pe7`) is D in P and in chess on cyl:8×8 and flat:8×8, CHECKED-2 by computation
only. Ke5, Kd5 and Kf5 draw; Kf7 loses (T = 11 with the queen clause, 10 without).

## Task

1. Write a hand proof that White cannot force a win from P7 w, in P and on both boards. The proof must show:
   - after each of Ke5, Kd5, Kf5, Black has a drawing strategy against every White play (no forced White promotion,
     no forced mate), for instance an explicit blockade strategy with an invariant;
   - every other White move loses or is illegal, and Kf7 loses (give the forcing line).
   State the strategy as a finite rule ("Black keeps the king on {…} and plays … when …"), and prove that it keeps
   the invariant against every White move.
2. Check the strategy mechanically. Write a checker that plays Black's rule against every White reply in the
   reachable state space (P model, both boards) and confirms that White never wins and Black never needs a move the
   rule does not give. Report the number of states checked. Use your own move generator written from SPEC.md, and
   compare its P values on the reachable states with `kp_p --pmodel` (K7 build) or K24's `mine.c`.
3. If the proof also covers chess through Lemma 2.7a (EPW and EPB), say so, and check the EPW and EPB parts the same
   way.
4. Label: PROVED only if every step is written out and the mechanical check passes; otherwise say exactly which step
   is missing.

## Output

`FINDINGS.md` (5-line summary; the proof; the checker's results; exact commands), `PROOF.md` if the proof is long,
`EDITS.md` in the EDITS format (`### EDIT <title>`, `<<<<<<< OLD`, `=======`, `>>>>>>> NEW`; each OLD copied from the
current LOOPY.md, occurring exactly once), `summary.json`.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Every solver run over about one CPU-minute goes through
`kings/delegate/heavy.sh` (nice 15). Under 3 GB RSS and under 20 minutes per run. No file over 50 MB. No installs,
no network. Never use pkill, killall, `kill -- -1` or any pattern kill. Kill only PIDs you started and recorded in
`pids.log`. Delete binaries and bulk outputs at the end.
