# Findings

Independent blind review of Theorem 2.11K: **PROVED** under its stated hypotheses.
The blind proof uses passed-pawn geometry, the king-distance bound, and move-count timing.
After comparison, every listed LOOPY step is **SOUND**; no counterexample or proof gap found.
The new proof treats the double-step square and captures of other β pawns explicitly.
No executable solver or random-position test was run; the verdict rests on the written derivation.

## Route compared

My blind route proves the pawn invariant directly from monotone pawn direction, the e.p.-aware passed test, and H4's bound on β pawns next to p. LOOPY organizes that argument as the induction invariants \(J_\beta\), \(J_\omega\), and \(I_1\), invoking Step 2 of Proposition 2.11. Both routes use (SQ) and the triangle inequality to protect p from the king, then use H5K to exclude an earlier ω promotion. I made the timing count explicit for both move orders and separately tracked the initial double-step's skipped square. I did not rely on the proposition's proof in the blind derivation.

## LOOPY proof audit

| Item | Verdict | Reason |
|---|---|---|
| (F1) | **SOUND** | Pawn file changes require a capture onto a square occupied by a pawn; en passant also lands on the captured pawn's file. Capturing a β pawn removes it and cannot create a pawn on a previously pawn-free file. |
| (F2) | **SOUND** | This is the stipulated P rule: the first promotion wins immediately for its maker. |
| (F3) | **SOUND** | By definition, Π moves only p on β turns; ω moves on its own turns. |
| Step 1 | **SOUND** | H2 and (F1) keep all pawns off files adjacent to β's stationary king. Legal king moves keep the kings nonadjacent, so β is not in check and a push cannot expose its king. |
| Step 2 | **SOUND** | The stated induction maintains the strip-rank bounds at alternating turns; H1/H4 supply the initial bounds, and pawn captures of β pawns only remove possible blockers. It excludes both an ordinary capture of p and landing ahead of p on its file. H1's e.p.-aware clause and the same induction handle e.p. against p. |
| Step 3 | **SOUND** | After n_j king moves, (SQ) leaves distance at least two from q_j, so the king cannot capture p on that turn. At the next push, (SQ) for q_{j+1} after n_{j+1} moves leaves distance at least two from the landing square. The skipped double-step square is separately bounded and cannot be occupied before the double push; if visited afterward, it is behind p. |
| Step 4 | **SOUND** | Steps 1–3 ensure β can push legally. NS excludes stalemate at every ω turn; an ω position with no legal move while in check is mate and already a β win. |
| Step 5 | **SOUND** | Deleting p only opens squares for ω's pawns in G^K_ω; the game retains β's king and other pawns, permits their captures by ω's king, and includes the initial e.p. right. Actual legal play before p promotes is therefore represented by an allowed play in that game. H5K rules out promotion within the e moves. |
| (H3K) ⟹ (NS) | **SOUND** | On the m-th ω turn, at most m−1 king moves have elapsed. The supplied t is empty, unattacked by pawns, and not adjacent to β's king, so it is a legal king destination even if ω is in check. If e=0, there is no ω turn before promotion. |

## Tests and label

No computational test was run. The theorem did not appear false during the blind derivation, so I did not build or run `kp_p`. The statement is proved here by a written derivation; this review contributes an independent, non-Claude-family proof. This is **not CHECKED-2**, which requires two independent implementations.

**Recommended label: PROVED**, with the provenance updated to record this independent derivation. The previously reported LOOPY computational results remain claims of that report; I did not reproduce them in this task. No new numeric result was computed, so there is no numeric reproduce command to give.
