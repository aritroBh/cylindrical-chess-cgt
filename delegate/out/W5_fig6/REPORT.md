# W5: Fig. 6 (least pawns in a ring, *2 and *3)

## Least known *3 ring on C_n (project records only; nothing computed)
| n | pawns | kind of fact | label | source |
|---|---|---|---|---|
| 3..6 | none known | no *3 ring in the records; only censuses (C5: none up to 9 pawns; whole board: none with <= 8 pawns on <= 8 files) | C1 | RESULTS.md:445; dist/tog/supp/s06.tex:99-100; dist/tog/sections/08_star2.tex:123 |
| 7 | 10 | exact minimum: 8 ten-pawn rings are *3 (scanner, independent solver, cylcgt); no 9-pawn ring has nimber >=3 (scanner, 4 splits); <= 8 pawns none | existence C2, minimality C1 | RESULTS.md:331-336; research/star26_rings/c7/progress.txt:1-4; 08_star2.tex:123-124; s06.tex:103-105 |
| 8 | 10 | exact minimum: one *3 class (11 colour classes: 10 *2, 1 *3); no 9-pawn ring *3 (scanner and c8check, 4 chunks, star3=0) | existence C2, minimality C1 (C2 at 9 pawns by two scanners) | RESULTS.md:364-365; research/c8_independent/out9_{0,1,2,3}.txt:1; research/star26_rings/c8/progress*.txt; s06.tex:105 |
| 9 | none known | no 9- or 10-pawn ring is *3 (948,860 and 44,960,428 rings); 11 pawns open; both n+2 odd families fail at n=9 | C1 (9 pawns C2) | research/c9_rings/REPORT.md:14-16; RESULTS.md:380, 389 |
| 10 | 12 | exact minimum (n+2): none with 10 or 11 pawns; witness = the n+2 family (S) | C1 (min.); witness C2 | research/c9_rings/star3/REPORT.md:16-19; RESULTS.md:374, 414; s06.tex:105-106 |
| 11 | 12 | exact minimum (n+1): none with 11 pawns (15,461,385 rings); two 12-pawn rings are *3 | min. C1; witnesses C2 | research/c9_rings/star3/REPORT.md:11-15; RESULTS.md:403; 08_star2.tex:125; s06.tex:108-109 |
| 12 | 13 | exact minimum (n+1): none with 12 pawns (140,587,958 rings); T_12 is *3 | min. C1; witness C2 | research/c9_rings/star3/REPORT.md:20-23; RESULTS.md:412-414 |
| 13..20 | n+1 | upper bound only (family S_n/T_n); minimum unknown | S (proved for n >= 12) | RESULTS.md:402-409; 08_star2.tex:125; s06.tex:110-111 |

Also: n+2 pawns for even n >= 8 and odd n >= 11 (S), RESULTS.md:372-376. No disagreement between the paper text, Table S3 (the supplement has no cylinder *3 table; s06 tab:mobring and tab:heights are about *2 on the strip and about heights) and the records. The "nine pawns / Mobius" *3 rings (s06.tex:136, 165) are strip rings and are not used.

## Changes
- research/figures_2026_11/f2_least_pawns.py: three_comp now (7,10),(8,10),(10,12),(11,12),(12,13); square marker size 2.0 -> 2.9pt, and the *2 dots at n=7,8 are redrawn on top (forget plot) so the *2 values there stay visible; docstring updated. No new marker style or legend entry: filled square = exact minimum, open triangle = upper bound. Page size unchanged (229.4 x 189.94 pt).
- Regenerated figure PDF (and PNG preview); copied to dist/tog/figures/f2_least_pawns.pdf (md5 before: both 909cf073..., identical; after: both 56c714a6...). No other copy exists (paper/ieee and dist/tog/long have no use of this figure).
- dist/tog/sections/08_star2.tex lines 99-100 only. long/ and ieee 08_star2.tex do not contain this caption: untouched.

## Caption
Before (last sentences): "...The dashed line is one pawn per file. $\nim{3}$ is plotted from $n=10$; ten-pawn $\nim{3}$ rings also exist on $\cyl{7}$ and $\cyl{8}$."
After: "...The dashed line is one pawn per file. No $\nim{3}$ ring is known for $n\le6$ or $n=9$; ten pawns are the least on $\cyl{7}$ and $\cyl{8}$."
(changed part 203 -> 206 characters, +3.)

## Build
tectonic tog.tex: 10 pages; tog_review.tex: 10 pages; no Overfull warnings in tog.log. Figure on page 7 (Fig. 6).
PNGs inspected: <scratchpad>/f2_new.png (figure, 200 dpi) and .../tog_p7.png (page 7, 110 dpi): points, legend readable, no overlaps.
Not committed or added.
