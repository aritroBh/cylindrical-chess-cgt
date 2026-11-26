# K65 review (orchestrator, 2026-11-25)

Item: census of exact over groups (Definition 4.8) on the flat 8×8 board, classification of every group by (B1),
condition (C) and ladder length N\*, chess verdicts from the tablebase. Three parties: the investigator
(`findings.txt`), the referee (`verify/VERIFY.md`), and a separate checker for the referee's own findings
(`kings/delegate/out/K66/VERIFY.md`).

## What entered the note (`kings/theory/LOOPY.md`)

1. Corollary 4.17's paragraph: the census of {b,c,f} and {b,e,f} (23 and 25 groups, 38 distinct, 26 up to reflection
   and file translation, four with 2 + 2 pawns in three shapes); (B1) for 27, not for 11; chess verdicts.
2. Corollary 4.19: real groups with the results of ω without (B1) exist (seven in the census; one described move by
   move). The sentence "No known real group has the results of ω without (B1)" is gone.
3. Proposition 4.24 (new): a real exact over group with N\* = 3, `Kg5 ke5/ke6 Pb2 Pf2 Pf6 pc4 pf5 pf7`. The remark
   after Corollary 4.23 now asks for N\* ≥ 4.
4. The open-questions line.

## Labels and their basis

- {b,c,f}: CHECKED-2 (p45a, r48). {b,e,f}: the count 25 is COMPUTED-1 (p45a); the referee's r48 run on this class was
  still going when this review was written. Each of the 38 groups is exact by three programs.
- (B1) for all 38, Aux at every failing move, ladders: ax65 and pk_sum (both by the referee) and, for the 11 groups
  where (B1) fails, k66 (the K66 checker, written without sight of the referee's code): three programs, two authors.
  (B1) for the 27 groups where it holds was not rechecked by K66.
- Proposition 4.24: PROVED given CHECKED-2 computations (Theorem 4.18 and Corollary 4.19 applied to computed values;
  all values confirmed by K66).
- Chess: KNOWN (Syzygy through the Lichess API, 120 lookups by the referee, 23 re-probed by K66, all equal). Five of
  the 19 groups with at most seven men are exact over groups in chess. The reading: Definition 4.8 with chess values,
  every non-losing White root move counted as a freeze. Nothing is claimed about sums or contexts in chess.

## Changes made at integration

- The referee's edits applied (5 of 5), then K66's one edit (a citation: Theorem 4.18 (b), (c) instead of Corollary
  4.19).
- By hand: the label of the {b,e,f} count (COMPUTED-1 until r48 ends); K66 named where its program adds a check; the
  reading used for the chess verdicts and the sentence that nothing is claimed about sums in chess; two lines of play
  for Proposition 4.24 from K66; one sentence in Corollary 4.23's paragraph (three groups with N\* = 2, one with 3).
- The investigator's `EDITS.md` is superseded and was not applied.

## Process notes

- The investigator broke the memory rule: eight group-check runs passed 3 GB (highest 3.52 GB); its watchdog polled
  every 2 seconds and the chain went on after kills. It stopped its own processes. The referee and the checker stayed
  under 1.5 GB (watchdog on the solver's own process, ten polls a second, limit 2.0 GB, no kill).
- Not searched: {a,b,e}, {a,d,e} (K67 running), seven two-file classes outside the four three-file classes, other
  shapes. Not checked: the near-miss counters; groups with eight men in chess (no tablebase).
