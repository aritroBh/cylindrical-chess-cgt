# K67: the other two file classes of the known shape on flat 8×8, and a search for a ladder longer than 3

Investigator brief, 2026-11-25. Output in `kings/delegate/out/K67/`.

## Background (read these)

`kings/theory/LOOPY.md`: Definition 4.8, Lemma 4.15, Corollary 4.17, Theorem 4.18, Corollary 4.19, Theorem 4.20,
Corollary 4.23. `kings/delegate/briefs/K65_brief.md`, `kings/delegate/out/K65/findings.txt` (sections 0 to 4: the
search programs, counters, timing, and the memory breach to avoid), `kings/delegate/out/K65/verify/VERIFY.md` (the
classification of the 38 groups; the referee's programs ax65 and pk_sum in `verify/src/`, small and fast).

Known after K65. On flat 8×8 (ranks 2 to 7, at most 3 + 3 pawns, every king placement) the classes {b,c,f} and
{b,e,f} hold 23 and 25 exact over groups, 38 distinct. 27 have (B1); 7 have the results of ω without (B1); 4 fail
condition (C) at one bad move, three with N\* = 2 and one with N\* = 3. Five of the 19 groups with at most seven men
are exact over groups in chess by the tablebase. Not searched: {a,b,e} and {a,d,e} (with these the four reflection
classes of the shape {f, f+1, f+4} are complete), the two-file classes not inside a searched class, other shapes.

## Questions

1. **Census.** Search {a,b,e} and {a,d,e} on flat 8×8 with p45a (copies of K65's programs inside your folder;
   0.71 h and 1.3 GB a class measured there), then with r48 (3.7 h and about 1.0 GB a class). Report every exact over
   group as in K65 (roots, shuttle, freezes, q's, men), the counters of both programs, and the union with K65's 38:
   how many distinct groups in the four classes, how many up to reflection and file translation, how many per number
   of men. Before the long runs repeat one K65 counter as a regression (the {b,c,f} hit count 23 with p45a is
   enough if it fits the budget; otherwise the flat 8×7 {b,c,f} count: 785,481,597 placements, 3 exact).
2. **Classification of every new group.** Definition 4.8 again (ref3m and `kp_p` through def48.py, as K65), then
   with ax65 and pk_sum: (B1) at every bad Black root move; Aux at every failing move; where Aux is lost, the values
   of x_m ⊞ u_0 (White to move) and of the root (Black to move) beside T_0, T_1, … until the first non-win, so N\*.
   A group with N\* ≥ 4 answers an open question: report it at once with full detail.
3. **Chess.** For every new group with at most seven men: is it an exact over group in chess? Use the reading and
   the script of K65's referee (`verify/src/tb65.py`; copy it) through `realchess/probe.py` with your own cache and
   ledger inside your folder, cap 150 requests; nothing written in `realchess/`. Reuse cached answers of K65 where a
   position repeats.
4. **If time remains:** the two-file classes of flat 8×8 not contained in a searched three-file class (list them up
   to reflection first, with p45a's measured time for one), cheapest first, same reporting.

## Budget and rules

- Time: about ten hours of solver time in all; p45a on both classes first, classification of its hits next, r48
  last. Write `findings.txt` as you go, so that an interrupted run still leaves a usable report.
- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: every run over a minute goes through `kings/delegate/heavy.sh <cmd>` (at most two heavy processes at once
  across all agents, nice 15; other agents use it too, so expect to wait) under `/usr/bin/time -l`. Every solver
  sizes its arrays before allocating and exits if they would pass 2 GB. Every run has a watchdog on the solver's
  own recorded PID that polls at least five times a second and kills at 2.0 GB. After any watchdog kill the whole
  chain stops and you report. No chain of runs without the watchdog. Do NOT run vgsum59 or pr57 on eight-man groups
  (they passed 3 GB in K65); ax65 and pk_sum do that work in under 0.2 GB.
- Runs over 2 minutes: background, and wait for them before reporting.
- Write only inside `kings/delegate/out/K67/`. No git commands that change anything. Do not touch `paper/`, `dist/`,
  `cylcgt/`, `realchess/`, `delegate/` or other `kings/delegate/out/` directories (read them freely). No downloads;
  network only for the tablebase lookups of item 3.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.
- Labels: KNOWN (tablebase), CHECKED-2 (two separately written programs agree), COMPUTED-1. No hand proofs asked for.

## Deliverables

- `findings.txt`: the short answer first (the census of the four classes as a table a paper could quote, the
  classification, the chess verdicts), then the search table with counters for both programs, then what was not
  searched or checked.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
- `EDITS.md` for `kings/theory/LOOPY.md` in the format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`. The K65 census paragraph is not installed in the note yet: write your edit as replacement sentences
  for the text of `kings/delegate/out/K65/verify/EDITS.md` (OLD taken from its NEW text), at most eight lines, marked
  "not yet refereed". No new numbered statement unless a group with N\* ≥ 4 is found.
