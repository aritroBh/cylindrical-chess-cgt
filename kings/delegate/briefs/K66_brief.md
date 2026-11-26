# K66: independent check of the K65 referee's own findings

Checker brief, 2026-11-25. Output in `kings/delegate/out/K66/`.

## Why

K65's referee did more than referee: with two programs it wrote itself (ax65, pk_sum) it found (i) a real exact over
group with ladder length N\* = 3, (ii) seven real groups with the results of ω although (B1) fails, (iii) five
seven-man groups that are exact over groups in chess by the tablebase. Two programs by one author are a weak
CHECKED-2, and (i) is to become a numbered statement. You are the independent check.

## Read

`kings/theory/LOOPY.md`: Definition 4.8, Lemma 4.15, Theorem 4.18 with its Aux game and ladders T_N, Corollary 4.19,
Theorem 4.20, Corollary 4.23 and the remark after it. `kings/delegate/out/K65/verify/VERIFY.md` and
`kings/delegate/out/K65/verify/EDITS.md` (the claims). `kings/delegate/briefs/K61_over_test_blind.md` §1 (the sum's
rules in one place). Do NOT read `kings/delegate/out/K65/verify/src/ax65.cpp`, `pk_sum.cpp`, or the K65 logs of
their results before your own numbers exist: write your own solver from the note's definitions (flat 8×8, promotion
game P, kings and pawns, e.p., check rule, the sum's rule for moves elsewhere). You may use any language; the state
spaces are small (the referee reports under 0.2 GB).

## Check

1. **Your solver first.** Validate on F2 = `Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6` (exact; (B1) at all nine bad Black root
   moves) and on C125_14 = `Kb5 kd5/kd6 Pb6 Pc2 Pf5 pb7 pc5 pf6` (claimed: (B1) fails only at …Kd5–d4, Aux lost
   there, x_m ⊞ u_0 W beside T_0, T_1 and lost beside T_2).
2. **N\* = 3.** G = C125_15 = `Kg5 ke5/ke6 Pb2 Pf2 Pf6 pc4 pf5 pf7` (Black shuttles e5–e6; freezes f2–f3 at e5,
   f2–f4 at e6). Claimed: exact (every clause of Definition 4.8); eleven bad Black root moves; (B1) fails at
   …Ke5–d4, …Ke5–e4, …Ke5–d6, …f5–f4 (e5 root), …Ke6–d6; Aux lost only at …Ke5–e4 and won at the other four
   failures; at …Ke5–e4, x_m ⊞ u_0 with White to move is W beside T_0, T_1, T_2 and D beside T_3 (and not W for
   T_4 to T_6); the e5 root with Black to move is W beside u_0 of T_2 and D beside u_0 of T_3. Confirm or refute each
   value. Then give a line of play a reader can follow: how White wins beside T_2 and how Black holds the draw
   beside T_3 (principal variation from your solver, with the reason in a sentence or two).
3. **Seven groups without (B1).** For C125_09, C125_13, C125_22, C125_23, C145_16, C145_24, C145_25 (positions in
   VERIFY.md table 2): exactness, the list of bad moves where (B1) fails, and Aux won at each of them.
4. **The other two N\* = 2 groups**, C125_16 and C145_19: the failing move, Aux lost, W beside T_0, T_1, not W
   beside T_2.
5. **Chess.** Table 3 of VERIFY.md says five seven-man groups are exact over groups in chess. Write your own
   evaluation of Definition 4.8 with chess values from the tablebase answers (the referee's cache is in
   `kings/delegate/out/K65/verify/logs/tbcache.tar.xz`; unpack a copy inside your folder, read offline). State
   exactly which clauses "exact in chess" means, whether that reading is fair to Definition 4.8 (note the remark on
   C125_01 and C125_02), and give the verdict for all 15 groups the referee probed. Spot-check at most 25 cached
   answers with fresh lookups through `realchess/probe.py` (`Prober`, your own cache and ledger inside
   `kings/delegate/out/K66/`, cap 25; nothing written in `realchess/`). For each of the five YES groups give the FEN
   of both roots and both q's.
6. Does the referee's EDITS.md say anything the checks do not support? List each sentence that needs a change, with
   the corrected sentence.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: size every array before allocating and exit if it would pass 2 GB. Any run over a minute goes through
  `kings/delegate/heavy.sh <cmd>` under `/usr/bin/time -l` (at most two heavy processes at once across all agents;
  others are using it, so expect to wait), with a watchdog on the solver's own recorded PID that polls at least five
  times a second and kills at 2.0 GB. After any watchdog kill stop the whole chain and report. No chain of runs
  without the watchdog.
- Runs over 2 minutes: background, and wait for them before reporting.
- Write only inside `kings/delegate/out/K66/`. No git commands that change anything. Do not touch `paper/`, `dist/`,
  `cylcgt/`, `realchess/`, `delegate/` or other `kings/delegate/out/` directories (read them as allowed above).
  No downloads; network only for the tablebase lookups above.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.
- Labels: KNOWN (tablebase), CHECKED-2, COMPUTED-1. A computed fact is never PROVED.

## Deliverables

- `VERIFY.md`: verdict first, then one table row per claim (confirmed / refuted / corrected, your value, your
  program), the two lines of play of item 2, the chess table, what was not checked.
- `EDITS.md` only if a sentence of the referee's EDITS.md must change: same format (`### EDIT title`,
  `<<<<<<< OLD`, `=======`, `>>>>>>> NEW`), OLD text taken from the referee's NEW text.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
