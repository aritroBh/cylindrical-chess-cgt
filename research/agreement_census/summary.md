### Headline per configuration (board, pawn set, promotion set, cap)

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ('cyl:4x4', 'le2', 'Q', 2) | 2 | 1 | 0 | 0 | 0/1 | 0.0% | [0.0, 79.3] | 1 | 0 | 1 | 1 |
| ('cyl:4x4', 'le2', 'QRBN', 2) | 2 | 1 | 0 | 0 | 0/1 | 0.0% | [0.0, 79.3] | 1 | 0 | 1 | 1 |
| ('cyl:5x5', 'ext3', 'Q', 1) | 260 | 95 | 100 | 26 | 38/39 | 97.4% | [86.8, 99.5] | 1 | 0 | 0 | 1 |
| ('cyl:5x5', 'le2', 'Q', 2) | 240 | 104 | 65 | 0 | 49/71 | 69.0% | [57.5, 78.6] | 20 | 2 | 11 | 22 |
| ('cyl:5x5', 'le2', 'QRBN', 1) | 240 | 104 | 65 | 32 | 35/39 | 89.7% | [76.4, 95.9] | 3 | 1 | 0 | 4 |
| ('cyl:6x6', 'le2', 'Q', 2) | 42 | 16 | 0 | 0 | 13/26 | 50.0% | [32.1, 67.9] | 13 | 0 | 10 | 13 |
| ('cyl:6x6', 'le2', 'QRBN', 1) | 42 | 16 | 0 | 13 | 13/13 | 100.0% | [77.2, 100.0] | 0 | 0 | 0 | 0 |
| ('flat:5x6', 'ext3', 'Q', 2) | 8 | 2 | 0 | 0 | 5/6 | 83.3% | [43.6, 97.0] | 1 | 0 | 0 | 1 |
| ('flat:5x6', 'le2', 'Q', 2) | 42 | 16 | 0 | 0 | 23/26 | 88.5% | [71.0, 96.0] | 3 | 0 | 1 | 3 |
| ('flat:5x6', 'le2', 'QRBN', 1) | 42 | 16 | 0 | 11 | 15/15 | 100.0% | [79.6, 100.0] | 0 | 0 | 0 | 0 |

#### ('cyl:5x5', 'ext3', 'Q', 1): by model class

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 64 | 0 | 23 | 19 | 22/22 | 100.0% | [85.1, 100.0] | 0 | 0 | 0 | 0 |
| N | 10 | 0 | 8 | 1 | 1/1 | 100.0% | [20.7, 100.0] | 0 | 0 | 0 | 0 |
| R | 64 | 0 | 42 | 6 | 15/16 | 93.8% | [71.7, 98.9] | 1 | 0 | 0 | 1 |
| race | 122 | 95 | 27 | 0 | 0 | - | - | - | - | - | - |

#### ('cyl:5x5', 'ext3', 'Q', 1): by pawns (W/B)

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1/3 | 60 | 16 | 30 | 2 | 12/12 | 100.0% | [75.7, 100.0] | 0 | 0 | 0 | 0 |
| 2/3 | 60 | 22 | 30 | 5 | 3/3 | 100.0% | [43.8, 100.0] | 0 | 0 | 0 | 0 |
| 3/1 | 60 | 22 | 10 | 9 | 19/19 | 100.0% | [83.2, 100.0] | 0 | 0 | 0 | 0 |
| 3/2 | 60 | 26 | 20 | 9 | 4/5 | 80.0% | [37.6, 96.4] | 1 | 0 | 0 | 1 |
| 3/3 | 20 | 9 | 10 | 1 | 0 | - | - | - | - | - | - |

Races at start, ('cyl:5x5', 'ext3', 'Q', 1): real outcome (wtm,btm) counts: {('W/L', 'L/L'): 7, ('W/L', 'W/L'): 60, ('W/L', 'D/L'): 10, ('W/D', 'W/L'): 1, ('W/W', 'W/L'): 15, ('W/W', 'D/L'): 1, ('W/W', 'W/W'): 1}

#### ('cyl:5x5', 'le2', 'Q', 2): by model class

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 40 | 0 | 12 | 0 | 21/28 | 75.0% | [56.6, 87.3] | 6 | 1 | 3 | 7 |
| N | 30 | 0 | 16 | 0 | 9/14 | 64.3% | [38.8, 83.7] | 5 | 0 | 3 | 5 |
| P | 13 | 0 | 6 | 0 | 2/7 | 28.6% | [8.2, 64.1] | 5 | 0 | 3 | 5 |
| R | 40 | 0 | 18 | 0 | 17/22 | 77.3% | [56.6, 89.9] | 4 | 1 | 2 | 5 |
| race | 117 | 104 | 13 | 0 | 0 | - | - | - | - | - | - |

#### ('cyl:5x5', 'le2', 'Q', 2): by pawns (W/B)

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1/1 | 30 | 17 | 5 | 0 | 3/8 | 37.5% | [13.7, 69.4] | 5 | 0 | 4 | 5 |
| 1/2 | 60 | 22 | 20 | 0 | 13/18 | 72.2% | [49.1, 87.5] | 4 | 1 | 3 | 5 |
| 2/1 | 60 | 26 | 10 | 0 | 18/24 | 75.0% | [55.1, 88.0] | 5 | 1 | 3 | 6 |
| 2/2 | 90 | 39 | 30 | 0 | 15/21 | 71.4% | [50.0, 86.2] | 6 | 0 | 1 | 6 |

Races at start, ('cyl:5x5', 'le2', 'Q', 2): real outcome (wtm,btm) counts: {('W/W', 'L/L'): 44, ('L/L', 'L/L'): 23, ('W/W', 'W/W'): 13, ('W/W', 'D/D'): 7, ('D/D', 'L/L'): 6, ('W/W', 'W/D'): 1, ('W/W', 'D/L'): 4, ('D/L', 'L/L'): 3, ('W/D', 'L/L'): 1, ('W/D', 'D/L'): 2}

#### ('cyl:5x5', 'le2', 'QRBN', 1): by model class

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 40 | 0 | 12 | 13 | 14/15 | 93.3% | [70.2, 98.8] | 0 | 1 | 0 | 1 |
| N | 30 | 0 | 16 | 7 | 6/7 | 85.7% | [48.7, 97.4] | 1 | 0 | 0 | 1 |
| P | 13 | 0 | 6 | 7 | 0 | - | - | - | - | - | - |
| R | 40 | 0 | 18 | 5 | 15/17 | 88.2% | [65.7, 96.7] | 2 | 0 | 0 | 2 |
| race | 117 | 104 | 13 | 0 | 0 | - | - | - | - | - | - |

#### ('cyl:5x5', 'le2', 'QRBN', 1): by pawns (W/B)

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1/1 | 30 | 17 | 5 | 5 | 3/3 | 100.0% | [43.8, 100.0] | 0 | 0 | 0 | 0 |
| 1/2 | 60 | 22 | 20 | 6 | 12/12 | 100.0% | [75.7, 100.0] | 0 | 0 | 0 | 0 |
| 2/1 | 60 | 26 | 10 | 9 | 13/15 | 86.7% | [62.1, 96.3] | 1 | 1 | 0 | 2 |
| 2/2 | 90 | 39 | 30 | 12 | 7/9 | 77.8% | [45.3, 93.7] | 2 | 0 | 0 | 2 |

Races at start, ('cyl:5x5', 'le2', 'QRBN', 1): real outcome (wtm,btm) counts: {('W/W', 'L/L'): 8, ('L/L', 'L/L'): 5, ('W/L', 'L/L'): 24, ('W/W', 'W/L'): 28, ('W/W', 'W/W'): 6, ('D/L', 'L/L'): 1, ('W/L', 'W/L'): 25, ('W/L', 'D/L'): 7}

#### ('cyl:6x6', 'le2', 'Q', 2): by model class

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 6 | 0 | 0 | 0 | 6/6 | 100.0% | [61.0, 100.0] | 0 | 0 | 0 | 0 |
| N | 5 | 0 | 0 | 0 | 0/5 | 0.0% | [0.0, 43.4] | 5 | 0 | 5 | 5 |
| P | 9 | 0 | 0 | 0 | 1/9 | 11.1% | [2.0, 43.5] | 8 | 0 | 5 | 8 |
| R | 6 | 0 | 0 | 0 | 6/6 | 100.0% | [61.0, 100.0] | 0 | 0 | 0 | 0 |
| race | 16 | 16 | 0 | 0 | 0 | - | - | - | - | - | - |

#### ('cyl:6x6', 'le2', 'Q', 2): by pawns (W/B)

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1/1 | 12 | 6 | 0 | 0 | 0/6 | 0.0% | [0.0, 39.0] | 6 | 0 | 6 | 6 |
| 1/2 | 12 | 4 | 0 | 0 | 5/8 | 62.5% | [30.6, 86.3] | 3 | 0 | 2 | 3 |
| 2/1 | 12 | 4 | 0 | 0 | 5/8 | 62.5% | [30.6, 86.3] | 3 | 0 | 2 | 3 |
| 2/2 | 6 | 2 | 0 | 0 | 3/4 | 75.0% | [30.1, 95.4] | 1 | 0 | 0 | 1 |

Races at start, ('cyl:6x6', 'le2', 'Q', 2): real outcome (wtm,btm) counts: {('L/L', 'L/L'): 5, ('W/W', 'L/L'): 4, ('W/W', 'W/W'): 5, ('W/D', 'D/L'): 2}

#### ('cyl:6x6', 'le2', 'QRBN', 1): by model class

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 6 | 0 | 0 | 0 | 6/6 | 100.0% | [61.0, 100.0] | 0 | 0 | 0 | 0 |
| N | 5 | 0 | 0 | 5 | 0 | - | - | - | - | - | - |
| P | 9 | 0 | 0 | 8 | 1/1 | 100.0% | [20.7, 100.0] | 0 | 0 | 0 | 0 |
| R | 6 | 0 | 0 | 0 | 6/6 | 100.0% | [61.0, 100.0] | 0 | 0 | 0 | 0 |
| race | 16 | 16 | 0 | 0 | 0 | - | - | - | - | - | - |

#### ('cyl:6x6', 'le2', 'QRBN', 1): by pawns (W/B)

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1/1 | 12 | 6 | 0 | 6 | 0 | - | - | - | - | - | - |
| 1/2 | 12 | 4 | 0 | 3 | 5/5 | 100.0% | [56.6, 100.0] | 0 | 0 | 0 | 0 |
| 2/1 | 12 | 4 | 0 | 3 | 5/5 | 100.0% | [56.6, 100.0] | 0 | 0 | 0 | 0 |
| 2/2 | 6 | 2 | 0 | 1 | 3/3 | 100.0% | [43.8, 100.0] | 0 | 0 | 0 | 0 |

Races at start, ('cyl:6x6', 'le2', 'QRBN', 1): real outcome (wtm,btm) counts: {('L/L', 'L/L'): 1, ('W/L', 'L/L'): 3, ('W/L', 'W/L'): 8, ('W/W', 'W/L'): 3, ('W/W', 'W/W'): 1}

#### ('flat:5x6', 'ext3', 'Q', 2): by model class

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 2 | 0 | 0 | 0 | 2/2 | 100.0% | [34.2, 100.0] | 0 | 0 | 0 | 0 |
| P | 2 | 0 | 0 | 0 | 1/2 | 50.0% | [9.5, 90.5] | 1 | 0 | 0 | 1 |
| R | 2 | 0 | 0 | 0 | 2/2 | 100.0% | [34.2, 100.0] | 0 | 0 | 0 | 0 |
| race | 2 | 2 | 0 | 0 | 0 | - | - | - | - | - | - |

#### ('flat:5x6', 'ext3', 'Q', 2): by pawns (W/B)

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1/3 | 4 | 1 | 0 | 0 | 3/3 | 100.0% | [43.8, 100.0] | 0 | 0 | 0 | 0 |
| 3/1 | 4 | 1 | 0 | 0 | 2/3 | 66.7% | [20.8, 93.9] | 1 | 0 | 0 | 1 |

Races at start, ('flat:5x6', 'ext3', 'Q', 2): real outcome (wtm,btm) counts: {('L/L', 'L/L'): 1, ('W/W', 'W/D'): 1}

#### ('flat:5x6', 'le2', 'Q', 2): by model class

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 6 | 0 | 0 | 0 | 6/6 | 100.0% | [61.0, 100.0] | 0 | 0 | 0 | 0 |
| N | 5 | 0 | 0 | 0 | 5/5 | 100.0% | [56.6, 100.0] | 0 | 0 | 0 | 0 |
| P | 9 | 0 | 0 | 0 | 6/9 | 66.7% | [35.4, 87.9] | 3 | 0 | 1 | 3 |
| R | 6 | 0 | 0 | 0 | 6/6 | 100.0% | [61.0, 100.0] | 0 | 0 | 0 | 0 |
| race | 16 | 16 | 0 | 0 | 0 | - | - | - | - | - | - |

#### ('flat:5x6', 'le2', 'Q', 2): by pawns (W/B)

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1/1 | 12 | 6 | 0 | 0 | 5/6 | 83.3% | [43.6, 97.0] | 1 | 0 | 1 | 1 |
| 1/2 | 12 | 4 | 0 | 0 | 8/8 | 100.0% | [67.6, 100.0] | 0 | 0 | 0 | 0 |
| 2/1 | 12 | 4 | 0 | 0 | 7/8 | 87.5% | [52.9, 97.8] | 1 | 0 | 0 | 1 |
| 2/2 | 6 | 2 | 0 | 0 | 3/4 | 75.0% | [30.1, 95.4] | 1 | 0 | 0 | 1 |

Races at start, ('flat:5x6', 'le2', 'Q', 2): real outcome (wtm,btm) counts: {('L/L', 'L/L'): 5, ('W/W', 'L/L'): 3, ('W/W', 'W/W'): 2, ('D/D', 'L/L'): 2, ('W/D', 'D/D'): 1, ('W/D', 'W/D'): 1, ('W/W', 'W/D'): 1, ('W/L', 'D/L'): 1}

#### ('flat:5x6', 'le2', 'QRBN', 1): by model class

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 6 | 0 | 0 | 0 | 6/6 | 100.0% | [61.0, 100.0] | 0 | 0 | 0 | 0 |
| N | 5 | 0 | 0 | 4 | 1/1 | 100.0% | [20.7, 100.0] | 0 | 0 | 0 | 0 |
| P | 9 | 0 | 0 | 7 | 2/2 | 100.0% | [34.2, 100.0] | 0 | 0 | 0 | 0 |
| R | 6 | 0 | 0 | 0 | 6/6 | 100.0% | [61.0, 100.0] | 0 | 0 | 0 | 0 |
| race | 16 | 16 | 0 | 0 | 0 | - | - | - | - | - | - |

#### ('flat:5x6', 'le2', 'QRBN', 1): by pawns (W/B)

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1/1 | 12 | 6 | 0 | 6 | 0 | - | - | - | - | - | - |
| 1/2 | 12 | 4 | 0 | 1 | 7/7 | 100.0% | [64.6, 100.0] | 0 | 0 | 0 | 0 |
| 2/1 | 12 | 4 | 0 | 3 | 5/5 | 100.0% | [56.6, 100.0] | 0 | 0 | 0 | 0 |
| 2/2 | 6 | 2 | 0 | 1 | 3/3 | 100.0% | [43.8, 100.0] | 0 | 0 | 0 | 0 |

Races at start, ('flat:5x6', 'le2', 'QRBN', 1): real outcome (wtm,btm) counts: {('L/L', 'L/L'): 1, ('W/L', 'L/L'): 2, ('W/W', 'W/L'): 3, ('W/L', 'W/L'): 8, ('W/W', 'W/W'): 1, ('W/L', 'D/L'): 1}

#### POOLED Q cap2 all boards/sets: by board

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ('cyl:4x4', 'le2') | 2 | 1 | 0 | 0 | 0/1 | 0.0% | [0.0, 79.3] | 1 | 0 | 1 | 1 |
| ('cyl:5x5', 'le2') | 240 | 104 | 65 | 0 | 49/71 | 69.0% | [57.5, 78.6] | 20 | 2 | 11 | 22 |
| ('cyl:6x6', 'le2') | 42 | 16 | 0 | 0 | 13/26 | 50.0% | [32.1, 67.9] | 13 | 0 | 10 | 13 |
| ('flat:5x6', 'ext3') | 8 | 2 | 0 | 0 | 5/6 | 83.3% | [43.6, 97.0] | 1 | 0 | 0 | 1 |
| ('flat:5x6', 'le2') | 42 | 16 | 0 | 0 | 23/26 | 88.5% | [71.0, 96.0] | 3 | 0 | 1 | 3 |

#### POOLED Q cap2 le2 sets: by model class

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| L | 52 | 0 | 12 | 0 | 33/40 | 82.5% | [68.0, 91.3] | 6 | 1 | 3 | 7 |
| N | 40 | 0 | 16 | 0 | 14/24 | 58.3% | [38.8, 75.5] | 10 | 0 | 8 | 10 |
| P | 32 | 0 | 6 | 0 | 9/26 | 34.6% | [19.4, 53.8] | 17 | 0 | 10 | 17 |
| R | 52 | 0 | 18 | 0 | 29/34 | 85.3% | [69.9, 93.6] | 4 | 1 | 2 | 5 |
| race | 150 | 137 | 13 | 0 | 0 | - | - | - | - | - | - |

#### POOLED Q cap2 le2 sets: all

| group | rows | race | one side illegal | undetermined | match/testable | accuracy | Wilson 95% CI | king effect | convention | mismatches with a real draw | mismatches |
|---|---|---|---|---|---|---|---|---|---|---|---|
| all | 326 | 137 | 65 | 0 | 85/124 | 68.5% | [59.9, 76.1] | 37 | 2 | 23 | 39 |

#### Side-level (each legal, exactly valued side to move, non-race, Q cap 2, le2)

| board | agree/sides | accuracy | Wilson 95% CI |
|---|---|---|---|
| cyl:4x4 | 0/2 | 0.0% | [0.0, 65.8] |
| cyl:5x5 | 152/194 | 78.4% | [72.0, 83.6] |
| cyl:6x6 | 32/52 | 61.5% | [48.0, 73.5] |
| flat:5x6 | 49/52 | 94.2% | [84.4, 98.0] |

#### Q-only vs QRBN (cap 2) per position

- ('cyl:4x4', 'le2'): {'both exact, equal': 2}
