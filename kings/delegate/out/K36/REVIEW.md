# K36 review: blind non-Claude proof of Theorem 2.7 (integrated 2026-10-28)

**Outcome: accepted.** Codex (gpt-6-luna, reasoning effort high) wrote `PROOF.md` (blind), `FINDINGS.md` and
`REPORT.md`. It ran no computations. The integrator applied `EDITS_INTEGRATOR.md` (2 blocks, 0 rejected, cell counts
unchanged) and edited the K7 caveat in the preamble.

- **Blindness.** In `kings/delegate/logs/K36.log`:
  - before `PROOF.md` (line 759), the only reads are the packet, `kings/SPEC.md`, the kpsolve header, and a search of
    Codex's memory file that found nothing;
  - LOOPY is first opened at line 1353.
- **Overlap.** 36 of 1,959 5-grams (1.8 percent) and 3 8-grams occur in LOOPY from Theorem 2.7 to Corollary 2.8
  (`overlap.py`).
- **Verdicts.**
  - All of these are SOUND: Steps 0–6 (I2–I5 included), part (a), the window form (b), and the K3 remark.
  - The list "The conditions cannot be dropped" is consistent with the theorem's scope. K36 did not recompute its
    examples.
- **The one gap, and its repair.**
  - The gap: Step 0 (I1) cites Lemma 2.2 "applied from Q". In (b), s's king may stand off F_Z, so Q need not be a
    position of Definition 2.1.
  - Why it does not matter: the proof of Lemma 2.2 uses only the pawn placement and the empty buffer, never the kings.
    The integrator checked this against the proof text.
  - The repair: a sentence saying so is added to Step 0.
- **Label.** Theorem 2.7 stays PROVED after repair, in P. It is now re-derived once outside the Claude family.
