# K59 review

2026-11-24. Investigator and referee were separate Opus agents; the referee did not see the investigator's
reasoning before writing its own solver. AI work, no human re-derivation.

## Result

- **Corollary 4.16, extended: PROVED given CHECKED-2 computations.** The four exact groups of cyl:8×7 have the
  results of over beside every finite D-game. The Black-side condition (B1) holds at all 46 non-shuttle Black root
  moves by two programs (`vgsum59`, pr56).
- **Corollary 4.17 (new): PROVED given CHECKED-2 computations.** Five exact over groups on flat 8×7, with no wrap,
  have the results of over beside every finite D-game. The smallest has 2 + 2 pawns:
  `Ka4 kc4/kc5 Pb2 Pf5 pb6 pf6`. Definition 4.8 and (B1) each rest on three separately written programs.
- Four of the five are also exact with (B1) on flat 8×8, and all five on flat 9×7 (two programs each).

## What the referee did

- Wrote its own solver (`verify/src/kref.cpp`, no shared code) and re-derived Definition 4.8 and (B1) for all five
  flat groups: same move lists, same values.
- Sanity tests of that solver: the 2 + 3 group of cyl:10×6 passes; the 3 + 3 group of cyl:8×6 fails (B1) at exactly
  1…e5–e4 and differs from over beside \*, as known.
- Direct sums with its solver: F2 and F4 beside 63 test games, F2 beside 600 random games; 0 differences from over.
- Read the diff of `vgsum59` against `vgsum`: memory layout only.
- One correction: the five groups are five placements but four shapes. F4 is F3 reflected and moved one file.

## Not done

- The referee's solver was not run on the cyl:8×7 groups; their (B1) rests on `vgsum59` and pr56.
- No search was re-run by the referee. The four file classes rest on the two search programs of K45, which agree.
- The larger-board placements (flat 9×7, 8×8) were confirmed from logs only.
- Direct sums by the referee's solver for F2 and F4 only.
- Other file classes of flat 8×7, full searches of flat 9×7 and 8×8, P contexts and chess: open.
- The new test of Theorem 4.18 was not run on these groups (they pass through (B1), so it is not needed).

## Notes

The investigator's `EDITS.md` is kept for the record; the note uses `verify/EDITS.md` (6 edits). The 1,416 per-group
log files are packed in `logs/grp.tar.xz`.
