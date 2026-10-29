# K39 review: Z_B and Z_C in chess on the cylinder (integrated 2026-10-29)

**Outcome: accepted with the referee's fixes.** The first investigator was stopped by a network error after its runs;
a second one finished from those runs, re-running only the four part-2 runs cut off by the time limit. The referee
wrote a third solver (`verify/rf39.cpp`, from SPEC.md) and reproduced every root and move value. Its full replacement
set `verify/EDITS.md` was applied: 8 applied, 0 rejected, table cell counts unchanged.

- Fix in the edits: beside context e2/e4, Kc3–d2 from (c3, b5) loses, and Kc3–d2 from (c3, a4) is the drawing move
  instead; beside e2/e3 it is illegal. K39's text said it stays D beside all (D, D) contexts.
- `findings.txt` repeats that error (section 0 item 4 and section 3) and omits context 3 as a decisive context;
  `logs/part2_table.txt` and `VERIFY.md` are correct and take precedence.
- Not run: cap 2 for the 4 undecided Black-to-move roots of Pe4 / pf4 (over 3 GB), and the other 4,413 contexts.
