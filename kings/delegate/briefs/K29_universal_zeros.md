# K29: universal zeros in P (LOOPY §8 open question 6)

**Output directory:** `kings/delegate/out/K29/` (create it). Write only there; your report goes in `FINDINGS.md`.
Do not edit any existing file. Do not run git.

## Background (read these)

- `kings/theory/LOOPY.md`: §8 item 6; the status rows P2.10(b) and P2.10; Proposition 2.10 and its proof; the K23
  block that defines Z_T, G1 = {Pe3, pe4}, G2 = {Pe2, pe3}, Φ and Ψ (find it with `grep -n "Z_T = " kings/theory/LOOPY.md`).
- `kings/delegate/out/K23/`: `FINDINGS.md` or `summary.json`, `scripts/` (`gen_ctx.py`, `classify.py`, `pk2.c`,
  `reproduce.sh`) and `verify/` (`ref3.cpp`, `ref3m.cpp`, `gen.py`, `analyze.py`).
- `kings/SPEC.md` for the P model and the position syntax.

Z_T is a frozen group with T ≥ 2 whose zero is context-dependent in P (P13, CHECKED-2). The question is whether
**some** frozen group with T ≥ 2 acts as 0 beside every context.

## Task

1. Make "acts as 0 beside H" exact, as K23 did: the P outcome pair of Z + H equals the P outcome pair of H with the
   group replaced by parked kings (K23's Φ = Ψ test). Say which parking you use and why it is neutral.
2. Build a candidate list of frozen groups with T ≥ 2 on cyl:7×6, cyl:8×6 and flat 7×6 or 8×6. Include Z_T's
   relatives: the sortie king further from the buffer, longer buffers, and groups whose sortie cannot reach the
   context files before the punisher's T-move win. Explain how you enumerate them, with the exact boundary.
3. For each candidate, solve it against every context of at most 2 pawns a side on the files outside F_Z and its
   buffer (or the largest complete set that fits, with the exact boundary). Use kp_p `--pmodel` (K7 build), and check
   every claimed universal zero, and a sample of the failures, with ref3 or ref3m.
4. Report one of:
   - a universal zero within the stated context class, with its full table (CHECKED-2 if two solvers agree on
     every context); or
   - the failing context for each candidate, with the mechanism in a sentence where you can find it.
   Either is a valid result. "None found" needs the exact search boundary.
5. If you find a mechanism that forces failure (for example, the sortie king always reaches the buffer in time),
   state it as a CONJECTURE or prove it. A proof needs every step written out.

## Output

`FINDINGS.md` (5-line summary first; a table of candidates × outcome; exact commands), `EDITS.md` in the EDITS format
(`### EDIT <title>`, `<<<<<<< OLD`, `=======`, `>>>>>>> NEW`; each OLD copied from the current LOOPY.md, occurring
exactly once), `summary.json`.

## Rules

`delegate/COMMON.md`, rules 5 and 7. Every solver run goes through `kings/delegate/heavy.sh` (2 heavy processes
across all kings/ jobs, nice 15). Under 3 GB RSS and under 20 minutes per run. No file over 50 MB. No installs, no
network. Never use pkill, killall, `kill -- -1` or any pattern kill. Kill only PIDs you started and recorded in
`pids.log`. Delete binaries and bulk outputs at the end.
