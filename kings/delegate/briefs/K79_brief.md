# K79: the clean pairs beside every pawn placement on the file: a second program, and why the kings stay

Investigator brief, 2026-11-26. Output in `kings/delegate/out/K79/`.

## Background (read these)

`kings/theory/LOOPY.md`: Definitions 1.3, 2.1, 4.8, Lemma 4.15, Corollary 4.17, Theorem 4.18, Proposition 4.25 and
the paragraphs "K72" and "K75" after it. `kings/delegate/out/K75/REVIEW.md`, `kings/delegate/out/K75/verify/VERIFY.md`
(the table of clean pairs, how p74 was run in parts, the hand comparison), `kings/delegate/out/K72/verify/VERIFY.md`.
Programs: `kings/delegate/out/K75/src/` (pk.cpp, ref3m.cpp with memory guards, gen.py, the predictors),
`kings/delegate/out/K75/verify/src/` (p74.c, mk76.py, run scripts).

Known. In the promotion game P on flat 8×8, six (group, file) pairs have the result that ω predicts beside ALL 729
placements of pawns on the context file (ranks 2–7, each square empty, White or Black), at both roots and both
q's, either side to move (5,832 positions a pair): C014_01 `Ka5 kc4/kc5 Pa4 Pa6 Pb2 pa7` on h, C145_13
`Ka5 kc5/kc6 Pb2 Pe5 Pe6 pb7 pe7` on h, C145_17 on h, C145_20 on h, C125_21 on h, C125_20 on a. This rests on one
program (p74), so it is COMPUTED-1. Four more pairs are clean at 2 + 2 by p74 only: C125_17 h, C125_18 h,
C014_06 g, C014_06 h.

## Questions

1. **Second program.** Solve the same positions with pk or ref3m (separately written from p74), splitting the
   729 placements into parts that fit in 2 GB (pk and ref3m need about 8 KB a configuration; measure). Order: the
   six all-729 pairs, six-man and seven-man groups first; then the four 2 + 2 pairs. Compare position by position
   with p74's values (rerun p74 yourself where its outputs are not kept per position). Report for each pair:
   positions compared, disagreements, and the label the statement now deserves.
2. **3 + 3 for the four eight-man pairs that stopped at 2 + 2** (C125_17 h, C125_18 h, C014_06 g, C014_06 h), with
   p74 in parts, only if the budget allows after item 1 (the referee estimated 1.8 h a pair): at least one pair.
3. **Why the kings stay (hand work, for C014_01 on h first, then C145_13 on h).** State and try to prove by hand a
   pinning lemma of this kind: in the group alone, after any king move that is not the shuttle (Black) or any
   king move at all (White), the other side wins by a named plan within a stated number of moves, and this plan
   needs no move that a context on file h could disturb and is faster than any gain the wandering king can make on
   file h (count the tempi: the king needs at least four moves to reach the g-file). Then say exactly what would
   still be missing for a proof of "C014_01 has the results of ω beside every pawn context on file h" (for example:
   the roots' values beside contexts where a context pawn promotes within three moves are settled by the D-sum
   already; which case is not?). Label every statement PROVED (complete hand proof in the text), PROVED given
   CHECKED-2 facts (name them), or COMPUTED. A partial result with honest labels is what is wanted; do not close
   a branch with "the solver confirms" under a PROVED label.
4. **A statement a paper could quote** for the best pair, with its label, of the form: "beside every placement of
   pawns on file h (729 placements; both roots and both freeze positions, either side to move), the position has
   the result that ω predicts."

## Budget and rules

- Time: about five hours of solver time. Write `findings.txt` as you go.
- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: every solver sizes its arrays before allocating and exits if they would pass 2 GB. Measure the smallest
  input of each kind first with `/usr/bin/time -l` (both size and time). A run measured under 30 seconds and under
  0.6 GB may be started directly, one at a time. Every other run goes through `kings/delegate/heavy.sh <cmd>` under
  `/usr/bin/time -l`, ONE slot only (another agent has the other), a few seconds between chained runs, with a
  watchdog on the solver's own recorded PID that polls at least five times a second and kills at 2.0 GB. After any
  watchdog kill the whole chain stops and you report. No chain of runs without the watchdog. Do NOT run vgsum59,
  pr57 or ref3pv.
- Runs over 2 minutes: background, and wait for them before reporting. Do not hand back while a run of yours is
  still going, and do not stop a run in order to hand back.
- Write only inside `kings/delegate/out/K79/` (temporary files in a `tmp/` there, deleted at the end). No git
  commands that change anything. Do not touch `paper/`, `dist/`, `cylcgt/`, `realchess/`, `delegate/` or other
  `kings/delegate/out/` directories (read them freely). No network, no downloads.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.
- Labels: CHECKED-2 (two separately written programs agree; say which), COMPUTED-1, PROVED only for a complete
  hand proof. A computed fact is never PROVED.

## Deliverables

- `findings.txt`: the short answer first (the table of pairs with positions compared, disagreements, label; the
  quotable sentence), then the pinning lemma with its proof or its gaps, then what was not done.
- `PROOF.md` if item 3 gives anything with a PROVED label.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
- `EDITS.md` for `kings/theory/LOOPY.md` (format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit LOOPY.md):
  change only the labels and the sentence about the clean pairs in the paragraph "K75", at most four lines changed,
  marked "not yet refereed".
