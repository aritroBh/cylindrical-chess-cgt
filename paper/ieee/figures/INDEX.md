# Figure index (paper/ieee/figures)

Built by `.venv/bin/python paper/ieee/make_figures.py` (tectonic; TikZ/pgfplots sources in `src/`).
Re-verify every board with `PYTHONPATH=. .venv/bin/python paper/ieee/make_figures.py --check`.

- **Value settings:** cylcgt, count race rule, e.p.-aware passed test, e.p. on. "Cylinder" means
  `Board(8,8,True,True)` (files a and h adjacent), "ordinary" means `Board(8,8,False,True)`; C3 and C4 mean
  3- and 4-file cylinders with 8 ranks. "+BIG" is a passed pawn (\BIG).
- **"All settings"** means the same value under the count, mover and opponent race rules, with the textbook and
  the e.p.-aware test, and with e.p. on and off (13 combinations, all computed).
- **Legality:** no pawn on rank 1 or 8. Kings are not adjacent, counting adjacency across the seam on a
  cylinder. Neither king is in check, so either side may move. Pawn-only diagrams have no kings, as in 2025.
- **Sizes:** small boards are 1.62 in wide (two per column with subfig) and column boards 2.58 in. The bar
  charts are 3.2–3.3 in (\columnwidth) with 8 pt text, and dawson_grundy is 6.8 in (figure*).
- **Kings beside pawns:** "+ trébuchet" means the king group Kf5 Pg4 / Kh4 Pg5 on the f–h files of the
  ordinary board.

| File | Shows (pieces; upper case = white) | Verified value (settings) | Legal? | 2025 | Notes |
|---|---|---|---|---|---|
| zero.pdf | Pe4 / pe5, cylinder | 0, all settings | yes (pawns only) | Pos. 2.1 | unchanged |
| zero_seam.pdf | Pa4 Ph3 / pa5 ph6, cylinder | 0, all settings | yes (pawns only) | replaces Pos. 2.2 | 2.2 (W a2 h1 / B a3 h4) has an illegal white pawn on h1. This is 2.2 moved up two ranks, so it has the same game tree: whoever moves first loses a pawn across the seam (h3–h4 a5xh4; h6–h5 a4xh5). It is also the zero that `one` moves to |
| one.pdf | Pa4 Ph2 / pa5 ph6, cylinder | 1 = {0 \| }, all settings | yes (pawns only) | replaces Pos. 3.1 | 3.1 (W a3 h1 / B a4 h5) is illegal (h1). This is 3.1 moved up one rank. White h2–h3 goes to zero_seam. White h2–h4 loses to a5xh4. Black's only move, h6–h5, loses to a4xh5. Robust: unlike 3.1, it does not depend on e.p. |
| two.pdf | Pa5 Ph2 / pa6 ph7, cylinder | 2 = {0, 1 \| }, e.p. on, every race rule and both passed tests; ⇑⋆ with e.p. off | yes (pawns only) | replaces Pos. 3.2 | 3.2 (W a4 h1 / B a5 h6) is illegal (h1). This is 3.2 moved up one rank. White h2–h4 → 0 and h2–h3 → 1, which is exactly the 2025 text's {0, 1 \| }. Both black moves, h7–h6 and h7–h5, are answered by a5xh6, the second one en passant across the seam. It is the only 4-pawn legal h/a-file analogue with value 2 (search: 2 hits, both e.p.-dependent) |
| star.pdf | Pe4 / pe6, cylinder | ⋆, all settings | yes (pawns only) | Pos. 4.1 | unchanged |
| up.pdf | Pe2 / pe5, cylinder | ↑ = {0, ⋆ \| ⋆}, all settings | yes (pawns only) | Pos. 4.2, corrected | the 2025 diagram (W e3 / B e6) is one rank off and has value 0. Options: e2–e3 → ⋆, e2–e4 → 0; black e5–e4 → ⋆ |
| tiny1_2025.pdf | Pa4 Ph2 Ph4 / pa5 pa6 pa7 ph3, cylinder | tiny(1), all settings | yes (pawns only) | Pos. 4.3 | unchanged. Options: a4xa5?? no: white h4–h5 → {0 \| −BIG⋆}, h4xa5 → 0; black a5xh4 → −1/2±1/2 = {0 \| −1} |
| trebuchet_2025.pdf | Kh5 Pa4 / kb4 pa5, cylinder | 0 (mutual zugzwang); not a pawn value | yes; kings two files apart across the seam | Pos. 5.1 | a zugzwang only because of the seam. A real mutual zugzwang with explicit kings (two independent king-and-pawn solvers, RESULTS §3) |
| trebuchet.pdf | Kf5 Pg4 / kh4 pg5, ordinary board | 0 (mutual zugzwang); not a pawn value | yes | — | real mutual zugzwang (Lichess tablebase; fact sheet "Kings"). This is the king group used beside every ordinary-board pawn figure |
| kinggroup72.pdf | Ke6 Pd7 / kd8 pe7, cylinder (central, so the seam plays no part) | 0 only under the convention; real chess: White to move draws (Kd5, Ke5 or Kf5), only Black to move loses | yes | king group of Pos. 7.2 | not a zugzwang in real chess (kpsolve and Lichess, RESULTS §3) |
| puzzle71.pdf | Pa4 Pa5 Pc2 Pc3 Pf3 Pf4 Ph2 Ph3 / pa7 pc5 pc6 pf7 ph6, cylinder | components: c-file ±1; f-file {3/2±1/2 \| 0} = {{2\|1}\|0}; {h,a} = {+BIG \| ⋆}, not 1. Total: outcome L (white wins whoever starts). All settings | yes (pawns only) | Pos. 7.1 | the 2025 total 1±1+{{2\|1}\|0} is wrong only in the {h,a} part |
| puzzle72.pdf | Ke6 Pa2 Pb2 Pd7 Ph3 / kd8 pa6 pb7 pe7 ph7, cylinder | pawn part W a2 b2 h3 / B a6 b7 h7: an infinitesimal with mean 0 and temperature 0, outcome N, not ±1 (count, both tests, every race rule with e.p. on). The king group is as in kinggroup72 | yes | Pos. 7.2 | with e.p. off the pawn part is outcome R and its value depends on the race rule (diagram audit) |
| puzzle73.pdf | Kg8 Pa1 Pa5 Pc1 Pc3 Pd3 Pf7 Pg1 Ph1 / kf6 pc2 pd4 pd5 pd6 pg3 pg7 ph4, cylinder | all pawns: +BIG (a5 and f7 already passed), all settings. Its {c,d} part (W c1 c3 d3 / B c2 d4 d5 d6) is tiny(1), not 1 | **no**: white pawns on a1, c1, g1 and h1 | Pos. 7.3 | drawn exactly as in 2025, to show the corrections. The kings are not adjacent and neither is in check. The king group Kg8 Pf7 / Kf6 Pg7 is not a zugzwang (Kg8–f8 and Kf6–g6 are spare moves). A legal copy of the {c,d} part one rank up, W c2 c4 d4 / B c3 d5 d6 d7, is also tiny(1) (verify/diagrams/shift_output.txt) |
| sum_counter.pdf | Pb2 Pd4 Pg3 Ph5 / pa7 pc7 pf7 pg4, cylinder | sum model: outcome R (e.p. off, both tests; also with e.p. on). Whole board: N [C2, fact sheet] | yes (pawns only) | — | counterexample to the old sum-safety test (§V). Only the sum-model outcome was recomputed here |
| ep_test.pdf | Pa2 / pb4, ordinary board; green arrow a2–a4 | 0, all settings | yes (pawns only) | — | §II example: after a2–a4 black may reply b4xa3 e.p., so a4 is not passed under the e.p.-aware test. The value is 0 under both tests, so do not caption it with a value difference |
| elkies_dup.pdf | Pa2 / pa6, ordinary board | ⇑⋆ (double-up star), all settings; the same on the cylinder | yes (pawns only) | — | single-file value (fact sheet "Atlas") |
| hot3.pdf | Pa2 Pb4 / pa5 pb7, ordinary board | ±3, all settings; the same on the cylinder | yes (pawns only) | — | hottest value without ±BIG: b4xa5 → 3, a5xb4 → −3 |
| ring3_threequarters.pdf | Pa2 Pb4 / pb7 pc6, C3 (3-file cylinder) | 3/4 (count, both tests); 0 under the mover rule; {⋆2, {⋆2 \| 0} \| 0} under the opponent rule | yes (pawns only) | — | cylinder-only value from a 3-file ring (fact sheet: "3/4 becomes 0 under mover") |
| ring3_quarter.pdf | Pa2 Pb2 / pc5 pc6, C3 | 1/4±1/4 (count and mover, both tests, e.p. on); 1±1 under the opponent rule; 1/2⋆ with e.p. off | yes (pawns only) | — | cylinder-only value from a 3-file ring |
| ring4.pdf | Pa2 Pc2 / pb7 pd7, C4 (4-file cylinder) | {2±1 \| −2±1} (e.p.-aware, count and mover); {3/2±1/2 \| −3/2±1/2} (textbook); ±1/2 with e.p. off | yes (pawns only) | — | the 4-file ring form of the ⋆2 candidate |
| eighth.pdf | Pa2 Pb2 Pb3 / pa5 pa6 pb6 + trébuchet, ordinary board | 1/8, all settings | yes | — | FEN 8/8/pp6/p4Kp1/6Pk/1P6/PP6/8. White a2–a4 → 0; black b6–b5 → 1/4; so {0 \| 1/4} = 1/8 |
| upsecstar.pdf | Pa2 Pb2 Pb6 / pa6 pb7 pc5 + trébuchet, ordinary board | ↑²⋆ = {0, ⋆ \| ↓}, all settings | yes | — | FEN 8/1p6/pP6/2p2Kp1/6Pk/8/PP6/8 |
| tiny1.pdf | Pa2 Pb2 Pb6 / pa6 pb7 pc6 + trébuchet, ordinary board | tiny(1) = {0 ‖ 0 \| −1} (e.p. on: every race rule, both tests); ↑ with e.p. off | yes | — | white a2–a3 → 0; black a6–a5 → {0 \| −1} |
| star2_textbook.pdf | Pa2 Pc2 / pb7 pd7 + trébuchet, ordinary board (column size, no arrow) | {2±1 \| −2±1} (e.p.-aware, count and mover); ⋆2 (textbook test, count or mover, and with e.p. off); 0 under the opponent rule | yes | — | FEN 8/1p1p4/8/5Kp1/6Pk/8/P1P5/8, the textbook ⋆2 candidate |
| star2_seven_a.pdf | Pa4 Pb3 Pd2 Pd3 / pa7 pb7 pc5 + trébuchet, ordinary board | ⋆2 (count and mover, both tests, e.p. on); not ⋆2 under the opponent rule or with e.p. off | yes | — | position A: {0, ⋆ \| 0, ⋆} |
| star2_seven_b.pdf | Pb4 Pc2 Pd2 / pa6 pa7 pc6 pd5 + trébuchet, ordinary board | ⋆2 (count and mover, both tests, e.p. on); not ⋆2 under the opponent rule or with e.p. off | yes | — | position B |
| star2_eight_five.pdf | Pa3 Pb3 Pc2 Pe2 / pa6 pc5 pd5 pe3 + trébuchet, ordinary board | ⋆2 (count, e.p.-aware only); textbook {1 \| 0, ⋆}; opponent/e.p.-aware ⇑ | yes | — | extra: one of the three 8-pawn ⋆2 positions on 5 files |
| eighth_open.pdf | Pb2 Pb5 / pa5 pb4 + trébuchet, ordinary board | +BIG (b5 is passed), all settings; real chess, White to move: White wins (kpsolve, queen promotion) | yes | — | extra: the 8-man decisive end position in the 1/8 certification (§IX) |
| kpk_rookpawn.pdf | Ka6 Pa5 / ka8, cylinder | White wins with either side to move on the cylinder; a draw with either side to move on the ordinary board (atlas/cylinder/kpk, rerun) | yes | — | the rook-pawn fortress is gone on the cylinder |
| dawson_strip.pdf | Dawson's chess, 3×6 strip: white pawns on rank 1, black pawns on rank 3 | — (illustration) | rank-1 pawns are part of Dawson's game | — | §XI start position |
| dawson_ring.pdf | the same on the 3×6 cylinder; a red arrow under the board marks the f→a wrap | — (illustration) | as above | — | §XI ring version |
| tb_bars.pdf | grouped bars: % of positions won by White, White to move, plane / cylinder / torus, for KQK KRK KBBK KBNK KNNK KRBK KRRK KQRK | values from the fact sheet "Tablebases" [C2] | — | — | \columnwidth, area legend |
| kpk_bars.pdf | grouped bars: % of KPK positions won by White, plane vs cylinder, White / Black to move, with value labels | 76.51 / 78.89 and 58.09 / 55.88 (fact sheet "KPK", two solvers) | — | — | \columnwidth, area legend |
| star2_by_pawns.pdf | bars: number of ⋆2 positions by pawn count 4–8 (ordinary boards of width ≤ 4, count rule, e.p.-aware) | 0, 0, 0, 2, 4 (4–6 pawns [C2]; 7 and 8 pawns [C1], every hit re-checked [C2]) | — | — | \columnwidth |
| dawson_grundy.pdf | Grundy values g(n) of the 3×n strip (octal 0.137) for n ≤ 120; red dots where g(m)=0, i.e. the 3×(m+3) cylinder is a first-player win | computed by dawson.octal (period 34, last exception 51) | — | — | full width (figure*) |
| CoverPic.png | photograph of a cylindrical chessboard with all pieces (Wikimedia Commons) | — | — | Fig. 1 of 2025 | byte-identical copy of prior_work/Pictures/CoverPic.png. Credit it in the caption and the references |

`superseded/` holds an earlier set of `p_*` figures that another run left here (old style, 2025 positions as
drawn, including the illegal 2.2, 2.3, 3.1 and 3.2). The script no longer builds them and the paper should not
use them. Each one has a counterpart above: p_zero1→zero, p_one1→one, p_two1→two, p_star1→star, p_up1→up,
p_tiny1→tiny1_2025, p_treb_cyl→trebuchet_2025, p_puzzle1–3→puzzle71–73, p_ep→ep_test,
p_sumcounter→sum_counter, p_hot3→hot3, p_ring3a→ring3_threequarters, p_ring3b→ring3_quarter, p_ring4→ring4,
p_eighth→eighth, p_upsecstar→upsecstar, p_tiny1pos→tiny1, p_star2cand→star2_textbook,
p_star2sevenA/B→star2_seven_a/b, p_star2five→star2_eight_five, p_kpk→kpk_rookpawn,
p_dawson_strip/ring→dawson_strip/ring. p_zero2 and p_zero3 (2.2 and 2.3 as drawn) are replaced by zero_seam.
