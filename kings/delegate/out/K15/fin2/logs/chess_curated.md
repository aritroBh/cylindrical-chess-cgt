| board | cap | position | White to move: A B | Black to move: A B | dud_D prediction (W to move, B to move) | agrees | kpsolve time, peak RSS |
|---|---|---|---|---|---|---|---|
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3` (G8a alone) | D D | D D | D D | yes / yes | 11.8 s, 145 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg3 pg4` (G8a + Pg3 pg4 (blocked pair)) | D D | D D | D D | yes / yes | 240.9 s, 969 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg3 pg5` (G8a + Pg3 pg5 (one move)) | D D | D D | D D | yes / yes | 310.4 s, 1168 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg2 pg5` (G8a + Pg2 pg5 (gap pair)) | D D | D D | D D | yes / yes | 376.1 s, 1391 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg2` (G8a + Pg2 (one White pawn, far from queening)) | W W | W W | W W | yes / yes | 143.3 s, 567 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 pg5` (G8a + pg5 (one Black pawn)) | L L | L L | L L | yes / yes | 151.3 s, 587 MB |
| cyl:8x6 | 1 | `Kb2 kc4 Pa3 Pe2 pa4 pe3 Pg4 pg3` (G8a + Pg4 pg3 (two passers racing)) | W W | W L | W L | yes / undecided at cap 1 (bounds W L; the value is between them) | 862.3 s, 2891 MB |

**G8a and G8b, all 16 roots (4 king states x 2 sides to move x 2 groups), chess at cap 2, `--moves`** (`fin2/chess/cyl_8x6_G8_states_c2_mv.out`; 526.9 s CPU, peak RSS 515 MB): the value is exact (A = B, no "capped promotions met" line) and (D, D) at all 16 roots; 72 legal moves, 16 of them draw (the shuttles, one for each side at each root), the other 56 each lose for the side that plays them (exact). The 16 root values and the 72 per-move values are the same as in the P model (`kp_p --pmodel` and `ref3m`): move lists identical at 16 of 16 roots (rest: see the file). At cap 1 the roots are exact (D, D) too, but 12 of the 72 move values are bounds only (`fin2/chess/cyl_8x6_G8_states_c1_mv.out`, 15.2 s), which is why cap 2 was run.
