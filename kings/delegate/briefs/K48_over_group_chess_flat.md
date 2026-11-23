# K48: the K45 over group in chess, and on flat and taller boards

K45 found the exact over group Z_O = `Kf5 kd4 Pb2 Pb4 Pe2 pa4 pb5 pe5` on cyl:8×6 in plain P (Definition 4.8,
CHECKED-2), on files a, b, e. Read LOOPY Definition 4.8, the K45 bullet, K45's findings and VERIFY, and how K28 and K39
took Z_B and Z_C to chess (cap 1 with the capture refinement, cap 2 with one officer a side).

1. Chess. Solve the two roots of Z_O and every child (all moves of both sides, and the positions after each freeze) in
   chess on cyl:8×6: kpsolve at cap 1 (both bounds), then the capture refinement or restricted cap 2 where cap 1 leaves
   a gap, as in K39. Is Z_O still "every move but the freeze loses, and after the freeze both sides to move lose"?
   List each move whose chess value differs from its P value. Two solvers for every value that matters.
2. Flat boards. K45 searched cylinders only. Run the Definition 4.8 test (K45's code as one implementation, your own or
   the K45 referee's `r45.cpp` as the second) on flat 8×6, 9×6 and 10×6: at most 3 + 3 pawns on three files within a
   six-file span, every king placement. Does an exact over group exist without the wrap?
3. Taller boards, if time allows: the same three files on cyl:8×7 and cyl:8×8.
4. Output findings.txt and EDITS.md for LOOPY (the K45 bullet, Conjecture 4.7 status row, §8 item 2).
