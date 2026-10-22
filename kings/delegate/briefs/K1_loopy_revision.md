# K1: revise the A8 theory note after four adversarial reviews

**Output directory:** `kings/delegate/out/K1/` (create it). Write only there.

## Inputs (read completely)

- `kings/theory/LOOPY.md`: the theory note (labels PROVED / CONJECTURE / KNOWN on every claim). Do not edit
  it in place.
- `kings/theory/REVIEWS.md`: four referee reports on it, verbatim, with numbered items.
- `kings/results/PREDICTIONS.md`: what the exact chess solver `kings/kpsolve` found for the note's §6
  predictions, with two baselines.
- `kings/results/theory_P4_cap2_moves.txt`: the move values explaining why prediction P4 fails.
- `kings/SPEC.md`: the exact chess rules the solver uses.

## Task

Write `kings/delegate/out/K1/LOOPY.md`, a revised copy of the note that answers every numbered review item.

1. **Status table.** Right after the title block, add a section "Status after review (2026-10-21)". Give a
   table with every numbered result (definitions excluded), its final label, and a one-line note citing the
   review item. Labels:
   - **PROVED** (unchanged and sound per the reviews);
   - **PROVED after repair** (only if you write the complete repaired proof);
   - **FALSE as originally stated → corrected statement**;
   - **CONJECTURE**;
   - **GAP: proof incomplete**;
   - **KNOWN**.
   If you cannot complete a proof, the label is GAP or CONJECTURE, never PROVED.
2. **Repairs** (mark each inline as "(revised after review: Rk item n)"):
   - **Definition 1.10 and Theorem 1.11(b).** The threat set must count moves into ⊕ or ⊖ by *either*
     player.
     - State (V4) hereditarily, on re-split components (cylcgt re-splits at every node), with the king
       group Z deleted.
     - Correct the claim "S(X) is cylcgt.pawns.value", and the remark after Theorem 1.9.
   - **Proposition 1.13 and Theorem 3.3(b).** Use A′ = { | ⊖}, whose translation is −B−1, or restate for
     {∅ | ⊖}. Make 3.3(b) consistent.
   - **Theorem 2.4.** Restrict G to games without draws (the P-game alternative is false: Review 2 item 4).
     Fix the "sharp form" of Theorem 1.14 (Review 2 item 6).
   - **Theorem 2.7 and Definition 2.6.** Replace the invalid pass-budget step by the k = ∞ argument plus
     (L3), if you can write it rigorously.
     - Drop "every k is needed".
     - Note that (L3′) cannot apply for T ≥ 2 on a 3-file group.
   - **Proposition 2.10(a):** needs H ≥ 5.
   - **Lemma 2.9:** state the hidden hypothesis (the defender has no pawns the attacker's pawns can
     capture).
   - **Proposition 4.3:** correct it, or downgrade it.
   - **(A_Q)** is false in general:
     - `Ke2 Pb5 ka5 w -` is a promotion-model win but a chess draw;
     - so is flat 4×4 `Kd1 Pb3 ka3 w -`.

     Make it a per-position hypothesis checked by kpsolve.
   - **The "each hypothesis is needed" table:** fix the (V1a) and (V1b) rows.
   - **Labels:** fix unlabelled claims and the label misuses the reviewers list (Remark 2.11, P11, §5.5,
     §5.6, "PROVED (diagram audit)").
3. **§6.**
   - Add kpsolve's result for every prediction.
   - **P4** (a CONJECTURE) is refuted in 3 of its 6 contexts. Give the mechanism, and note that it is
     consistent with Proposition 2.10(b).
   - Replace the "naive convention" headline with the honest comparison. Literal cylcgt gets P2, P3 and P10
     right, so those do not separate the theory from cylcgt. The cases that do are P1, P5, P7, P9 and P4.
4. **Evidence mismatches.** Fix the minor ones the reviewers list: Appendix A pawn counts, pass budgets, §5.5
   Kd3, P2 + H* e3–e4.

## Deliverables

- `kings/delegate/out/K1/LOOPY.md`.
- `kings/delegate/out/K1/REPORT.md`: first a 5-line summary, then the status table, then every change with
  its review item.

You may run the solver to check positions: build it with
`cc -O2 -o kings/delegate/out/K1/kp kings/kpsolve.c`, then pipe in a position, for example
`echo "Ka5 Pb4 kc6 pb5 w -" | kings/delegate/out/K1/kp --board cyl:7x6 --cap 1`. Keep runs small.
