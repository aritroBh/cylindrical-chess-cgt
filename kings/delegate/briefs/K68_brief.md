# K68: a hand proof that one seven-man position of the ordinary chessboard is an exact over group

Theory brief, 2026-11-25. Hand proofs; a small solver only as an oracle. Output in `kings/delegate/out/K68/`.

## Why

Every real exact over group in the note rests on computation ("PROVED, given CHECKED-2 computations"). A paper is
stronger with one real example proved by hand from start to finish. The best candidate is the most rigid of the five
groups that are exact in chess as well (K65, tablebase):

G = C125_05 = `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6` on the flat 8×8 board. White: Kd4, Pb6, Pc2, Pc5. Black: king on b4
or b5 (the shuttle), pb7, pc6. Freezes: c2–c4 at the b4 root, c2–c3 at the b5 root. The pawns b6/b7 and c5/c6 block
each other, so only the kings and the c2 pawn move until something is captured.
FEN of the roots: `8/1p6/1Pp5/2P5/1k1K4/8/2P5/8` and `8/1p6/1Pp5/1kP5/3K4/8/2P5/8`.

## Read

`kings/theory/LOOPY.md`: Definition 1.1, 1.3 (the games P and D, D-sums), Definition 4.8 (clauses O0 to O4),
Lemma 4.15 with (B1), Corollary 4.17 and its K65 paragraph, Theorem 4.18. `kings/delegate/briefs/K61_over_test_blind.md`
§1 (the rules of the sum in one place). `kings/delegate/out/K65/verify/VERIFY.md` (computed facts about this group:
exact, (B1) at every bad move, exact in chess) and `kings/delegate/out/K66/VERIFY.md` §4 (the chess reading).

## Questions, in order

1. **P, Definition 4.8.** Prove by hand every clause of Definition 4.8 for G in the promotion game P (first
   promotion wins, mate loses, stalemate draws when alone): the values of both roots for each side to move, that the
   shuttle is Black's only move that keeps the group's structure, that the freeze is White's only non-losing root
   move, and that both freeze positions q are lost for the side to move. State the clause numbers as in the note.
2. **P, (B1).** List the bad (non-shuttle) Black root moves and prove (B1) at each: after the move, with White to
   move, White wins beside −1 under the sum's rule. Then Lemma 4.15 gives the results of ω beside every finite
   D-game with no computed fact at all. Say so as a theorem.
3. **Chess.** Prove by hand as much of the same in chess with promotion to real pieces as you can (the tablebase
   already gives it as KNOWN): at least the values of the two roots and the two q's for both sides to move. Where a
   queen ending must be judged, a clear standard argument is enough (for instance a new queen against bare pawns
   with the enemy king far away, or promotion with check); where you cannot close a line by hand, say exactly which
   position is left to the tablebase.
4. **Why it works.** Two or three sentences a chess reader recognises: which squares are the key or corresponding
   squares, why the choice between the single and the double step of the c pawn is the whole point, and why the
   2 + 2 groups fail in chess while this one does not.

## Method and honesty

- Use any small solver as an oracle to find the lines and to test each lemma before you write it (copy
  `kings/delegate/out/K65/verify/src/ax65.cpp` or write your own; P values of every reachable position of this group
  fit in a few megabytes). The proof itself must be readable and checkable without a computer: named lemmas, zones of
  squares, explicit lines; case lists are fine when each case is closed by an argument in the text.
- Label each statement PROVED (complete hand proof in the text), PROVED given KNOWN tablebase facts (name the
  positions), or COMPUTED-1 (only the oracle says so). Do not call a statement PROVED if any branch is closed by
  "the solver confirms". A shorter list of honest PROVED statements is worth more than a long doubtful one.
- After the proof is written, test every claimed value and every "only move" claim in it against the oracle and,
  for the chess part, against the cached tablebase answers in `kings/delegate/out/K65/verify/logs/tbcache.tar.xz`
  (unpack a copy inside your folder; offline, no network). Report the comparison.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
- Toy computations only: nothing over 500 MB or over a minute; if a run would be longer, it goes through
  `kings/delegate/heavy.sh <cmd>` under `/usr/bin/time -l` and must stay under 2 GB.
- Write only inside `kings/delegate/out/K68/`. No git commands that change anything. Do not touch `paper/`, `dist/`,
  `cylcgt/`, `realchess/`, `delegate/` or other `kings/delegate/out/` directories (read them freely). No network,
  no downloads.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.

## Deliverables

- `PROOF.md`: statements and full hand proofs, each labelled; a diagram of the position in text; the summary first.
- `findings.txt`: the short answer (what is PROVED, what is left to the tablebase or the solver), then the oracle
  comparison.
- `src/`, `logs/` (xz anything over 256 KB), `pids.log` if anything ran in the background.
- `EDITS.md` for `kings/theory/LOOPY.md` (format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit LOOPY.md
  itself): one new numbered statement, Proposition 4.25, placed after Proposition 4.24, with a pointer to PROOF.md,
  marked "one AI proof, not yet refereed".
