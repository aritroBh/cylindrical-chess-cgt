| class | n | outcome P | has listed win | has legal win | positions w/ illegal listed | illegal listed moves | random legal % | random pawn % |
|---|---|---|---|---|---|---|---|---|
| SHARED | 163 | 33 | 130 | 114 | 72 | 85 | 25.0 | 45.5 |
| ADJACENT | 14 | 2 | 12 | 12 | 0 | 0 | 24.6 | 67.9 |
| APART | 23 | 10 | 13 | 13 | 0 | 0 | 13.8 | 47.8 |
| ADJ+APART | 37 | 12 | 25 | 25 | 0 | 0 | 17.9 | 55.4 |
| ALL200 | 200 | 45 | 155 | 139 | 72 | 85 | 23.7 | 47.3 |

Engine right (k/n %, Wilson95 over n) and right among positions with a listed winning move (k/nw %, Wilson95); wrong answers that were king moves (kw/wrong)

| class | engine | k/n | % | CI | k/nw | % | CI | king moves among wrong |
|---|---|---|---|---|---|---|---|---|
| SHARED | SF1k | 32/163 | 19.6 | 14-26 | 32/130 | 24.6 | 18-33 | 59/131 |
| SHARED | SF10k | 30/163 | 18.4 | 13-25 | 30/130 | 23.1 | 17-31 | 57/133 |
| SHARED | SF100k | 32/163 | 19.6 | 14-26 | 32/130 | 24.6 | 18-33 | 61/131 |
| SHARED | SF1M | 33/163 | 20.2 | 15-27 | 33/130 | 25.4 | 19-33 | 54/130 |
| SHARED | Lc1k | 42/163 | 25.8 | 20-33 | 42/130 | 32.3 | 25-41 | 67/121 |
| SHARED | Lc10k | 44/163 | 27.0 | 21-34 | 44/130 | 33.8 | 26-42 | 62/119 |
| ADJACENT | SF1k | 10/14 | 71.4 | 45-88 | 10/12 | 83.3 | 55-95 | 3/4 |
| ADJACENT | SF10k | 10/14 | 71.4 | 45-88 | 10/12 | 83.3 | 55-95 | 3/4 |
| ADJACENT | SF100k | 10/14 | 71.4 | 45-88 | 10/12 | 83.3 | 55-95 | 3/4 |
| ADJACENT | SF1M | 10/14 | 71.4 | 45-88 | 10/12 | 83.3 | 55-95 | 3/4 |
| ADJACENT | Lc1k | 10/14 | 71.4 | 45-88 | 10/12 | 83.3 | 55-95 | 3/4 |
| ADJACENT | Lc10k | 10/14 | 71.4 | 45-88 | 10/12 | 83.3 | 55-95 | 3/4 |
| APART | SF1k | 13/23 | 56.5 | 37-74 | 13/13 | 100.0 | 77-100 | 6/10 |
| APART | SF10k | 13/23 | 56.5 | 37-74 | 13/13 | 100.0 | 77-100 | 6/10 |
| APART | SF100k | 13/23 | 56.5 | 37-74 | 13/13 | 100.0 | 77-100 | 6/10 |
| APART | SF1M | 13/23 | 56.5 | 37-74 | 13/13 | 100.0 | 77-100 | 6/10 |
| APART | Lc1k | 13/23 | 56.5 | 37-74 | 13/13 | 100.0 | 77-100 | 6/10 |
| APART | Lc10k | 13/23 | 56.5 | 37-74 | 13/13 | 100.0 | 77-100 | 6/10 |
| ADJ+APART | SF1k | 23/37 | 62.2 | 46-76 | 23/25 | 92.0 | 75-98 | 9/14 |
| ADJ+APART | SF10k | 23/37 | 62.2 | 46-76 | 23/25 | 92.0 | 75-98 | 9/14 |
| ADJ+APART | SF100k | 23/37 | 62.2 | 46-76 | 23/25 | 92.0 | 75-98 | 9/14 |
| ADJ+APART | SF1M | 23/37 | 62.2 | 46-76 | 23/25 | 92.0 | 75-98 | 9/14 |
| ADJ+APART | Lc1k | 23/37 | 62.2 | 46-76 | 23/25 | 92.0 | 75-98 | 9/14 |
| ADJ+APART | Lc10k | 23/37 | 62.2 | 46-76 | 23/25 | 92.0 | 75-98 | 9/14 |
| ALL200 | SF1k | 55/200 | 27.5 | 22-34 | 55/155 | 35.5 | 28-43 | 68/145 |
| ALL200 | SF10k | 53/200 | 26.5 | 21-33 | 53/155 | 34.2 | 27-42 | 66/147 |
| ALL200 | SF100k | 55/200 | 27.5 | 22-34 | 55/155 | 35.5 | 28-43 | 70/145 |
| ALL200 | SF1M | 56/200 | 28.0 | 22-35 | 56/155 | 36.1 | 29-44 | 63/144 |
| ALL200 | Lc1k | 65/200 | 32.5 | 26-39 | 65/155 | 41.9 | 34-50 | 76/135 |
| ALL200 | Lc10k | 67/200 | 33.5 | 27-40 | 67/155 | 43.2 | 36-51 | 71/133 |

All embedded rows in meta.json, by class and k (APART = clean):

| class | k=1 | k=2 | k=3 | k=4 | total |
|---|---|---|---|---|---|
| SHARED | 1640 | 7461 | 7486 | 364 | 16951 |
| ADJACENT | 638 | 718 | 44 | 0 | 1400 |
| APART | 1422 | 183 | 0 | 0 | 1605 |
| all | 3700 | 8362 | 7530 | 364 | 19956 |

## Stockfish crashes
Stockfish exited on 27 of 200 positions at every budget (all have a listed winning move, all have >8 pawns for one side; classes: {'SHARED': 27}), scored as errors. Lc0 answered them.

| engine | right/ n | % | Wilson95 | right / n with a listed win | % | Wilson95 |
|---|---|---|---|---|---|---|
| SF1k (the 173 non-crash positions) | 55/173 | 31.8 | 25-39 | 55/128 | 43.0 | 35-52 |
| SF10k (the 173 non-crash positions) | 53/173 | 30.6 | 24-38 | 53/128 | 41.4 | 33-50 |
| SF100k (the 173 non-crash positions) | 55/173 | 31.8 | 25-39 | 55/128 | 43.0 | 35-52 |
| SF1M (the 173 non-crash positions) | 56/173 | 32.4 | 26-40 | 56/128 | 43.8 | 35-52 |
| Lc1k (the 173 non-crash positions) | 57/173 | 32.9 | 26-40 | 57/128 | 44.5 | 36-53 |
| Lc10k (the 173 non-crash positions) | 60/173 | 34.7 | 28-42 | 60/128 | 46.9 | 38-55 |
