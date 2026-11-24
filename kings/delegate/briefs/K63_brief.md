# K63: the 2 + 2 over group on the ordinary chessboard, in chess and beside other pawns

Investigator brief, 2026-11-24. Computation with careful reading of what each number means. Output in
`kings/delegate/out/K63/`.

## Background (read these)

`kings/theory/LOOPY.md`: Definition 4.8, Lemma 4.15, Corollary 4.16, Corollary 4.17, the K45, K47 and K48 bullets of
Conjecture 4.7. `kings/delegate/out/K59/findings.txt`, `kings/delegate/out/K59/REVIEW.md`,
`kings/delegate/out/K59/verify/VERIFY.md` (and its solver `verify/src/kref.cpp`). For the chess runs:
`kings/delegate/out/K48/` (how kpsolve was run on the cyl:8×6 group at cap 1, what "cap" means, what was and was not
settled). For P contexts: the K47 and K55 outputs (`kings/delegate/out/K47/`, `kings/delegate/out/K55/`), which
explain why a P context is not a D-sum component.

The object. F2 = `Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6` (White Ka4, Pb2, Pf5; Black king on c4 or c5, pb6, pf6). On flat 8×7
and flat 8×8 it is an exact over group of Definition 4.8 in the promotion game P, with (B1), so as the P game of its
own pieces in a D-sum it has the results of over (Corollary 4.17). On flat 8×8 it is a position of ordinary chess
with six men. Black shuttles c4–c5; White's freezes are b2–b4 at the c4 root and b2–b3 at the c5 root.

## Questions

1. **In chess (model C), on flat 8×8.** With promotion to real pieces, what are the results of the two roots (each
   side to move), of each freeze position q (each side to move), and of every root move? Is the structure of
   Definition 4.8 kept (shuttle the only non-losing Black root move; a freeze the only non-losing White root moves;
   each q a mutual zugzwang)? Use kpsolve at cap 1 as K48 did, and cap 2 only if a measured small run shows it stays
   under 2 GB. State exactly what a cap-k result proves about real chess and what it leaves undecided. If the repository
   has any exact chess evidence for six-man positions (look in `realchess/` and `cylcgt/` for what exists; read
   only), say whether it can be used here; do not download tablebases or anything else.
   Do the same for F1, F3, F4 on flat 8×8 if time and memory allow, F2 first.
2. **Flat 8×8 against flat 8×7.** List the differences between F2's P graph on the two boards (the extra rank changes
   promotion distance: which root moves and values change, if any).
3. **Beside other pawns in P, on the same board.** F2 occupies files a to c and f. Put a small context on the free
   files (g, h; and d, e where it does not touch the group: say which placements are separated in the sense of the
   note's context definitions) with at most 1 + 1 pawns first, then 2 + 2 if cheap: for each context X whose own
   P value or D-result you can state, compare the result of the whole position F2 + X in P (one board, one game, no
   sum rule) with the D-sum prediction r(ω ⊞ X). Report where they agree and every disagreement with its line of
   play. K47 found that the cyl:8×6 group is not over beside contexts; the question is whether F2, which does have the
   results of over in D-sums, behaves better, and which P-context effects (a king walking to the context, pawn
   races, checks from promotions) break the prediction.
4. **Mirror.** State the exact under group obtained by the colour flip of F2 on flat 8×8, as a chess position.

## Checks

- Every chess or P value you report must come from two programs where two exist (kpsolve and `kp_p`, ref3m, the
  K59 referee's `kref.cpp` for P). Say COMPUTED-1 or CHECKED-2 for each table. No hand proofs are asked for, but
  a short forcing line for each root move in P (why it loses) is welcome if it is short.
- Sanity: reproduce Corollary 4.17's statement for F2 on flat 8×8 (exact, (B1) at every non-shuttle Black root
  move) before anything new.

## Deliverables

- `findings.txt`: the short answer first (one paragraph a reader of the paper could use), then tables, then what was
  not checked.
- `src/`, `logs/` (xz anything over 256 KB; pack many small files into one tar.xz), `pids.log`.
- `EDITS.md` for `kings/theory/LOOPY.md` in the format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy. Do not edit LOOPY.md itself.
  Add to Corollary 4.17's paragraph or to the K45 bullet; no new numbered statement unless something is proved.
  Mark everything "not yet refereed".

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Every run over a minute or over 500 MB goes through `kings/delegate/heavy.sh <cmd>` under `/usr/bin/time -l`
  (at most two heavy processes at once across all agents, nice 15). Design for under 2 GB; measure the smallest
  input first. Nothing may go over 3 GB: if a run would, do not start it; report the measured size instead.
- Runs over 2 minutes: background, and wait for them before reporting.
- Write only inside `kings/delegate/out/K63/`. No git commands that change anything. Do not touch `paper/`, `dist/`,
  `cylcgt/`, `realchess/`, `delegate/`, or other `kings/delegate/out/` directories (read them freely).
- No downloads. No binaries left behind, no absolute home paths in text files, no executable bits on scripts.
