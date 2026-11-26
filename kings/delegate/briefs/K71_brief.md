# K71: remove the computed lemma from Proposition 4.25 (redesign the reduction, then prove by hand)

Theory brief, 2026-11-25. Hand proofs; small solvers only as oracles. Output in `kings/delegate/out/K71/`.

## Where things stand

Proposition 4.25 of `kings/theory/LOOPY.md`: G = `Kd4 kb4/kb5 Pb6 Pc2 Pc5 pb7 pc6` on flat 8×8 is an exact over
group in the promotion game P. Proved by hand: everything except "every White king move at the two roots and at
the two freeze positions q1, q2 (White to move) loses". That part is reduced by hand (Lemma C of
`kings/delegate/out/K68/PROOF.md`) to Lemma B: Black Kb6, pb7, pc6 against a White king and one pawn on c2, c3 or
c4, White to move, is a Black win; 42 positions are used, computed by three programs, no hand proof. The referee
(`kings/delegate/out/K68/verify/VERIFY.md` §5, §6) could not prove it: no single Black first move wins throughout;
the hard cases are the pawn on c2 with the White king on b3, c3, d3 and the pawn on c4 with the king on c3, where
White attacks the pawn pair and defends with stalemate (lines of 36 to 44 plies).

Read: PROOF.md (§1 rules, Lemma A, Lemma C), VERIFY.md whole, LOOPY.md Definition 4.8 (O3)/(O4) and
Proposition 4.25. Do NOT open `kings/delegate/out/K70/` (another model is attempting Lemma B as stated, blind;
keep the two attempts independent).

## Task

You are free to change the reduction. What must be proved is only this:

(T) In P, from each of the four positions R1 (b4 root), R2 (b5 root), Q1, Q2 with White to move, after each
White king move (17 moves in all) Black wins.

1. **Find the cheapest route.** With the oracle, look for a Black strategy from the 17 positions that avoids the
   hard part of Lemma B: Black need not play …K×c5 and …K×b6 at once, and need not answer every White move the
   same way. Candidates: take c5 and keep the king in front of the pawns; go for the c-pawn γ first (…Kb4–b3 or
   …Kc4 when legal) while b6 cannot run (Pb6 is blocked by pb7; K×b7 needs Kc7 or a7/a8/b8/c8); answer a White
   king march to d6/c7 by a counted race. Measure each candidate by the longest forced line and by the number of
   distinct "zones" the proof needs; report the table.
2. **Write the proof** of (T) for the best route: zones of the White king, a rule for Black in each zone, an
   invariant that is kept, and a counted finish (Black promotes on c1 or b1 before White can promote or stalemate
   itself). Stalemate is a draw in P: every line where White could run out of moves must be closed explicitly.
   Case lists are fine when each case is closed by an argument in the text.
3. **Test the written strategy** by program: play the strategy literally (as written, rule by rule) against every
   White reply, as the referee did for Lemma A (298,179 plays there), and report plays, failures, longest play.
   A passed test is a check, not a proof; the proof must stand without it.
4. **If (T) cannot be fully proved by hand,** prove as much as you can and state exactly which positions are left
   (a list as short as possible, each with its P value and length from the oracle).

Oracle: build `kings/delegate/out/K68/verify/src/r68.cpp` in your scratch directory (10 s, 25 MB; usage in
VERIFY.md §8), or write your own.

## Labels and honesty

PROVED (complete hand proof in the text) / PARTIAL (say what is missing) / CHECKED-2 / COMPUTED-1. Do not close a
branch with "the solver confirms". A shorter honest result is worth more than a long doubtful one.

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
- Toy computations only: nothing over 500 MB or over two minutes. The machine is loaded; do not start anything
  heavier.
- Write only inside `kings/delegate/out/K71/`. No git commands that change anything. Do not touch `paper/`,
  `dist/`, `cylcgt/`, `realchess/`, `delegate/` or other `kings/delegate/out/` directories (read them as allowed
  above). No network, no downloads.
- No binaries left behind, no `__pycache__`, no absolute home paths in text files, no executable bits on scripts.

## Deliverables

- `PROOF_T.md`: summary and label table first; then the proof.
- `findings.txt`: the short answer, the route table of item 1, the strategy test of item 3.
- `src/`, `logs/` (xz anything over 256 KB).
- `EDITS.md` for `kings/theory/LOOPY.md` only if the label of Proposition 4.25 changes (format `### EDIT title` /
  `<<<<<<< OLD` / old / `=======` / new / `>>>>>>> NEW`, each OLD matching the current file exactly once; test
  with `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy; do not edit
  LOOPY.md), marked "one AI proof, not yet refereed".
