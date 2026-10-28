# K33 review: blind non-Claude proofs of the K21 sum theorems (integrated 2026-10-28)

**Outcome: accepted.** Codex (gpt-6-luna) wrote `PROOF.md` (blind), `FINDINGS.md` (comparison) and `REPORT.md` (a short
pointer), with `random_tests.py`. The integrator applied `EDITS_INTEGRATOR.md` (4 blocks, 0 rejected, cell counts unchanged).

- **Blindness.** Before `PROOF.md` was written, the log (`kings/delegate/logs/K33.log`) shows only these reads:
  - `blind_packet.md`, which has the definitions and statements and no proofs;
  - skill files;
  - one search of Codex's own memory file for the project, which found nothing (exit 1).
  LOOPY and K21 were opened only after it wrote "PROOF.md is saved, so the blind phase is complete".
- **Overlap.** 46 of 2,335 5-grams (2.0 percent) and 11 of 2,332 8-grams of `PROOF.md` occur in LOOPY's section from
  "**Sums with loopy components" to Proposition 3.12. To reproduce: `python3 kings/delegate/out/K33/overlap.py
  kings/delegate/out/K33/PROOF.md "**Sums with loopy components" "**Proposition 3.12"`.
- **Verdicts.**
  - Every proof step of Theorem 3.7, Lemma 3.8a, Theorem 3.8 and Theorem 3.11 is SOUND.
  - Theorem 3.8(a)–(c), Corollary 3.8b and Corollary 3.11a follow; (c) gives necessity for dominance only, as LOOPY
    says.
  - No gap and no counterexample was found.
- **Random tests.** COMPUTED-1, one implementation; the integrator did not rerun them. To run:
  `PYTHONPATH=. .venv/bin/python kings/delegate/out/K33/random_tests.py` (seed 330027).
- **Not covered.** Propositions 3.9, 3.10 and 3.12 were not in the packet, so their labels are unchanged.
- **Codex chain note.** The chain script stopped after K33 because the K33 log contains the words "usage limit". They
  come from a quoted note about Claude agents, not from a Codex quota error.
