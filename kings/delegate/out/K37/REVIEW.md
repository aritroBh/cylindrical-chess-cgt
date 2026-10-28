# K37 review: non-Claude check of Lemma 2.9 under (B1) (integrated 2026-10-28)

**Outcome: accepted as an audit only.** Codex (gpt-6-luna, effort high) wrote `PROOF.md` and `FINDINGS.md`. The
integrator applied `EDITS_INTEGRATOR.md` (1 block, 0 rejected, cell counts unchanged).

- **Not blind in the end.** The log (`kings/delegate/logs/K37.log`) shows this order:
  1. a first `PROOF.md` (line 753), which used a moving blockade king and flagged its own gap in answering checks;
  2. LOOPY's proof read (lines 781 and 2518);
  3. `PROOF.md` rewritten (line 2645) along LOOPY's fixed-king strategy.
  So the final proof is not independent of LOOPY's.
- **Audit.** Every step of LOOPY's proof is SOUND: the strategy, the invariants J1 and J2, king moves, pushes, e.p.,
  the recapture after each s̄ move, the induction, and the rank count behind (B1) at H = 4.
- **Not done.**
  - The brief asked for an exhaustive brute-force test with its own local-game solver. None was run, so there are no
    counts.
  - The lemma's tests remain those of K22 and its referee.
- **Label.** Lemma 2.9 stays PROVED after repair, under (B1). The status row now records the K37 audit, and that it
  is not a second proof.
