# T-two-core: two cores in one ring, and a primitive-core search for *4

All files are in `research/star4_rings/two_core/`. Game: whole-board pawn game on the n-file cylinder, 8 ranks, race rule "count", e.p. on,
a pawn that can be taken e.p. is not passed, the game ends at the first passed pawn. A ring has a pawn on every file. Value = outcome signature
of G+*h, h = 0..7 (a nimber *k is `N`^k `P` `N`^(7-k)).

## Summary (5 lines)

1. **Additivity holds exactly whenever the ring is a nimber, but the ring is not always a nimber.** In 1,890 two-core rings (n <= 24) whose
   walls match the cores' own wall types, 1,513 are nimbers and all 1,513 equal the nim-sum of the two single-core values (0 exceptions; likewise 403/403 in a
   wall-length scan, 36/36 in 3-core rings and 6/6 in 4-core rings). 333 rings are decisive (Black wins 286x, White 22x, ...), 1 is all-N, 43 hit the node limit.
2. **The failures are a finite-range coupling through the wall, not a different sum rule.** Opposite-handed pairs fail 30% of the time, same-handed 8%. In 30 pairs
   scanned with both wall lengths up to 11, every pair becomes a nimber (still equal to the nim-sum) once one wall reaches length 7..11; e.g. W4 B7 and W4B6 (both *1) with walls 3 and 3 give an
   all-Black win (n = 9), and *0 only when one wall has length 11.
3. **No *4 anywhere.** Across 207,975 distinct rings evaluated (values: *0 4,313, *1 2,287, *2 911, *3 462, all-N 83,449, other 116,553) the largest nimber is *3 and no signature even begins
   NNNN except the all-N one (all-N is the common "fuzzy" class; 56,608 of the 83,449 were re-run to h = 11: all still all-N, 13 aborted). Since sums of cores of value <= *3 stay <= *3, a *4 needs a primitive core of value >= *4.
4. **Primitive-core search, width <= 6** (exhaustive width <= 3; truncations, two rounds of neutral-network expansion, edit bursts, 33,776 uniform random legal blocks): 17 width-5
   cores with single-core ring value *2, 29 width-6 cores with *3 (15 of them are a width-5 *2 core with one file attached at an end; 14 do not decompose that way), nothing >= *4. Width <= 3 has nothing above *1.
5. **Engine and checks.** I used two value-neutral patches of rg.c (poisoned-child skip, local passed-pawn test; 400 + 5,150 signature comparisons, 0 differences) and re-ran 641 + 804 rings with the
   **original** rg: all equal except 5 big two-core rings (n >= 18) that overflow the original rg's table even at TBITS = 24 (2.2 GB). The machine load was 270-360, so the planned big-core samples were cut (see Caveats).

## 1. Setup

### Engine
- `rg.c` copied unmodified, built `cc -O2 -DMAXN=64 -o rg rg.c -lpthread` (binary `rg`, used for verification only).
- `rgx.c` = rg.c plus (a) in `win()` a non-terminal child is skipped if the opponent has an immediate terminal win (the child would return "opponent wins" anyway: value-neutral, and far fewer table entries: the original rg's table overflows on the n >= 18 two-core rings), (b) per-position node limit `NODELIM`, (c) the table is cleared between positions when 35% full, `FULL`/`ABORT` printed instead of `exit(3)`.
- `rgy.c` = rgx.c plus a local passed-pawn test (only files within 1 of the moved/captured files and of the e.p. file are re-checked; exact because every searched node has no passed pawn), and `ILLEGAL` for a root that already holds a passed pawn. About 1.5x faster, identical search tree. Build: `cc -O2 -DMAXN=26 -o rgy rgy.c -lpthread`. All experiments use rgy.
- Validation: rgx vs the stored rg signatures of 400 n=10 positions (`diff_in.txt`, `diff_ref.txt`, `diff_out.txt`): 400/400 identical. rgy vs cached rgx on 5,150 rings, n = 5..24 (`dt_in.txt`, `dt_ref.txt`, `dt_out.txt`): 0 signature differences; on 6 heavy rings the node counts are identical. Original rg re-runs: section 6.
- Every ring is cached under its rotation/reflection canonical form (`results*.tsv`: ring, signature, nodes).

### Notation
- `wall(L, first)`: alternating wall of L single-pawn files, `first` = `W` (W2 B4 W2 ...) or `B` (B4 W2 B4 ...). The W2 pawn has the black pawn two ranks above it on the next file.
- A *core* is a linear block of tokens. `block + wall(L, first)` closed into a ring is the *single-core ring*.
- A *typed stable core* is (block, first, parity, v): the single-core ring has the same nimber v for every wall length of that parity tested (even: 2,4,6 then 8,10 ; odd: 3,5,7 then 9,11; small blocks: 4,6,8,10 / 5,7,9,11). The wall type fixes the pawn next to each end of the core: first = pawn right of the core, `last` = pawn left of the core (`last` = first for odd wall, the other pawn for even).
- *Matched walls* in A + W1 + B + W2 (cyclic): W1 starts with A's first pawn and ends with B's last pawn; W2 starts with B's first pawn and ends with A's last pawn. This fixes the parity of L1, L2; I use L in 2,4,6 (even) and 3,5 (odd), n <= 24. Each core then sees exactly its own wall type on both sides.
- *Handedness* of a core = its `first`. Two cores are same-handed if they start their walls with the same pawn.
- Prediction = vA xor vB. Reference rings (section 3 end): refA = A + W1 + W2, refB = B + W2 + W1 (single-core rings with the same total wall).

### Core library
- 91 rings from `research/star26_rings` (C7: 63 *2 and 8 *3; C8: 18 *2 and 2 *3), all re-evaluated with the whole-board engine: 91/91 keep the same value (`c78_rings.tsv`). Plus P_8, Q_8 and the C8 *3 ring. Each ring was cut at every position and closed with walls of length 2..7, both first pawns (8,244 rings, `c78_cuts.tsv`): 113 typed stable cores, 106 after the long-wall check (`validate_big.py`): *2: 71, *1: 13, *0: 13, *3: 9 (81 of width 7, 24 of width 8, 1 of width 6). The C8 *3 ring `W5 B7 W4 W4B7 B6 W3B6 W2 B5` itself never qualified (it is *3 only with walls of length 2 and 4; from length 6 on the value is NLNLLLLL, a non-nimber: the pumping that works for P_n and Q_n does not hold for it, `t4.py`); 7 of the 113 typed cores were dropped by the long-wall check (`lib_big_unstable.json`).
- Small cores: all blocks of width 1, 2, 3 over 35 tokens (<= 1 white pawn on ranks 2..6 and <= 1 black pawn on ranks 3..7 per file; 35 + 1,225 + 42,875 blocks, 8 wall types each, `blocks_w*.tsv`). Stable values: *1 in 7 / 86 / 932 typed cores of width 1 / 2 / 3, *0 in 17 / 177 / 1,759, **nothing stable above *1**. Single-file *1 cores: `W3B5` (wall starting W2, odd), `W4B6` and `W5B7` (W2-first even or odd, B4-first even): the "W r / B r+2" files. Two-file examples: `B7 W4`, `W4 B7`, `B6 W3` ... (86 of them).
- `X2` = `W5 B7 W4 W4B7 B6 W3B6` (the P_n core) is a stable *2 for W2-first even walls (L = 2..12). `QC` = `W3B6 W3 W2B5 B5 W2 B4 W4 B7` (Q_8 cut after B7) is a stable *3 for B4-first even walls and W2-first odd walls (L = 2..12 resp. 3..11).


## 2. Two cores in one ring (matched walls)

Rows = rings A + W1 + B + W2, n <= 24. *nimber* = signature is a nimber *k with k <= 7; *N+* = all N for h = 0..7; *decisive/other* = L/R wins and mixed signatures; *undecided* = 3M-node limit. SS = both cores small (width 1-3, value *0/*1), BS = one core from the C7/C8 library (width 6-8, value >= *0) and one small, BB = both from the library, UN = unmatched-wall grids.

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


## 3. Three- and four-core rings, reference rings

- Cores drawn from the library with even wall types, matched walls (lengths 2,4 or 3,5), n <= 24, 70 random rings (`triple.py`, `triple.tsv`):

| cores | rings | nimbers | nimber = nim-sum |
|---|---|---|---|
| 3, same handedness | 41 | 30 | 30 |
| 3, mixed handedness | 18 | 6 | 6 |
| 4, same handedness | 8 | 5 | 5 |
| 4, mixed handedness | 3 | 1 | 1 |

  One 3-core ring (cores `W5B7 W4B4 W2B6` *1, `W2 W5 W2B7 B7 W5B7 W4B7 B4` *2, `W4B5 W3B4` *0, n = 20) predicted *3 is all-N for h = 0..15, so it is not a nimber at all.
- Reference rings (the exact reading of "single-core ring of the same wall length"): refA = A + W1 + W2 and refB = B + W2 + W1. Among matched rows with both reference rings nimbers (733): the ring is a nimber equal to refA xor refB in 542, a nimber *different* from it in **0**, not a nimber in 191 (190 decisive + 1 all-N). The reference values always equal the stable values (0 differences). The 190 are listed, smallest n first, in `nonadditive_examples.tsv`.

## 4. Where additivity fails and how long the coupling is

Smallest example (n = 9): A = `W4 B7` (*1 with B4-first even walls), B = `W4B6` (*1 with W2-first even walls), W1 = `B4 W2 B4`, W2 = `W2 B4 W2`:

| L1 (W1 = B4 W2 ...) | n | signature of `W4 B7 + wall(L1,B) + W4B6 + W2 B4 W2` |
|---|---|---|
| 3 | 9 | RRRRRRRR |
| 5 | 11 | RRRRRRRR |
| 7 | 13 | RRRRRRRR |
| 9 | 15 | RRRRRRRR |
| 11 | 17 | PNNNNNNN = *0 = *1 xor *1 |

(`W4 B7` alone with `wall(L,B)`: L = 4,6,8,10: *1; L = 5,7: RRRR; L = 9: *1. So the single-core ring itself needs an odd wall of length 9 before the parity of the wall stops mattering.)

`fail_scan.py`: 30 (A, B, first pawns) groups whose matched rings with all L <= 6 were non-nimbers, and 10 groups that were nimbers; L1, L2 up to 11 of the matching parity, n <= 24; 937 rings, 403 of them nimbers, and all 403 equal vA xor vB. The 10 nimber groups are nimbers at every length. All 30 failing groups become nimbers for some longer wall (nimber only for some lengths in all 30): the first nimber ring has its longer wall at length 7 (4 groups), 8 (1), 9 (3), 10 (6), 11 (16; the scan stops at 11, so these may need more). In the grids I looked at (6 of the 30; all in `failscan.tsv`) nimber-ness is controlled by *one* of the two wall lengths crossing a threshold, so the cores see each other through up to about 10 wall files. My reading (not proved): wall pawns next to a core end can move (not poisoned), each such move changes the neighbourhood of the next wall pawn, so a chain of tempo moves runs along the wall until it meets the other core.

Relative handedness and wall parity predict failure only partly (tables in section 2): of 396 (A, B, first-pawn) groups with at least two matched rings (lengths 2..6), 324 are nimbers at every tested length, 56 fail at every tested length, 16 are mixed (typically one wall length, 3 versus 5, decides). The 56 groups that fail at every length up to 6 are the ones the length scan above tests further.

Remark on Q_n: Q_n = `W4 B7` + (B4 W2)^k + `W3B6 W3 W2B5 B5` + `W2 B4` is itself a two-block ring with value *3. `W4 B7` is a stable *1, but the other block with the same walls (`W3B6 W3 W2B5 B5` + wall) is not a nimber at all (RNNN / LLLL), so Q_n is a case where a nimber (*3) appears from a stable *1 and a non-nimber block (not analysed further).

## 5. Search for a primitive core of value >= *4 (width <= 6)

Single-core ring = block (4..6 files) + wall of length 4 or 5, first pawn W2 or B4. Value = nimber of the ring signature. All scripts use `p3lib.py`.

| stage | script | what | engine calls | result |
|---|---|---|---|---|
| exhaustive | `blocks.py 1/2/3` | all blocks of width 1, 2, 3 over 35 tokens, 8 walls each | 69,311 distinct rings | max stable nimber *1 (no *2 at all) |
| A | `p3_seeds.py` | 2,189 blocks of width 5/6 obtained by deleting 1..3 tokens from each cut core of value >= 1 (+ X2, Q6) | 2,189 blocks x 4 walls | 29 (block, wall) with *2, none *3 |
| B1 | `p3_neigh.py 80000 1 1 0` | neutral-network expansion: neighbours = substitute one token (75 tokens), delete, insert; expand a neighbour only if it is a nimber >= 2 in the same wall type; 260 sampled neighbours per seed | 13,749 calls, 24,700 states | queue exhausted; *3: 19, *2: 57 states; best *3 |
| B2 | `p3_neigh.py` (SEEDFILES, NBSAMPLE=700) | same, seeded with every nimber >= 2 found so far (105 seeds) | 25,789 calls, 65,703 states | queue exhausted; *3: 5, *2: 51 states; best *3 |
| C (failed) | `p3_rand.py` | random hill-climb on a score | 9,648 calls | collapsed onto the all-N plateau (8,477 all-N, 3 *0): not informative |
| C | `p3_burst.py 40000 21 a` | 2-4 simultaneous edits of a seed (170 seeds at the end), accept if nimber >= 2 | 40,000 calls, 69,594 candidates | *3: 6, *2: 13 states; best *3 |
| D | `p3_sample.py 14 5` | uniform random legal blocks, tokens uniform over 35, width 4/5/6, uniform wall | 33,776 legal of 138,784 drawn | width 4: *0 160, *1 82; width 5: *0 51, *1 23; width 6: *0 16, *1 4; **no *2 at all**, no *3 |
| E | `nplus_check.py`, `nplus_check2.py` | the all-N signature also covers *8 and above: re-run all-N single-core rings of the search with h up to 11 | 56,608 rings (58,743 runs, two scans overlap) | all remain all-N (13 hit the 1M-node limit): no *8..*11 |

Distinct primitive-looking cores of width <= 6 found (`cores_w6_nimber2.tsv`, `cores_w6_nimber3.tsv`; value listed for walls of length 4..9):
- value *2: 142 (block, first wall pawn) pairs, **17 of width 5**, e.g. `W3B6 B6 W4B7 W4 W6B7` (B4-first even walls, L = 4,6,8; also W2-first odd walls), `B5 W23 W4B6 B57 W3`; 104 of the 142 are stable over the whole length range of their parity.
- value *3: 29 pairs, all of width 6, 28 stable; 15 of them are a width-5 *2 core plus one file at an end (e.g. `W3B6 W3 W2B5 B5 W2B3` + `W4B6`), the other 14 are not (deleting any single token with the same wall does not give *2; they may be primitive or decompose with a changed wall).
- Representative *3 rings (n = 10): `W3B6 W3 W2B5 B5 W2B3 W4B6 B4 W2 B4 W2`, `W4B6 W6B7 W4 W4B7 B6 W3B6 W2 B4 W2 B4`, `W3B6 B6 W4B7 W4 W6B7 W4B6 B4 W2 B4 W2`.
- No block or ring anywhere has signature NNNNP...; the leading-N-run histogram over all 207,975 rings is {0: 111,936, 1: 10,468, 2: 1,637, 3: 485, all-N: 83,449}.

Conclusion for this task: **no *4 found** in single-core rings of width <= 6 (about 200,000 distinct rings in total, of which the exhaustive part covers width <= 3 only), none in two-, three- and four-core rings, and none among the all-N rings re-run to h = 11. This is a bounded search, not a proof: widths 4-6 are sampled (seeded by the known *2/*3 cores plus a uniform baseline), not enumerated.

## 6. Verification with the original rg

- `verify.py`: 641 rings (all 409 *3 rings of the cache at that time, 60 *2, 40 *1, the n = 9..17 non-additive family, 80 two-core nimber rings, 60 decisive two-core rings), original `./rg solve 7` (TBITS = 23): 634 identical. The other 7 are two-core rings with n = 18..24 for which the original table (no poisoned-child skip) overflows ("solver table full"); a retry with TBITS = 24 verified 2 of them (NNNPNNNN, 6.5M and 8.5M nodes), 5 stay unverified (`verify_result.txt`, `verify_retry.out`).
- `verify2.py`: all 804 rings (321 *2, 73 *3, 410 non-nimber) formed by the 171 width <= 6 *2/*3 cores with walls of length 4..9: **0 mismatches** with the original rg (`verify2_result.txt`).

## 7. Caveats

- **Sampling.** The load average was 270-360 on 14 cores, my nice-15 workers got about 18% of a core, so the planned task lists were cut: two-core tasks planned SS 1,161 / BS 3,966 / BB 575 / UN 595, done SS 1,161 (all), BS 574, BB 145, UN 145 (random subsets, the lists were shuffled before cutting). BB rows (big x big) are the heaviest: 41 of 145 hit the 3M-node limit and are *undecided*, not counted as failures.
- **Matched is not the only reading.** Unmatched walls (`UN unmatched`: 135 rings, 35 nimbers, 79 decisive, 21 all-N) are far less often nimbers, but the 35 nimbers also equal vA xor vB.
- **Stable values depend on wall length.** Single-core values were required to agree over L = 2..11 (big cores) or 4..11 (small); the C8 ring `W5 B7 W4 W4B7 B6 W3B6 W2 B5` is *3 only for L = 2,4, so ring values at n = 10, 12 can differ from the asymptotic wall.
- **Width, tokens.** The primitive search uses <= 1 white and <= 1 black pawn per file (plus 40 sampled two-pawn tokens in stage B, 220 in the vocabulary of stage C); the C7/C8 library cores contain doubled pawns. Walls are always W2/B4 alternating, lengths 4/5 in the search.
- **Verification gaps.** 5 large two-core rings are only checked with rgx/rgy; the *2/*3 width <= 6 cores are checked with three engines (rg, rgx/rgy through different code paths).
- All-N means "N for h = 0..7"; I resolved the ambiguity (a nimber >= *8) for 56,608 of the 83,449 all-N rings (to h = 11), not for the other 26,841 (library cuts, two-core, three-core), apart from the one 3-core ring checked to h = 15.
- Limits were respected: at most two engine processes (rg/rgx/rgy; the python drivers are idle most of the time) at a time (nice 15, <= 1 GB RSS each, original-rg verification up to 2.3 GB), no pkill/killall (my processes were stopped by PID only), no git, nothing written outside this directory. Total engine CPU was roughly one CPU-hour (estimated: at most two workers at 15-20% of a core each over about 3 hours of wall time, plus short serial jobs), under the 3 h cap.

## 8. Commands

```
cd research/star4_rings/two_core
cc -O2 -DMAXN=64 -o rg  rg.c  -lpthread                 # original, unmodified copy
cc -O2 -DMAXN=26 -o rgx rgx.c -lpthread                 # patched (value-neutral) variants
cc -O2 -DMAXN=26 -o rgy rgy.c -lpthread
python3 cores1.py; python3 cores2.py; python3 cores3.py  # C7/C8 hits -> cuts x walls -> typed cores (lib_big.json)
python3 validate_big.py                                  # long-wall check -> lib_big_ok.json
python3 blocks.py 1; python3 blocks.py 2; python3 blocks.py 3; python3 summarize_blocks.py 3
python3 gen_tasks.py                                     # tasks.jsonl (planned), lib_all.json
python3 twocore.py 0 2 & python3 twocore.py 1 2 &        # first 1,300 rows (rows_*.tsv), then
python3 twocore.py 0 2 tasks2.jsonl rows2 & python3 twocore.py 1 2 tasks2.jsonl rows2 &   # reshuffled remainder (rows2_*.tsv)
python3 fail_scan.py; python3 triple.py 70 3
python3 report_tables.py                                 # tables.md (section 2)
python3 p3_seeds.py; python3 p3_neigh.py 80000 1 1 0; SEEDFILES=p3_hits.tsv,p3_neigh_hits_0.tsv NBSAMPLE=700 TAG=r2 python3 p3_neigh.py 60000 2 1 0
python3 p3_burst.py 40000 21 a; python3 p3_sample.py 14 5; python3 nplus_check.py 15; python3 nplus_check2.py 13
python3 verify.py; ./verify_retry.sh; python3 verify2.py; python3 final_stats.py
```

Files: `results*.tsv` (ring, signature, nodes; the full cache), `rows*_k.tsv` (+ `rows_header.txt`) two-core rows, `failscan.tsv`, `triple.tsv`, `nonadditive_examples.tsv`,
`cores_w6_nimber2.tsv`, `cores_w6_nimber3.tsv`, `p3_*hits*.tsv`, `final_stats.json`, `tables.md`, `verify*_result.txt`.
