# Your part: K1c, Sections 3–6 and Appendix A

**Output directory:** `kings/delegate/out/K1c/`.

Items to fix (see REVIEWS.md, especially Review 4 and Review 1 items 5, 10, 11):
- **Theorem 4.2:** the gap.
- **Proposition 4.3:** false as stated (a check counterexample). Correct it, or downgrade it.
- **§4 commentary:** the minor items.
- **§5 labels and wording** (§5.1 "PROVED (diagram audit)", §5.2, §5.5, §5.6, "So Z_onT1 realises on"):
  label every unlabelled claim.
- **§6:**
  - Add kpsolve's result for every prediction, from `kings/results/PREDICTIONS.md`.
  - P4 (a CONJECTURE) is refuted in 3 of its 6 contexts: H\* and H\*2 (White to move draws), and H0 (Black to
    move draws). The mechanism is in `theory_P4_cap2_moves.txt`: the defending king walks to the locked
    context pawns. This is consistent with Proposition 2.10(b).
  - Replace the "naive convention" headline with the honest comparison. Literal cylcgt gets P2, P3 and P10
    right, so those do not separate the theory from cylcgt. The cases that do are P1, P5, P7, P9 and P4.
  - The P2 + H\* note: e3–e4 stalemates Black.
- **Appendix A and Conjecture 4.7:** the pawn-count mismatch.
