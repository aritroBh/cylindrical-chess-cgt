## 7. Verdicts (P model; labels as defined below; every boundary is explicit)

**Open question 2, first half: do dud groups without a pawn break exist on the cylinder? YES, in P.**
- cyl:7×6: Z_B and its mirror. cyl:8×6: Z_B, Z_C and their mirrors. Each has every non-shuttle move losing at once at all 8 roots (no pawn move that does not lose at once exists, so there is no pawn break).
- Z_C has no pawn move at all and no textbook passer; Z_B has pawn pushes at its roots (b4–b5 or a3–a4 for White, c4–c3 or b3–b2 for Black) that all lose at once, and all four of its pawns are textbook passers (each blocked by a king in P).
- Roots and move lists: **CHECKED-2** (kpp and ref3m, fresh builds). The exhaustive searches: **CHECKED-2** for at most 2 + 2 pawns on flat 7×6, flat 8×6, cyl:7×6, cyl:8×6 (a second enumerator and a second solver on all four, a third enumerator on two boards, 2.4 to 2.8 million root move lists per board, 0 differences); **COMPUTED-1** for 3 + 2, 2 + 3 and flat 7×7 (the 3 + 2 / 2 + 3 results are partly fresh, partly reused, section 8).
- Exact boundary: F_Z = {a, b, c}; at most 2 + 2 (five boards), 3 + 2 and 2 + 3 (flat 7×6, cyl:7×6, cyl:8×6); every placement with K1 and K2 and both kings on adjacent pairs, no cut-off. Nothing else is exact there. Not searched: other F_Z on flat boards, 4 or more files for duds, more than 3 + 2 pawns, 5 or 7 or 8 ranks beyond flat 7×7 (and Z_B and Z_C themselves fail on those).
- No hand proof on the cylinder (K27's 26 certificates cover flat 7×6 only). In chess nothing is claimed (the one cap-1 probe of Z_C, section 2, gives bounds (W, L): undecided).
- "No dud on the cylinder" (the earlier scratch statement of §5.3 and Appendix A) is **false in P**.

**Open question 2, second half, and Conjecture 4.7: no exact over or under group exists in any searched range (COMPUTED-1).** First half of the conjecture supported; second half (wider groups) neither supported nor refuted. Section 3 has the exact boundaries and Lemma 4.9 (PROVED).

**Exact on and off groups exist on every board searched, passer-free ones included; beside contexts they agree with Theorem 3.4(b), (c) except in a few contexts where (Pun) fails** (sections 4 and 6; COMPUTED-1).

**Z_B beside contexts:** equal to dud_D in every one of the exhaustive ≤ 3-pawn contexts (section 6). **Z_C is not** a two-shuttle component beside every context.

