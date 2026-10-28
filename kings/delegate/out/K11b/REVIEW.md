# K11b review: blind re-derivation of Proposition 2.11 (accepted, 2026-10-27)

- **Model.** Codex (gpt-6-luna), launched with NOFALLBACK=1, so the OpenCode fallback that copied the proof in K11
  could not run. The log is `kings/delegate/logs/K11b.log`.
- **Blind order kept.** Before writing `PROOF.md` it read only LOOPY lines 1317–1350 (Setting to Statement),
  `cylcgt/pawns.py` (`passed`, `ep_capturable`, `promote_distance`) and the header and move generator of
  `kpsolve.c`. It read Steps 0–5 afterwards. One recursive search in Phase 2, after the draft existed, printed
  matching lines from the K10 and K12 outputs. It reports this itself.
- **Not a copy.** I compared lower-cased words with `difflib`: the final `PROOF.md` matches LOOPY's proof in 197 of
  its 1,479 words (13%), against 96% for K11. 65% of the blind draft in the log survives in the final file. The edits
  after the comparison made the en-passant-to-path case explicit and tightened the projection to G_ω.
- **Integrator's reading.** The proof is complete: p cannot be captured (ordinary or e.p.) or blocked, β's pushes are
  legal, ω always has a legal king move, ω's pawn play projects into G_ω, and the timing gives e = d − 1 or d. It uses
  each of (H1)–(H5) once.
- **Its new point, adopted in LOOPY's P11 row.** At a root race `value()` raises RaceError, so W(X) is undefined and
  the root clause needs a convention. K12 used the count rule with N the side to move.
- **No kpsolve batch was run.** None was needed, because no hypothesis was claimed redundant and nothing was found
  false.
