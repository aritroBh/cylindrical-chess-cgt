# K35 review: blind non-Claude check of Theorem 2.11K (integrated 2026-10-28)

**Outcome: accepted as an audit; not as a complete independent proof.** Codex (gpt-6-luna) wrote `PROOF.md` (blind),
`FINDINGS.md` (comparison) and `REPORT.md`. It ran no computations. The integrator applied `EDITS_INTEGRATOR.md`
(2 blocks, 0 rejected, cell counts unchanged).

- **Blindness.** Before `PROOF.md` was written, the log (`kings/delegate/logs/K35.log`) shows these reads, none of
  which contains the proof:
  - `delegate/COMMON.md`, `RESULTS.md` and `RESEARCH_PLAN.md` (neither mentions Theorem 2.11K, (SQ) or (H5K));
  - `blind_packet.md`;
  - `cylcgt/pawns.py` and the kpsolve header;
  - a search of Codex's memory file.
- **Overlap.** 15 of 1,594 5-grams (0.9 percent) occur in LOOPY's block from "**Real-king square rule" to
  CONJECTURE′ (`overlap.py`, the same script as K33's).
- **Audit.** It marked every step of LOOPY's proof SOUND: (F1)–(F3), Steps 1–5 and (H3K) ⟹ (NS).
- **Gap in K35's own proof** (found by the integrator).
  - What it misses: section 1 argues that no ω pawn can capture p, but it treats only ω pawns already on the files
    next to p. An ω pawn can also reach such a file by capturing a β pawn there. Section 1 uses (H4) only for landing on
    p's own file.
  - Why the statement still holds: (H4) puts that β pawn at ρ ≤ ρ(p₀) + 1. So the capturing pawn lands at most one rank
    ahead of p's starting square, and only while p is still there (s = ω, first move). β then pushes, and the pawn,
    which attacks toward smaller ρ, never reaches p.
  - LOOPY's Step 2 invariants (J_β), (J_ω) cover this case.
  - So K35 is a sound audit of LOOPY's proof, but its PROOF.md is not a complete second proof.
- **Label.** Theorem 2.11K stays PROVED in P, with the K35 audit recorded and the remaining gap in K35's own proof
  stated.
