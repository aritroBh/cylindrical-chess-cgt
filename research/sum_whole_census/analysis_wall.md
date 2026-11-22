## Headline (orbit representatives; N = positions, D = outcome(S) != outcome(W))

| test | rule | N | D | rate [Wilson 95%] |
|---|---|---|---|---|
| textbook | count | 599098 | 11595 | 11595/599098 = 1.935% [1.901, 1.971] |
| textbook | mover | 599098 | 10496 | 10496/599098 = 1.752% [1.719, 1.786] |
| textbook | opponent | 599098 | 12104 | 12104/599098 = 2.020% [1.985, 2.056] |
| e.p.-aware | count | 599098 | 11300 | 11300/599098 = 1.886% [1.852, 1.921] |
| e.p.-aware | mover | 599098 | 9243 | 9243/599098 = 1.543% [1.512, 1.574] |
| e.p.-aware | opponent | 599098 | 12100 | 12100/599098 = 2.020% [1.984, 2.056] |

## Weighted by orbit size (all legal positions, not only representatives)

| test | rule | N_w | D_w | rate [Wilson 95%] |
|---|---|---|---|---|
| textbook | count | 2386432 | 46096 | 46096/2386432 = 1.932% [1.914, 1.949] |
| textbook | mover | 2386432 | 41720 | 41720/2386432 = 1.748% [1.732, 1.765] |
| textbook | opponent | 2386432 | 48136 | 48136/2386432 = 2.017% [1.999, 2.035] |
| e.p.-aware | count | 2386432 | 44920 | 44920/2386432 = 1.882% [1.865, 1.900] |
| e.p.-aware | mover | 2386432 | 36720 | 36720/2386432 = 1.539% [1.523, 1.554] |
| e.p.-aware | opponent | 2386432 | 48120 | 48120/2386432 = 2.016% [1.999, 2.034] |

## by number of components at the root

| test | rule | (1,) | (2,) | (3,) |
|---|---|---|---|---|
| textbook | count | 0/430665 = 0.000% [0.000, 0.001] | 11595/167515 = 6.922% [6.801, 7.044] | 0/918 = 0.000% [0.000, 0.417] |
| textbook | mover | 8/430665 = 0.002% [0.001, 0.004] | 10488/167515 = 6.261% [6.146, 6.378] | 0/918 = 0.000% [0.000, 0.417] |
| textbook | opponent | 0/430665 = 0.000% [0.000, 0.001] | 12104/167515 = 7.226% [7.103, 7.351] | 0/918 = 0.000% [0.000, 0.417] |
| e.p.-aware | count | 0/430665 = 0.000% [0.000, 0.001] | 11300/167515 = 6.746% [6.627, 6.867] | 0/918 = 0.000% [0.000, 0.417] |
| e.p.-aware | mover | 0/430665 = 0.000% [0.000, 0.001] | 9243/167515 = 5.518% [5.409, 5.628] | 0/918 = 0.000% [0.000, 0.417] |
| e.p.-aware | opponent | 0/430665 = 0.000% [0.000, 0.001] | 12100/167515 = 7.223% [7.100, 7.348] | 0/918 = 0.000% [0.000, 0.417] |

## by hereditarily_safe

| test | rule | (True,) | (False,) |
|---|---|---|---|
| textbook | count | 0/539893 = 0.000% [0.000, 0.001] | 11595/59205 = 19.584% [19.267, 19.906] |
| textbook | mover | 0/539893 = 0.000% [0.000, 0.001] | 10496/59205 = 17.728% [17.423, 18.038] |
| textbook | opponent | 0/539893 = 0.000% [0.000, 0.001] | 12104/59205 = 20.444% [20.121, 20.771] |
| e.p.-aware | count | 0/540503 = 0.000% [0.000, 0.001] | 11300/58595 = 19.285% [18.967, 19.606] |
| e.p.-aware | mover | 0/540503 = 0.000% [0.000, 0.001] | 9243/58595 = 15.774% [15.481, 16.072] |
| e.p.-aware | opponent | 0/540503 = 0.000% [0.000, 0.001] | 12100/58595 = 20.650% [20.324, 20.980] |

## by sum_safe()

| test | rule | (True,) | (False,) |
|---|---|---|---|
| textbook | count | 0/581022 = 0.000% [0.000, 0.001] | 11595/18076 = 64.146% [63.444, 64.842] |
| textbook | mover | 8/580276 = 0.001% [0.001, 0.003] | 10488/18822 = 55.722% [55.011, 56.430] |
| textbook | opponent | 0/581431 = 0.000% [0.000, 0.001] | 12104/17667 = 68.512% [67.823, 69.193] |
| e.p.-aware | count | 0/581544 = 0.000% [0.000, 0.001] | 11300/17554 = 64.373% [63.661, 65.078] |
| e.p.-aware | mover | 0/583437 = 0.000% [0.000, 0.001] | 9243/15661 = 59.019% [58.247, 59.787] |
| e.p.-aware | opponent | 0/581431 = 0.000% [0.000, 0.001] | 12100/17667 = 68.489% [67.800, 69.170] |

## hereditarily_safe x sum_safe()

| test | rule | (True, True) | (False, True) | (False, False) | (True, False) |
|---|---|---|---|---|---|
| textbook | count | 0/539893 = 0.000% [0.000, 0.001] | 0/41129 = 0.000% [0.000, 0.009] | 11595/18076 = 64.146% [63.444, 64.842] | 0/0 = 0.000% [0.000, 0.000] |
| textbook | mover | 0/539893 = 0.000% [0.000, 0.001] | 8/40383 = 0.020% [0.010, 0.039] | 10488/18822 = 55.722% [55.011, 56.430] | 0/0 = 0.000% [0.000, 0.000] |
| textbook | opponent | 0/539893 = 0.000% [0.000, 0.001] | 0/41538 = 0.000% [0.000, 0.009] | 12104/17667 = 68.512% [67.823, 69.193] | 0/0 = 0.000% [0.000, 0.000] |
| e.p.-aware | count | 0/540503 = 0.000% [0.000, 0.001] | 0/41041 = 0.000% [0.000, 0.009] | 11300/17554 = 64.373% [63.661, 65.078] | 0/0 = 0.000% [0.000, 0.000] |
| e.p.-aware | mover | 0/540503 = 0.000% [0.000, 0.001] | 0/42934 = 0.000% [0.000, 0.009] | 9243/15661 = 59.019% [58.247, 59.787] | 0/0 = 0.000% [0.000, 0.000] |
| e.p.-aware | opponent | 0/540503 = 0.000% [0.000, 0.001] | 0/40928 = 0.000% [0.000, 0.009] | 12100/17667 = 68.489% [67.800, 69.170] | 0/0 = 0.000% [0.000, 0.000] |

## by total pawns

| test | rule | n=2 | n=3 | n=4 | n=5 | n=6 |
|---|---|---|---|---|---|---|
| textbook | count | 0/132 = 0.000% [0.000, 2.828] | 0/995 = 0.000% [0.000, 0.385] | 30/9684 = 0.310% [0.217, 0.442] | 1020/75564 = 1.350% [1.270, 1.435] | 10545/512723 = 2.057% [2.018, 2.096] |
| textbook | mover | 0/132 = 0.000% [0.000, 2.828] | 0/995 = 0.000% [0.000, 0.385] | 33/9684 = 0.341% [0.243, 0.478] | 896/75564 = 1.186% [1.111, 1.265] | 9567/512723 = 1.866% [1.829, 1.903] |
| textbook | opponent | 0/132 = 0.000% [0.000, 2.828] | 0/995 = 0.000% [0.000, 0.385] | 30/9684 = 0.310% [0.217, 0.442] | 1100/75564 = 1.456% [1.373, 1.544] | 10974/512723 = 2.140% [2.101, 2.180] |
| e.p.-aware | count | 0/132 = 0.000% [0.000, 2.828] | 0/995 = 0.000% [0.000, 0.385] | 30/9684 = 0.310% [0.217, 0.442] | 1000/75564 = 1.323% [1.244, 1.407] | 10270/512723 = 2.003% [1.965, 2.042] |
| e.p.-aware | mover | 0/132 = 0.000% [0.000, 2.828] | 0/995 = 0.000% [0.000, 0.385] | 30/9684 = 0.310% [0.217, 0.442] | 780/75564 = 1.032% [0.963, 1.107] | 8433/512723 = 1.645% [1.610, 1.680] |
| e.p.-aware | opponent | 0/132 = 0.000% [0.000, 2.828] | 0/995 = 0.000% [0.000, 0.385] | 30/9684 = 0.310% [0.217, 0.442] | 1080/75564 = 1.429% [1.347, 1.516] | 10990/512723 = 2.143% [2.104, 2.183] |

## Theorem check: hereditarily_safe True and S != W

- textbook/count: 0 violations
- textbook/mover: 0 violations
- textbook/opponent: 0 violations
- e.p.-aware/count: 0 violations
- e.p.-aware/mover: 0 violations
- e.p.-aware/opponent: 0 violations

## sum_safe() True but S != W (false positives of the heuristic); smallest by pawns then text

- textbook/count: 0 positions; smallest: none
- textbook/mover: 8 positions; smallest: W: a5 c3 e2 / B: b7 d4 e6 (S=N, W=R, hss=False, ncomp=1, 6 pawns)
- textbook/opponent: 0 positions; smallest: none
- e.p.-aware/count: 0 positions; smallest: none
- e.p.-aware/mover: 0 positions; smallest: none
- e.p.-aware/opponent: 0 positions; smallest: none

## S != W confusion (S outcome, W outcome) : count

- textbook/count: S=L,W=N:3883, S=L,W=R:428, S=N,W=L:577, S=N,W=R:399, S=P,W=L:31, S=P,W=N:723, S=P,W=R:25, S=R,W=L:820, S=R,W=N:4709
- textbook/mover: S=L,W=N:3555, S=L,W=R:473, S=N,W=L:226, S=N,W=R:345, S=P,W=L:49, S=P,W=N:792, S=P,W=R:36, S=R,W=L:431, S=R,W=N:4589
- textbook/opponent: S=L,W=N:3440, S=L,W=R:809, S=N,W=L:421, S=N,W=R:483, S=P,W=L:37, S=P,W=N:628, S=P,W=R:59, S=R,W=L:1243, S=R,W=N:4984
- e.p.-aware/count: S=L,W=N:3931, S=L,W=R:416, S=N,W=L:699, S=N,W=R:361, S=P,W=L:74, S=P,W=N:708, S=P,W=R:22, S=R,W=L:672, S=R,W=N:4417
- e.p.-aware/mover: S=L,W=N:3413, S=L,W=R:160, S=N,W=L:270, S=N,W=R:206, S=P,W=L:82, S=P,W=N:799, S=P,W=R:46, S=R,W=L:344, S=R,W=N:3923
- e.p.-aware/opponent: S=L,W=N:3435, S=L,W=R:905, S=N,W=L:438, S=N,W=R:502, S=P,W=L:37, S=P,W=N:608, S=P,W=R:75, S=R,W=L:1255, S=R,W=N:4845

## 5 smallest S != W positions per (test, rule)

- textbook/count:
    - `W: a5 d3 / B: b6 e4` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 d4 / B: b6 e5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e4 / B: b6 d5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e5 / B: b6 d6` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a6 d2 / B: b7 e3` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
- textbook/mover:
    - `W: a5 d2 / B: b7 e4` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 d3 / B: b6 e4` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 d4 / B: b6 e5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e4 / B: b6 d5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e5 / B: b6 d6` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
- textbook/opponent:
    - `W: a5 d3 / B: b6 e4` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 d4 / B: b6 e5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e4 / B: b6 d5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e5 / B: b6 d6` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a6 d2 / B: b7 e3` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
- e.p.-aware/count:
    - `W: a5 d3 / B: b6 e4` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 d4 / B: b6 e5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e4 / B: b6 d5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e5 / B: b6 d6` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a6 d2 / B: b7 e3` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
- e.p.-aware/mover:
    - `W: a5 d3 / B: b6 e4` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 d4 / B: b6 e5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e4 / B: b6 d5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e5 / B: b6 d6` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a6 d2 / B: b7 e3` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
- e.p.-aware/opponent:
    - `W: a5 d3 / B: b6 e4` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 d4 / B: b6 e5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e4 / B: b6 d5` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a5 e5 / B: b6 d6` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
    - `W: a6 d2 / B: b7 e3` S=P W=N hss=False sum_safe=False ncomp=2 pawns=4
