# K39: the cylinder duds in chess, and Z_B beside chess contexts (LOOPY §8 item 2, what is left)

Output: `kings/delegate/out/K39/` (write only there; no git; do not edit LOOPY.md or REPORT.md).

After K15b, K26 and K28 (LOOPY §5.7 and §8 item 2): in P, Z_B (cyl:7×6, cyl:8×6), Z_C (`Pa2 Pc4 / pa3 pc5`, kings c2/c3 and
a4/a5, cyl:8×6) and G8a/G8b (cyl:8×6) are exactly two-shuttle duds. In chess on flat 7×6 Z_B is not exactly two-shuttle
(K28: Kc3–d2 from (c3, b5) draws). Open: Z_B and Z_C in chess on the cylinder (Z_B on cyl:7×6 has cap-1 bounds (W, L);
cyl:8×6 not run), and the effect of K28's draw on chess contexts of Z_B on flat 7×6.

1. For Z_B (cyl:7×6, cyl:8×6) and Z_C (cyl:8×6): solve every root and every non-shuttle deviation in chess at cap 1, then at
   cap 2 or with the capture refinement where cap 1 does not decide. Tools: kpsolve (`kings/kpsolve.c`), and K28's
   `kq3.cpp` and `ownref.cpp` (`kings/delegate/out/K28/verify/`). Decide for each group whether it is exactly two-shuttle in chess.
2. For Z_B on flat 7×6 in chess: does Z_B still act as dud_D beside small chess contexts (one or two pawns a side on files
   e–g)? Compare the chess value of Z + H with the chess value of H with the kings parked as in K15/K26; report counts and
   every disagreement.
3. Two implementations for every value you report as CHECKED-2.
4. `FINDINGS` (as findings.txt if FINDINGS.md is refused) and `EDITS.md` for LOOPY (§5.7, §8 item 2, the P3.2′ row), each OLD once.
Memory: under 3 GB per process; a run that would need more is NOT_RUN with an estimate.
