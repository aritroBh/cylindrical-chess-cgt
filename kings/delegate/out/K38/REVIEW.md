# K38 review: hand proof for P5 (integrated 2026-10-29)

**Outcome: accepted with the referee's fixes.** The referee's `verify/EDITS.md` (7 edits, the same OLD texts as K38's)
was applied: 7 applied, 0 rejected, table cell counts unchanged.

- K38 proved P5 w a draw by hand in P, EPW, EPB and chess on cyl:7×6 and flat 7×6, without Lemma 2.7a (`PROOF.md`).
- The referee re-derived every case of Lemma D, Parts 0, A, B, C and Lemma K′, and re-checked them with its own code
  (`verify/rgen.py`, `rcheck.py`, `rlemmaK.py`): 296 invariant positions per board, 0 failures; damaged invariants are
  rejected.
- Fix: K38 counted K28's `ownref` as a second chess solver on flat. `ownref` has no double step and c5 is on Black's
  second rank, so it solved a different game. The chess values rest on kpsolve cap 2 and the referee's `rchess.cpp`
  (cap 1, A = B), CHECKED-2 on both boards.
- Integrated together with K40 and the K41 fixes in one commit.
