# K34 review: blind non-Claude proofs of the K14 two-shuttle results (integrated 2026-10-28)

**Outcome: accepted, with one K34 claim withdrawn.** Codex (gpt-6-luna) wrote `PROOF.md` (blind) and `FINDINGS.md`
(comparison), with `blind_check.py` and `blind_deletions.py`. The integrator applied `EDITS_INTEGRATOR.md` (3 blocks, 0
rejected, cell counts unchanged).

- **Blindness.** Before `PROOF.md` was written, the only command in `kings/delegate/logs/K34.log` reads
  `blind_packet.md`.
- **Overlap.** 42 of 2,692 5-grams (1.6 percent) and 3 of 2,689 8-grams occur in LOOPY's section from Proposition 3.2′
  to "Which hypotheses hold" (`overlap.py`, the same script as K33's).
- **Verdicts.**
  - Lemma A, Lemma B (with the e.p. flag), Proposition 3.2′(a)–(c) and Lemma 3.2″ are SOUND.
  - Theorem 3.2‴ (a), (b) and the draw conclusion are SOUND under the stated hypotheses.
- **Random test.** 1,000 instances (seed 340027) of r(G ⊞ Z) = r(G ⊞ dud_D), 0 mismatches. COMPUTED-1, one
  implementation.
- **Withdrawn K34 claim.**
  - The claim: at G = 0, deleting one shuttle arrow changes only the source state, so LOOPY's "changes the result at all
    four states" would be FALSE.
  - Why it fails: `blind_deletions.py` does not compute that table. It only asserts that *some* outcome changes, and it
    prints exactly that.
  - The integrator's script `integrator_g0.py`, written from Definition 1.2, gives all four states changed for each of
    the eight deletions. For example, deleting the White shuttle at (z, w) gives LD, DL, DL, LD at (z,w), (z,w′), (z′,w),
    (z′,w′). This agrees with LOOPY's "One arrow" example and with the K14 referee's table.
  - The G = 0 statement is now CHECKED-2.
