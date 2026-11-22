# Suggested captions (IEEE style, sentence case)

Build: from the repo root, `.venv/bin/python research/figures_2026_11/f1_ring_cylinder.py` (likewise f2, f3).
Needs tectonic and pdftoppm (as paper/ieee/make_figures.py); matplotlib is not installed, so the figures are TikZ/pgfplots.

## F1 f1_ring_cylinder
Fig. X. The ring M_10 on the cylinder C_10: (a) in perspective, with the far half dashed; (b) unrolled, where file j
is next to file a across the seam (orange). One pawn stands on each file, and the position has value *2.
Data: position B4 W2 B6 W2 W3 B6 B7 W3 B7 W5 given by the caller; value *2 from paper/ieee/sections/08_star2.tex
(lines 144-146: one pawn per file is *2 on C_10, label C2). The ring itself was not re-evaluated here.

## F2 f2_least_pawns
Fig. X. Least number of pawns in a ring of value *2 (steps) and *3 on C_n. Filled markers are computed, open ones
proved for all n; the dashed line is one pawn per file.
Data: *2 = n+3 for n=3..7, ten for n=7..10 (08_star2.tex lines 140-144, 14_conclusion.tex line 13; C2), n for n>=10
(whole-board game, S; C2 witnesses on C_10, C_11 in 08_star2.tex line 145). Markers: filled for n<=11 (computed or
explicit C2 witness; n=10, 11 are also covered by the S result), open for n>=12. *3 = n+2 = 12 on C_10, n+1 = 12 on
C_11, 13 on C_12 (C1), at most n+1 for n>=12 (S): 14_conclusion.tex line 13-14 and 01_intro.tex lines 46-48.
Open triangles for n>=13 are upper bounds only (n=12 is exact, 13).

## F3 f3_model_vs_chess
Fig. X. Agreement between the model and real chess, with Wilson 95% intervals. Top: flat 8x8 beside a trebuchet,
2049 decisive positions, by race rule (count rule best). Bottom: exact kpsolve results on small boards.
Data: research/flat_xtarget_census/REPORT.md table 2 (e.p.-aware test): count 1896/2049, mover 1701/2049,
opponent 1714/2049 (92.5, 83.0, 83.7%). research/agreement_census/REPORT.md headline table (Q, cap 2):
cyl 6x6 13/26, flat 5x6 23/26, cyl 5x5 (compact layout, no buffer files) 49/71. Intervals computed in the script
(Wilson, z=1.96); they match the reports' [91.3, 93.6], [81.3, 84.6], [82.0, 85.2], [32.1, 67.9], [71.0, 96.0], [57.5, 78.6].
Caveat to state in the text: intervals treat positions as independent (reports say they are optimistic).

## F1 wide (f1_ring_cylinder_wide, double column, 7.07 x 2.50 in)
Fig. X. The ring M_10 on the cylinder C_10. (a) Perspective view; the seam between files j and a (orange) faces the viewer,
and the far wall is dashed and faded. Only pawns that can be seen are drawn: 7 of the 10 (five on the near wall, two on
the far wall above the rim). (b) The same position unrolled, showing all ten pawns, one per file; file j is next to file a
across the dashed seam, and the faded columns repeat j and a. White moves up. The position has value *2.
Data: as for F1 above (position B4 W2 B6 W2 W3 B6 B7 W3 B7 W5; checked by the coordinator against
research/c9_rings/REPORT.md). Rotation chosen by the script (seam 9 degrees left of the front centre) to maximise visible pawns;
the script prints "visible 7 front 5 far 2". Hidden: d2, e3 (behind the front wall), h3 (on the far side).
