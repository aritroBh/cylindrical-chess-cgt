# K55 review (2026-11-23)

Questions: do the other exact groups of K45 have the results of over in sums, and what is the value of Z_O (the 3 + 3
group of cyl:8×6)?

Investigator: an Opus agent (`findings.txt`, `EDITS.md`, `src/`, `logs/`). Referee: a second Opus agent with its own
solver, sharing no code with the two used by the investigator (`VERIFY.md`, `verify/`). AI work, no human
re-derivation.

## Verdict

- **The 2 + 3 group `Kg4 kf6/kg6 Pb3 Pe2 pa5 pb4 pe5` of cyl:10×6 has the results of over** against all 752 test
  games tried (3,008 results; CHECKED-2, and the referee's third solver agrees on the 124 results it re-ran, among
  them every test that separates Z_O from over). A finite battery, not a proof of equality.
- **The 3 + 3 pawn group on cyl:9×6 and 10×6 gives exactly Z_O's results** (38 differences from over on K47's 275
  tests; CHECKED-2).
- **Why they differ (COMPUTED-1, referee):** at Z_O's d4 root Black's 1…e5–e4 wins as soon as Black has one spare
  move. In the 2 + 3 group every non-shuttle Black move at either root loses against every finite reserve tried (up to
  40 spare moves); against unlimited passes some draw, none wins.
- **Value of Z_O: not identified.** Over 3,000 candidates scanned (COMPUTED-1), none survives at either root; K47's
  signatures tiny-2 and ⇑\* fail against their own negatives. The investigator's scan left {0 | tiny-30} standing at
  the d5 root; the referee refuted it.
- **Z_O is not a stopper,** and LOOPY §3 gives no order on loopy D-games, so no test here proves an equality.
- **Solver changes for width 10 are sound:** the widened hash keys are injective, full keys are compared, and the
  referee's solver finds the same component sizes. The P values agree with `kp_p --pmodel` on 300 sampled states except
  one stalemate state (a draw in P, a loss under the sum's rule that a side with no move loses); counting stalemate
  as a draw changes none of the 104 results re-run.

## Integration

The referee's replacement set `verify/EDITS.md` was applied to `kings/theory/LOOPY.md`: 3 applied, 0 rejected, table
cell counts unchanged. It changes the investigator's set where that said the 2 + 3 group "equals over", completes the
d5-root statement, cites the refutation of {0 | tiny-30}, and adds the limits (no loopy or D-game battery and no P
contexts for the 2 + 3 group; nothing on cyl:11×6 or wider).

## Process notes

The investigator's measurement runs went over the 3 GB limit several times for a short time (peak 4.0 GB) before its
watchdog stopped them; none of those outputs is used. The referee peaked at 1.68 GB. Only recorded own PIDs were
stopped; binaries removed.

## Open

Whether the 2 + 3 group is over (K56 tests a criterion and a lemma); the value of Z_O; the 2 + 3 group against loopy
test games and beside P contexts; groups on cyl:11×6 and wider.
