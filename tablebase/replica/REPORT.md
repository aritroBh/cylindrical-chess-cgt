# B2 replication: 4-man tablebases on the plane, cylinder and torus

**Status: verified.** Two independent implementations agree on every summary number and on every
position of every table, for both sides to move. That is 24 tables and about 607 million position
values, with no differences. Every claim the prototype made in RESEARCH_PLAN.md §1.3 holds exactly.

- Replica: [`replica.c`](replica.c), written for this check.
- Prototype: [`../egt_prototype.c`](../egt_prototype.c).

## How the replica was kept independent

- `replica.c` was written from the rules below without opening `egt_prototype.c`.
- Its results were committed (`52475ac`) before the prototype was opened, built or run.
- Later edits only add output: mate and stalemate counts, a table dump, and a draw classifier.
  `git diff 52475ac -- tablebase/replica/replica.c` shows the solving code is unchanged.
- The two programs reach the same tables by different routes:

| | Replica | Prototype |
|---|---|---|
| Iteration | Alternating passes: odd plies mark white wins, even plies mark black losses | One loop on depth in moves, a black pass then a white pass |
| Units | Plies | Moves |
| Black captures | Re-tests the target square with the captured man removed | One attack map for all white men |
| Termination | Two quiet passes, and depth beyond the longest sub-table win | First iteration with no change |
| Self-checks | Bellman equations and board symmetries, on every position | None |
| Threads | 14 | 1 |

The self-checks pass on all tables. The Bellman check re-derives every value from its children. The
symmetry check confirms invariance under the board's own symmetries:
- plane: mirrors and transpose;
- cylinder: file shift and both mirrors;
- torus: both shifts, mirror and transpose.

## Rules modelled

- Board: 8×8. The cylinder glues files a and h. The torus also glues ranks 1 and 8.
- Moves: standard piece moves, with wraparound on glued edges.
- Sliders stop when their ray returns to their own square, so a rook cannot "go round the rank"
  as a null move.
- No castling, no 50-move rule. Stalemate is a draw.
- When black captures, play continues in the smaller table. Bare kings are a draw.
- A white-to-move position is legal when the men stand on distinct squares, the kings are not
  adjacent (wraparound included), and the black king is not in check.
- With two identical men (RR, same-coloured BB), both orderings are counted. Percentages are
  unaffected.

## Plane sanity check

All published flat-board maxima are reproduced:

| Material | Max DTM | Expected |
|---|---|---|
| KQK | 10 | 10 |
| KRK | 16 | 16 |
| KBBK (opposite colours) | 19 | 19 |
| KBNK | 33 | 33 |
| KNNK | not forced (0.0107% won, all mate in 1) | not forced |

## Results (white to move)

"Won" is the share of legal white-to-move positions that white wins. DTM is in moves. The example
is the first maximal position in index order. Upper case is white; k is the black king.

| Board | Material | Legal | Won | Won % | Max DTM | A maximal position |
|---|---|---|---|---|---|---|
| plane | KQK | 144,508 | 144,508 | 100.0000% | 10 | Ka1 Qb2 kf5 |
| plane | KRK | 175,168 | 175,168 | 100.0000% | 16 | Ka1 Rb2 kc3 |
| plane | KBBK | 10,164,056 | 5,007,216 | 49.2640% | 19 | Ka1 Bd1 Bh4 kd2 |
| plane | KBBK, opposite colours | 5,008,256 | 5,007,216 | 99.9792% | 19 | Ka1 Bd1 Bh4 kd2 |
| plane | KBBK, same colour | 5,155,800 | 0 | 0 | none | none |
| plane | KBNK | 10,875,504 | 10,822,184 | 99.5097% | 33 | Ka1 Be1 Nh6 kc1 |
| plane | KNNK | 11,499,304 | 1,232 | 0.0107% | 1 | Ka1 Nd2 Ne3 kc1 |
| plane | KRBK | 9,366,840 | 9,366,840 | 100.0000% | 16 | Ka1 Rc2 Bd4 kd3 |
| plane | KRRK | 8,325,184 | 8,325,184 | 100.0000% | 7 | Ka1 Rb1 Rc2 kd3 |
| plane | KQRK | 6,911,296 | 6,911,296 | 100.0000% | 6 | Ka1 Qh1 Rc3 kd4 |
| **cylinder** | KQK | 127,568 | 127,568 | 100.0000% | 10 | Ka1 Qa8 ke5 |
| **cylinder** | KRK | 172,480 | 4,832 | **2.8015%** | 3 | Ka3 Rb2 ka1 |
| **cylinder** | KBBK | 8,539,584 | 4,026,816 | 47.1547% | 14 | Ka1 Bc1 Bc2 kc3 |
| **cylinder** | KBBK, opposite colours | 4,026,816 | 4,026,816 | **100.0000%** | **14** | Ka1 Bc1 Bc2 kc3 |
| **cylinder** | KBBK, same colour | 4,512,768 | 0 | 0 | none | none |
| **cylinder** | KBNK | 9,733,264 | 2,384 | **0.0245%** | 2 | Ka3 Bc2 Ng1 ka1 |
| **cylinder** | KNNK | 10,861,312 | 832 | 0.0077% | 1 | Ka1 Nd2 Ne3 kc1 |
| **cylinder** | KRBK | 8,519,136 | 8,497,216 | 99.7427% | 13 | Ka1 Rc2 Ba3 kb3 |
| **cylinder** | KRRK | 8,168,384 | 8,168,384 | 100.0000% | 8 | Ka1 Ra2 Rb4 kc5 |
| **cylinder** | KQRK | 6,116,528 | 6,116,528 | 100.0000% | 5 | Ka1 Qh1 Rb2 kc3 |
| **torus** | KQK | 124,416 | 0 | 0 | none | none |
| **torus** | KRK | 169,600 | 0 | 0 | none | none |
| **torus** | KBBK | 8,335,488 | 0 | 0 | none | none |
| **torus** | KBBK, opposite colours | 3,916,800 | 0 | 0 | none | none |
| **torus** | KBBK, same colour | 4,418,688 | 0 | 0 | none | none |
| **torus** | KBNK | 9,228,288 | 0 | 0 | none | none |
| **torus** | KNNK | 10,129,536 | 0 | 0 | none | none |
| **torus** | KRBK | 8,222,336 | 1,792 | 0.0218% | 1 | Ka1 Rd2 Bh5 kc1 |
| **torus** | KRRK | 8,002,560 | 8,002,560 | 100.0000% | 7 | Ka1 Rb1 Rc2 kd3 |
| **torus** | KQRK | 5,874,176 | 5,874,176 | 100.0000% | 5 | Ka1 Qa3 Rc2 kd1 |

### Which material wins

In chess terms, "wins" means won from almost every position. The exceptions are positions where
white loses a man or stalemates at once. Each cell gives the verdict, the share of legal
white-to-move positions won, and the longest mate.

| Material | Plane | Cylinder | Torus |
|---|---|---|---|
| KQK | win, 100%, 10 | win, 100%, 10 | draw, 0 |
| KRK | win, 100%, 16 | **draw**, 2.80%, 3 | draw, 0 |
| KBBK, opposite colours | win, 99.98%, 19 | **win, 100%, 14** | draw, 0 |
| KBNK | win, 99.51%, 33 | **draw**, 0.0245%, 2 | draw, 0 |
| KNNK | draw, 0.0107%, 1 | draw, 0.0077%, 1 | draw, 0 |
| KRBK | win, 100%, 16 | win, 99.74%, 13 | **draw**, 0.0218%, 1 |
| KRRK | win, 100%, 7 | win, 100%, 8 | win, 100%, 7 |
| KQRK | win, 100%, 6 | win, 100%, 5 | win, 100%, 5 |

Two cases are measured exactly (`./replica <board> <men> draws`):
- **Cylinder KRBK** is a win in the same sense as flat KBNK. In all 21,920 drawn positions, every
  white move lets black take a man at once or stalemates him.
- **Flat KBNK**, for comparison, has 53,320 drawn positions. In 42,384 of them the loss of a man
  or stalemate comes at once. In the other 10,936, white has a move that avoids both at once, yet
  still cannot win.

## Agreement with the prototype

### Its claims in RESEARCH_PLAN.md §1.3

| Claim | Replica | Status |
|---|---|---|
| Cylinder KQK: 100%, max 10 | 100% (127,568 / 127,568), max 10 | confirmed |
| Cylinder KRK: 2.8% won, not forced | 2.8015% (4,832 / 172,480), max 3 | confirmed |
| Cylinder KBBK, opposite colours: 100%, max 14 | 100% (4,026,816 / 4,026,816), max 14 | confirmed |
| Cylinder KBNK: 0.024% | 0.0245% (2,384 / 9,733,264), max 2 | confirmed |
| Cylinder KNNK: 0.008% | 0.0077% (832 / 10,861,312), max 1 | confirmed |
| Cylinder KRBK: 99.743%, max 13 | 99.7427% (8,497,216 / 8,519,136), max 13 | confirmed |
| Torus KQK, KRK, KBBK, KBNK, KNNK: no wins | 0 won in each | confirmed |
| Torus KRBK: 0.022% | 0.0218% (1,792 / 8,222,336), max 1 | confirmed |

### Number by number

[`compare.py`](compare.py) checks the five numbers the prototype prints for each table: legal
white-to-move positions, won, max DTM, black-to-move mates and stalemates. For KBBK it also checks
the two opposite-colour counts. All 126 numbers in the 24 tables agree; the log is in
[`prototype_results/`](prototype_results/).

### Position by position

[`compare_positions.py`](compare_positions.py) compares every value in every table, white and black
to move, after converting the replica's plies to moves. Every one of the 24 tables has 0
differences ([`position_compare.txt`](position_compare.txt)).

There were no discrepancies to trace.

## Observations

- **Torus KBBK mates exist but can never happen.** There are 1,536 black-to-move checkmates, for
  example Ka1 Bg5 Bh5 kc1. Yet no white-to-move position is won, not even in 1, so no legal white
  move ever produces one. In the example, c1 lies on both diagonals of g5, four steps away in each
  direction, so the bishop checks along four rays. If the bishop moved last, it came from one of
  those diagonals, where nothing stands between it and c1. If another man moved, it could have
  blocked at most one of the four rays. Either way black was already in check with white to move,
  which is illegal.
- **Torus KRBK mates can happen but cannot be forced.** All 1,792 wins are mates in 1, for example
  Ka1 Rd2 Bh5 kc1, 1.Rd1#. From every other position black escapes.
- **Cylinder KRK wins only from mating nets already in place.** The longest is 3 moves:
  Ka3 Rb2 ka1, then 1.Rb3 Kh1 2.Rg3 Ka1 3.Rg1#. On the cylinder, h1 and h2 are neighbours of a1.
  In the final position the rook covers h1, and the king on a3 covers h2 across the glued edge.
- **Black-to-move maxima can exceed white-to-move maxima.** In KRRK and KQRK, black can capture a
  rook and drop into the longer KRK or KQK table. For example, plane KRRK has a white-to-move
  maximum of 7 but a black-to-move maximum of 16 (the KRK maximum).
- **Cylinder versus plane.** KQK keeps its maximum of 10. KRRK needs one move more (8 against 7)
  and KQRK one move fewer (5 against 6).

## Notes on the prototype for the 5- and 6-man extension

None of these affects the 4-man results above, since every position agrees.

1. **Early stop.** It stops at the first iteration with no change, even when a capture into a
   sub-table could still resolve positions at a greater depth. A table whose depth profile has a
   gap below the sub-table's longest win would come out wrong. The replica refuses to stop before
   passing the longest sub-table win.
2. **Value range.** Values are `int8_t`, and depth is capped at 120 moves. That is ample here (the
   maximum is 33) but may not be for larger tables.
3. **No self-check.** It has no built-in check of its own output.

## Mating lines from the maximal positions

White plays a fastest mate and black a slowest defence (`./replica <board> <men> probe "<pos>"`).
Lower-case k moves are black's; `kxB` is a capture.

```
cyl   KQK   Ka1 Qa8 ke5        1.Ka1-a2 ke5-e6 2.Ka2-a3 ke6-e5 3.Ka3-a4 ke5-f4 4.Qa8-d5 kf4-e3 5.Ka4-a3 ke3-e2
                               6.Ka3-h3 ke2-e3 7.Kh3-g3 ke3-e2 8.Qd5-d4 ke2-e1 9.Kg3-f3 ke1-f1 10.Qd4-a1#
cyl   KRK   Ka3 Rb2 ka1        1.Rb2-b3 ka1-h1 2.Rb3-g3 kh1-a1 3.Rg3-g1#
cyl   KBBK  Ka1 Bc1 Bc2 kc3    1.Ka1-b1 kc3-c4 2.Kb1-b2 kc4-d4 3.Kb2-b3 kd4-c5 4.Kb3-c3 kc5-c6 5.Kc3-c4 kc6-d6
                               6.Bc1-e3 kd6-e6 7.Kc4-c5 ke6-e7 8.Kc5-d5 ke7-d7 9.Be3-f2 kd7-e7 10.Bf2-h4 ke7-d7
                               11.Bc2-d3 kd7-e8 12.Kd5-e6 ke8-f8 13.Bh4-e1 kf8-e8 14.Bd3-f1#
cyl   KBNK  Ka3 Bc2 Ng1 ka1    1.Ng1-h3 ka1-h1 2.Bc2-e4#
cyl   KNNK  Ka1 Nd2 Ne3 kc1    1.Nd2-b3#
cyl   KRBK  Ka1 Rc2 Ba3 kb3    1.Rc2-a2 kb3-c4 2.Ka1-b1 kc4-d4 3.Kb1-c2 kd4-d5 4.Kc2-d3 kd5-e5 5.Kd3-e3 ke5-f5
                               6.Ba3-b2 kf5-g6 7.Ke3-f4 kg6-h5 8.Kf4-f5 kh5-h6 9.Kf5-g4 kh6-g6 10.Ra2-h2 kg6-f7
                               11.Kg4-f5 kf7-f8 12.Kf5-e6 kf8-g8 13.Rh2-h8#
cyl   KRRK  Ka1 Ra2 Rb4 kc5    1.Ra2-b2 kc5-c6 2.Ka1-h2 kc6-c5 3.Kh2-g3 kc5-c6 4.Kg3-f4 kc6-c7 5.Kf4-e4 kc7-c8
                               6.Rb4-b7 kc8-d8 7.Rb2-c2 kd8-e8 8.Rc2-c8#
cyl   KQRK  Ka1 Qh1 Rb2 kc3    1.Ka1-h2 kc3-d3 2.Qh1-d5 kd3-e3 3.Kh2-g2 ke3-f4 4.Rb2-d2 kf4-g4 5.Rd2-d4#
torus KRBK  Ka1 Rd2 Bh5 kc1    1.Rd2-d1#
torus KRRK  Ka1 Rb1 Rc2 kd3    1.Ka1-b2 kd3-d4 2.Rb1-e1 kd4-d5 3.Rc2-d2 kd5-c5 4.Re1-e6 kc5-b5 5.Kb2-b3 kb5-c5
                               6.Kb3-a4 kc5-c4 7.Re6-c6#
torus KQRK  Ka1 Qa3 Rc2 kd1    1.Ka1-b1 kd1-e1 2.Kb1-c8 ke1-f1 3.Qa3-g3 kf1-f8 4.Kc8-d7 kf8-f1 5.Rc2-f2#
```

## Reproduce

Run these from this folder, one command per block.

Solve every table with the self-checks. This takes about 15 seconds on 14 cores and writes
`results/`:

```bash
./run_all.sh
```

Cross-check against the prototype, number by number and then position by position. This takes
about 3 minutes, because the prototype is single-threaded:

```bash
./crosscheck.sh
```

Print one position's value and mating line:

```bash
./replica cyl BB probe "Ka1 Bc1 Bc2 kc3"
```
