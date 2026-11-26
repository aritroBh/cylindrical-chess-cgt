# K74: referee of K72 (the five chess-exact over groups beside real pawns, promotion game P)

Referee brief, 2026-11-25. Output in `kings/delegate/out/K72/verify/` (create it). You are independent of the
investigator: do not trust its programs, its predictor or its counts; reproduce what you can with your own means.

## Read

`kings/delegate/briefs/K72_brief.md` (the task), `kings/delegate/out/K72/findings.txt`, `EDITS.md`, `src/`, `logs/`
there. `kings/theory/LOOPY.md`: Definitions 1.1, 1.3, 2.1, Definition 4.8, Lemma 4.15, Corollary 4.17 (K63 and K65
paragraphs), Proposition 4.25. `kings/delegate/out/K63/verify/VERIFY.md` (how the same comparison was refereed for
the group F2).

## The claims to check

1. The table of `findings.txt` §0: for each of 11 (group, context file) pairs, the number of contexts of at most
   1 + 1 and at most 2 + 2 pawns on that file where all eight P results (two roots, two q's, either side to move)
   equal the prediction, and the number of differing positions. The positive claim that matters most: **C125_10
   beside every context of at most 2 + 2 pawns on file h: 283 of 283, 2,264 positions.**
2. The prediction itself: r(ω ⊞ X) at the roots and r(X) at the q's, with X the D-game of the context pawns alone.
   Is this what Lemma 4.15 and Corollary 4.17 predict, with the right side to move at each of the eight positions?
   Is the D-game of a one-file context modelled as in the note (Definition 1.3; a side with no move, promotion,
   double steps)? Recompute the 283 predictions with your own few lines of code, not with `dpred.py`.
3. Which files qualify (Definition 2.1): F_Z, buffer, context for each group.
4. "Every failing context has pawns of both colours on the context file; every one-colour context agrees."
5. The two failure kinds and the examples of §0 items 2 and 3 (ten smallest counterexamples). The label COMPUTED-1
   for the mechanism sentences. The sentence "exactness in chess does not protect a group".
6. The wording and labels of `EDITS.md`. Say which hypothesis of the note's decomposition statements fails in the
   failing contexts (the kings leave F_Z), so that nobody reads the failures as contradicting a theorem.

## How

- **Your own solver for P.** Write a third program yourself (kings and pawns on the flat 8×8 board, first promotion
  wins, mate loses, stalemate and infinite play are draws, en passant, double steps); do not derive it from
  `pk.cpp` or `ref3m.cpp` (you may read them afterwards to explain a disagreement). Test it first on known values:
  the Lemma B table of `kings/delegate/out/K68/verify/logs/` (162 positions) or the values in
  `kings/delegate/out/K65/verify/VERIFY.md`.
- With it: all 1 + 1 contexts of all 11 pairs (11 × 43 × 8 positions); all 283 contexts of C125_10 on h; and all
  283 contexts of at least two other pairs, one of each failure kind (suggested: C125_08 on h, C145_07 on a). More
  if the budget allows. Compare position by position with the investigator's tables.
- **By hand, on a board:** play through the ten smallest counterexamples of §0 item 3. For each: is the position
  as stated, is the line legal, and is the claimed P result right (give the winning or drawing idea in two
  sentences; your solver decides the side lines)? For C125_10, give in a few sentences the reason one would expect
  no failure (which king is how far from file h, and whose pawns it could reach), marked as an explanation, not a
  proof, and try for half an hour to find a context of 3 + 3 pawns on h, or a context on file h of a kind the
  investigator's enumeration left out, where C125_10 fails; report what you tried.
- Recount items 1 and 4 from the per-context tables with your own script.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Memory: your solver sizes its arrays before allocating and exits if they would pass 2 GB. Measure the smallest
  input first with `/usr/bin/time -l`. A run measured under 30 seconds and under 0.6 GB may be started directly,
  one at a time. Every other run goes through `kings/delegate/heavy.sh <cmd>` (two slots shared by all agents;
  both are in use by long searches now, one frees in about 1.5 hours, the other in about 4: plan the short work
  first and expect to wait) under `/usr/bin/time -l`, with a watchdog on the solver's own recorded PID that polls
  at least five times a second and kills at 2.0 GB. After any watchdog kill the whole chain stops and you report.
  Do NOT run vgsum59 or pr57.
- Runs over 2 minutes: background, and wait for them before reporting. Do not hand back while a run of yours is
  still going.
- Write only inside `kings/delegate/out/K72/verify/`. No git commands that change anything. Do not touch `paper/`,
  `dist/`, `cylcgt/`, `realchess/`, `delegate/` or other directories (read them freely). No network, no downloads.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.
- Labels: CHECKED-2 (two separately written programs agree; say which), COMPUTED-1, PROVED only for a complete
  hand proof. A computed fact is never PROVED.

## Deliverables (in `kings/delegate/out/K72/verify/`)

- `VERIFY.md`: verdict first (each of the six claims: confirmed, corrected, or refuted, with the label it
  deserves), then the comparison table (positions compared, disagreements), the hand checks, the C125_10 search,
  process notes (anything the investigator did against its rules).
- `EDITS.md`: the edit for `kings/theory/LOOPY.md` as you would install it (same format as the investigator's,
  each OLD matching the current file exactly once, tested with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit LOOPY.md).
  At most seven lines. No "not yet refereed" mark if you confirm.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
