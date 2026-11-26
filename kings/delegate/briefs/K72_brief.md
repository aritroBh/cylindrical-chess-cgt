# K72: the chess-exact over groups beside real pawns on the same board (promotion game P)

Investigator brief, 2026-11-25. Output in `kings/delegate/out/K72/`.

## Background (read these)

`kings/theory/LOOPY.md`: Definitions 1.1, 1.3, 2.1 (groups, buffer files, contexts), Definition 4.8, Lemma 4.15,
Corollary 4.17 with its K63 and K65 paragraphs, Proposition 4.25. `kings/delegate/out/K63/REVIEW.md`,
`kings/delegate/out/K63/verify/VERIFY.md` (how the P contexts of F2 were set up, solved and compared with the
D-sum prediction; which programs; the memory breach to avoid). `kings/delegate/out/K65/verify/VERIFY.md` table 3
and `kings/delegate/out/K66/VERIFY.md` §4 (the five groups that are exact over groups in chess).

Known. The results of ω are proved for D-sums: the other components are abstract finite D-games. For the 2 + 2
group F2 with real pawns on file h of the same board (the kings can walk there) the P result equals the D-sum
prediction in 271 of 283 contexts; the 12 failures have a blocked White pawn on h2 that the Black king wins.
F2 is not exact in chess. Not tested: the five seven-man groups that are exact in chess, which are more rigid:

- C125_05 `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6`
- C125_08 `Ke5 kc5/kc6 Pb2 Pb6 Pf6 pb7 pf7`
- C125_10 `Kc5 ke5/ke6 Pb6 Pf2 Pf6 pb7 pf7`
- C145_07 `Kg4 ke4/ke5 Pe6 Pf2 Pf5 pe7 pf6`
- C145_09 `Kd4 kf4/kf5 Pe2 Pe5 Pf6 pe6 pf7`

## Questions

1. **Contexts on the same board.** For each of the five groups, put context pawns on files that are free and
   separated from the group's files by at least one empty buffer file (Definition 2.1; say for each group which
   files qualify, and treat the rim file and the far side separately). Contexts: every legal placement of at most
   1 + 1 pawns on one context file, then at most 2 + 2 on one file if memory allows (K63's breach came from two
   context files; do not use two). For each context X: the D-value or at least the D-outcome class of X alone (as
   K63 did), the prediction "G has the results of ω beside X" for both roots and both sides to move, and the P
   result of the whole position. Report: number of contexts, number where every result equals the prediction, and
   every failure with its mechanism in one sentence (which king walks where and wins what).
2. **Is rigidity enough?** Compare with F2's 271 of 283. If a group has no failure, say so plainly and say what
   was and was not covered; if it has failures, are they of the same kind as F2's (a blocked rim pawn within reach
   of the shuttling king) or new?
3. **A statement a paper could quote.** For the best group: one sentence of the form "beside every context of at
   most a + b pawns on file(s) …, the result is the one that ω predicts", with the count, or the smallest
   counterexample as a diagram in text.
4. **Second program.** Every count is CHECKED-2 only if two separately written programs agree on the P values
   (K63 used three; copy what you need into your folder). Otherwise label COMPUTED-1.

No chess (the positions have nine or more men; out of the tablebase's reach). No hand proofs asked for.

## Budget and rules

- Time: about three hours of solver time. Write `findings.txt` as you go.
- The machine is loaded (two long searches are running). Measure the smallest input first with `/usr/bin/time -l`.
  Every run over a minute goes through `kings/delegate/heavy.sh <cmd>` (at most two heavy processes at once
  across all agents; both slots are in use now, so expect to wait, possibly an hour) under `/usr/bin/time -l`.
- Memory: every solver sizes its arrays before allocating and exits if they would pass 2 GB. Every run over a
  minute has a watchdog on the solver's own recorded PID that polls at least five times a second and kills at
  2.0 GB. After any watchdog kill the whole chain stops and you report. No chain of runs without the watchdog. Do
  NOT run vgsum59 or pr57 on positions of eight or more men.
- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Runs over 2 minutes: background, and wait for them before reporting. Do not hand back while a run of yours is
  still going.
- Write only inside `kings/delegate/out/K72/`. No git commands that change anything. Do not touch `paper/`,
  `dist/`, `cylcgt/`, `realchess/`, `delegate/` or other `kings/delegate/out/` directories (read them freely).
  No network, no downloads.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.
- Labels: CHECKED-2 (two separately written programs agree), COMPUTED-1. A computed fact is never PROVED.

## Deliverables

- `findings.txt`: the short answer first (a table: group, context files, contexts, agreeing, failing), then the
  failures with mechanisms, then what was not covered.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
- `EDITS.md` for `kings/theory/LOOPY.md` (format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit LOOPY.md):
  at most six lines added to Corollary 4.17's paragraph or after Proposition 4.25, marked "not yet refereed".
