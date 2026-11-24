# K60: an exact test for "has the results of over"

Investigator brief, 2026-11-23. Theory first, small computations second. Output in `kings/delegate/out/K60/`.

## Background (read these in `kings/theory/LOOPY.md`)

Definition 1.1 and 1.3 (D-games, D-sums, result function), Theorems 3.7, 3.8, 3.11 (loopy sums), Proposition 4.6
(over_D = ω, 0_D), Definition 4.8 (exact over group), Definition 4.12, Lemma 4.13, Proposition 4.14, Lemma 4.15,
Corollary 4.16, and the K47, K55 bullets of Conjecture 4.7. Also `kings/delegate/out/K57/PROOF.md`,
`kings/delegate/out/K57/VERIFY.md`, `kings/delegate/out/K58/PROOF.md` (Codex's blind proof and its abstract witness),
`kings/delegate/out/K56/PROOF.md` (mind the erratum at its top).

What is known. Lemma 4.15: an exact over group G with (B1) has the results of ω beside every finite D-game. (B1) says
that after every non-shuttle Black root move the position is a White win beside −1 under the sum's rule. (B1) is
sufficient. It is not necessary in the abstract, and it cannot be dropped: Z_O fails it at one move and differs from ω
at 38 of 1,100 results (K47).

## Questions

1. **Exact condition.** For an exact over group G, state a condition (C) on the positions B′ reached by Black's
   non-shuttle root moves that is necessary and sufficient for G to have the results of ω beside every finite D-game.
   The obvious candidate: for every such B′, every finite D-game T and position t, White to move does at least as well
   in B′ ⊞ t as Black-to-move's best in ω ⊞ t allows (make this precise; decide whether the comparison is with
   ω ⊞ t White to move, or with the Black-to-move value of ω ⊞ t, and prove which one is right). Prove necessity and
   sufficiency by hand. Say exactly where Lemma 4.15's proof uses (B1) and how (C) replaces it.
2. **Decidability on the group's own graph.** (C) quantifies over all T. Is it equivalent to a condition that can be
   computed on the finite game graph of the group alone (for instance a win, or a non-loss, in one fixed auxiliary game
   played on the group's graph, such as the group beside a mirrored copy of ω, or beside finitely many pass tokens with
   a stated rule)? Either prove such an equivalence, or prove a finite test family suffices (a finite list of D-games
   T_1, …, T_n, possibly depending on the size of the group's graph, such that results of ω beside these give results
   of ω beside all), or give evidence that no such reduction holds. A partial result with its exact scope is welcome;
   an overclaim is not.
3. **A real instance or a proof there is none so far.** Among the exact groups known (H10; Z_O on cyl:8×6 and its flat
   translates; the four cyl:8×7 groups; the five flat 8×7 groups of K59, `kings/delegate/out/K59/findings.txt`, not
   yet refereed), only Z_O and its translates fail (B1). So no known real group has the results of ω without (B1).
   If your test from question 2 is computable, implement it and run it on abstract toy groups first (see below), then,
   if memory allows, on Z_O (expected: fails, at 1…e5–e4) and H10 (expected: passes). An abstract exact group that
   fails (B1) and has the results of ω is wanted as an explicit small example, with the check.

## Checks

- Validate every general statement by brute force on abstract toy groups before believing it: random and adversarial
  exact groups (with and without checks and e.p. rights, as in `kings/delegate/out/K57/verify/src/toyref.py`; you may
  read it, but write your own generator and D-sum solver), each beside a few hundred finite D-games (loopy, with and
  without terminals, with draws). Report counts and every counterexample found on the way.
- The side-to-move, the no-move-loses rule in a sum, stalemate, checks (no move elsewhere while in check) and the e.p.
  right (cleared by a move elsewhere) are where earlier proofs went wrong. Treat each explicitly.

## Deliverables

- `PROOF.md`: statements with full hand proofs, each labelled PROVED (hand proof), CONJECTURE, or COMPUTED-1.
  Solver results are never PROVED.
- `findings.txt`: short answer first, then what was and was not checked.
- `src/` (your code), `logs/` (xz anything over 256 KB), `pids.log`.
- `EDITS.md` for `kings/theory/LOOPY.md` in the format `### EDIT title` / `<<<<<<< OLD` / old / `=======` / new /
  `>>>>>>> NEW`, each OLD matching the current file exactly once; test with
  `.venv/bin/python kings/delegate/apply_edits.py <src> <dst> <edits>` on a scratch copy. Do not edit LOOPY.md itself.
  Mark everything "not yet refereed".

## Rules

- Never kill or signal a process you did not start. Never use pkill, killall, `kill -- -1` or `kill $(pgrep …)`.
  Kill only PIDs you recorded yourself.
- Any run over a minute or over 500 MB goes through `kings/delegate/heavy.sh <cmd>` under `/usr/bin/time -l`. Design
  for under 2 GB; measure the smallest input first; no solver batches on 10-file boards. Another agent is using the
  same two slots, so expect to wait.
- Runs over 2 minutes: background, and wait for them before reporting.
- Write only inside `kings/delegate/out/K60/`. No git commands that change anything. Do not touch `paper/`, `dist/`,
  `cylcgt/`, `delegate/`, or `kings/delegate/out/K59/`.
- No binaries left behind, no absolute home paths in text files.
