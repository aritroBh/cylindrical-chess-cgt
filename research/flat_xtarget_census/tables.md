
## 0. Pool

| item | value |
|---|---|
| distinct positions (normal FEN) | 2154 |
| source conflicts (same FEN, different result) | 0 |
| positions by men | {4: 1, 5: 20, 6: 247, 7: 1283, 8: 597, 9: 6} |
| kpsolve exact positions | 36 |
| kpsolve positions also answered by a Lichess/search source (all agree, 0 conflicts) | 13 |


## 1. Reproduction of the A2 node figures (462 positions, 295 resolved)

| setting | agree | disagree | real draw | outside |
|---|---|---|---|---|
| textbook|count | 263 | 19 | 13 | 0 |
| textbook|mover | 261 | 21 | 13 | 0 |
| textbook|opponent | 239 | 43 | 13 | 0 |
| e.p.-aware|count | 268 | 14 | 13 | 0 |
| e.p.-aware|mover | 266 | 16 | 13 | 0 |
| e.p.-aware|opponent | 247 | 35 | 13 | 0 |

| setting | configurations whose outcome class agrees |
|---|---|
| textbook|count | 91/119 |
| textbook|mover | 90/119 |
| textbook|opponent | 85/119 |
| e.p.-aware|count | 92/119 |
| e.p.-aware|mover | 91/119 |
| e.p.-aware|opponent | 85/119 |

Real classes of the 119 configurations: {'R': 6, 'N': 89, 'D': 13, 'L': 10, 'P': 1}.

Stored values in realchess/results/comp_Wa2c2_Bb7d7_nodes_vs_model_offline.json: e.p.-aware count 268/14/13, mover 266/16/13, opponent 247/35/13; textbook count 263/19/13, mover 261/21/13, opponent 239/43/13; configurations 92/91/85 (e.p.-aware) and 91/90/85 (textbook) of 119.


## 2. Whole pool by kind of position (decisive agreement, Wilson 95% CI)

| passer test | race rule | kind | agree / decisive | real draws | not scored | n |
|---|---|---|---|---|---|---|
| textbook | count | end-position side | 1204/1352 = 89.1% [87.3, 90.6] | 52 | 0 | 1404 |
| textbook | mover | end-position side | 1040/1352 = 76.9% [74.6, 79.1] | 52 | 0 | 1404 |
| textbook | opponent | end-position side | 1050/1352 = 77.7% [75.4, 79.8] | 52 | 0 | 1404 |
| textbook | count | internal node | 670/697 = 96.1% [94.4, 97.3] | 53 | 0 | 750 |
| textbook | mover | internal node | 619/697 = 88.8% [86.3, 90.9] | 53 | 0 | 750 |
| textbook | opponent | internal node | 639/697 = 91.7% [89.4, 93.5] | 53 | 0 | 750 |
| textbook | count | all | 1874/2049 = 91.5% [90.2, 92.6] | 105 | 0 | 2154 |
| textbook | mover | all | 1659/2049 = 81.0% [79.2, 82.6] | 105 | 0 | 2154 |
| textbook | opponent | all | 1689/2049 = 82.4% [80.7, 84.0] | 105 | 0 | 2154 |
| e.p.-aware | count | end-position side | 1204/1335 = 90.2% [88.5, 91.7] | 52 | 0 | 1387 |
| e.p.-aware | mover | end-position side | 1040/1335 = 77.9% [75.6, 80.0] | 52 | 0 | 1387 |
| e.p.-aware | opponent | end-position side | 1050/1335 = 78.7% [76.4, 80.8] | 52 | 0 | 1387 |
| e.p.-aware | count | internal node | 692/714 = 96.9% [95.4, 98.0] | 53 | 0 | 767 |
| e.p.-aware | mover | internal node | 661/714 = 92.6% [90.4, 94.3] | 53 | 0 | 767 |
| e.p.-aware | opponent | internal node | 664/714 = 93.0% [90.9, 94.6] | 53 | 0 | 767 |
| e.p.-aware | count | all | 1896/2049 = 92.5% [91.3, 93.6] | 105 | 0 | 2154 |
| e.p.-aware | mover | all | 1701/2049 = 83.0% [81.3, 84.6] | 105 | 0 | 2154 |
| e.p.-aware | opponent | all | 1714/2049 = 83.7% [82.0, 85.2] | 105 | 0 | 2154 |


### 2b. End-position sides by evidence class and by men (e.p.-aware, count)

| evidence | men | agree / decisive | real draws | n |
|---|---|---|---|---|
| tablebase <=7 men | 5 | 20/20 = 100.0% [83.9, 100.0] | 0 | 20 |
| tablebase <=7 men | 6 | 124/127 = 97.6% [93.3, 99.2] | 12 | 139 |
| tablebase <=7 men | 7 | 848/909 = 93.3% [91.5, 94.7] | 40 | 949 |
| Lichess 8-man category only | 8 | 149/215 = 69.3% [62.8, 75.1] | 0 | 215 |
| 8+ men search over tablebase | 8 | 27/28 = 96.4% [82.3, 99.4] | 0 | 28 |
| kpsolve (exact) | 8 | 30/30 = 100.0% [88.6, 100.0] | 0 | 30 |
| kpsolve (exact) | 9 | 6/6 = 100.0% [61.0, 100.0] | 0 | 6 |


## 3. Per target (positions of the target's own tree that have an exact real result)


### 3.1 Passer test: textbook

| target | kind | n | real draws | count a/d | mover a/d | opponent a/d | count agree/decisive [CI] | men |
|---|---|---|---|---|---|---|---|---|
| A2 (refuted *2) | end-position side | 571 | 20 | 464/87 | 399/152 | 432/119 | 464/551 = 84.2% [80.9, 87.0] | {7: 453, 8: 118} |
| A2 (refuted *2) | internal node | 304 | 13 | 272/19 | 270/21 | 248/43 | 272/291 = 93.5% [90.0, 95.8] | {8: 304} |
| up-second-star | end-position side | 18 | 0 | 18/0 | 17/1 | 17/1 | 18/18 = 100.0% [82.4, 100.0] | {6: 4, 7: 8, 8: 6} |
| up-second-star | internal node | 2 | 0 | 2/0 | 0/2 | 2/0 | 2/2 = 100.0% [34.2, 100.0] | {7: 2} |
| tiny(1) | end-position side | 20 | 0 | 20/0 | 19/1 | 19/1 | 20/20 = 100.0% [83.9, 100.0] | {6: 4, 7: 8, 8: 8} |
| tiny(1) | internal node | 2 | 0 | 2/0 | 0/2 | 2/0 | 2/2 = 100.0% [34.2, 100.0] | {7: 2} |
| cand 2 (refuted) | end-position side | 36 | 1 | 34/1 | 27/8 | 28/7 | 34/35 = 97.1% [85.5, 99.5] | {5: 4, 6: 14, 7: 14, 8: 4} |
| cand 2 (refuted) | internal node | 51 | 3 | 48/0 | 41/7 | 47/1 | 48/48 = 100.0% [92.6, 100.0] | {6: 25, 7: 23, 8: 3} |
| cand 5 | end-position side | 26 | 3 | 18/5 | 13/10 | 18/5 | 18/23 = 78.3% [58.1, 90.3] | {6: 16, 7: 5, 8: 5} |
| cand 5 | internal node | 9 | 1 | 8/0 | 4/4 | 8/0 | 8/8 = 100.0% [67.6, 100.0] | {6: 3, 7: 6} |
| 1/8 | end-position side | 303 | 2 | 295/6 | 289/12 | 291/10 | 295/301 = 98.0% [95.7, 99.1] | {5: 16, 6: 51, 7: 218, 8: 12, 9: 6} |
| 1/8 | internal node | 31 | 3 | 28/0 | 25/3 | 26/2 | 28/28 = 100.0% [87.9, 100.0] | {6: 12, 7: 19} |
| cand 3 | end-position side | 241 | 4 | 226/11 | 217/20 | 219/18 | 226/237 = 95.4% [91.9, 97.4] | {5: 16, 6: 42, 7: 170, 8: 11, 9: 2} |
| cand 3 | internal node | 35 | 3 | 30/2 | 25/7 | 30/2 | 30/32 = 93.8% [79.9, 98.3] | {6: 18, 7: 17} |
| cand 4 | end-position side | 61 | 5 | 47/9 | 39/17 | 49/7 | 47/56 = 83.9% [72.2, 91.3] | {6: 22, 7: 24, 8: 15} |
| cand 4 | internal node | 17 | 2 | 14/1 | 11/4 | 15/0 | 14/15 = 93.3% [70.2, 98.8] | {6: 4, 7: 13} |
| cand 6 | end-position side | 106 | 5 | 93/8 | 75/26 | 85/16 | 93/101 = 92.1% [85.1, 95.9] | {5: 8, 6: 13, 7: 69, 8: 16} |
| cand 6 | internal node | 23 | 0 | 23/0 | 23/0 | 21/2 | 23/23 = 100.0% [85.7, 100.0] | {6: 6, 8: 17} |
| pos A (*2 cand.) | end-position side | 20 | 0 | 20/0 | 20/0 | 20/0 | 20/20 = 100.0% [83.9, 100.0] | {8: 20} |
| pos B (*2 cand.) | end-position side | 20 | 0 | 20/0 | 20/0 | 20/0 | 20/20 = 100.0% [83.9, 100.0] | {8: 20} |


### 3.2 Passer test: e.p.-aware

| target | kind | n | real draws | count a/d | mover a/d | opponent a/d | count agree/decisive [CI] | men |
|---|---|---|---|---|---|---|---|---|
| A2 (refuted *2) | end-position side | 609 | 20 | 496/93 | 419/170 | 450/139 | 496/589 = 84.2% [81.0, 86.9] | {7: 470, 8: 139} |
| A2 (refuted *2) | internal node | 319 | 13 | 292/14 | 290/16 | 271/35 | 292/306 = 95.4% [92.5, 97.3] | {8: 319} |
| up-second-star | end-position side | 18 | 0 | 18/0 | 17/1 | 17/1 | 18/18 = 100.0% [82.4, 100.0] | {6: 4, 7: 8, 8: 6} |
| up-second-star | internal node | 2 | 0 | 2/0 | 0/2 | 2/0 | 2/2 = 100.0% [34.2, 100.0] | {7: 2} |
| tiny(1) | end-position side | 20 | 0 | 20/0 | 19/1 | 19/1 | 20/20 = 100.0% [83.9, 100.0] | {6: 4, 7: 8, 8: 8} |
| tiny(1) | internal node | 2 | 0 | 2/0 | 0/2 | 2/0 | 2/2 = 100.0% [34.2, 100.0] | {7: 2} |
| cand 2 (refuted) | end-position side | 36 | 1 | 34/1 | 27/8 | 28/7 | 34/35 = 97.1% [85.5, 99.5] | {5: 4, 6: 14, 7: 14, 8: 4} |
| cand 2 (refuted) | internal node | 51 | 3 | 48/0 | 47/1 | 47/1 | 48/48 = 100.0% [92.6, 100.0] | {6: 25, 7: 23, 8: 3} |
| cand 5 | end-position side | 25 | 3 | 18/4 | 13/9 | 18/4 | 18/22 = 81.8% [61.5, 92.7] | {6: 16, 7: 5, 8: 4} |
| cand 5 | internal node | 10 | 1 | 9/0 | 4/5 | 9/0 | 9/9 = 100.0% [70.1, 100.0] | {6: 3, 7: 6, 8: 1} |
| 1/8 | end-position side | 309 | 2 | 301/6 | 295/12 | 297/10 | 301/307 = 98.0% [95.8, 99.1] | {5: 16, 6: 51, 7: 224, 8: 12, 9: 6} |
| 1/8 | internal node | 31 | 3 | 28/0 | 26/2 | 26/2 | 28/28 = 100.0% [87.9, 100.0] | {6: 12, 7: 19} |
| cand 3 | end-position side | 241 | 4 | 226/11 | 217/20 | 219/18 | 226/237 = 95.4% [91.9, 97.4] | {5: 16, 6: 42, 7: 170, 8: 11, 9: 2} |
| cand 3 | internal node | 35 | 3 | 30/2 | 29/3 | 30/2 | 30/32 = 93.8% [79.9, 98.3] | {6: 18, 7: 17} |
| cand 4 | end-position side | 60 | 5 | 47/8 | 39/16 | 49/6 | 47/55 = 85.5% [73.8, 92.4] | {6: 22, 7: 24, 8: 14} |
| cand 4 | internal node | 18 | 2 | 15/1 | 11/5 | 16/0 | 15/16 = 93.8% [71.7, 98.9] | {6: 4, 7: 13, 8: 1} |
| cand 6 | end-position side | 106 | 5 | 93/8 | 75/26 | 85/16 | 93/101 = 92.1% [85.1, 95.9] | {5: 8, 6: 13, 7: 69, 8: 16} |
| cand 6 | internal node | 23 | 0 | 23/0 | 23/0 | 21/2 | 23/23 = 100.0% [85.7, 100.0] | {6: 6, 8: 17} |
| pos A (*2 cand.) | end-position side | 20 | 0 | 20/0 | 20/0 | 20/0 | 20/20 = 100.0% [83.9, 100.0] | {8: 20} |
| pos B (*2 cand.) | end-position side | 20 | 0 | 20/0 | 20/0 | 20/0 | 20/20 = 100.0% [83.9, 100.0] | {8: 20} |

a/d = agree/disagree among decisive sides. A position in several targets' trees is counted in each row; the rows are not additive (see section 2 for the distinct-position totals).


## 4. Ranking of the six settings (passer test x race rule)


### all decisive scored positions (n = 2049)

| rank | setting | agree / n [95% CI] |
|---|---|---|
| 1 | e.p.-aware|count | 1896/2049 = 92.5% [91.3, 93.6] |
| 2 | textbook|count | 1874/2049 = 91.5% [90.2, 92.6] |
| 3 | e.p.-aware|opponent | 1714/2049 = 83.7% [82.0, 85.2] |
| 4 | e.p.-aware|mover | 1701/2049 = 83.0% [81.3, 84.6] |
| 5 | textbook|opponent | 1689/2049 = 82.4% [80.7, 84.0] |
| 6 | textbook|mover | 1659/2049 = 81.0% [79.2, 82.6] |

| better-ranked | lower-ranked | only first right | only second right | exact McNemar p |
|---|---|---|---|---|
| e.p.-aware|count | textbook|count | 22 | 0 | 4.768e-07 |
| e.p.-aware|count | e.p.-aware|opponent | 209 | 27 | 4.758e-36 |
| e.p.-aware|count | e.p.-aware|mover | 204 | 9 | 3.329e-49 |
| e.p.-aware|count | textbook|opponent | 234 | 27 | 2.468e-42 |
| e.p.-aware|count | textbook|mover | 246 | 9 | 3.904e-61 |
| textbook|count | e.p.-aware|opponent | 209 | 49 | 1.043e-24 |
| textbook|count | e.p.-aware|mover | 200 | 27 | 8.051e-34 |
| textbook|count | textbook|opponent | 212 | 27 | 8.518e-37 |
| textbook|count | textbook|mover | 224 | 9 | 7.198e-55 |
| e.p.-aware|opponent | e.p.-aware|mover | 231 | 218 | 0.5712 |
| e.p.-aware|opponent | textbook|opponent | 26 | 1 | 4.172e-07 |
| e.p.-aware|opponent | textbook|mover | 273 | 218 | 0.01473 |
| e.p.-aware|mover | textbook|opponent | 239 | 227 | 0.6104 |
| e.p.-aware|mover | textbook|mover | 42 | 0 | 4.547e-13 |
| textbook|opponent | textbook|mover | 251 | 221 | 0.1819 |


### end-position sides only (e.p.-aware tree) (n = 1335)

| rank | setting | agree / n [95% CI] |
|---|---|---|
| 1 | textbook|count | 1204/1335 = 90.2% [88.5, 91.7] |
| 2 | e.p.-aware|count | 1204/1335 = 90.2% [88.5, 91.7] |
| 3 | textbook|opponent | 1050/1335 = 78.7% [76.4, 80.8] |
| 4 | e.p.-aware|opponent | 1050/1335 = 78.7% [76.4, 80.8] |
| 5 | textbook|mover | 1040/1335 = 77.9% [75.6, 80.0] |
| 6 | e.p.-aware|mover | 1040/1335 = 77.9% [75.6, 80.0] |

| better-ranked | lower-ranked | only first right | only second right | exact McNemar p |
|---|---|---|---|---|
| textbook|count | e.p.-aware|count | 0 | 0 | 1 |
| textbook|count | textbook|opponent | 173 | 19 | 2.824e-32 |
| textbook|count | e.p.-aware|opponent | 173 | 19 | 2.824e-32 |
| textbook|count | textbook|mover | 173 | 9 | 1.699e-40 |
| textbook|count | e.p.-aware|mover | 173 | 9 | 1.699e-40 |
| e.p.-aware|count | textbook|opponent | 173 | 19 | 2.824e-32 |
| e.p.-aware|count | e.p.-aware|opponent | 173 | 19 | 2.824e-32 |
| e.p.-aware|count | textbook|mover | 173 | 9 | 1.699e-40 |
| e.p.-aware|count | e.p.-aware|mover | 173 | 9 | 1.699e-40 |
| textbook|opponent | e.p.-aware|opponent | 0 | 0 | 1 |
| textbook|opponent | textbook|mover | 192 | 182 | 0.6417 |
| textbook|opponent | e.p.-aware|mover | 192 | 182 | 0.6417 |
| e.p.-aware|opponent | textbook|mover | 192 | 182 | 0.6417 |
| e.p.-aware|opponent | e.p.-aware|mover | 192 | 182 | 0.6417 |
| textbook|mover | e.p.-aware|mover | 0 | 0 | 1 |


### internal nodes only (n = 714)

| rank | setting | agree / n [95% CI] |
|---|---|---|
| 1 | e.p.-aware|count | 692/714 = 96.9% [95.4, 98.0] |
| 2 | textbook|count | 670/714 = 93.8% [91.8, 95.4] |
| 3 | e.p.-aware|opponent | 664/714 = 93.0% [90.9, 94.6] |
| 4 | e.p.-aware|mover | 661/714 = 92.6% [90.4, 94.3] |
| 5 | textbook|opponent | 639/714 = 89.5% [87.0, 91.5] |
| 6 | textbook|mover | 619/714 = 86.7% [84.0, 89.0] |

| better-ranked | lower-ranked | only first right | only second right | exact McNemar p |
|---|---|---|---|---|
| e.p.-aware|count | textbook|count | 22 | 0 | 4.768e-07 |
| e.p.-aware|count | e.p.-aware|opponent | 36 | 8 | 2.545e-05 |
| e.p.-aware|count | e.p.-aware|mover | 31 | 0 | 9.313e-10 |
| e.p.-aware|count | textbook|opponent | 61 | 8 | 3.243e-11 |
| e.p.-aware|count | textbook|mover | 73 | 0 | 2.118e-22 |
| textbook|count | e.p.-aware|opponent | 36 | 30 | 0.5386 |
| textbook|count | e.p.-aware|mover | 27 | 18 | 0.2327 |
| textbook|count | textbook|opponent | 39 | 8 | 5.54e-06 |
| textbook|count | textbook|mover | 51 | 0 | 8.882e-16 |
| e.p.-aware|opponent | e.p.-aware|mover | 39 | 36 | 0.8176 |
| e.p.-aware|opponent | textbook|opponent | 26 | 1 | 4.172e-07 |
| e.p.-aware|opponent | textbook|mover | 81 | 36 | 3.866e-05 |
| e.p.-aware|mover | textbook|opponent | 57 | 35 | 0.02802 |
| e.p.-aware|mover | textbook|mover | 42 | 0 | 4.547e-13 |
| textbook|opponent | textbook|mover | 59 | 39 | 0.05439 |


### race terminals only (both sides have a passer) (n = 345)

| rank | setting | agree / n [95% CI] |
|---|---|---|
| 1 | textbook|count | 317/345 = 91.9% [88.5, 94.3] |
| 2 | e.p.-aware|count | 317/345 = 91.9% [88.5, 94.3] |
| 3 | textbook|mover | 182/345 = 52.8% [47.5, 58.0] |
| 4 | e.p.-aware|mover | 182/345 = 52.8% [47.5, 58.0] |
| 5 | textbook|opponent | 163/345 = 47.2% [42.0, 52.5] |
| 6 | e.p.-aware|opponent | 163/345 = 47.2% [42.0, 52.5] |

| better-ranked | lower-ranked | only first right | only second right | exact McNemar p |
|---|---|---|---|---|
| textbook|count | e.p.-aware|count | 0 | 0 | 1 |
| textbook|count | textbook|mover | 144 | 9 | 1.859e-32 |
| textbook|count | e.p.-aware|mover | 144 | 9 | 1.859e-32 |
| textbook|count | textbook|opponent | 173 | 19 | 2.824e-32 |
| textbook|count | e.p.-aware|opponent | 173 | 19 | 2.824e-32 |
| e.p.-aware|count | textbook|mover | 144 | 9 | 1.859e-32 |
| e.p.-aware|count | e.p.-aware|mover | 144 | 9 | 1.859e-32 |
| e.p.-aware|count | textbook|opponent | 173 | 19 | 2.824e-32 |
| e.p.-aware|count | e.p.-aware|opponent | 173 | 19 | 2.824e-32 |
| textbook|mover | e.p.-aware|mover | 0 | 0 | 1 |
| textbook|mover | textbook|opponent | 182 | 163 | 0.3325 |
| textbook|mover | e.p.-aware|opponent | 182 | 163 | 0.3325 |
| e.p.-aware|mover | textbook|opponent | 182 | 163 | 0.3325 |
| e.p.-aware|mover | e.p.-aware|opponent | 182 | 163 | 0.3325 |
| textbook|opponent | e.p.-aware|opponent | 0 | 0 | 1 |


### excluding Lichess-8-man-category-only positions (n = 1805)

| rank | setting | agree / n [95% CI] |
|---|---|---|
| 1 | e.p.-aware|count | 1718/1805 = 95.2% [94.1, 96.1] |
| 2 | textbook|count | 1713/1805 = 94.9% [93.8, 95.8] |
| 3 | e.p.-aware|mover | 1603/1805 = 88.8% [87.3, 90.2] |
| 4 | textbook|mover | 1576/1805 = 87.3% [85.7, 88.8] |
| 5 | e.p.-aware|opponent | 1530/1805 = 84.8% [83.0, 86.3] |
| 6 | textbook|opponent | 1522/1805 = 84.3% [82.6, 85.9] |

| better-ranked | lower-ranked | only first right | only second right | exact McNemar p |
|---|---|---|---|---|
| e.p.-aware|count | textbook|count | 5 | 0 | 0.0625 |
| e.p.-aware|count | e.p.-aware|mover | 124 | 9 | 5.382e-27 |
| e.p.-aware|count | textbook|mover | 151 | 9 | 2.19e-34 |
| e.p.-aware|count | e.p.-aware|opponent | 209 | 21 | 3.879e-40 |
| e.p.-aware|count | textbook|opponent | 217 | 21 | 3.197e-42 |
| textbook|count | e.p.-aware|mover | 122 | 12 | 4.283e-24 |
| textbook|count | textbook|mover | 146 | 9 | 5.237e-33 |
| textbook|count | e.p.-aware|opponent | 209 | 26 | 1.083e-36 |
| textbook|count | textbook|opponent | 212 | 21 | 6.435e-41 |
| e.p.-aware|mover | textbook|mover | 27 | 0 | 1.49e-08 |
| e.p.-aware|mover | e.p.-aware|opponent | 218 | 145 | 0.0001502 |
| e.p.-aware|mover | textbook|opponent | 224 | 143 | 2.767e-05 |
| textbook|mover | e.p.-aware|opponent | 218 | 172 | 0.02257 |
| textbook|mover | textbook|opponent | 221 | 167 | 0.007054 |
| e.p.-aware|opponent | textbook|opponent | 9 | 1 | 0.02148 |


### positions where the settings differ (n = 495)

| rank | setting | agree / n [95% CI] |
|---|---|---|
| 1 | e.p.-aware|count | 459/495 = 92.7% [90.1, 94.7] |
| 2 | textbook|count | 437/495 = 88.3% [85.2, 90.8] |
| 3 | e.p.-aware|opponent | 277/495 = 56.0% [51.6, 60.3] |
| 4 | e.p.-aware|mover | 264/495 = 53.3% [48.9, 57.7] |
| 5 | textbook|opponent | 252/495 = 50.9% [46.5, 55.3] |
| 6 | textbook|mover | 222/495 = 44.8% [40.5, 49.3] |

| better-ranked | lower-ranked | only first right | only second right | exact McNemar p |
|---|---|---|---|---|
| e.p.-aware|count | textbook|count | 22 | 0 | 4.768e-07 |
| e.p.-aware|count | e.p.-aware|opponent | 209 | 27 | 4.758e-36 |
| e.p.-aware|count | e.p.-aware|mover | 204 | 9 | 3.329e-49 |
| e.p.-aware|count | textbook|opponent | 234 | 27 | 2.468e-42 |
| e.p.-aware|count | textbook|mover | 246 | 9 | 3.904e-61 |
| textbook|count | e.p.-aware|opponent | 209 | 49 | 1.043e-24 |
| textbook|count | e.p.-aware|mover | 200 | 27 | 8.051e-34 |
| textbook|count | textbook|opponent | 212 | 27 | 8.518e-37 |
| textbook|count | textbook|mover | 224 | 9 | 7.198e-55 |
| e.p.-aware|opponent | e.p.-aware|mover | 231 | 218 | 0.5712 |
| e.p.-aware|opponent | textbook|opponent | 26 | 1 | 4.172e-07 |
| e.p.-aware|opponent | textbook|mover | 273 | 218 | 0.01473 |
| e.p.-aware|mover | textbook|opponent | 239 | 227 | 0.6104 |
| e.p.-aware|mover | textbook|mover | 42 | 0 | 4.547e-13 |
| textbook|opponent | textbook|mover | 251 | 221 | 0.1819 |

The pairs share positions and many positions share one terminal (two sides) and overlapping trees, so the McNemar p-values and CIs treat dependent items as independent and are optimistic. Draws are excluded from this section; they are model-independent in count (the model has no draw value).


## 5. Which features predict disagreement? (e.p.-aware, count; decisive scored positions)


### Subset: all decisive scored positions

| feature | coef (log-odds of disagreement) | approx SE | odds ratio | z |
|---|---|---|---|---|
| intercept | -3.006 | 0.308 |  | -9.77 |
| men_minus_8 | +0.587 | 0.219 | 1.8 | +2.68 |
| a_file_pawns | -0.131 | 0.168 | 0.877 | -0.78 |
| race | -0.333 | 0.236 | 0.717 | -1.41 |
| ep_available | -3.124 | 0.711 | 0.044 | -4.39 |
| end_position | +1.084 | 0.262 | 2.96 | +4.14 |
| white_to_move | -0.010 | 0.179 | 0.99 | -0.06 |
| l8_only | +1.650 | 0.279 | 5.21 | +5.92 |

n = 2049 decisive scored positions, 153 disagreements. Ridge penalty 0.5 on slopes (the data are sparse and partly collinear: race implies end_position). Standard errors are model-based and ignore clustering.


### Decision stumps (single split, weighted Gini reduction)

| feature <= threshold | disagree in <= branch | disagree in > branch | Gini reduction |
|---|---|---|---|
| l8_only <= 0 | 87/1805 = 4.8% [3.9, 5.9] | 66/244 = 27.0% [21.9, 32.9] | 0.0104 |
| men_minus_8 <= -1 | 72/1459 = 4.9% [3.9, 6.2] | 81/590 = 13.7% [11.2, 16.7] | 0.0032 |
| end_position <= 0 | 22/714 = 3.1% [2.0, 4.6] | 131/1335 = 9.8% [8.3, 11.5] | 0.0021 |
| a_file_pawns <= 0 | 14/543 = 2.6% [1.5, 4.3] | 139/1506 = 9.2% [7.9, 10.8] | 0.0017 |
| men_minus_8 <= -2 | 3/246 = 1.2% [0.4, 3.5] | 150/1803 = 8.3% [7.1, 9.7] | 0.0011 |
| a_file_pawns <= 1 | 148/1807 = 8.2% [7.0, 9.5] | 5/242 = 2.1% [0.9, 4.7] | 0.0008 |
| ep_available <= 0 | 153/1946 = 7.9% [6.7, 9.1] | 0/103 = 0.0% [0.0, 3.6] | 0.0006 |
| a_file_pawns <= 2 | 153/2002 = 7.6% [6.6, 8.9] | 0/47 = 0.0% [0.0, 7.6] | 0.0003 |
| men_minus_8 <= -3 | 0/21 = 0.0% [0.0, 15.5] | 153/2028 = 7.5% [6.5, 8.8] | 0.0001 |
| men_minus_8 <= 0 | 153/2043 = 7.5% [6.4, 8.7] | 0/6 = 0.0% [0.0, 39.0] | 0.0000 |


### Disagreement rate by single feature value (e.p.-aware, count)

| feature | value | disagree / decisive [CI] |
|---|---|---|
| men_minus_8 | -4 | 0/1 = 0.0% [0.0, 79.3] |
| men_minus_8 | -3 | 0/20 = 0.0% [0.0, 16.1] |
| men_minus_8 | -2 | 3/225 = 1.3% [0.5, 3.8] |
| men_minus_8 | -1 | 69/1213 = 5.7% [4.5, 7.1] |
| men_minus_8 | 0 | 81/584 = 13.9% [11.3, 16.9] |
| men_minus_8 | 1 | 0/6 = 0.0% [0.0, 39.0] |
| a_file_pawns | 0 | 14/543 = 2.6% [1.5, 4.3] |
| a_file_pawns | 1 | 134/1264 = 10.6% [9.0, 12.4] |
| a_file_pawns | 2 | 5/195 = 2.6% [1.1, 5.9] |
| a_file_pawns | 3 | 0/47 = 0.0% [0.0, 7.6] |
| race | 0 | 125/1704 = 7.3% [6.2, 8.7] |
| race | 1 | 28/345 = 8.1% [5.7, 11.5] |
| ep_available | 0 | 153/1946 = 7.9% [6.7, 9.1] |
| ep_available | 1 | 0/103 = 0.0% [0.0, 3.6] |
| end_position | 0 | 22/714 = 3.1% [2.0, 4.6] |
| end_position | 1 | 131/1335 = 9.8% [8.3, 11.5] |
| white_to_move | 0 | 79/1062 = 7.4% [6.0, 9.2] |
| white_to_move | 1 | 74/987 = 7.5% [6.0, 9.3] |
| l8_only | 0 | 87/1805 = 4.8% [3.9, 5.9] |
| l8_only | 1 | 66/244 = 27.0% [21.9, 32.9] |


### Subset: excluding Lichess-8-man-category-only positions

| feature | coef (log-odds of disagreement) | approx SE | odds ratio | z |
|---|---|---|---|---|
| intercept | -3.056 | 0.319 |  | -9.57 |
| men_minus_8 | +0.560 | 0.228 | 1.75 | +2.46 |
| a_file_pawns | -0.105 | 0.180 | 0.9 | -0.58 |
| race | +0.524 | 0.270 | 1.69 | +1.94 |
| ep_available | -1.124 | 0.977 | 0.325 | -1.15 |
| end_position | +0.699 | 0.283 | 2.01 | +2.47 |
| white_to_move | +0.212 | 0.220 | 1.24 | +0.96 |
| l8_only | +0.000 | 1.414 | 1 | +0.00 |

n = 1805 decisive scored positions, 87 disagreements. Ridge penalty 0.5 on slopes (the data are sparse and partly collinear: race implies end_position). Standard errors are model-based and ignore clustering.


### Decision stumps (single split, weighted Gini reduction)

| feature <= threshold | disagree in <= branch | disagree in > branch | Gini reduction |
|---|---|---|---|
| a_file_pawns <= 0 | 14/542 = 2.6% [1.5, 4.3] | 73/1263 = 5.8% [4.6, 7.2] | 0.0004 |
| men_minus_8 <= -2 | 3/246 = 1.2% [0.4, 3.5] | 84/1559 = 5.4% [4.4, 6.6] | 0.0004 |
| race <= 0 | 65/1528 = 4.3% [3.4, 5.4] | 22/277 = 7.9% [5.3, 11.7] | 0.0004 |
| end_position <= 0 | 22/685 = 3.2% [2.1, 4.8] | 65/1120 = 5.8% [4.6, 7.3] | 0.0003 |
| a_file_pawns <= 1 | 82/1564 = 5.2% [4.2, 6.5] | 5/241 = 2.1% [0.9, 4.8] | 0.0002 |
| a_file_pawns <= 2 | 87/1758 = 4.9% [4.0, 6.1] | 0/47 = 0.0% [0.0, 7.6] | 0.0001 |
| ep_available <= 0 | 87/1771 = 4.9% [4.0, 6.0] | 0/34 = 0.0% [0.0, 10.2] | 0.0001 |
| men_minus_8 <= -3 | 0/21 = 0.0% [0.0, 15.5] | 87/1784 = 4.9% [4.0, 6.0] | 0.0001 |
| white_to_move <= 0 | 41/943 = 4.3% [3.2, 5.8] | 46/862 = 5.3% [4.0, 7.0] | 0.0000 |
| men_minus_8 <= 0 | 87/1799 = 4.8% [3.9, 5.9] | 0/6 = 0.0% [0.0, 39.0] | 0.0000 |


### Disagreement rate by single feature value (e.p.-aware, count)

| feature | value | disagree / decisive [CI] |
|---|---|---|
| men_minus_8 | -4 | 0/1 = 0.0% [0.0, 79.3] |
| men_minus_8 | -3 | 0/20 = 0.0% [0.0, 16.1] |
| men_minus_8 | -2 | 3/225 = 1.3% [0.5, 3.8] |
| men_minus_8 | -1 | 69/1213 = 5.7% [4.5, 7.1] |
| men_minus_8 | 0 | 15/340 = 4.4% [2.7, 7.2] |
| men_minus_8 | 1 | 0/6 = 0.0% [0.0, 39.0] |
| a_file_pawns | 0 | 14/542 = 2.6% [1.5, 4.3] |
| a_file_pawns | 1 | 68/1022 = 6.7% [5.3, 8.3] |
| a_file_pawns | 2 | 5/194 = 2.6% [1.1, 5.9] |
| a_file_pawns | 3 | 0/47 = 0.0% [0.0, 7.6] |
| race | 0 | 65/1528 = 4.3% [3.4, 5.4] |
| race | 1 | 22/277 = 7.9% [5.3, 11.7] |
| ep_available | 0 | 87/1771 = 4.9% [4.0, 6.0] |
| ep_available | 1 | 0/34 = 0.0% [0.0, 10.2] |
| end_position | 0 | 22/685 = 3.2% [2.1, 4.8] |
| end_position | 1 | 65/1120 = 5.8% [4.6, 7.3] |
| white_to_move | 0 | 41/943 = 4.3% [3.2, 5.8] |
| white_to_move | 1 | 46/862 = 5.3% [4.0, 7.0] |
| l8_only | 0 | 87/1805 = 4.8% [3.9, 5.9] |


## 6. Every mismatch classified (e.p.-aware, count)

| class | count | by men | with e.p. right |
|---|---|---|---|
| disagree: one-sided passer, the passer's owner does not win in real chess | 103 | {7: 42, 8: 61} | 0 |
| real draw; model says loss (end-position side) | 36 | {6: 6, 7: 30} | 0 |
| real draw; model says win (internal node) | 32 | {6: 5, 7: 18, 8: 9} | 0 |
| disagree: race terminal (race rule picks the wrong winner) | 28 | {6: 3, 7: 19, 8: 6} | 0 |
| disagree: internal node (model first-player outcome wrong) | 22 | {7: 8, 8: 14} | 0 |
| real draw; model says loss (internal node) | 21 | {6: 5, 7: 12, 8: 4} | 0 |
| real draw; model says win (end-position side) | 16 | {6: 6, 7: 10} | 1 |


### Disagreements and real draws by target and mechanism (e.p.-aware, count)

| target | resolved positions | mismatches | by class |
|---|---|---|---|
| A2 (refuted *2) | 928 | 140 | {'real draw; model says win (internal node)': 9, 'real draw; model says loss (internal node)': 4, 'disagree: internal node (model first-player outcome wrong)': 14, "disagree: one-sided passer, the passer's owner does not win in real chess": 78, 'real draw; model says loss (end-position side)': 20, 'disagree: race terminal (race rule picks the wrong winner)': 15} |
| up-second-star | 20 | 0 | {} |
| tiny(1) | 22 | 0 | {} |
| cand 2 (refuted) | 87 | 5 | {'disagree: race terminal (race rule picks the wrong winner)': 1, 'real draw; model says win (internal node)': 1, 'real draw; model says loss (internal node)': 2, 'real draw; model says loss (end-position side)': 1} |
| cand 5 | 35 | 8 | {'real draw; model says loss (internal node)': 1, 'disagree: race terminal (race rule picks the wrong winner)': 3, 'real draw; model says loss (end-position side)': 1, "disagree: one-sided passer, the passer's owner does not win in real chess": 1, 'real draw; model says win (end-position side)': 2} |
| 1/8 | 340 | 11 | {"disagree: one-sided passer, the passer's owner does not win in real chess": 6, 'real draw; model says win (internal node)': 2, 'real draw; model says loss (end-position side)': 2, 'real draw; model says loss (internal node)': 1} |
| cand 3 | 276 | 20 | {'real draw; model says win (internal node)': 2, "disagree: one-sided passer, the passer's owner does not win in real chess": 9, 'real draw; model says loss (end-position side)': 4, 'disagree: race terminal (race rule picks the wrong winner)': 2, 'disagree: internal node (model first-player outcome wrong)': 2, 'real draw; model says loss (internal node)': 1} |
| cand 4 | 78 | 16 | {'disagree: internal node (model first-player outcome wrong)': 1, 'real draw; model says loss (internal node)': 1, "disagree: one-sided passer, the passer's owner does not win in real chess": 4, 'real draw; model says win (internal node)': 1, 'real draw; model says win (end-position side)': 3, 'disagree: race terminal (race rule picks the wrong winner)': 4, 'real draw; model says loss (end-position side)': 2} |
| cand 6 | 129 | 13 | {'disagree: race terminal (race rule picks the wrong winner)': 5, 'real draw; model says loss (end-position side)': 5, "disagree: one-sided passer, the passer's owner does not win in real chess": 3} |
| pos A (*2 cand.) | 20 | 0 | {} |
| pos B (*2 cand.) | 20 | 0 | {} |


## 7. Sensitivity of the class counts to the setting

| setting | disagreements | by kind |
|---|---|---|
| textbook|count | 175 | {'node': 27, 'terminal': 120, 'race': 28} |
| textbook|mover | 390 | {'node': 78, 'terminal': 120, 'race': 192} |
| textbook|opponent | 360 | {'race': 182, 'node': 58, 'terminal': 120} |
| e.p.-aware|count | 153 | {'node': 22, 'terminal': 103, 'race': 28} |
| e.p.-aware|mover | 348 | {'node': 53, 'terminal': 132, 'race': 163} |
| e.p.-aware|opponent | 335 | {'race': 182, 'node': 50, 'terminal': 103} |


## 8. Headline numbers excluding positions whose only evidence is a Lichess 8-man category

| passer test | kind | count rule: agree / decisive | real draws | n |
|---|---|---|---|---|
| textbook | end-position side | 1055/1120 = 94.2% [92.7, 95.4] | 52 | 1172 |
| textbook | internal node | 658/685 = 96.1% [94.3, 97.3] | 53 | 738 |
| textbook | all | 1713/1805 = 94.9% [93.8, 95.8] | 105 | 1910 |
| e.p.-aware | end-position side | 1055/1120 = 94.2% [92.7, 95.4] | 52 | 1172 |
| e.p.-aware | internal node | 663/685 = 96.8% [95.2, 97.9] | 53 | 738 |
| e.p.-aware | all | 1718/1805 = 95.2% [94.1, 96.1] | 105 | 1910 |


## 9. One-sided passer disagreements (e.p.-aware, count): who moves and how far the passer is

| mover | passer distance to queen (moves, capped 6) | disagree / one-sided decisive sides |
|---|---|---|
| owner to move | dist 1 | 0/46 = 0.0% [0.0, 7.7] |
| owner to move | dist 2 | 0/135 = 0.0% [0.0, 2.8] |
| owner to move | dist 3 | 2/137 = 1.5% [0.4, 5.2] |
| owner to move | dist 4 | 3/54 = 5.6% [1.9, 15.1] |
| owner to move | dist 5 | 0/24 = 0.0% [0.0, 13.8] |
| owner's opponent to move | dist 1 | 2/120 = 1.7% [0.5, 5.9] |
| owner's opponent to move | dist 2 | 16/155 = 10.3% [6.5, 16.1] |
| owner's opponent to move | dist 3 | 28/144 = 19.4% [13.8, 26.7] |
| owner's opponent to move | dist 4 | 33/114 = 28.9% [21.4, 37.9] |
| owner's opponent to move | dist 5 | 19/61 = 31.1% [20.9, 43.6] |
