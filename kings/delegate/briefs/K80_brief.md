# K80: referee of K78 (the seven two-file classes of flat 8×8; 58 groups in eleven classes)

Referee brief, 2026-11-26. Output in `kings/delegate/out/K78/verify/` (create it). You are independent of the
investigator: do not trust its counts or its classification; reproduce what you can with other means.

## Read

`kings/delegate/briefs/K78_brief.md` (the task), `kings/delegate/out/K78/findings.txt`, `EDITS.md`, `src/`, `logs/`,
`in/`. `kings/delegate/out/K67/REVIEW.md` and `kings/delegate/out/K67/verify/VERIFY.md` (how the last census was
refereed: K77; its programs in `verify/src/`). `kings/theory/LOOPY.md`: Definition 4.8, Lemma 4.15 with (B1),
Corollary 4.17 (census paragraph), Theorem 4.18.

## The claims to check

1. **The list of classes.** Exactly seven two-file classes, up to left-right reflection, lie in none of the four
   three-file classes {a,b,e}, {a,d,e}, {b,c,f}, {b,e,f} or their reflections. Recount by hand or with your own
   few lines. Also say plainly what the eleven classes together cover and what they do not (for example: every
   group with pawns on at most two files? on which three-file sets?), so that the note's sentence is exact.
2. **Search.** The seven rows of the table (placements, six counters, exact groups 0, 0, 0, 0, 1, 6, 3); p45a and
   r48 agree on every counter and hit. Read the raw outputs with your own parser. Check the two-file invocation:
   is "pawns on these two files or on one of them" really what both programs enumerate, and is the test on {b,e}
   sound (same three groups as the b,e-only hits of the searched three-file classes)? Check that the programs are
   the K65/K67 ones (diff). You are not asked to repeat a search of a full class, but each two-file r48 run took
   about ten minutes: repeat ONE class of your choice with r48 or p45a built by you from the K65 sources, as an
   end-to-end check.
3. **The 10 hits are exact, and the four empty classes are empty.** With a third program (the K74 referee's
   `p74.c` with K77's `def77.py`, or your own) verify Definition 4.8 for each of the 10 hits and for 30 near misses
   of your choice; for the empty classes pick 20 placements that look like the hits of the other classes
   (translates and reflections of the five new shapes into {a,c}, {a,f}, {a,g}, {a,h} where they fit) and confirm
   that none is exact, with the clause that fails.
4. **Census.** 58 distinct groups in the eleven classes, 32 up to reflection and file translation; 5, 24, 29 with
   6, 7, 8 men; five new shapes. Recount with your own script from the hit lists of all classes.
5. **Classification.** (B1) at all 81 bad Black root moves of the 10 new groups (three programs: ax65, pk_sum,
   s77). Recompute with a program not among these three for at least three groups of different shapes, or show
   another independent route; say what each of the ten rests on. Totals over 58: 44, 9, 5.
6. **Chess.** None of the five seven-man groups is an exact over group in chess. Re-read the cached tablebase
   answers offline with your own script (`logs/tbcache.tar.xz`, unpacked inside your folder); if an answer you
   need is missing you may query through `realchess/probe.py` with your own cache and ledger inside your folder,
   cap 60 requests, nothing written in `realchess/`.
7. **The edit.** Write it against the current `kings/theory/LOOPY.md` (the census paragraph was changed today by
   K77's edit; the investigator's OLD may or may not still match). Check every number.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: every solver sizes its arrays before allocating and exits if they would pass 2 GB (r48 caps its memo at
  about 1 GB; keep the watchdog on it). Measure the smallest input of each kind first with `/usr/bin/time -l`. A
  run measured under 30 seconds and under 0.6 GB may be started directly, one at a time. Every other run goes
  through `kings/delegate/heavy.sh <cmd>` under `/usr/bin/time -l`, ONE slot only (another agent has the other),
  a few seconds between chained runs, with a watchdog on the solver's own recorded PID that polls at least five
  times a second and kills at 2.0 GB. After any watchdog kill the whole chain stops and you report. Do NOT run
  vgsum59, pr57 or ref3pv.
- Runs over 2 minutes: background, and wait for them before reporting. Do not hand back while a run of yours is
  still going. Budget: about two hours of solver time.
- Write only inside `kings/delegate/out/K78/verify/` (temporary files in a `tmp/` there, deleted at the end). No git
  commands that change anything. Do not touch `paper/`, `dist/`, `cylcgt/`, `realchess/`, `delegate/` or other
  directories (read them freely). No downloads; network only for the tablebase lookups of item 6.
- No binaries left behind, no `__pycache__`, no unpacked cache folder, no absolute home paths in text files, no
  executable bits on scripts.
- Labels: KNOWN (tablebase), CHECKED-2 (two separately written programs agree; say which), COMPUTED-1, PROVED only
  for a complete hand proof. A computed fact is never PROVED.

## Deliverables (in `kings/delegate/out/K78/verify/`)

- `VERIFY.md`: verdict first (each of the seven claims: confirmed, corrected or refuted, with its label), then the
  table of the 10 hits (roots, shuttle, freezes, q's, men, shape, bad moves, chess verdict, which programs agree),
  the recount, what the eleven classes cover, process notes.
- `EDITS.md`: the edit for `kings/theory/LOOPY.md` as you would install it (format `### EDIT title` /
  `<<<<<<< OLD` / old / `=======` / new / `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit LOOPY.md).
  Change only sentences of the census paragraph of Corollary 4.17; keep its counts for the four three-file classes
  and add the two-file classes and the totals over eleven classes without making any existing number false. No
  "not yet refereed" mark if you confirm.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
