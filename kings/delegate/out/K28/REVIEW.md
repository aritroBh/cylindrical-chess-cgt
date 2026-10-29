# K28 review: the five unsettled chess deviations of Z_B (integrated 2026-10-29)

**Outcome: accepted with the referee's fixes.** The investigator wrote `FINDINGS.md` and `EDITS.md`; the referee wrote
`VERIFY.md` (ACCEPT_WITH_FIXES) and replacement edits `verify/EDITS.md`. The integrator applied the replacement edits
(7 blocks, 0 rejected; table cell counts unchanged).

## Result

- Four of the five deviations lose for the mover (c4–c3 from (b2, a4), a3–a4 from (c3, b5), Kc3xc4 and Ka4xa3 from (c3, a4)).
- Kc3–d2 from (c3, b5) draws: the child `Kd2 Pa3 Pb4 kb5 pb3 pc4 b -` is exactly D (kq3 at cap 2 gives (D, D); kpsolve with
  a per-colour cap patch, White held to one queen, gives the lower bound D; `ownref` with the capture refinement gives D).
- So 25 of the 26 deviations lose and **Z_B is not exactly two-shuttle in chess**. CHECKED-2, no hand proof of the draw.

## What the referee changed

- Two more places in LOOPY still said that chess was open (the P3.2′ table row and §8 item 2); both are now edited.
- "Refuted by measurement" about K27's 20 GB estimate overclaimed: only kq3 was measured on a 4-pawn child. Reworded.
- "kpsolve and kq3 agree on every move" holds for the 3-pawn positions only. Reworded.
- The brief's statement of which side wins in rows 1 and 2 was wrong; "loses for the mover" is the test used.

## Limits

- kpsolve at cap 2 on the four 3-pawn positions was not re-run by the referee (the shared queue held its jobs for about
  four hours); it read the investigator's log. Rows 3 and 4 have two re-run implementations, not three.
- The mirror group follows by τ, by symmetry only. The effect of the draw on chess contexts of Z_B is not computed.

## Cleanup

The integrator deleted the referee's five build binaries in `verify/bin/` and a `__pycache__` file. Sources remain.
