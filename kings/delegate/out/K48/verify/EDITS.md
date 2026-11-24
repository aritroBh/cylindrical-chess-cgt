### EDIT Conjecture 4.7, K45 bullet, K48 addendum (K48, 2026-11-23; referee version)
<<<<<<< OLD
contexts that are D-sums, widths 13 and 15 and beyond 16.
=======
contexts that are D-sums, widths 13 and 15 and beyond 16. K48 (2026-11-23; `kings/delegate/out/K48/findings.txt`, `VERIFY.md`; AI work, no human re-derivation). Every group named in this addendum is exact in the sense of Definition 4.8 only; none of their values in sums was computed, and the cyl:8×6 group is not over (K47). *Chess.* The cyl:8×6 group in chess at cap 1, with and without the capture refinement (kp39 and own39, two code families, agree on every root and move value: CHECKED-2 as bounds). The d4 freeze survives exactly: the root (kd4, White to move) is exactly W, e2–e4 wins, and its q (`Kf5 kd4 Pb2 Pb4 Pe4 pa4 pb5 pe5`) is an exact mutual zugzwang in chess, as it is in P (K47's hand proof) (Black to move: all 4 moves lose; White to move: all 6 lose; both bounds agree, so promotions beyond the cap do not matter there). The other three roots, the d5 freeze e2–e3 and its q stay at bounds (W, L). Of the 49 move values at the four roots and at the two q's (each with both sides to move), 28 are exact, and all 28 agree with P (27 lose at once, e2–e4 wins); 21 are undecided (for 9 of them, White king moves, chess excludes a White win). So no move is known to have a chess value different from its P value, and whether the group is exact in chess is open; restricted cap 2 (one officer a side) was started and not completed. Chess on flat boards was not run. *Flat boards.* The group needs no wrap: on flat 8×6 the exhaustive search (every class of three files within a six-file span, one per left-right reflection, at most 3 + 3 pawns on ranks 2 to 5, every king placement; K45's implementation A and the K45 referee's solver adapted to flat boards agree counter for counter on all 20 classes: 2,515,002,479 placements per orientation, exactly 3 exact over groups of Definition 4.8 up to left-right reflection; CHECKED-2) finds exactly this group and its translates by one and two files (`Kg5 ke4 Pc2 Pc4 Pf2 pb4 pc5 pf5`, and the reflection of the translate to files c, d, g), each with its left-right reflection and its mirror under group; ref3m and kp_p confirm the three over groups and their mirrors. On flat 9×6 and 10×6 every translate whose White king fits on the board is exact (4 resp. 5 groups; both implementations on the classes of this shape, CHECKED-2; ref3m on 9×6 and kp_p on both widths confirm each translate); the other classes of those widths were not searched. *Taller boards.* On cyl:8×7 with pawns on files a, b, e (ranks 2 to 6) there are 4 exact over groups of Definition 4.8 (exactly 4 in the search with at most 3 + 3 pawns on these files: implementations A and R agree counter for counter, and ref3m and kp_p confirm each group; CHECKED-2), e.g. `Kd4 kf4 Pb3 Pb5 Pe2 pb4 pb6 pe6` (Black shuttles f4–f5, freezes e2–e4 and e2–e3); the cyl:8×6 group itself is not exact on cyl:8×7 ((O1) fails: Kd4–c4 and e5–e4 do not lose). Other file classes of cyl:8×7, and cyl:8×8, were not searched.
>>>>>>> NEW

### EDIT Conjecture 4.7, To settle, chess (K48, 2026-11-23; referee version)
<<<<<<< OLD
chess (kpsolve was not run for any over candidate)
=======
chess (kpsolve was not run for any over candidate; K48, 2026-11-23, ran it for the cyl:8×6 group: at cap 1 only the d4 freeze and its zero are settled, the rest needs cap 2; see the K45 bullet)
>>>>>>> NEW

### EDIT C4.7 status row, K48 (K48, 2026-11-23; referee version)
<<<<<<< OLD
cyl:10×6, 11×6, 12×6 (F4 = 0) | R1 item 10
=======
cyl:10×6, 11×6, 12×6 (F4 = 0). K48 (2026-11-23): the group is exact in the sense of Definition 4.8 also on flat 8×6, where it and its two translates are, up to left-right reflection, the only exact groups of the six-file-span search (CHECKED-2), and on flat 9×6, 10×6 (translates); on cyl:8×7 (files a, b, e) there are 4 other exact groups (CHECKED-2); in chess on cyl:8×6 only its d4 freeze and that freeze's zero are settled at cap 1 (CHECKED-2), the rest is open | R1 item 10
>>>>>>> NEW

### EDIT §8 item 2, over groups, K48 (K48, 2026-11-23; referee version)
<<<<<<< OLD
The two investigations use different definitions and scopes; where they overlap they agree.
=======
K48 (2026-11-23) found the same group exact in the sense of Definition 4.8 on flat 8×6, 9×6 and 10×6, so the wrap is not needed (CHECKED-2 on flat 8×6, where it and its two translates are, up to left-right reflection, the only exact groups with at most 3 + 3 pawns on three files within six), four further exact groups on cyl:8×7, and, in chess on cyl:8×6 at cap 1, the d4 freeze's zero exact but the rest of the group undecided (Conjecture 4.7, K45 bullet). The two investigations use different definitions and scopes; where they overlap they agree.
>>>>>>> NEW
