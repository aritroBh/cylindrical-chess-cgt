## Headline (orbit representatives; N = positions, D = outcome(S) != outcome(W))

| test | rule | N | D | rate [Wilson 95%] |
|---|---|---|---|---|
| textbook | count | 404023 | 11595 | 11595/404023 = 2.870% [2.819, 2.922] |
| textbook | mover | 404023 | 10496 | 10496/404023 = 2.598% [2.549, 2.647] |
| textbook | opponent | 404023 | 12104 | 12104/404023 = 2.996% [2.944, 3.049] |
| e.p.-aware | count | 404023 | 11300 | 11300/404023 = 2.797% [2.746, 2.848] |
| e.p.-aware | mover | 404023 | 9243 | 9243/404023 = 2.288% [2.242, 2.334] |
| e.p.-aware | opponent | 404023 | 12100 | 12100/404023 = 2.995% [2.943, 3.048] |

## Weighted by orbit size (all legal positions, not only representatives)

| test | rule | N_w | D_w | rate [Wilson 95%] |
|---|---|---|---|---|
| textbook | count | 1610551 | 46096 | 46096/1610551 = 2.862% [2.836, 2.888] |
| textbook | mover | 1610551 | 41720 | 41720/1610551 = 2.590% [2.566, 2.615] |
| textbook | opponent | 1610551 | 48136 | 48136/1610551 = 2.989% [2.963, 3.015] |
| e.p.-aware | count | 1610551 | 44920 | 44920/1610551 = 2.789% [2.764, 2.815] |
| e.p.-aware | mover | 1610551 | 36720 | 36720/1610551 = 2.280% [2.257, 2.303] |
| e.p.-aware | opponent | 1610551 | 48120 | 48120/1610551 = 2.988% [2.962, 3.014] |

## by number of components at the root

| test | rule | (1,) | (2,) | (3,) |
|---|---|---|---|---|
| textbook | count | 0/261725 = 0.000% [0.000, 0.001] | 11595/141380 = 8.201% [8.059, 8.345] | 0/918 = 0.000% [0.000, 0.417] |
| textbook | mover | 8/261725 = 0.003% [0.002, 0.006] | 10488/141380 = 7.418% [7.283, 7.556] | 0/918 = 0.000% [0.000, 0.417] |
| textbook | opponent | 0/261725 = 0.000% [0.000, 0.001] | 12104/141380 = 8.561% [8.417, 8.708] | 0/918 = 0.000% [0.000, 0.417] |
| e.p.-aware | count | 0/261725 = 0.000% [0.000, 0.001] | 11300/141380 = 7.993% [7.852, 8.135] | 0/918 = 0.000% [0.000, 0.417] |
| e.p.-aware | mover | 0/261725 = 0.000% [0.000, 0.001] | 9243/141380 = 6.538% [6.410, 6.668] | 0/918 = 0.000% [0.000, 0.417] |
| e.p.-aware | opponent | 0/261725 = 0.000% [0.000, 0.001] | 12100/141380 = 8.558% [8.414, 8.705] | 0/918 = 0.000% [0.000, 0.417] |

## by hereditarily_safe

| test | rule | (True,) | (False,) |
|---|---|---|---|
| textbook | count | 0/344818 = 0.000% [0.000, 0.001] | 11595/59205 = 19.584% [19.267, 19.906] |
| textbook | mover | 0/344818 = 0.000% [0.000, 0.001] | 10496/59205 = 17.728% [17.423, 18.038] |
| textbook | opponent | 0/344818 = 0.000% [0.000, 0.001] | 12104/59205 = 20.444% [20.121, 20.771] |
| e.p.-aware | count | 0/345428 = 0.000% [0.000, 0.001] | 11300/58595 = 19.285% [18.967, 19.606] |
| e.p.-aware | mover | 0/345428 = 0.000% [0.000, 0.001] | 9243/58595 = 15.774% [15.481, 16.072] |
| e.p.-aware | opponent | 0/345428 = 0.000% [0.000, 0.001] | 12100/58595 = 20.650% [20.324, 20.980] |

## by sum_safe()

| test | rule | (True,) | (False,) |
|---|---|---|---|
| textbook | count | 0/385947 = 0.000% [0.000, 0.001] | 11595/18076 = 64.146% [63.444, 64.842] |
| textbook | mover | 8/385201 = 0.002% [0.001, 0.004] | 10488/18822 = 55.722% [55.011, 56.430] |
| textbook | opponent | 0/386356 = 0.000% [0.000, 0.001] | 12104/17667 = 68.512% [67.823, 69.193] |
| e.p.-aware | count | 0/386469 = 0.000% [0.000, 0.001] | 11300/17554 = 64.373% [63.661, 65.078] |
| e.p.-aware | mover | 0/388362 = 0.000% [0.000, 0.001] | 9243/15661 = 59.019% [58.247, 59.787] |
| e.p.-aware | opponent | 0/386356 = 0.000% [0.000, 0.001] | 12100/17667 = 68.489% [67.800, 69.170] |

## hereditarily_safe x sum_safe()

| test | rule | (True, True) | (False, True) | (False, False) | (True, False) |
|---|---|---|---|---|---|
| textbook | count | 0/344818 = 0.000% [0.000, 0.001] | 0/41129 = 0.000% [0.000, 0.009] | 11595/18076 = 64.146% [63.444, 64.842] | 0/0 = 0.000% [0.000, 0.000] |
| textbook | mover | 0/344818 = 0.000% [0.000, 0.001] | 8/40383 = 0.020% [0.010, 0.039] | 10488/18822 = 55.722% [55.011, 56.430] | 0/0 = 0.000% [0.000, 0.000] |
| textbook | opponent | 0/344818 = 0.000% [0.000, 0.001] | 0/41538 = 0.000% [0.000, 0.009] | 12104/17667 = 68.512% [67.823, 69.193] | 0/0 = 0.000% [0.000, 0.000] |
| e.p.-aware | count | 0/345428 = 0.000% [0.000, 0.001] | 0/41041 = 0.000% [0.000, 0.009] | 11300/17554 = 64.373% [63.661, 65.078] | 0/0 = 0.000% [0.000, 0.000] |
| e.p.-aware | mover | 0/345428 = 0.000% [0.000, 0.001] | 0/42934 = 0.000% [0.000, 0.009] | 9243/15661 = 59.019% [58.247, 59.787] | 0/0 = 0.000% [0.000, 0.000] |
| e.p.-aware | opponent | 0/345428 = 0.000% [0.000, 0.001] | 0/40928 = 0.000% [0.000, 0.009] | 12100/17667 = 68.489% [67.800, 69.170] | 0/0 = 0.000% [0.000, 0.000] |

## by total pawns

| test | rule | n=2 | n=3 | n=4 | n=5 | n=6 |
|---|---|---|---|---|---|---|
| textbook | count | 0/57 = 0.000% [0.000, 6.314] | 0/450 = 0.000% [0.000, 0.846] | 30/5140 = 0.584% [0.409, 0.832] | 1020/46102 = 2.212% [2.082, 2.351] | 10545/352274 = 2.993% [2.938, 3.050] |
| textbook | mover | 0/57 = 0.000% [0.000, 6.314] | 0/450 = 0.000% [0.000, 0.846] | 33/5140 = 0.642% [0.458, 0.900] | 896/46102 = 1.944% [1.821, 2.074] | 9567/352274 = 2.716% [2.663, 2.770] |
| textbook | opponent | 0/57 = 0.000% [0.000, 6.314] | 0/450 = 0.000% [0.000, 0.846] | 30/5140 = 0.584% [0.409, 0.832] | 1100/46102 = 2.386% [2.251, 2.529] | 10974/352274 = 3.115% [3.058, 3.173] |
| e.p.-aware | count | 0/57 = 0.000% [0.000, 6.314] | 0/450 = 0.000% [0.000, 0.846] | 30/5140 = 0.584% [0.409, 0.832] | 1000/46102 = 2.169% [2.040, 2.306] | 10270/352274 = 2.915% [2.860, 2.971] |
| e.p.-aware | mover | 0/57 = 0.000% [0.000, 6.314] | 0/450 = 0.000% [0.000, 0.846] | 30/5140 = 0.584% [0.409, 0.832] | 780/46102 = 1.692% [1.578, 1.814] | 8433/352274 = 2.394% [2.344, 2.445] |
| e.p.-aware | opponent | 0/57 = 0.000% [0.000, 6.314] | 0/450 = 0.000% [0.000, 0.846] | 30/5140 = 0.584% [0.409, 0.832] | 1080/46102 = 2.343% [2.208, 2.485] | 10990/352274 = 3.120% [3.063, 3.178] |

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
