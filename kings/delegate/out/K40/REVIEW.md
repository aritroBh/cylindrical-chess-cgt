# K40 review: Gafni's K+P v K without edges (integrated 2026-10-29)

**Outcome: accepted with the referee's fixes.** The referee's `verify/EDITS.md` (one replacement for §8 item 5) was
applied: 1 applied, 0 rejected, table cell counts unchanged.

- Referee's own sum solver `verify/src/vsum.c` agrees with K40's `kpsum.c` on 71,842,272 results (CHECKED-2); the
  bare P table agrees across four solvers on 1,056,504 positions.
- Fixes in the replacement: atlas disagreement range 0.75–3.4% (K40 said 1.4–3.0%); the odd-width fortress puts each
  king on one of the two files at distance (W−1)/2, not on one antipodal file; on 4 files 24 disagreements per board
  are underpromotion wins that the queen-only atlas misses; labels raised to CHECKED-2 and "refereed once"; H = 7 added;
  K4, K6, K8 cited.
- K40's pids.log lists 65955 and 29511 while its report says 65955 and 65981; none is running.
