Node cap 3,000,000 per search, time cap 120 s; 'solved' counts searches (2 per instance: White first, Black first).

| k | instances | pawns (median) | plain α-β: solved | plain: median nodes | plain: median s | α-β+TT: solved | TT: median nodes | TT: median s | CGT sum (cached comps) median s | CGT from scratch median s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 6 | 3.0 | 12/12 | 4 | 2.49e-05 | 12/12 | 4 | 1.27e-05 | 1.7e-05 | 0.0025 |
| 2 | 6 | 7.0 | 12/12 | 43 | 0.000332 | 12/12 | 35 | 0.000278 | 5.1e-05 | 0.044 |
| 3 | 6 | 11.0 | 12/12 | 196 | 0.00298 | 12/12 | 134 | 0.00184 | 9.5e-05 | 0.045 |
| 4 | 6 | 15.0 | 12/12 | 1,468 | 0.0248 | 12/12 | 628 | 0.00975 | 0.00014 | 0.048 |
| 5 | 6 | 19.0 | 12/12 | 15,034 | 1.11 | 12/12 | 1,998 | 0.12 | 0.00014 | 0.059 |
| 6 | 6 | 22.5 | 7/12 | > cap (5 unsolved) | — | 12/12 | 22,424 | 1.02 | 0.00015 | 0.075 |

Outcome agreement with CGT where the search finished: 69/69.
