# K23 review: the zero is context-dependent (integrated 2026-10-27)

**Outcome: accepted with fixes.** The edits went into `kings/theory/LOOPY.md` through `EDITS_FINAL.md`, which is
K23's ten blocks rewritten by a fix-round agent. That rewrite fixes all nine problems in `VERIFY.md` and adds four
new blocks, mostly for stale text.

- **Label.** The example (Z_T acts as 0 beside {Pe3, pe4} and not beside {Pe2, pe3} on cyl:7x6) is
  **CHECKED-2, with three implementations agreeing**: the kpsolve family, `pk2.c`, and the referee's `ref3.cpp`. It is
  not "PROVED by example", because no hand proof is given. `summary.json` still says "PROVED by example" and is
  superseded by this review.
- **Integrator re-runs**, all with the referee's generator and its independent solver `ref3`:
  - cyl:7x6, contexts on e–f, ≤ 3 + 3 pawns, ranks 2–5: 3,237 contexts, 99 differ (4 with a passer, 95 without);
    39 passer-free ones with frozen (L, W); 44 (context, side to move) pairs; 0 unresolved. This matches the agent's
    numbers, which the referee could not re-run for lack of a lock slot.
  - cyl:8x6, the 81 single-file contexts on f with ≤ 4 + 4 pawns: 0 differ, as the agent says.
  - The mirror G1′ = {Pf3, pf4}: Φ = Ψ = (L, W), as the agent says.
- **Known bug in `ref3`.** It reads the board size at offset 4 of the `--board` string, so `flat:WxH` silently gives
  X for every position; pass `flat7x6` instead. K23 used cylinders only, so it is unaffected.
- **Still open.** The general statement for every frozen group with T ≥ 2 remains a CONJECTURE, now open question 6.
  The chess draws in P4 are chess-only effects whose cause was not examined.
