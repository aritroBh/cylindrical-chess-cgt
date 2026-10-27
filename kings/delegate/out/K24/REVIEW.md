# K24 review: predictions P6 and P7 (integrated 2026-10-27)

**Outcome: accepted with fixes.** `EDITS_FINAL.md` is K24's edits rebased onto the K19 text, which had already raised
P5–P7 to CHECKED-2. The rebase drops the referee's §5.1 block, because K19 had already fixed that error, and no longer
cites `REPORT.md`, which K24 could not write.

- **New: Lemma 2.7a (transfer from a promotion model to chess), PROVED.** If White cannot win when every promotion is
  a White win (EPW), White cannot win chess; the same holds for Black with EPB. The integrator read the proof: a chess
  winning strategy is an EPW winning strategy, because the two games coincide until the first promotion, and either
  way ends in a White win. It is complete.
- **What it gives.** EPW = EPB = D for P5 and P7 with White to move, in two implementations (K24's `mine.c` and the
  referee's `psolve.py`). So the chess value of those w-entries is a draw by the lemma, not only by kpsolve. P6 uses the
  reduction to KPK instead.
- **New facts.**
  - P6 is (L, L) in P on flat:8x8, so there is no zugzwang there.
  - The four P-model solvers agree on every entry and every per-move value. They are K19's solver, kp_p, `mine.c` and
    `psolve.py`.
- **Not repeated by the referee.** The `mine.c`/kp_p cross-check on 11,102 positions; the text says so.
- **Open.** A hand proof that White cannot win 7.2 in P is open question 7.
