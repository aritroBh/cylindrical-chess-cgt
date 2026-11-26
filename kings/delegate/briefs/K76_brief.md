# K76: referee of K75 (which over groups keep the results of ω beside real pawns; a rule for the kings)

Referee brief, 2026-11-26. Output in `kings/delegate/out/K75/verify/` (create it). You are independent of the
investigator: do not trust its counts, its predictor or its rule; reproduce what you can with other means.

## Read

`kings/delegate/briefs/K75_brief.md` (the task), `kings/delegate/out/K75/findings.txt`, `EDITS.md`, `src/`, `logs/`.
`kings/delegate/out/K72/REVIEW.md` and `kings/delegate/out/K72/verify/VERIFY.md` (the same experiment for five
groups, refereed; its referee wrote a third P solver, `kings/delegate/out/K72/verify/src/p74.c`, from the rules,
which solved all 729 placements on one file for a seven-man group in 0.64 GB). `kings/theory/LOOPY.md`:
Definitions 1.3, 2.1, 4.8, Lemma 4.15, Corollary 4.17, Theorem 4.18, the paragraph "K72" after Proposition 4.25.

## The claims to check

1. The table: 58 (group, context file) pairs of the 48 groups (7 groups have no separated file), contexts of at most
   1 + 1 pawns, agree/fail counts and the direction of each failure; 11 clean pairs (10 groups); 427 failing contexts,
   all with pawns of both colours.
2. The files (Definition 2.1) and the three distances dW, dA, dB of each pair; the roots, freezes and q's of the 48
   groups as read into `in/groups48.txt` (compare with the K65 and K67 sources, at least for every clean pair and
   ten others).
3. The prediction for groups without (B1): what is proved for class "Aux won" (Theorem 4.18) and for "Aux lost"
   (only the bound). Is every comparison made against a statement that the note proves for that class?
4. The larger sizes: C125_10 h, C145_13 h at 2 + 2 (283/0); C014_01 h at 3 + 3 (583/0).
5. "2 + 2 does not fit for the eight-man clean pairs."
6. The rule (R1), (R2), (R3) and the tempo refinement (R1'): are they true of the table as stated, with exactly the
   exceptions listed? Is (R3) worth stating as a CONJECTURE, or is it a description of 58 data points (say which)?
   Is there a simpler or sharper statement that the table supports?
7. The four quotable sentences and `EDITS.md`: wording, labels. K67's ten groups rest on one search program so far;
   check that this is said wherever they are used.

## How

- **Third solver.** Copy `p74.c` (and what it needs) from `kings/delegate/out/K72/verify/src/` into your folder; it
  is separately written from pk and ref3m. Test it first on three pairs against the K72 tables. Then: all 58 pairs
  at 1 + 1 (if a pair does not fit or is slow, say so and do at least all 11 clean pairs and 15 failing ones, both
  directions); the three larger claims of item 4.
- **Extend where p74 fits** (this is new work; label it COMPUTED-1): for every clean pair, the largest of 2 + 2,
  3 + 3, all 729 placements that fits in 2 GB (measure first). Report for each clean pair the largest size at which
  it is still clean, and the smallest failing context if one appears (K72's referee found that C125_10 h fails at
  4 + 1). Any failure you find: confirm it with pk on that context alone.
- **Recount** items 1 and 6 from the per-pair tables with your own script; recompute the distances from the group
  strings yourself.
- **By hand, on a board:** for three clean pairs (C014_01 h, C145_13 h, one eight-man pair) say in a few sentences
  why neither king can profit from walking to the file (explanation, not a proof); for three failing pairs at the
  same distances as a clean one (the cell dW 7, dB 5), play through the smallest failing context and say what is
  different. That comparison is the most useful thing you can give: it decides whether a rule in distances exists.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: every solver sizes its arrays before allocating and exits if they would pass 2 GB. Measure the smallest
  input of each kind first with `/usr/bin/time -l`. A run measured under 30 seconds and under 0.6 GB may be started
  directly, one at a time. Every other run goes through `kings/delegate/heavy.sh <cmd>` (two slots shared by all
  agents; do not take both slots at once; leave a gap of a few seconds between chained runs so that a waiting agent
  can get a slot) under `/usr/bin/time -l`, with a watchdog on the solver's own recorded PID that polls at least
  five times a second and kills at 2.0 GB. After any watchdog kill the whole chain stops and you report. No chain of
  runs without the watchdog. Do NOT run vgsum59, pr57 or ref3pv (ref3pv reached 1.99 GB in K75).
- Runs over 2 minutes: background, and wait for them before reporting. Do not hand back while a run of yours is
  still going. Budget: about three hours of solver time.
- Write only inside `kings/delegate/out/K75/verify/` (temporary files in a `tmp/` there, deleted at the end). No git
  commands that change anything. Do not touch `paper/`, `dist/`, `cylcgt/`, `realchess/`, `delegate/` or other
  directories (read them freely). No network, no downloads.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.
- Labels: CHECKED-2 (two separately written programs agree; say which), COMPUTED-1, CONJECTURE, PROVED only for a
  complete hand proof. A computed fact is never PROVED.

## Deliverables (in `kings/delegate/out/K75/verify/`)

- `VERIFY.md`: verdict first (each of the seven claims: confirmed, corrected or refuted, with its label), the
  comparison counts (positions compared, disagreements), the table of clean pairs with the largest clean size, the
  hand comparison, your judgement of the rule, process notes.
- `EDITS.md`: the edit for `kings/theory/LOOPY.md` as you would install it (format `### EDIT title` /
  `<<<<<<< OLD` / old / `=======` / new / `>>>>>>> NEW`; anchor OLD on the line `*Computable test (K43).*` only, so
  that the new paragraph comes after the K72 paragraph; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit LOOPY.md).
  At most seven lines. No "not yet refereed" mark if you confirm.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
