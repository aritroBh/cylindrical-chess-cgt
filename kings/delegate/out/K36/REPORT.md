# K36 report

**PROVED:** Theorem 2.7(a) and its window form (b) hold in P under (L1)–(L3).
**PROVED:** The projection argument covers king/Z-pawn moves and treats context-pawn moves as passes.
**PROVED:** (L2)'s μ_s ≥ T+1 blocks context promotion through s's T-th turn; (L3) excludes real stalemate.
**GAP:** LOOPY Step 0 applies Lemma 2.2 outside its stated both-kings-on-F_Z setup in (b); a direct pawn-movement induction repairs it.
**CHECKED-2:** Not claimed; this review is an independent proof audit, not a second computation or solver run.

## Files

- [PROOF.md](PROOF.md): blind proof written before reading LOOPY.
- [FINDINGS.md](FINDINGS.md): comparison, step-by-step audit, conditions-list review, and recommendation.

## Verification

No code, solver, or tests were run. There are no computed counts to reproduce. The listed K7 P-solver examples remain reported data and were not independently rechecked here. The recommended theorem label is **PROVED (in P), after the Step 0 wording repair**; no chess or D-model conclusion is claimed.
