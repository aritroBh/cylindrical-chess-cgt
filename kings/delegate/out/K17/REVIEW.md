# K17 review: is (V1a) needed? (integrated 2026-10-28)

**Outcome: accepted with fixes.** The integrator applied `EDITS_FINAL3.md`: 6 blocks, 0 rejected, cell counts
unchanged, one new status row (P1.15) with the same cells as its table.

How it got there:
- `EDITS.md`: the investigator's edits.
- `VERIFY.md`: the referee, ACCEPT_WITH_FIXES.
- `EDITS_FINAL.md`: the first fix round (Sonnet), checked by Haiku.
- `EDITS_FINAL2.md`: the second fix round, three residual points from the Haiku check.
- `EDITS_FINAL3.md`: the integrator's two wording fixes, below.

## Result in LOOPY

- **The clause "no checks" of (V1a) is needed, CHECKED-2.** The counterexample is cyl:6×6 `Ka2 kb4 Pa3 pa4 Pd2 pe3 b -`.
  - It is P = White wins by three solvers (kp_p, K17's `refp.py` and K23's `ref3m`).
  - D gives outcome N (the referee's own D and `cylcgt`).
  - The twin with kb5 satisfies (V1)–(V4), and there P = D. A deeper example and a frozen example behave the same,
    CHECKED-2.
- **The same position is an isolated counterexample to (S1) of the sharp form** (block B1).
- **Proposition 1.15(a), PROVED.** In the structured class, (V1a) fails only by a check from a Z-pawn or by (E).
- **Proposition 1.15(b).** The bounded (E) search found no isolated counterexample. Its counts are CHECKED-2, and
  "(E) can be dropped when (HSS) holds" is a CONJECTURE within the boundary.

## Integrator fixes in EDITS_FINAL3.md (from the second Haiku check)

- **The (V1a) row's claim that (V4) holds at X.** The row cites K17's `tempo_ok` field (`check2.py`, `k17lib.py`), which
  tests (H − 2)·n + 1 < BIG with n the number of pawns. That is the bound of Definition 1.10, so it covers the tempo half
  of (V4). The row now says so and uses the JSON field names `V4_X_hss_exact`, `V4_strong` and `tempo_ok`.
- **Proposition 1.15(b).** Its sentence "the second half of (V4) … was not part of the test" now says that it is the (E)
  search that tested only (HSS). The checker had read it as contradicting the row.

## Not changed

`summary.json` is the investigator's output and stays verbatim. It still has the withdrawn 1,128 count and labels the
deeper example COMPUTED-1; LOOPY gives 752 and CHECKED-2, per the referee.
