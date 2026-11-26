# K78: the seven two-file classes of flat 8×8 that lie in none of the four searched classes

Investigator brief, 2026-11-26. Output in `kings/delegate/out/K78/`.

## Background (read these)

`kings/theory/LOOPY.md`: Definition 4.8, Lemma 4.15, Corollary 4.17 (its census paragraph), Theorem 4.18,
Proposition 4.24. `kings/delegate/briefs/K67_brief.md`, `kings/delegate/out/K67/findings.txt` and
`kings/delegate/out/K67/REVIEW.md` (the same work for two three-file classes: programs, counters, regression,
classification pipeline, tablebase script, watchdog; copy what you need from `kings/delegate/out/K67/src/`).
`kings/delegate/out/K67/verify/VERIFY.md` (the referee's programs p74-based `def77.py` and the sum solver `s77.c`
in `verify/src/`: a third check that is small and fast).

Known. On flat 8×8 (ranks 2 to 7, at most 3 + 3 pawns, every king placement) the four classes {a,b,e}, {a,d,e},
{b,c,f}, {b,e,f} hold 48 exact over groups (Definition 4.8), 27 up to reflection and file translation. A group
with pawns on two files lies in a searched class when its two files do. Not searched, up to reflection: the
two-file classes {a,c}, {a,f}, {a,g}, {a,h}, {b,d}, {b,g}, {c,e}.

## Questions

1. **Census.** Check the list of seven first (which two-file sets, up to left-right reflection, are contained in
   none of the four classes or their reflections). Search each with p45a, then with r48 (pawns on exactly these two
   files or fewer; say how you pass a two-file class to each program and test that on a two-file class with a known
   answer: a two-file subclass of a searched class must reproduce exactly the groups of that class that have
   pawns on those two files only). Report every exact over group (roots, shuttle, freezes, q's, men), the counters
   of both programs, and the union with the 48.
2. **Classification of every new group**, as K67: Definition 4.8 again by ref3m and `kp_p` through def48.py; (B1)
   at every bad Black root move; Aux at every failing move; where Aux is lost, the ladder until the first non-win,
   so N\*. Use ax65 and pk_sum, and s77 as a third program. A group with N\* ≥ 4 answers an open question: report
   it with full detail.
3. **Chess.** For every new group with at most seven men: is it an exact over group in chess (K65's reading;
   copy `tb67.py`)? Through `realchess/probe.py` with your own cache and ledger inside your folder, cap 150
   requests; nothing written in `realchess/`.
4. **If nothing is found in a class,** say so with the counters: "no exact over group with pawns on these two
   files" is a result.

## Budget and rules

- Time: about eight hours of solver time. Measure p45a and r48 on the first class before planning the rest (a
  two-file class has far fewer pawn placements than a three-file class, so expect minutes, not hours; if not,
  search all seven with p45a first and r48 in order of cost). Write `findings.txt` as you go.
- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: every run over a minute goes through `kings/delegate/heavy.sh <cmd>` under `/usr/bin/time -l`. Use ONE
  slot only, never both (another agent needs the other); leave a few seconds between chained runs. Every solver
  sizes its arrays before allocating and exits if they would pass 2 GB. Every run has a watchdog on the solver's
  own recorded PID that polls at least five times a second and kills at 2.0 GB. After any watchdog kill the whole
  chain stops and you report. No chain of runs without the watchdog. Do NOT run vgsum59, pr57 or ref3pv.
- Runs over 2 minutes: background, and wait for them before reporting. Do not hand back while a run of yours is
  still going, and do not stop a run of yours in order to hand back.
- Write only inside `kings/delegate/out/K78/` (temporary files in a `tmp/` there, deleted at the end). No git
  commands that change anything. Do not touch `paper/`, `dist/`, `cylcgt/`, `realchess/`, `delegate/` or other
  `kings/delegate/out/` directories (read them freely). No downloads; network only for the tablebase lookups of
  item 3.
- No binaries left behind, no `__pycache__`, no unpacked cache folder, no absolute home paths in text files, no
  executable bits on scripts.
- Labels: KNOWN (tablebase), CHECKED-2 (two separately written programs agree; say which), COMPUTED-1. No hand
  proofs asked for. A computed fact is never PROVED.

## Deliverables

- `findings.txt`: the short answer first (a table: class, placements, exact groups, new groups; then the census of
  all classes with pawns on at most the searched files, as a sentence a paper could quote), then the
  classification and chess verdicts, then what was not searched.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
- `EDITS.md` for `kings/theory/LOOPY.md` (format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit LOOPY.md):
  replace only the sentence of Corollary 4.17 that begins "Not searched: the seven two-file classes", by at most
  four lines, marked "not yet refereed". No new numbered statement unless a group with N\* ≥ 4 is found.
