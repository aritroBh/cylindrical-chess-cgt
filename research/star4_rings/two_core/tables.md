
**Matched walls, by kind (SS = small x small, BS = big x small, BB = big x big)**

| group | rows | undecided | nimber | nim=nim-sum | nim!=nim-sum | N+ (all-N) | decisive/other | % nimber of decided |
|---|---|---|---|---|---|---|---|---|
| SS | 1161 | 0 | 953 | 953 | 0 | 0 | 208 | 82.1 |
| BS | 574 | 2 | 479 | 479 | 0 | 1 | 92 | 83.7 |
| BB | 145 | 41 | 73 | 73 | 0 | 0 | 31 | 70.2 |
| all matched | 1890 | 43 | 1513 | 1513 | 0 | 1 | 333 | 81.9 |

**Matched walls, by relative handedness of the two cores (same = both cores start their wall with the same pawn)**

| group | rows | undecided | nimber | nim=nim-sum | nim!=nim-sum | N+ (all-N) | decisive/other | % nimber of decided |
|---|---|---|---|---|---|---|---|---|
| same handedness | 1040 | 28 | 931 | 931 | 0 | 0 | 81 | 92.0 |
| opposite handedness | 850 | 15 | 582 | 582 | 0 | 1 | 252 | 69.7 |

**Matched walls, by shorter wall length min(L1,L2)**

| group | rows | undecided | nimber | nim=nim-sum | nim!=nim-sum | N+ (all-N) | decisive/other | % nimber of decided |
|---|---|---|---|---|---|---|---|---|
| min L = 2 | 520 | 16 | 445 | 445 | 0 | 0 | 59 | 88.3 |
| min L = 3 | 747 | 16 | 549 | 549 | 0 | 1 | 181 | 75.1 |
| min L = 4 | 292 | 10 | 253 | 253 | 0 | 0 | 29 | 89.7 |
| min L = 5 | 281 | 1 | 219 | 219 | 0 | 0 | 61 | 78.2 |
| min L = 6 | 50 | 0 | 47 | 47 | 0 | 0 | 3 | 94.0 |

**Matched walls, by wall parities (e = even, o = odd)**

| group | rows | undecided | nimber | nim=nim-sum | nim!=nim-sum | N+ (all-N) | decisive/other | % nimber of decided |
|---|---|---|---|---|---|---|---|---|
| L1 e, L2 e | 416 | 16 | 368 | 368 | 0 | 0 | 32 | 92.0 |
| L1 e, L2 o | 453 | 11 | 397 | 397 | 0 | 0 | 45 | 89.8 |
| L1 o, L2 e | 483 | 8 | 392 | 392 | 0 | 0 | 83 | 82.5 |
| L1 o, L2 o | 538 | 8 | 356 | 356 | 0 | 1 | 173 | 67.2 |

**Matched walls, by the stable values (vA, vB) of the two cores**

| group | rows | undecided | nimber | nim=nim-sum | nim!=nim-sum | N+ (all-N) | decisive/other | % nimber of decided |
|---|---|---|---|---|---|---|---|---|
| *0 + *0 | 46 | 2 | 31 | 31 | 0 | 0 | 13 | 70.5 |
| *0 + *1 | 366 | 1 | 295 | 295 | 0 | 0 | 70 | 80.8 |
| *0 + *2 | 126 | 14 | 88 | 88 | 0 | 1 | 23 | 78.6 |
| *0 + *3 | 13 | 0 | 9 | 9 | 0 | 0 | 4 | 69.2 |
| *1 + *1 | 895 | 0 | 745 | 745 | 0 | 0 | 150 | 83.2 |
| *1 + *2 | 312 | 0 | 267 | 267 | 0 | 0 | 45 | 85.6 |
| *1 + *3 | 50 | 2 | 37 | 37 | 0 | 0 | 11 | 77.1 |
| *2 + *2 | 67 | 16 | 38 | 38 | 0 | 0 | 13 | 74.5 |
| *2 + *3 | 15 | 8 | 3 | 3 | 0 | 0 | 4 | 42.9 |

**Unmatched wall types (kind UN, full 100-point wall grids for a few core pairs): prediction vA^vB**

| group | rows | undecided | nimber | nim=nim-sum | nim!=nim-sum | N+ (all-N) | decisive/other | % nimber of decided |
|---|---|---|---|---|---|---|---|---|
| UN matched | 10 | 0 | 8 | 8 | 0 | 0 | 2 | 80.0 |
| UN unmatched | 135 | 0 | 35 | 35 | 0 | 21 | 79 | 25.9 |

**Non-nimber signatures among matched, decided rings**

`RRRRRRRR` x286, `LLLLLLLL` x22, `RNRRRRRR` x14, `LLLNLLLL` x2, `RRNRRRRR` x2, `NRRRRRRR` x2, `NLLLLLLL` x2, `NNNNNNNN` x1, `NRNRRRRR` x1, `LNNLLLLL` x1, `RNNRRRRR` x1

**Matched rings that are nimbers but differ from vA xor vB: 0**


**Reference-ring version (single-core rings built by splicing the two walls, A+W1+W2 and B+W2+W1)**

rows with both reference rings nimbers: 733; ring is a nimber equal to refA xor refB: 542; ring is a nimber different from it: 0; ring not a nimber: 191

**Largest ring value seen in the two-core experiment:** 3

**Length scan (wall lengths up to 11) of 30 pairs whose matched rings with L<=6 were all non-nimbers, and 10 pairs that were all nimbers**

- fail groups, nimber only for some lengths: 30
- ok groups, all nimber: 10
- value of every nimber ring in the length scan equals vA xor vB: True (403 nimber rings)
- for the failing groups, the smallest longer wall that restores a nimber has length (max of the two lengths of the first nimber ring) in [7, 7, 7, 7, 8, 9, 9, 9, 10, 10, 10, 10, 10, 10, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11, 11]

**Three- and four-core rings (matched walls)**

- 3 cores, same handedness: rings 41, nimbers 30, equal to nim-sum 30
- 3 cores, mixed handedness: rings 18, nimbers 6, equal to nim-sum 6
- 4 cores, same handedness: rings 8, nimbers 5, equal to nim-sum 5
- 4 cores, mixed handedness: rings 3, nimbers 1, equal to nim-sum 1
