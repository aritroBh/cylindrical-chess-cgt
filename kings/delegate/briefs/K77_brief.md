# K77: referee of K67 (census of the file classes {a,b,e}, {a,d,e} on flat 8×8; 48 groups in four classes)

Referee brief, 2026-11-26. Output in `kings/delegate/out/K67/verify/` (create it). You are independent of the
investigator: do not trust its counts or its classification; reproduce what you can with other means.

## Read

`kings/delegate/briefs/K67_brief.md` (the task), `kings/delegate/out/K67/findings.txt`, `EDITS.md`, `src/`, `logs/`,
`in/`. `kings/delegate/out/K65/REVIEW.md` and `kings/delegate/out/K65/verify/VERIFY.md` (how the first two classes
were refereed; the referee's programs ax65, pk_sum, tb65.py in `verify/src/`). `kings/theory/LOOPY.md`: Definition
4.8, Lemma 4.15 with (B1), Corollary 4.17 (its census paragraph, which the edit replaces), Theorem 4.18, Corollary
4.19, Propositions 4.24, 4.25.

## The claims to check

1. **Search.** {a,b,e}: 4,018,737,400 placements, 10 exact; {a,d,e}: 3,992,135,379 placements, 3 exact; p45a and
   r48 agree on every counter and every hit. Both programs were run by the investigator: read the raw outputs
   (`logs/search/`), compare counters and hit lists yourself, and check that the two programs are the unchanged K65
   ones apart from the memory guard (diff against the K65 copies). You are not asked to repeat a four-hour search.
   Do one independent spot check instead: with a third program (for example
   `kings/delegate/out/K72/verify/src/p74.c`, a P solver written from the rules by another referee, or your own)
   verify Definition 4.8 directly for each of the 13 hits (values of both roots for either side, every Black root
   move, every White root move, both q's), and for 30 near misses of your choice (same pawns, king squares moved by
   one) that the search says are not exact.
2. **Census.** 48 distinct groups in the four classes, 27 up to reflection and file translation; 5, 19, 24 groups
   with 6, 7, 8 men; 10 new groups; one new shape, `Ka5 kc4/kc5 Pa4 Pa6 Pb2 pa7`. Recount with your own script from
   the hit lists of all four classes (K65's are in `kings/delegate/out/K65/`).
3. **Classification of the 10 new groups.** (B1) at every bad move for 7; Aux won at every failing move for 2
   (C014_04, C014_09); Aux lost for 1, C014_08 `Kd5 kf4/kf5 Pa2 Pb3 Pe2 pa5 pb4 pe5` at …e5–e4 with N\* = 2. The
   investigator used the K65 referee's two programs. Write your own small solver for the D-sum values that decide
   C014_08 (x_m ⊞ u_0 beside T_0, T_1, T_2 and the root beside T_2) and for the two "Aux won" groups, or show
   another independent route; say for each of the ten which programs agree. Totals over 48: 34, 9, 5.
4. **Chess.** C034_01 and C034_02 are exact over groups in chess; C014_01, C014_04, C014_05 are not. Re-read the
   cached tablebase answers with your own script and reading (offline from `logs/tbcache.tar.xz`, unpacked inside
   your folder; if an answer you need is missing, you may query through `realchess/probe.py` with your own cache
   and ledger inside your folder, cap 60 requests, nothing written in `realchess/`). Check the claim that C034_01
   and C034_02 are reflected translates of K65's C145_07 and C145_09.
5. **The edit.** The investigator's OLD text is out of date (the census sentence of Corollary 4.17 was changed
   since). Write the edit against the current `kings/theory/LOOPY.md`. Check every number in it. Labels: the search
   is CHECKED-2 only if you find the two programs' outputs really equal; tablebase facts KNOWN.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: every solver sizes its arrays before allocating and exits if they would pass 2 GB. Measure the smallest
  input of each kind first with `/usr/bin/time -l`. A run measured under 30 seconds and under 0.6 GB may be started
  directly, one at a time. Every other run goes through `kings/delegate/heavy.sh <cmd>` (two slots shared by all
  agents; never hold both; leave a few seconds between chained runs) under `/usr/bin/time -l`, with a watchdog on
  the solver's own recorded PID that polls at least five times a second and kills at 2.0 GB. After any watchdog
  kill the whole chain stops and you report. Do NOT run vgsum59, pr57 or ref3pv. Do not rerun p45a or r48 on a
  full class.
- Runs over 2 minutes: background, and wait for them before reporting. Do not hand back while a run of yours is
  still going. Budget: about two hours of solver time.
- Write only inside `kings/delegate/out/K67/verify/` (temporary files in a `tmp/` there, deleted at the end). No git
  commands that change anything. Do not touch `paper/`, `dist/`, `cylcgt/`, `realchess/`, `delegate/` or other
  directories (read them freely). No downloads; network only for the tablebase lookups of item 4.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.
- Labels: KNOWN (tablebase), CHECKED-2 (two separately written programs agree; say which), COMPUTED-1, PROVED only
  for a complete hand proof. A computed fact is never PROVED.

## Deliverables (in `kings/delegate/out/K67/verify/`)

- `VERIFY.md`: verdict first (each of the five claims: confirmed, corrected or refuted, with its label), then the
  table of the 13 hits with roots, shuttle, freezes, q's, men, class, N\*, chess verdict, and which programs
  agree; the recount; process notes (anything the investigator did against its rules; binaries or caches left).
- `EDITS.md`: the edit for `kings/theory/LOOPY.md` as you would install it (format `### EDIT title` /
  `<<<<<<< OLD` / old / `=======` / new / `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit LOOPY.md).
  Replace the census sentences only; do not touch the K63, K72 or other paragraphs. No "not yet refereed" mark if
  you confirm.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
