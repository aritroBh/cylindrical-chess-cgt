# K75: which over groups keep the results of ω beside real pawns? A distance rule for the kings

Investigator brief, 2026-11-25. Output in `kings/delegate/out/K75/`.

## Background (read these)

`kings/theory/LOOPY.md`: Definitions 1.1, 1.3, 2.1, Definition 4.8, Lemma 4.15, Corollary 4.17 (K63 and K65
paragraphs), Theorem 4.18. `kings/delegate/briefs/K72_brief.md` and `kings/delegate/out/K72/findings.txt` (the same
experiment for five groups; its programs in `kings/delegate/out/K72/src/`, inputs in `in.tar.xz`; a referee is
checking it now, so treat its numbers as COMPUTED and say where yours differ).
`kings/delegate/out/K65/verify/VERIFY.md` (the 38 groups of the classes {b,c,f}, {b,e,f} on flat 8×8, with roots,
shuttle, freezes, q's and their class: (B1), no (B1) but Aux won, Aux lost) and `kings/delegate/out/K67/findings.txt`
with `kings/delegate/out/K67/in/groups_new.txt` (10 more groups from {a,b,e}, {a,d,e}; their search is confirmed by
one program so far: mark them provisional).

Known after K72 (unrefereed). In P, beside real pawns on one separated file of the same 8×8 board, only one of five
seven-man groups (C125_10, White king c5, context file h) had the predicted result in all 283 contexts of at most
2 + 2 pawns. The other four fail already with 1 + 1 pawns. Every failure had pawns of both colours on the context
file. Two kinds: the shuttling Black king leaves and wins a White context pawn; or the White king leaves, wins a
Black context pawn and the q stops being a mutual zugzwang. The investigator's guess: the kind follows the king
that is near the context file, and a group is safe when both kings are far.

## Questions

1. **Screen all 48 groups.** For every group of the two lists and every context file that Definition 2.1 allows
   (one file, at distance ≥ 2 from F_Z, buffer files empty): all contexts of at most 1 + 1 pawns on that file (43
   contexts, 8 positions each: both roots and both q's, either side to move), P result against the prediction
   (r(ω ⊞ X) at the roots, r(X) at the q's, as K72; for a group without (B1) say what the prediction is and use
   the proved statement only: Theorem 4.18 where Aux is won, the ladder bound where Aux is lost). Table: group,
   men, class, context file, distance from the file to the White king and to each shuttle square of the Black
   king (in files), agree/fail counts, kind of each failure.
2. **Every pair with no failure at 1 + 1:** run at most 2 + 2 (283 contexts) if the tables fit in 2 GB (measure;
   K72's seven-man groups took 0.9 to 1.05 GB; eight-man groups may not fit: then report the largest context size
   that fits).
3. **A rule.** Find the simplest condition on the group and the file that separates the pairs with no failure from
   the others: for example in terms of the two king distances, of whose pawns stand on the file, of a count of
   tempi (king moves to reach a context pawn against moves the other side needs to promote or to punish the
   absence). State it as a CONJECTURE with the exact table that supports it, and list every pair that violates a
   simpler candidate rule. Also test K72's observation on all pairs: does every failing context have pawns of both
   colours?
4. **A statement a paper could quote:** how many of the 48 groups have at least one context file where all tested
   contexts agree, and the best three (most contexts, largest tested size), each as one sentence with the count.
5. **If time remains:** for the best pair, contexts of at most 3 + 3 pawns on the file if it fits.

## Budget and rules

- Time: about four hours of solver time. Write `findings.txt` as you go, so an interrupted run leaves a report.
- Programs: copy K72's `pk.cpp` and `ref3m.cpp` (with their memory guards) and its scripts into your folder; the
  P value of every position is CHECKED-2 only when both agree, else COMPUTED-1. Predictor: K72's `dpred.py` and a
  second one of your own.
- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: every solver sizes its arrays before allocating and exits if they would pass 2 GB. Measure the smallest
  input of each kind first with `/usr/bin/time -l`. A run measured under 30 seconds and under 0.6 GB may be
  started directly, one at a time. Every other run goes through `kings/delegate/heavy.sh <cmd>` (two slots shared
  by all agents; both are in use by long searches now and another agent is waiting too: do the short runs first
  and expect to wait an hour or more) under `/usr/bin/time -l`, with a watchdog on the solver's own recorded PID
  that polls at least five times a second and kills at 2.0 GB. After any watchdog kill the whole chain stops and
  you report. No chain of runs without the watchdog. Do NOT run vgsum59 or pr57.
- Runs over 2 minutes: background, and wait for them before reporting. Do not hand back while a run of yours is
  still going.
- Write only inside `kings/delegate/out/K75/`. No git commands that change anything. Do not touch `paper/`,
  `dist/`, `cylcgt/`, `realchess/`, `delegate/` or other `kings/delegate/out/` directories (read them freely).
  No network, no downloads.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.
- Labels: CHECKED-2 (two separately written programs agree), COMPUTED-1, CONJECTURE. A computed fact is never
  PROVED.

## Deliverables

- `findings.txt`: the short answer first (the table of question 1 in a form a paper could quote, the rule, the
  quotable sentences), then details, then what was not covered.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
- `EDITS.md` for `kings/theory/LOOPY.md` (format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit LOOPY.md):
  at most six lines after Proposition 4.25, marked "not yet refereed". A K72 paragraph may be installed there
  before you finish; anchor your OLD on the line `*Computable test (K43).*` only.
