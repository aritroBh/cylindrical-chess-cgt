# K15b + K26 review: dud and over groups on the cylinder (integrated 2026-10-29)

**Outcome: accepted with both referees' fixes, merged.** K15b (`../K15/FINDINGS.md`, referee `../K15/VERIFY_K15b.md`,
replacement blocks `../K15/verify/EDITS.md`) and K26 (`../K26/FINDINGS.md`, referee `../K26/VERIFY.md`, replacement
blocks `../K26/verify/EDITS.md`) edit the same passages of LOOPY, and both were written before K28 (2061cea4). A merger
wrote one rebased edit set (`EDITS_MERGED.md`, reconciliation in `MERGE_NOTES.md`). Three independent checkers
(numbers and labels, consistency of the note, the K15b/K26 reconciliation) found 14 points, all accepted by the fixer
(`EDITS_FINAL.md`, MERGE_NOTES section 5). The integrator applied `EDITS_FINAL.md`: 9 blocks, 0 rejected, table cell
counts unchanged.

## Result

- Open question 2, in P: yes. Z_B (cyl:7×6, cyl:8×6), Z_C (cyl:8×6) and G8a/G8b (cyl:8×6) are exactly two-shuttle
  duds without a pawn break. CHECKED-2 for boards of width at most 8; widths 9 and 10 are ref3m only (COMPUTED-1).
- Chess: G8a/G8b have the same move values at cap 2 (COMPUTED-1, one solver family). Z_B and Z_C on the cylinder in
  chess are open.
- No over group in either search: the second half of Conjecture 4.7 has no support; "none exists" is not claimed.

## Reconciliation

No real contradiction. K26's scope (F_Z = {a, b, c}) excludes G8a/G8b (files a and e); K15's census contains Z_C's
mirror and Z_B. Counts differ in kind: K15b's recount 24/23/14/7 counts groups up to symmetry, K26 counts exact
placements. K15's earlier 43/40/25/9 are not invariants.

## Integrator's decisions

- Accepted the fixer's raising of the cyl:8×8 Z_C-one-rank-up check to CHECKED-2: two solvers (kp_p and ref3m) agree in
  a checker's run (`check2/zc88.*`).
- §4 order is now Conjecture 4.7, Definition 4.8, Lemma 4.9.

## Cleanup

The integrator deleted seven build binaries in `../K15/verify/bin/` and compressed raw files over 256 KB in K15 and K26
with xz. Not committed: nothing was dropped.
