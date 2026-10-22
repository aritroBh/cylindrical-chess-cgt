# Your part: K1a, Section 1 and Theorem 2.4

**Output directory:** `kings/delegate/out/K1a/`.

Items to fix (see REVIEWS.md):
- **Definition 1.10 and Theorem 1.11(b).** The threat set must count moves into ⊕ or ⊖ by *either* player
  (Review 1 item 1; Review 2 item 1).
- **Definition 1.5 and the remark after Theorem 1.9.** "S(X) is cylcgt.pawns.value" is false, because
  cylcgt re-splits components at every node (Review 2 item 2). State (V4) hereditarily, on the re-split
  components, with the king group Z deleted (Review 2 item 5).
- **Proposition 1.13** (Review 1 item 2; Review 2 item 3). Use A′ = { | ⊖}, whose translation is −B−1, or
  restate it for {∅ | ⊖}.
- **Theorem 3.3(b):** make it consistent with the corrected 1.13 (Review 1 item 2).
- **Theorem 1.14:** fix (ii), (iii) and the sharp form (Review 2 items 5 and 6).
- **Theorem 2.4:** restrict G to games without draws. The P-game alternative is false: Review 2 item 4
  gives a counterexample.
- **The "each hypothesis is needed" table in §1.5:** fix the (V1a) and (V1b) rows (Review 1 item 4; Review 2
  item 7).
- **(A_Q)** (Review 1 item 6; Review 2 item 8). It is false in general: `Ke2 Pb5 ka5 w -` is a
  promotion-model win and a chess draw. Make it a per-position hypothesis that kpsolve checks.
- **Definitions 1.5 and 1.10, minor items:** Review 2 items 9 and 10.
