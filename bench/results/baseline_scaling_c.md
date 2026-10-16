Engine: c (bench/ab.c); cap per search: 30,000,000 nodes / 60 s (CPU). Each instance is searched twice (White first, Black first); medians are over all searches, with unsolved searches counted as infinite. Times are CPU seconds.

### Nested chains (instance k+1 = instance k plus one more component)

| k | instances | pawns (median) | plain α-β solved | plain median nodes | plain median s | α-β+TT solved | TT median nodes | TT median s | CGT sum of cached values, median s | CGT from scratch, median s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 8 | 4 | 16/16 | 3 | 3e-06 | 16/16 | 3 | 5e-06 | 3e-05 | 0.0061 |
| 2 | 8 | 7.5 | 16/16 | 10 | 7e-06 | 16/16 | 10 | 1.1e-05 | 6e-05 | 0.013 |
| 3 | 8 | 11 | 16/16 | 40 | 1.5e-05 | 16/16 | 32 | 2e-05 | 0.0001 | 0.015 |
| 4 | 8 | 15 | 16/16 | 386 | 0.0001 | 16/16 | 230 | 0.0001 | 0.0002 | 0.023 |
| 5 | 8 | 19 | 16/16 | 5,317 | 0.0014 | 16/16 | 1,235 | 0.00046 | 0.0003 | 0.052 |
| 6 | 8 | 23 | 15/16 | 182,011 | 0.032 | 16/16 | 11,770 | 0.0048 | 0.0002 | 0.063 |
| 7 | 8 | 26.5 | 12/16 | 2,330,852 | 0.5 | 16/16 | 55,772 | 0.02 | 0.0003 | 0.064 |
| 8 | 8 | 30 | 6/16 | > cap | > cap | 14/16 | 256,457 | 0.086 | 0.0004 | 0.073 |

Growth per added component (chains): median over chains and sides of nodes(k) / nodes(k-1), where both searches finished.

| k | plain α-β | α-β+TT |
|---|---|---|
| 2 | 5.1 (n=16) | 4.8 (n=16) |
| 3 | 3.6 (n=16) | 3.5 (n=16) |
| 4 | 8.3 (n=16) | 6.5 (n=16) |
| 5 | 5.3 (n=16) | 3.4 (n=16) |
| 6 | 18.0 (n=15) | 8.9 (n=16) |
| 7 | 2.9 (n=12) | 3.4 (n=16) |
| 8 | 31.8 (n=6) | 10.0 (n=14) |

### Benchmark rows (k <= 3 from val, k >= 4 from test)

| k | instances | pawns (median) | plain α-β solved | plain median nodes | plain median s | α-β+TT solved | TT median nodes | TT median s | CGT sum of cached values, median s | CGT from scratch, median s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 12 | 4 | 24/24 | 3 | 4e-06 | 24/24 | 3 | 5e-06 | 2e-05 | 0.0055 |
| 2 | 12 | 8 | 24/24 | 16 | 8e-06 | 24/24 | 16 | 1.4e-05 | 6e-05 | 0.0079 |
| 3 | 12 | 11 | 24/24 | 188 | 4.8e-05 | 24/24 | 100 | 4.8e-05 | 0.0002 | 0.026 |
| 4 | 12 | 14.5 | 22/24 | 249 | 8.1e-05 | 24/24 | 141 | 5.3e-05 | 0.0003 | 0.011 |
| 5 | 12 | 19 | 23/24 | 27,563 | 0.0085 | 24/24 | 3,565 | 0.0016 | 0.0008 | 0.06 |
| 6 | 12 | 23 | 18/24 | 1,826,316 | 0.69 | 22/24 | 39,468 | 0.013 | 0.002 | 0.074 |

Outcome agreement between the searches and CGT wherever both searches of an instance finished: 254/254.
