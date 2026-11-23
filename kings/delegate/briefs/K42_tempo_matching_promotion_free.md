# K42: tempo matching, the promotion-free form (LOOPY §8 item 1)

Read LOOPY §8 item 1 in full (K18's tests, Proposition 8.1 and its hypotheses (P1a)–(P1e)).
The promotion-free form is a CONJECTURE supported by every K18 test. Goal: settle it.

1. State the promotion-free form precisely (contexts with no pawn race, plain-only sortie, punisher
   second-player win in the context). Say which reading of "tempo answered by tempo" you prove.
2. Try a hand proof (strategy stealing / copying the defender's context tempo, as in the sharp form of
   Theorem 1.14). If a hypothesis of Proposition 8.1 can be dropped under promotion-freeness, prove it.
3. In parallel, search for a counterexample beyond K18's range: |F_Z| = 3 groups with up to 3 + 3 pawns,
   cyl:7×6, cyl:8×6, cyl:9×6, promotion-free contexts with up to 2 + 2 pawns. Reuse K18's `lg.cpp` only as a
   second check; write your own solver from SPEC.md and Definition 2.6.
4. Output: findings.txt, PROOF.md if a proof is found, EDITS.md for LOOPY §8 item 1 (and the status table
   row if the label changes). Labels: PROVED only for a hand proof; solver results CHECKED-2 at most.
