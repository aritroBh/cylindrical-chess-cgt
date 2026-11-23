# Theorem 2.7: timing clause corrected (integrated 2026-11-23)

Source: a Codex re-read of the paper's proofs appendix (`delegate/out/T83/REPORT.md`, section A.16) found that the
timing clause of Theorem 2.7(a), "it plays r and then wins with one of its next T moves", is false: the reply r can
already mate in the real position, helped by a context pawn that covers a square beside the king, although the
projection is not a local mate. Example: flat board, F_Z = {a, b}, `Ka6 Pb6 Pb7 Pd6 / Ka8 Pa7 Pe7`, Black to move:
m = Kb8 is forced and r = b6×a7 is mate (d6 covers c7), while the local game has Kc7 and a8=Q.

One agent verified the example against Definitions 2.1, 2.5 and 2.6 (and found a variant not in check at the root,
`Ka6 Pb6 Pb7 Pd6 / Kb8 Pa7 Pa3`), checked every use of the timing, and drafted `EDITS.md` (7 edits: 7 applied,
0 rejected, cell counts unchanged).

- The P-win of Theorem 2.7 stands. The statement now says s̄ wins by a promotion or a mate no later than its T-th move
  after r, and that r itself may mate. Steps 5 and 6 treat a real mate before projecting.
- Not affected: 2.7(b), Corollaries 2.7′ and 2.8, Proposition 2.10(a), §5, Propositions 8.1 and 8.1′ (their hypotheses
  keep s's king off squares that context pawns attack, so there a real mate is a local mate).
- The stalemate side has no gap: (L3) is stated over real plays, so a real stalemate that the projection does not see
  is excluded by hypothesis.
- The repair is one AI derivation of a finding from outside the Claude family; a Codex read of the repaired text is
  queued.
