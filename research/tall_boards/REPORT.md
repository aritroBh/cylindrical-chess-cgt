# Tall and short boards: how the number of ranks R changes the nimbers of the pawn game

Directory `research/tall_boards/`. Run 2026-11-22, about 2.7 h wall clock on a heavily loaded shared machine, at most two heavy processes at a time.
Labels: COMPUTED-1 = one program (the C solver `tw`); CHECKED-2 = `tw` and `cylcgt` (whole-board model, `.venv/bin/python`) both ran the exact claim.

## Summary (three lines)

1. **No *4 and no nimber above *3 occurs anywhere** in the 1,833,497,669 single-component positions solved (R = 5..12, cylinders of 3, 4, 5 files, flat boards of 3, 4 files); the nimbers found are only *0, *1, *2, *3 (COMPUTED-1). Positions solved by nimber, over all levels run: *0: 4,408,081, *1: 2,524,091, *2: 831, *3: 77.
2. **Height matters a lot and the minima are not monotone in R.** A *2 exists on short boards: with 4 pawns on R = 7 (3 files flat or cylinder, `W: a2 c2 / B: c3 b6`), with 6 to 8 pawns on R = 6 (not on R = 5, where every root on every board has been enumerated and none is *2 or *3). R = 8 gives 6 (C3), 7 (C4), 8 (C5), 7 (flat 4), 10 (flat 3) pawns, reproducing the repo's records. For R >= 9 the *2 minimum is 6 to 8 pawns and a *3 appears with 8 to 10 pawns on most boards.
3. **The paper's open question ("is there a *4 on eight ranks?") is not answered**; R = 8 reproduces every record I could match (about 200 M roots), and no height from 5 to 12 gives a *4 within the pawn counts reached (stated per row below). All 48 *2/*3 minimum positions and 16,000 random positions agree with `cylcgt`.

## The game (my reading of `cylcgt/pawns.py` and `cylcgt/cgt.py`)

Board of F files and R ranks, flat or cylindrical (file adjacency wraps). White pawns move up one square onto an empty square, and from rank 2 may also move two squares if both squares are empty. Black pawns move down, double step only from rank R-1. Captures are diagonal, forwards, onto an enemy pawn. En passant is on: after a double step with an enemy pawn beside the landing square, that enemy may capture the passed-over square, but only as its very next move; the right is gone after any other move (whole-board model: one e.p. right, cleared by any pawn move; for G + *h a move in *h does not clear it). A pawn is *passed* if no enemy pawn stands on its own or an adjacent file in front of it (ranks above for White, below for Black), except that a pawn which can be taken e.p. right now is not passed. The game ends at the first passed pawn: if only one side has one it wins (in CGT terms it is +-BIG); if one move creates passed pawns for both, the race rule "count" decides: the opponent of the mover wins unless the mover promotes strictly sooner, where a front passed pawn on rank r needs R-r moves (minus 1 for a White pawn still on rank 2, and symmetrically for Black on rank R-1). A player with no move loses (normal play). Value of G is `*k` when G + *h is a second-player win exactly for h = k, h = 0..7; I always record the 8-letter outcome string of G + *0 .. G + *7 (N first player wins, P second player, L Left, R Right) so that non-nimbers are not mistaken for nimbers: *k means the string is N in every position except P at position k.

## The solver `tw.c`

- State: two 64-bit masks (White, Black pawns) with square index `s = (rank-1)*F + file`, so any board with F*R <= 64 fits (F=5, R=12 uses 60 bits; the old packing used 8 bits per rank) plus a one-byte e.p. code (0 none; 1+sq: White just double-stepped and skipped square `sq`; 65+sq: Black did). Memo table of 2^25 entries x 24 bytes (about 0.8 GB RSS; `/usr/bin/time -l` measured 405 MB for the first 2^24 run, `ps` 788 MB for 2^25), cleared when half full.
- Each state stores two bytes, WL and WR: bit k says whether Left (Right) moving first wins G + *k, k = 0..7. Moves in G recurse; moves in *k use the mex rule. The race rule, the e.p.-aware passed test and the front-pawn distance are written from `pawns.py` (`passed`, `ep_capturable`, `promote_distance`, `_child`).
- Root class (same as `research/star4_hunt/` "roots" for flat boards, and rings as in `research/c9_rings/` for cylinders): White pawns on ranks 2..R-2, Black pawns on ranks 3..R-1 (a pawn elsewhere would be passed), distinct squares, **every file occupied** (one `cylcgt` component on a flat board; a ring on a cylinder), no passed pawn in the root, no e.p. right. Counted up to mirror (flat) or rotation and reflection (cylinder); splits nW + nB = p are taken with nW <= nB, and colour reversal (ranks flipped, colours swapped; it negates the game, so nimbers and the P/N pattern are unchanged) is identified when nW = nB. Enumeration is a file-by-file search with early passed-pawn pruning and a canonical-form test.
- **Not covered:** positions with an empty file (sums of components), flat boards of 1, 2 or 5+ files, cylinders of 6+ files. A *2 or *3 built as a sum of smaller roots is not looked for; the nim-sum argument of `research/star4_hunt/` is the only reason to expect nothing new there.

## Results: one table, board by R

"least p" = least number of pawns of a root with value *2 (*3). A number is exact when every smaller pawn count was enumerated completely; "none (space exhausted)" means every root of the board, for every pawn count, was solved; "none up to p pawns (N roots)" means every root with up to p pawns (N of them) was solved and nothing beyond was reached. The last column says up to which pawn count the enumeration was exhaustive. The nimber counts include the partly enumerated level where the run was stopped (budget), so they are lower bounds there. No hit of value >= *4 occurs in any row. COMPUTED-1 for "none" and for minimality; the existence of each reported minimum is CHECKED-2 (next section).

| board | R | least p for *2 | least p for *3 | roots found by nimber (all levels run) | exhaustive through p (roots) |
|---|---|---|---|---|---|
| flat 3 | 5 | none (space exhausted; all 236 roots) | none (space exhausted; all 236 roots) | *0:5 | all p (236) |
| flat 3 | 6 | 8 | none (space exhausted; all 7093 roots) | *0:102, *1:14, *2:2 | all p (7093) |
| flat 3 | 7 | 4 | none (space exhausted; all 196918 roots) | *0:1123, *1:343, *2:8 | all p (196918) |
| flat 3 | 8 | 10 | none (space exhausted; all 5378148 roots) | *0:13484, *1:4669, *2:10 | all p (5378148) |
| flat 3 | 9 | 7 | 9 | *0:112798, *1:45760, *2:76, *3:8 | 12 (46801529) |
| flat 3 | 10 | 7 | 9 | *0:277389, *1:132109, *2:72, *3:11 | 10 (66949989) |
| flat 3 | 11 | 7 | 9 | *0:401180, *1:209496, *2:39, *3:10 | 9 (77308779) |
| flat 3 | 12 | 6 | 9 | *0:563870, *1:317518, *2:52, *3:11 | 8 (46378490) |
| flat 4 | 5 | none (space exhausted; all 2196 roots) | none (space exhausted; all 2196 roots) | *0:6, *1:1 | all p (2196) |
| flat 4 | 6 | 6 | none (space exhausted; all 219491 roots) | *0:460, *1:99, *2:7 | all p (219491) |
| flat 4 | 7 | 4 | 6 | *0:300, *1:155, *2:16, *3:3 | 6 (16320) |
| flat 4 | 8 | 7 | 9 | *0:34368, *1:16697, *2:8, *3:1 | 9 (8804709) |
| flat 4 | 9 | 6 | 9 | *0:166252, *1:90346, *2:40, *3:8 | 9 (47185150) |
| flat 4 | 10 | 8 | 9 | *0:325452, *1:190901, *2:36, *3:2 | 8 (31784681) |
| flat 4 | 11 | 6 | 8 | *0:592307, *1:404064, *2:83, *3:6 | 8 (92189225) |
| flat 4 | 12 | 6 | 8 | *0:439129, *1:306552, *2:22, *3:4 | 7 (22999013) |
| cyl 3 | 5 | none (space exhausted; all 121 roots) | none (space exhausted; all 121 roots) | *1:2 | all p (121) |
| cyl 3 | 6 | none (space exhausted; all 3259 roots) | none (space exhausted; all 3259 roots) | *0:18, *1:4 | all p (3259) |
| cyl 3 | 7 | 4 | none (space exhausted; all 86802 roots) | *0:133, *1:40, *2:6 | all p (86802) |
| cyl 3 | 8 | 6 | none (space exhausted; all 2341874 roots) | *0:1542, *1:519, *2:5 | all p (2341874) |
| cyl 3 | 9 | 6 | none up to 12 pawns (22157669 roots) | *0:14135, *1:4931, *2:16 | 12 (22157669) |
| cyl 3 | 10 | 6 | 10 | *0:58563, *1:25804, *2:46, *3:2 | 10 (34005428) |
| cyl 3 | 11 | 6 | 9 | *0:100807, *1:50182, *2:26, *3:3 | 9 (40642158) |
| cyl 3 | 12 | 6 | 9 | *0:194064, *1:109915, *2:23, *3:5 | 8 (25132919) |
| cyl 4 | 5 | none (space exhausted; all 826 roots) | none (space exhausted; all 826 roots) | *0:8 | all p (826) |
| cyl 4 | 6 | 6 | none (space exhausted; all 72435 roots) | *0:149, *1:20, *2:1 | all p (72435) |
| cyl 4 | 7 | 6 | none up to 16 pawns (5914948 roots) | *0:3564, *1:894, *2:14 | 16 (5914948) |
| cyl 4 | 8 | 7 | none up to 11 pawns (27330078 roots) | *0:32617, *1:10217, *2:18 | 11 (27330078) |
| cyl 4 | 9 | 6 | none up to 9 pawns (17846310 roots) | *0:64059, *1:25674, *2:17 | 9 (17846310) |
| cyl 4 | 10 | 7 | none up to 8 pawns (12490171 roots) | *0:150813, *1:72447, *2:22 | 8 (12490171) |
| cyl 4 | 11 | 6 | none up to 8 pawns (36427305 roots) | *0:208711, *1:116275, *2:14 | 8 (36427305) |
| cyl 4 | 12 | 6 | none up to 7 pawns (9404519 roots) | *0:186583, *1:114255, *2:29 | 7 (9404519) |
| cyl 5 | 5 | none (space exhausted; all 5847 roots) | none (space exhausted; all 5847 roots) | *0:2, *1:3 | all p (5847) |
| cyl 5 | 6 | 8 | none (space exhausted; all 1786651 roots) | *0:345, *1:48, *2:6 | all p (1786651) |
| cyl 5 | 7 | 6 | 8 | *0:1046, *1:371, *2:12, *3:2 | 8 (288845) |
| cyl 5 | 8 | 8 | none up to 9 pawns (10252690 roots) | *0:53437, *1:21985, *2:35 | 9 (10252690) |
| cyl 5 | 9 | 6 | 9 | *0:100300, *1:51855, *2:30, *3:1 | 9 (52328153) |
| cyl 5 | 10 | 8 | none up to 8 pawns (22303091 roots) | *0:112321, *1:70152, *2:22 | 8 (22303091) |
| cyl 5 | 11 | 8 | none up to 7 pawns (4398382 roots) | *0:155198, *1:103735, *2:18 | 7 (4398382) |
| cyl 5 | 12 | none up to 7 pawns (9758648 roots) | none up to 7 pawns (9758648 roots) | *0:41441, *1:26039 | 7 (9758648) |


Pawn counts above the "exhaustive through p" column were either not reached or only partly enumerated (per-level detail with roots, solved, complete flag and CPU time in `results/levels.tsv`; `logs/progress.txt` is the log). Per-level root counts are reproduced by `tw --count` (about 15 M roots/s), solving is 1 to 300 microseconds per root depending on height and pawn count.

### Answers to the three questions

1. Least pawns for *2 and *3, and whether *4 occurs: see the table. *4 or higher: none in any row.
2. Monotone in R? **No.** For *2 on flat 3 files: none R=5, 8 (R=6), 4 (R=7), 10 (R=8), 7 (R=9,10,11), 6 (R=12). For cylinder 3: none, none, 4, 6, 6, 6, 6, 6. For cylinder 4: none, 6, 6, 7, 6, 7, 6, 6. The same 7-pawn gadget `W: a2 b2 b5 / B: a5 b6 c7 c8` is *2 on flat 3 files for R = 9, 10 and 11, and not for R = 8 (where the c8 pawn would be on the promotion rank). **A shorter board does admit *2:** R = 6 (6 to 8 pawns, except cylinder 3) and R = 7 (4 pawns on 3 files); R = 5 admits no *2 and no *3 at all (every root of every one of the five boards enumerated: 236, 2,196, 121, 826, 5,847 roots for flat 3, flat 4, cylinder 3, 4, 5). *3 never occurs for R <= 6 or on 3 files at R = 7, 8, nor on flat 4 at R = 6 (exhaustive), but it appears with 6 pawns on flat 4, R = 7.
3. *4 candidates: **none**. Largest nimber found is *3 (positions in the next list).

### Hit positions at the least pawn count (notation of `research/star4_hunt/REPORT.md`)

- flat 3, R=6, *2, p=8: 1 found (up to mirror/colour reversal); e.g. `W: a2 b2 c2 c3 / B: b4 c4 a5 c5`
- flat 3, R=7, *2, p=4: 1 found (up to mirror/colour reversal); e.g. `W: a2 c2 / B: c3 b6`
- flat 3, R=8, *2, p=10: 3 found (up to mirror/colour reversal); e.g. `W: a2 b2 a3 c3 a4 / B: c4 a5 c5 b6 c6`; also `W: a2 b2 c3 c4 b6 / B: b5 c5 a6 c6 b7`
- flat 3, R=9, *2, p=7: 1 found (up to mirror/colour reversal); e.g. `W: a2 b2 b5 / B: a5 b6 c7 c8`
- flat 3, R=9, *3, p=9: 2 found (up to mirror/colour reversal); e.g. `W: a2 b2 b5 a6 / B: a5 b6 c7 a8 c8`; also `W: b2 c2 b5 a6 / B: c5 b6 c7 a8 c8`
- flat 3, R=10, *2, p=7: 1 found (up to mirror/colour reversal); e.g. `W: a2 b2 b5 / B: a5 b6 c7 c8`
- flat 3, R=10, *3, p=9: 4 found (up to mirror/colour reversal); e.g. `W: a2 b2 b5 a6 / B: a5 b6 c7 a8 c8`; also `W: a2 b2 b5 c7 / B: a5 b6 a7 a8 c9`
- flat 3, R=11, *2, p=7: 1 found (up to mirror/colour reversal); e.g. `W: a2 b2 b5 / B: a5 b6 c7 c8`
- flat 3, R=11, *3, p=9: 10 found (up to mirror/colour reversal); e.g. `W: a2 b2 a5 c8 / B: b5 a6 b7 b8 c10`; also `W: a2 b2 b5 a6 / B: a5 b6 c7 a8 c8`
- flat 3, R=12, *2, p=6: 7 found (up to mirror/colour reversal); e.g. `W: a3 b3 c7 / B: a6 b10 c10`; also `W: b2 a3 b3 / B: b10 c10 b11`
- flat 3, R=12, *3, p=9: 11 found (up to mirror/colour reversal); e.g. `W: a2 b2 b5 b8 / B: a5 b6 c7 c8 b10`; also `W: a2 b2 b5 b8 / B: a5 b6 c7 c8 c11`
- cyl 3, R=7, *2, p=4: 1 found (up to mirror/colour reversal); e.g. `W: c2 a3 / B: b5 c5`
- cyl 3, R=8, *2, p=6: 1 found (up to mirror/colour reversal); e.g. `W: a2 b2 a3 / B: c6 b7 c7`
- cyl 3, R=9, *2, p=6: 4 found (up to mirror/colour reversal); e.g. `W: a2 b2 c2 / B: a8 b8 c8`; also `W: a2 b2 c2 / B: b4 b7 c8`
- cyl 3, R=10, *2, p=6: 4 found (up to mirror/colour reversal); e.g. `W: c2 a3 c3 / B: b8 c8 c9`; also `W: c2 a3 c4 / B: b7 c8 c9`
- cyl 3, R=10, *3, p=10: 2 found (up to mirror/colour reversal); e.g. `W: b2 a3 c3 a4 c7 / B: a5 c5 b6 b7 c9`; also `W: b2 a3 c3 c4 c7 / B: a5 c5 b6 b7 c9`
- cyl 3, R=11, *2, p=6: 1 found (up to mirror/colour reversal); e.g. `W: b2 a3 a6 / B: c5 b10 c10`
- cyl 3, R=11, *3, p=9: 3 found (up to mirror/colour reversal); e.g. `W: a2 b2 a5 c8 / B: b5 a6 b7 b8 c10`; also `W: a2 c2 a5 c8 / B: c5 a6 b7 b8 c10`
- cyl 3, R=12, *2, p=6: 1 found (up to mirror/colour reversal); e.g. `W: a3 b3 c7 / B: a6 b10 c10`
- cyl 3, R=12, *3, p=9: 5 found (up to mirror/colour reversal); e.g. `W: a2 b2 b5 b8 / B: a5 b6 c7 c8 c11`; also `W: a2 b2 b5 c9 / B: a5 b6 c7 c8 c11`
- flat 4, R=6, *2, p=6: 2 found (up to mirror/colour reversal); e.g. `W: a2 b2 d2 / B: a5 c5 d5`; also `W: a2 d2 b3 / B: c4 a5 d5`
- flat 4, R=7, *2, p=4: 2 found (up to mirror/colour reversal); e.g. `W: a2 c2 / B: d4 b6`; also `W: a2 d4 / B: b6 c6`
- flat 4, R=7, *3, p=6: 3 found (up to mirror/colour reversal); e.g. `W: a2 c2 d3 / B: c3 b6 c6`; also `W: a2 c2 d3 / B: c3 d5 b6`
- flat 4, R=8, *2, p=7: 1 found (up to mirror/colour reversal); e.g. `W: a2 b2 c4 / B: a5 b6 d6 d7`
- flat 4, R=8, *3, p=9: 1 found (up to mirror/colour reversal); e.g. `W: a2 b2 d2 c4 / B: d4 a5 b6 d6 d7`
- flat 4, R=9, *2, p=6: 4 found (up to mirror/colour reversal); e.g. `W: a3 c4 d4 / B: a6 b6 d7`; also `W: b2 a3 c3 / B: b7 d7 c8`
- flat 4, R=9, *3, p=9: 8 found (up to mirror/colour reversal); e.g. `W: a2 b2 d2 c4 / B: d4 a5 b6 d6 d7`; also `W: a2 b2 d3 b5 / B: a5 d5 b6 c7 c8`
- flat 4, R=10, *2, p=8: 26 found (up to mirror/colour reversal); e.g. `W: a2 b2 c2 d2 / B: d4 b5 c6 b7`; also `W: a2 b2 c2 d4 / B: b5 a7 b7 d7`
- flat 4, R=10, *3, p=9: 2 found (up to mirror/colour reversal); e.g. `W: b2 c2 b5 c6 / B: c5 b6 a7 a8 d9`; also `W: b2 c2 b5 d7 / B: c5 b6 a7 a8 d9`
- flat 4, R=11, *2, p=6: 11 found (up to mirror/colour reversal); e.g. `W: a3 b3 c4 / B: b8 c9 d9`; also `W: a3 b4 c4 / B: b8 c8 d9`
- flat 4, R=11, *3, p=8: 6 found (up to mirror/colour reversal); e.g. `W: a2 d3 a5 b5 / B: a4 c7 d7 b9`; also `W: c3 a5 b5 d8 / B: c7 d7 b9 d10`
- flat 4, R=12, *2, p=6: 5 found (up to mirror/colour reversal); e.g. `W: a3 c4 d5 / B: a7 b8 d9`; also `W: a3 c5 d5 / B: a7 b7 d9`
- flat 4, R=12, *3, p=8: 4 found (up to mirror/colour reversal); e.g. `W: b2 c3 d3 b7 / B: a5 d6 b10 c10`; also `W: b2 c3 d3 c7 / B: a5 d6 c10 d10`
- cyl 4, R=6, *2, p=6: 1 found (up to mirror/colour reversal); e.g. `W: c2 d2 a3 / B: b4 c5 d5`
- cyl 4, R=7, *2, p=6: 2 found (up to mirror/colour reversal); e.g. `W: a2 c2 d5 / B: c3 b6 d6`; also `W: d2 a3 c3 / B: b5 d5 c6`
- cyl 4, R=8, *2, p=7: 1 found (up to mirror/colour reversal); e.g. `W: b2 c2 a4 / B: c5 b6 d6 d7`
- cyl 4, R=9, *2, p=6: 3 found (up to mirror/colour reversal); e.g. `W: d2 a3 b3 / B: b7 c7 d8`; also `W: d2 a3 b4 / B: c6 b7 d8`
- cyl 4, R=10, *2, p=7: 1 found (up to mirror/colour reversal); e.g. `W: b2 c2 a4 / B: c5 b6 d6 d7`
- cyl 4, R=11, *2, p=6: 1 found (up to mirror/colour reversal); e.g. `W: a2 c2 b3 / B: c5 b6 d9`
- cyl 4, R=12, *2, p=6: 18 found (up to mirror/colour reversal); e.g. `W: a2 b2 d3 / B: b10 c11 d11`; also `W: a2 b2 d4 / B: b9 c11 d11`
- cyl 5, R=6, *2, p=8: 1 found (up to mirror/colour reversal); e.g. `W: a2 c2 d2 c3 / B: e4 b5 d5 e5`
- cyl 5, R=7, *2, p=6: 2 found (up to mirror/colour reversal); e.g. `W: a2 d2 c5 / B: b4 c6 e6`; also `W: e2 a3 c3 / B: b5 d5 e5`
- cyl 5, R=7, *3, p=8: 2 found (up to mirror/colour reversal); e.g. `W: a2 c2 d2 c4 / B: e4 b6 d6 e6`; also `W: a2 c2 d3 e5 / B: c3 d5 b6 e6`
- cyl 5, R=8, *2, p=8: 7 found (up to mirror/colour reversal); e.g. `W: a2 c2 d2 e2 / B: b4 c5 e6 e7`; also `W: a2 c2 d2 e2 / B: b4 e5 c6 e7`
- cyl 5, R=9, *2, p=6: 3 found (up to mirror/colour reversal); e.g. `W: a2 c3 d3 / B: b7 c7 e8`; also `W: a2 c4 d4 / B: b6 c6 e8`
- cyl 5, R=9, *3, p=9: 1 found (up to mirror/colour reversal); e.g. `W: c2 d2 a4 d5 / B: c5 d6 b7 e7 e8`
- cyl 5, R=10, *2, p=8: 22 found (up to mirror/colour reversal); e.g. `W: a2 a3 c4 e4 / B: b7 e7 d8 d9`; also `W: a2 d2 b3 e3 / B: b8 d8 c9 e9`
- cyl 5, R=11, *2, p=8: 18 found (up to mirror/colour reversal); e.g. `W: a2 b2 d4 e4 / B: b4 e8 c9 d9`; also `W: a2 c3 c4 d6 / B: b6 c8 c9 e10`


Every nimber-2/3 hit found is in `results/hits.tsv` (columns: files, wrap, R, p, HIT, nimber, nW, nB, position, signature).

## Validation

**Validation 1: `tw` against `cylcgt`, full 8-letter signature (COMPUTED-1 solver, CHECKED against cylcgt).** For each R = 5..12, 2,000 random root-like positions without passed pawns (3 to 7 pawns, 3, 4 or 5 files, flat and cylinder with equal probability, not required to occupy every file, so gapped positions are also tested, whole-board model `pawns.components = lambda bd, p: [p]`), `validate.py` + `run_validate.sh`. Python skipped positions that took more than 40 s (R = 10: 1, R = 11: 6, R = 12: 11; none for R <= 9) and drew another. **Differences: 0 in all of them.**

```
R=5 positions=2000 differences=0
R=6 positions=2000 differences=0
R=7 positions=2000 differences=0
R=8 positions=2000 differences=0
R=9 positions=2000 differences=0
R=10 positions=2000 differences=0
R=11 positions=2000 differences=0
R=12 positions=2000 differences=0
```
That is 16,000 positions with 0 differences; each R sample has 71 to 126 positions whose signature is *0 or *1, with the *2/*3 cases covered by validation 3.

**Validation 2: R = 8 control (exact matches with recorded lines).**
- `research/star4_hunt/REPORT.md` table A, flat 4 files, 11 pawns: roots 718,274 (2+9), 5,199,437 (3+8), 15,925,349 (4+7), 26,806,874 (5+6), total **48,649,934**; nimbers 0: **60,514**, 1: **24,230**, 2: **9**, 3: **1**, >= 4: 0. `tw` gives all of these (`results/control/control.out`).
- Same report, flat 5 files, 10 pawns: roots 2,658,896; 22,341,596; 64,796,378; 45,123,321, total **134,920,191**; **75 *2, 3 *3**, nothing higher. `tw` gives all of these (`results/control/control2.out`).
- `RESULTS.md` section 6c: C3 with 10 pawns, 741,110 rings (all splits, colours not exchanged), two *2: `tw --nocolsym` gives 741,110 and 2 (and 1 class up to colour reversal in the table's counting). C6 with 9 pawns: "three positions and their colour-reversed twins": `tw` finds 3 *2 in the nW < nB splits (13,506,022 roots). First ring *2 has n+3 pawns for n = 3, 4, 5: the table gives 6, 7, 8 for R = 8. "No *2 on flat boards of at most 4 files and 6 pawns": the table gives flat 4 minimum 7, flat 3 minimum 10. The flat 4-file R = 8 levels: 1 class of *2 at 7 pawns (`W: a2 b2 c4 / B: a5 b6 d6 d7`; star4 reports two 7-pawn cores A and B, which `RESULTS.md` says are one *2 up to colour reversal and mirror), 2 at 8 pawns, 5 at 9, and the first *3 at 9 pawns (`W: a2 b2 d2 c4 / B: d4 a5 b6 d6 d7`).
- Enumerator counts against `research/star4_hunt/h4 --count` at R = 8: 10 board/split combinations (flat 4, 5; cylinder 3, 4, 5) equal.
- Independent root counter (`indep_count.py`, brute force over labelled placements, no shared code) against `tw --count` at R = 5 to 12: 13 board/split cases (`results/indep_counts.txt`), all equal.

**Validation 3: every *2/*3 minimum reported is confirmed directly with `cylcgt`.** `val3.py` took the first hit at the least p for each board, R and q in {2, 3} (48 cases) and ran `pycheck.py`; **48 of 48 MATCH** the C signature (`results/validation3.txt`). Example (project root):

```
PYTHONPATH=. .venv/bin/python research/tall_boards/pycheck.py 3 0 7 "W: a2 c2 / B: c3 b6"
W: a2 c2 / B: c3 b6 | NNPNNNNN | *2
PYTHONPATH=. .venv/bin/python research/tall_boards/pycheck.py 4 0 7 "W: a2 c2 d3 / B: c3 d5 b6"
W: a2 c2 d3 / B: c3 d5 b6 | NNNPNNNN | *3
```
(arguments: files, wrap 0/1, ranks, position). No *4 candidate exists, so there was none to check.

## What was not reached (no silent caps)

- Cases whose enumeration stopped at the CPU budget are those where the last column of the table is smaller than the pawn counts of that board: levels beyond it were at most partly solved. Cases never finished at the "least *3" question: all the "none up to p pawns" cells. They are open, not negative; in particular cylinder 4 and 5 at R = 8..12 need more than 9 pawns and cylinder 5, R = 12 has no *2 up to 7 pawns (the next level has billions of roots).
- Gapped positions (sums), boards of 1-2 files and of 6 or more files, and tall boards beyond R = 12 were not run.
- `cylcgt` confirmation covers the minimum hits (existence), not "none" statements; those rest on `tw` alone, whose correctness is supported by validations 1 and 2 (16,000 + 150 M roots against records) and the enumerator counts by 23 independent comparisons.
- Python validation positions have at most 7 pawns; the 8 to 10 pawn *3 positions of the tall boards were confirmed individually (validation 3), but the solver was not compared with `cylcgt` on random 8 to 12 pawn positions.

## Rerun

From `research/tall_boards` (`tw` is built with `cc -O2 -o tw tw.c`; every heavy command below is run with `nice -n 15`):

```
cc -O2 -Wall -o tw tw.c
./tw --scan F WRAP R NW NB [--chunk i n] [--tlimit S] [--count] [--nocolsym]     # one split, e.g. ./tw --scan 4 0 8 4 5
python3 scan_driver.py WORKER BUDGET_S PASS            # all (board, R) cases; ONLY=F3c_R9 EXTEND=1 REVERSE=1 select/extend
./run_validate.sh                                       # validation 1 (needs project root venv; edit paths)
./run_controls.sh; ./run_control2.sh                    # validation 2 controls
(from project root) PYTHONPATH=. .venv/bin/python research/tall_boards/val3.py research/tall_boards/results/validation3.txt 420
./run_indep.sh; python3 aggregate.py; python3 hits_report.py; python3 make_report.py
```
Order I ran them: validation 1 with scan driver pass 1 (budget 420 s CPU per case, 240 s from R = 11 on), then pass 2 for a few cases (`F4c_R7`), pass 3-5 extensions of the narrow cases, controls, validation 3, independent counts. About 2.5 CPU hours of solving in total. PIDs of everything started are in `logs/*.pid` (stopped only by those PIDs; no pkill, killall, or git write command). Raw outputs are compressed with `zstd -19` and tested with `zstd -t` (`results/raw/*.zst`, `results/control/*.out.zst`, `results/val_R*.{eval,py,c}.zst`; originals removed after the test passed).

## Files

`tw.c` solver and enumerator; `scan_driver.py`, `aggregate.py`, `hits_report.py`, `make_report.py`; `validate.py`, `run_validate.sh`, `val3.py`, `pycheck.py`, `indep_count.py`, `run_indep.sh`, `run_controls.sh`, `run_control2.sh`; `results/{levels.tsv,hits.tsv,table.tsv,table.md,hits_at_minimum.md,validation1.txt,validation3.txt,indep_counts.txt}`; `logs/progress.txt`.
