# T78 — Referee: the one-sided extension of Corollary 3.8b (reservoirs `on` / `off` beside short components)

Output directory: `delegate/out/T78/` (create it). Write `REPORT.md` there and any scripts you use. Do not edit
anything else. Never run git. NEVER use pkill, killall, `kill -- -1` or `kill $(pgrep ...)`; signal only PIDs
you started and recorded yourself. Keep every process under 2 GB and under 30 minutes; if `nice` is denied by
your sandbox, run without it.

## What to referee

File: `kings/theory/LOOPY.md` (a long note on loopy games for king-and-pawn sums; the definitions you need are
Definition 1.10 (safe), the reserves λ, ρ, Λ_B, the quantities M_L(K), M_R(K), "event", "criterion", the
D-result, the translation K^B, Theorem 3.7, Lemma 3.8a, Theorem 3.8, Corollary 3.8b and Proposition 3.9). The
same text, lightly edited, is in `dist/tog/supp_src/s12_kings.md`.

Directly after Corollary 3.8b the note claims, without a separate proof:

> `on` and `off` are not covered by the corollary as stated (ρ(on) = λ(off) = ∞) but satisfy Theorem 3.8
> directly: S = on when K has no ⊖ event (only the σ = + condition is needed, and Λ(on) = 0), S = off when it
> has no ⊕ event, with K pairwise safe and B ≥ 1 + max(M_L(K), M_R(K)).

The note itself says this extension "has not been checked by an independent referee" (it was only tested on
1,810 random instances). You are that referee.

## Tasks

1. **Proof check.** Read Theorem 3.8 and its proof in full and decide whether the one-sided claim follows.
   Write out the argument step by step, quoting the exact hypothesis of Theorem 3.8 each step uses. Pay
   attention to: (a) whether Theorem 3.8's criterion really needs only the σ = + inequality when no ⊖ event is
   reachable, or whether its proof uses the σ = − inequality somewhere else (for example in an induction over
   positions where a ⊖ event could become reachable after a move in K); (b) what "K has no ⊖ event" must mean
   (at the root only, or at every reachable position of S ⊞ K?) for the argument to go through; (c) whether
   the bound B ≥ 1 + max(M_L(K), M_R(K)) is the right one or whether only one of M_L, M_R is needed / a larger
   B is needed; (d) the symmetric statement for `off`.
2. **Independent test.** Write your own small solver from the definitions (do not import the note's
   `dsum.py` or other code under `kings/`): compute the D-result of S ⊞ K by brute force on the loopy game
   graph, and the outcome of S + Σ K_i^B, for S = on (and S = off), K = 1 to 3 small short components with
   ⊕/⊖ events, enumerated exhaustively up to a small size (state the bound) rather than sampled. Report the
   number of instances, how many satisfy the hypotheses, and any counterexample (smallest first) — both to the
   claim as stated and to the natural weaker readings in (b).
3. **Verdict.** One of: CORRECT AS STATED; CORRECT WITH A CLARIFIED HYPOTHESIS (give the exact wording);
   WRONG (give the counterexample). Say plainly what you did not check.

Be sceptical: an earlier proof in this project passed two AI referees and was later refuted by a 3-pawn
counterexample outside the range of its exhaustive check. If the definitions in the note are ambiguous on a
point that matters, say so and test both readings.
