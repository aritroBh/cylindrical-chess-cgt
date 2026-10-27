# K14 review: two-sided Proposition 3.2, and the group Z_B (integrated 2026-10-27)

**Outcome: accepted with fixes.** `EDITS_FINAL.md` is K14's 14 blocks, rewritten after `VERIFY.md` by a fix-round
agent. It went into LOOPY with three more wording fixes by the integrator.

- **The negative search result is withdrawn.** K14 searched for an exactly frozen two-shuttle group with a move-count
  cut-off of 18. The referee searched flat 7x6 without it (817,270 placements) and found **Z_B**: White king b2/c3,
  Black king a4/b5, pawns Pa3 Pb4 pb3 pc4, and its mirror. In P every non-shuttle move loses at once at all 8 roots,
  and the shuttle draws. K14's own script lists Z_B with score 26 once the cut-off is raised to 40.
- **Integrator check.** The K23 referee's independent solver `ref3`, run with `--board flat7x6` (a parsing quirk:
  `flat:7x6` gives X everywhere), gives D at all 8 roots and the same move lists as kp_p. So Z_B alone is CHECKED-2 in
  P. The lists hold 26 non-shuttle moves, not the 27 the referee wrote.
- **Contexts.** These are COMPUTED-1, from the referee's kp_p run. Z_B matches r(G + dud_D) in 68 + 12 contexts and in
  the first 660 of 885 contexts with ≤ 2 + 2 pawns on f, g, with 0 differences; 225 contexts are untested. Z_A differs
  from it in 58 of those 885.
- **Chess is undecided.** With cap 1 the bounds at the 8 roots are (W, L). Wave 3 (K26, an exact group census without a
  cut-off; K27, a hand proof of Z_B and its chess status) follows this up.
- **Integrator wording fixes.** The §0 summary now says the D-model statement needs (Pun) and (A_Q) in chess. K14's
  search totals (6,674 and 1,147) are now an unreproduced record of what its script printed. Remarks about other jobs'
  slots are removed.
