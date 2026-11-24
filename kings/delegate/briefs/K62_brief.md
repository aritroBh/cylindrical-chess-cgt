# K62: is there a test family for "has the results of over" that does not depend on the group?

Investigator brief, 2026-11-24. Theory first; small toy computations only. Output in `kings/delegate/out/K62/`.

## Background (read these)

`kings/theory/LOOPY.md`: Definition 1.1, 1.3, Proposition 4.6, Definition 4.8, Lemma 4.15, Theorem 4.18, Corollary 4.19.
`kings/delegate/out/K60/PROOF.md` (mind the notes at its top), `kings/delegate/out/K60/verify/VERIFY.md`,
`kings/delegate/out/K61/PROOF.md` (Codex's blind proof; its layer operator F and the sets S_N are useful here),
`kings/delegate/briefs/K61_over_test_blind.md` §1 (the abstract model in one place).

What is known. Theorem 4.18: an exact over group G has the results of ω beside every finite D-game iff for each bad
Black root move m White wins x_m ⊞ u_0 in the ladder T_N for one N ≥ K, where K is the number of (board, e.p. right,
side) states of G. So the test game depends on G through K. On toy groups the family k·↓ is not exact for k ≤ 4, and at
2 bad moves (C) fails only beside some T_N (K60).

The e.p. rule throughout: a right only adds moves (every move legal without the right is legal with it, same result).

## Questions

1. **Ladder length.** For every N ≥ 1, is there an abstract exact over group G_N and a bad Black move m such that White
   wins x_m ⊞ u_0 in T_n for every n < N and does not win it in T_N? Give the construction with the smallest number
   of boards you can, with and without checks and e.p. rights, and prove it by hand. What is the sharp bound on the
   smallest sufficient N in terms of the group (K is an upper bound; is it the number of boards, or of Black-to-move
   states reachable from x_m, or something smaller)? Prove the bound and show it is attained.
2. **No universal finite family (the main question).** Prove or refute: for every finite set F of finite D-games there
   is an abstract exact over group that has the results of ω beside every T in F (every position, both sides to move,
   roots and q's as in the definition) and does not have the results of ω beside every finite D-game. If true, also
   settle the countable version: is {T_N : N ≥ 0} a universal family (yes by Theorem 4.18; say so), and is there a
   single finite D-game, necessarily loopy, that is universal? Aux is a Büchi game and not a D-game: is there a loopy
   finite D-game U (draws for infinite play, terminals allowed) with "G has the results of ω iff both roots, Black to
   move, have the result of ω beside U"? Prove or refute; a partial answer with its exact scope is welcome.
3. **Fixed boards.** For real groups on a fixed board (width w, height h, at most p pawns a side) K is bounded by the
   number of chess states, so one ladder T_{K(w,h,p)} is a test for every group on that board. State this as a
   corollary with an explicit (crude) bound, and say what the smallest N is on the real groups where it is known
   (Z_O: fails already beside T_2; H10 and the others pass through (B1), which is N-free).
4. **What a counter needs in chess.** In your G_N, what plays the role of the counter (for example a Black pawn that
   needs n quiet moves, or a White reserve of n tempo moves)? Say in two or three sentences whether a real
   king-and-pawn group could carry such a counter of length greater than 2 while staying exact, and what one would
   search for. No search is asked for here.

## Checks

- Validate each construction by brute force with your own small solver: D-sums with the rules of the K61 packet §1
  (promotion terminal; no move elsewhere in check; a move elsewhere clears the mover's right; no move anywhere loses;
  infinite play a draw; Aux with the Büchi rule). You may read `kings/delegate/out/K60/verify/src/r60lib.py` but
  write your own. Check exactness (O0–O4) of every group you construct, by program and by hand.
- For question 2, check your group against every game of F for a few explicit small F (for instance all D-games with
  at most 3 positions, and the ladders T_0..T_5), and exhibit the game that separates it from ω.

## Deliverables

- `PROOF.md`: statements with full hand proofs, each labelled PROVED (hand proof), CONJECTURE or COMPUTED-1. Solver
  results are never PROVED.
- `findings.txt`: the short answer first, then what was and was not checked.
- `src/`, `logs/` (xz anything over 256 KB), `pids.log`.
- `EDITS.md` for `kings/theory/LOOPY.md` in the format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy. Do not edit LOOPY.md itself.
  New statements are numbered 4.20 and up (4.17 is reserved). Mark everything "not yet refereed". Do not touch
  Corollary 4.16, the C4.7 status row or the "To settle" line (another item is editing them).

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Toy computations only: nothing over 500 MB or over a few minutes. Any run over a minute goes through
  `kings/delegate/heavy.sh <cmd>` under `/usr/bin/time -l`. No solver runs on real boards.
- Write only inside `kings/delegate/out/K62/`. No git commands that change anything. Do not touch `paper/`, `dist/`,
  `cylcgt/`, `delegate/`, or other `kings/delegate/out/` directories.
- No binaries left behind, no absolute home paths in text files.
