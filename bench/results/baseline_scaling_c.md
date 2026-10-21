Engine: c (bench/ab.c); cap per search: 30,000,000 nodes / 60 s (CPU). Each instance is searched twice (White first, Black first); medians are over all searches, with unsolved searches counted as infinite. Times are CPU seconds.

### Nested chains (instance k+1 = instance k plus one more component)

| k | instances | pawns (median) | plain α-β solved | plain median nodes | plain median s | α-β+TT solved | TT median nodes | TT median s | CGT sum of cached values, median s | CGT from scratch, median s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 8 | 4 | 16/16 | 2 | 4e-06 | 16/16 | 2 | 4e-06 | 3e-05 | 0.00013 |
| 2 | 8 | 8 | 16/16 | 6 | 5e-06 | 16/16 | 6 | 9e-06 | 0.0001 | 0.009 |
| 3 | 8 | 11 | 16/16 | 22 | 1e-05 | 16/16 | 22 | 3.4e-05 | 0.0002 | 0.011 |
| 4 | 8 | 15 | 16/16 | 429 | 0.00011 | 16/16 | 194 | 0.00015 | 0.0001 | 0.024 |
| 5 | 8 | 19 | 16/16 | 1,482 | 0.00037 | 16/16 | 543 | 0.00039 | 0.0002 | 0.026 |
| 6 | 8 | 22.5 | 15/16 | 48,792 | 0.012 | 16/16 | 4,434 | 0.0019 | 0.0003 | 0.042 |
| 7 | 8 | 26.5 | 13/16 | 149,440 | 0.034 | 16/16 | 8,442 | 0.005 | 0.0003 | 0.04 |
| 8 | 8 | 30 | 11/16 | 1,402,298 | 0.3 | 14/16 | 24,837 | 0.015 | 0.0004 | 0.052 |

Growth per added component (chains): median over chains and sides of nodes(k) / nodes(k-1), where both searches finished.

| k | plain α-β | α-β+TT |
|---|---|---|
| 2 | 3.2 (n=16) | 3.2 (n=16) |
| 3 | 2.9 (n=16) | 2.5 (n=16) |
| 4 | 23.3 (n=16) | 11.5 (n=16) |
| 5 | 5.5 (n=16) | 3.0 (n=16) |
| 6 | 8.8 (n=15) | 5.5 (n=16) |
| 7 | 1.7 (n=13) | 1.8 (n=16) |
| 8 | 1.8 (n=11) | 1.8 (n=14) |

Least-squares fit of ln(median nodes) against k, over k >= 3 where the median is finite (unsolved searches count as infinite in the median):

- plain α-β: about x8.9 nodes per added component (k = 3..8, 6 points)
- α-β+TT: about x4.0 nodes per added component (k = 3..8, 6 points)

### Benchmark rows (k <= 3 from val, k >= 4 from test)

| k | instances | pawns (median) | plain α-β solved | plain median nodes | plain median s | α-β+TT solved | TT median nodes | TT median s | CGT sum of cached values, median s | CGT from scratch, median s |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 12 | 4 | 24/24 | 3 | 3e-06 | 24/24 | 3 | 1e-05 | 2e-05 | 0.0018 |
| 2 | 12 | 7.5 | 24/24 | 14 | 6e-06 | 24/24 | 14 | 1.5e-05 | 3e-05 | 0.012 |
| 3 | 12 | 11 | 24/24 | 93 | 1.9e-05 | 24/24 | 70 | 3.7e-05 | 0.0002 | 0.011 |
| 4 | 12 | 14 | 24/24 | 602 | 7.3e-05 | 24/24 | 199 | 8.8e-05 | 0.0003 | 0.0098 |
| 5 | 12 | 18 | 24/24 | 3,516 | 0.0022 | 24/24 | 835 | 0.00039 | 0.0003 | 0.025 |
| 6 | 12 | 22 | 19/24 | 247,822 | 0.05 | 24/24 | 16,633 | 0.0046 | 0.0002 | 0.04 |

Outcome agreement between the searches and CGT wherever both searches of an instance finished: 262/262.

Double steps that left a passed pawn the opponent could take en passant, over all 544 searches: 0 (0 means the e.p.-aware passed test would give identical searches).
