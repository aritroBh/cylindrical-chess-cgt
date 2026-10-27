# Local growth from *3 seeds (research/star4_rings/grow)

**Summary (5 lines)**
1. **No *4 and no nimber above *3 was found.** 128,791 distinct rings (up to rotation, reflection and colour reversal) were solved on the whole-board cylinder game (G+*h, h = 0..7, rule "count", e.p. on); the only nimbers that occur are *0 (165), *1 (671), *2 (2,070) and *3 (4,737); no signature NNNNPNNN, none of *4..*7, and none of the form NNNN followed by a non-N.
2. **Seeds and hits:** 14 known *3 ring classes (C7 x4, C8 x1, C10 x7, C12, C14) grew into 4,723 new *3 rings in 3 rounds (239 + 3,670 + 814): 4,520 with a pawn on every file and 203 with one emptied file (from "remove one pawn" in rounds 1-2). The new *3 rings have 7 to 16 files and 10 to 22 pawns.
3. **Coverage is partial.** Round 1 is the complete one-step neighbourhood of the 14 seeds (10,618 rings). Round 2 solved 94,182 of 196,549 neighbours of the 239 new seeds (all one-pawn, pair and removal moves, random samples of the file insertions). Round 3 sampled 50,500 of 2,675,776 neighbours of 3,470 ring seeds, and the 45-minute deadline stopped it at 23,977 (by increasing file count, so n = 14 is partly and n = 15, 16 not covered). The cap of 200,000 evaluations was not reached.
4. **Checks:** all 403 re-solved *3 hits (all 253 of rounds 0-1 plus 150 random later ones) and 849 of 850 random rings of every value agree with the unmodified rg.c (-DMAXN=64), 0 disagreements (1 position too big for rg's table); the engine is invariant under rotation, reflection and colour reversal (480 solves, 0 inconsistencies), which justifies the canonical-form dedupe. 86 positions hit the 4M-node limit and are unresolved.
5. **Reading:** by construction every new *3 is one move from an earlier *3; the yield of new *3 per candidate is highest for pair_adj2 (8.8 %), then pair_same2 (5.2 %), remove1 (4.8 %), add1 (3.8 %), ins1_wb (3.1 %), ins2_single (1.8 %), ins1_single (1.0 %), pair_same3 (0.9 %), ins1_dbl (0). The closest things to a step up are 2,748 rings whose G+*3 is a one-sided win (NNNR / NNNL), which are not nimbers; nothing in the sampled neighbourhood points to a route from *3 to *4.

## What was run

- **Engine.** `rg.c` copied from research/ring_family_proof/ (original untouched). `rg` = the unmodified copy built with `cc -O2 -DMAXN=64 -o rg rg.c -lpthread` (used only for verification). `rgf` = `rgf.c`, the same code with four changes that do not alter any search result (see `diff rg.c rgf.c`; the edits are marked `RGF PATCH`): (a) the memo table is flushed when 70 % full instead of `exit(3)` (it is only a cache); (b) `NODELIM` aborts a position after that many nodes and never memoises anything computed after the abort; (c) `EARLYSTOP=1` stops the h loop at the first L or R (such a ring is not a nimber; the remaining characters print as ?); (d) every output line echoes its input position, and `DEADLINE_S` stops reading input. Built with `-DMAXN=20`; node counts and signatures are identical to the MAXN=64 build on the 14 seeds, and signatures are identical on 1,252 further positions (see Checks). Settings used: `TBITS=23 NODELIM=4000000 EARLYSTOP=1`.
- **Processes.** Two `rgf` workers at a time, each under `nice -n 15`, about 370 MB RSS each, started from `run_round.sh`; no pkill, no git, nothing outside this directory. CPU time of the workers: about 2,730 s in all (round 1: 42 s, round 2: 1,704 s, round 3: 981 s). Wall time about 2 h 55 min on a machine at load 250-280.
- **Seeds** (`seeds_all.txt`, 14 canonical classes, all re-confirmed NNNPNNNN by rgf): Q_8, Q_10, Q_12, Q_14, the C8 ring (same class as Q_8), the 4 C7 ring classes (8 hits of research/star26_rings/c7/p10_5_5 with label N,3, and the C8 hits there collapse onto the same classes), and the 12 C10 NNNP rings of wall_results.tsv, which are 6 classes besides Q_10.
- **Moves** (`growlib.py`, pawn ranks 2..7, any ring with a passed pawn for either side is dropped, at most 16 files): `add1` add one pawn on any empty square; `pair_same2` W r and B r+2 on one file; `pair_adj2` W r on file f and B r+2 on file f+1, and the colour-swapped version; `remove1` remove one pawn; `ins1_single` insert one file with one pawn; `ins1_wb` insert one file with W r and B s; `ins2_single` insert two adjacent files, one pawn each; `ins1_dbl` insert one file with two pawns of one colour. Extension beyond the brief: `pair_same3` (W r, B r+3 on one file, the pair shape that the seeds use). Insertions are tried in every gap.
- **Dedupe.** Every ring is replaced by the lexicographically smallest of its 4n images under file rotation, file reflection and colour reversal (swap W/B, rank r to 9-r); `symtest.py` solved 120 random neighbours in 4 random images each (480 solves, no aborts): identical signatures after exchanging L and R for the colour-reversed images. A ring is never solved twice (`cache.tsv` is the master record of every result).
- **Rounds.** Round r grows the new *3 of round r-1 (round 0 = the seeds). Round 3 used only rings with a pawn on every file (seeds and candidates; `RINGONLY=1`), because the 203 non-rings are flat-board-like and the task is about rings. Rings 1-2 kept non-rings, flagged in `hits_star3.tsv`.
- **Round 2 quotas** (random sample, seed 12345): add1 19,557 (all), pair_same2 6,637 (all), pair_adj2 13,970 (all), remove1 2,109 (all), ins1_single 13,909 (all), ins1_wb 15,000 of 36,776, ins2_single 18,000 of 73,578, ins1_dbl 3,000 of 24,463, pair_same3 2,000 of 5,550. **Round 3 quotas**: add1 9,500, pair_same2 6,000, pair_adj2 11,000, remove1 1,500, ins1_single 2,500, ins1_wb 9,000, ins2_single 9,000, ins1_dbl 1,000, pair_same3 1,000 (of 313,249 / 102,520 / 207,739 / 13,817 / 194,802 / 502,454 / 908,456 / 345,271 / 87,468 available). Quotas were set from round-1 yields so that the classes that produce *3 are sampled most; they are not exhaustive.
- **Round 3 coverage** by number of files, evaluated / sampled: n = 8: 51, 9: 402, 10: 934, 11: 2,454, 12: 6,399, 13: 7,410, 14: 6,327 of 10,876; n = 15: 0 of 9,426; n = 16: 0 of 12,548. The unevaluated 26,523 are exactly the largest rings, so round 3 says nothing about rings with 15 or 16 files.

## Counts

Evaluations by round and value (`*k` = signature with a single P at position k and N elsewhere; `allN` = NNNNNNNN, i.e. *8 or above or not a nimber, h <= 7 cannot tell; `non` = a ring whose signature contains L or R, so not a nimber; `ABORT` = unresolved at 4,000,000 nodes). Round 0 = the 14 seeds re-solved.

| round | evaluated | *0 | *1 | *2 | *3 | *4 | *5 | *6 | *7 | allN | non | ABORT | ERR |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 14 | 0 | 0 | 0 | 14 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 1 | 10618 | 26 | 64 | 124 | 239 | 0 | 0 | 0 | 0 | 3128 | 7037 | 0 | 0 |
| 2 | 94182 | 108 | 461 | 1562 | 3670 | 0 | 0 | 0 | 0 | 22768 | 65587 | 26 | 0 |
| 3 | 23977 | 31 | 146 | 384 | 814 | 0 | 0 | 0 | 0 | 5666 | 16876 | 60 | 0 |
| all | 128791 | 165 | 671 | 2070 | 4737 | 0 | 0 | 0 | 0 | 31562 | 89500 | 86 | 0 |

By move class (first class that produced the ring, rounds 1-3):

| class | evaluated | *0 | *1 | *2 | *3 | allN | non | ABORT | *3 yield |
|---|---|---|---|---|---|---|---|---|---|
| add1 | 25677 | 0 | 0 | 19 | 962 | 1832 | 22864 | 0 | 3.75% |
| pair_same2 | 10235 | 0 | 8 | 807 | 533 | 1600 | 7275 | 12 | 5.21% |
| pair_adj2 | 20701 | 35 | 341 | 47 | 1814 | 6473 | 11956 | 35 | 8.76% |
| remove1 | 3144 | 0 | 0 | 3 | 151 | 1 | 2989 | 0 | 4.80% |
| ins1_single | 15745 | 0 | 0 | 2 | 150 | 2716 | 12876 | 1 | 0.95% |
| ins1_wb | 20842 | 65 | 130 | 639 | 635 | 7148 | 12191 | 34 | 3.05% |
| ins2_single | 24897 | 57 | 188 | 457 | 454 | 10373 | 13365 | 3 | 1.82% |
| ins1_dbl | 4759 | 0 | 0 | 0 | 0 | 259 | 4500 | 0 | 0.00% |
| pair_same3 | 2777 | 8 | 4 | 96 | 24 | 1160 | 1484 | 1 | 0.86% |

Other signatures worth knowing: NNNR / NNNL (G+*3 is won by one side only, G+*0..*2 are N): 1,741 / 1,007 rings; NR / NL (G+*0 N, G+*1 one-sided): 2,246 / 1,563. Mean search 32,191 nodes, maximum 3,996,386.

*3 rings by files: 7: 5, 8: 19, 9: 88, 10: 164, 11: 362, 12: 940, 13: 732, 14: 1,110, 15: 523, 16: 794. By pawns: 10: 5, 12: 49, 13: 36, 14: 278, 15: 319, 16: 1,095, 17: 477, 18: 936, 19: 495, 20: 1,007, 21: 21, 22: 19. New *3 rings with a pawn on every file: 4,520; with one empty file: 203 (3 in round 1, 200 in round 2).

## Hits

- **\*4 (NNNNPNNN): none.** No *5, *6 or *7 either. No ring whose signature starts NNNN and then is not all N.
- **New *3 rings: 4,723**, every one in `hits_star3.tsv` (ring, files, pawns, all_files_occupied, round, move class, parent seed). Round 1 list (239) below; rounds 2 and 3 (3,670 and 814) in the TSV.
- **Unresolved:** 86 positions in `aborts.tsv` (26 in round 2, 60 in round 3; 11 to 16 files); nothing is known about them.
- **Selection of 10 notable rings** (`best.tsv`; there is no *4, so these are *3 rings chosen for extremes, not for closeness to *4):

| ring | files | pawns | round | why |
|---|---|---|---|---|
| `B47 W24 W6B7 B5 W2 W3B7 W5B7` | 7 | 12 | 1 | fewest pawns among new *3 rings |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 W3B4 W2B5 W3B4 W24B56` | 14 | 22 | 3 | most pawns among new *3 rings |
| `B4 B5 W3 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2` | 16 | 18 | 1 | most files among new *3 rings |
| `B4 B7 W4 B47 W25 B5 W2B5 W3 W3B6 W2 W5B4 W2B7 B4 W2` | 14 | 20 | 2 | largest search among new *3 rings (nodes) |
| `B6 W2 W6B7 W3B6 W3B56 W4B7 W2 W6B7` | 8 | 14 | 2 | smallest new *3 reached by move class pair_same2 |
| `B4 B7 W3 W2B3 B7 W2B5 W3 W3B6 W2` | 9 | 12 | 1 | smallest new *3 reached by move class ins2_single |
| `B5 W2 W2B4 W2B6 B7 W4 W3B4 W2B3` | 8 | 12 | 1 | smallest new *3 reached by move class ins1_wb |
| `B5 W2 W2B4 W2B6 B7 W24 W3B4 W2B3` | 8 | 13 | 2 | smallest new *3 reached by move class add1 |
| `B4 B7 W5B6 B5 W2 W3B6 W3 W2B5 B5 W2` | 10 | 13 | 2 | smallest new *3 reached by move class remove1 |
| `B4 W2 B7 W3 W2B3 B7 W2B5 W3 W3B6 W2` | 10 | 13 | 2 | smallest new *3 reached by move class ins1_single |

## Checks (`verify_summary.txt`)

Re-evaluation with the UNMODIFIED engine (rg.c built with -DMAXN=64, batches of 20, TBITS=22, fall back to one position per call):
 hits:        403 rings (all 253 *3 of rounds 0-1, plus 150 random *3 of rounds 2-3): 403 agree, 0 disagree, all *3
 sample 600:  random rings of every value: 599 agree, 0 disagree, 1 not solvable by rg inside TBITS=22 (not a disagreement)
 sample 250:  random rings of every value (different seed): 250 agree, 0 disagree
 "agree" = the full 8-character signature of rg matches rgf's signature on every position rgf computed (rgf stops at the first L/R and pads with '?').

## Caveats

- "No *4" holds for the evaluated sample only: 128,791 of the roughly 2.9 million one-step-reachable rings in rounds 1-3 (round 1 complete, round 2 48 %, round 3 1 % of the available neighbours, and none with 15 or 16 files in round 3).
- A ring with signature NNNNNNNN is not shown to be a non-nimber; its value is *8 or above or not a nimber.
- The 86 aborted positions are unresolved, they could hide anything.
- Round-2 and round-3 output files (`out_r2_*.txt` hold only the resumed second part of round 2) are partial copies; `cache.tsv` has all 128,791 results. Raw candidate and output files are gzipped.
- The convention is rg.c's whole-board model (one e.p. flag cleared by any move); the C7 seeds come from the scanner's convention, and rgf re-confirmed all four as *3 in this model.

## Commands (all from research/star4_rings/grow/)

```
cp ../../ring_family_proof/rg.c rg.c ; cc -O2 -DMAXN=64 -o rg rg.c -lpthread        # reference engine
cp rg.c rgf.c ; (apply the RGF PATCH edits) ; cc -O2 -DMAXN=20 -o rgf rgf.c -lpthread
python3 collect_seeds.py                       # seeds_all.txt (14 classes)
python3 symtest.py                             # 480 solves, symmetry invariance
python3 grow.py init                           # cache.tsv with the seeds as round 0
python3 grow.py gen 1 && ./run_round.sh 1 2400 && python3 grow.py merge 1
python3 grow.py gen 2 - ins1_wb:15000,ins2_single:18000,ins1_dbl:3000,pair_same3:2000
./run_round.sh 2 3000 ; python3 grow.py merge 2 ; python3 grow.py resume 2 ; ./run_round.sh 2 1800 ; python3 grow.py merge 2
RINGONLY=1 python3 grow.py gen 3 - add1:9500,pair_same2:6000,pair_adj2:11000,remove1:1500,ins1_single:2500,ins1_wb:9000,ins2_single:9000,ins1_dbl:1000,pair_same3:1000
./run_round.sh 3 2700 ; python3 grow.py merge 3
NLATE=150 python3 verify_ref.py hits ; python3 verify_ref.py sample 600 ; python3 verify_ref.py sample 250
python3 analyze.py ; python3 gen_report.py     # tables, hits_star3.tsv, aborts.tsv, best.tsv
```
`run_round.sh` runs `TBITS=23 NODELIM=4000000 EARLYSTOP=1 DEADLINE_S=<s> nice -n 15 ./rgf solve 7 < cand_rR_{a,b}.txt` as two background jobs.

## Round 1 *3 hits (239 new, one-step neighbours of the seeds; canonical form; move class)

| ring | files | pawns | class |
|---|---|---|---|
| `B47 W24 W6B7 B5 W2 W3B7 W5B7` | 7 | 12 | pair_adj2 |
| `B47 W25 B5 W2 W3B6 B6 W4B7 W4` | 8 | 12 | pair_adj2 |
| `B5 W2 W2B4 W2B6 B7 W4 W3B4 W2B3` | 8 | 12 | ins1_wb |
| `B5 W2 W3B6 B6 W4B7 W4 W6B7 W2B3` | 8 | 12 | ins1_wb |
| `B5 W2 W3B6 B6 W4B7 W4 W6B7 W5B6` | 8 | 12 | ins1_wb |
| `B5 W2 W6B7 W3B6 B6 W4B7 W4 W6B7` | 8 | 12 | ins1_wb |
| `B6 W2 W3B6 B6 W4B7 W2 W6B7 W2B3` | 8 | 12 | ins1_wb |
| `B6 W2 W6B7 W3B6 B6 W4B7 W2 W6B7` | 8 | 12 | ins1_wb |
| `B4 B7 W3 W2B3 B7 W2B5 W3 W3B6 W2` | 9 | 12 | ins2_single |
| `B4 B7 W4 W2B3 B5 W2 W2B4 W2B6 W2` | 9 | 12 | ins2_single |
| `B4 B7 W4 W2B3 B5 W2B5 W3 W3B6 W2` | 9 | 12 | ins2_single |
| `B4 W2 B4 W25B7 B7 W2 W2B5 B7 W4` | 9 | 12 | ins2_single |
| `B4 W2 B5 W2 W3B6 B6 W4B7 W4 W6B7` | 9 | 12 | ins2_single |
| `B4 W2 B5 W2 W4B7 B7 W2 W2B47 W5` | 9 | 12 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W4 W6B7` | 9 | 12 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2B3 B7 W4` | 9 | 12 | ins1_wb |
| `B4 W2 B6 W2 W3B6 B6 W4B7 W2 W6B7` | 9 | 12 | ins2_single |
| `B4 W2 W3 B7 W3B6 W3 W2B5 B7 W2B3` | 9 | 12 | ins2_single |
| `B4 W2 W4 B7 W2B6 W2B4 W2 B5 W2B3` | 9 | 12 | ins2_single |
| `B4 W2 W4 B7 W3B6 W3 W2B5 B5 W2B3` | 9 | 12 | ins2_single |
| `B4 W25B7 B7 W2 W2B5 B6 W4 B7 W4` | 9 | 12 | ins2_single |
| `B5 B6 W4 W6B7 W4 B7 W5B7 W3B7 W2` | 9 | 12 | ins2_single |
| `B5 B6 W4 W6B7 W4 W4B7 B6 W3B6 W2` | 9 | 12 | ins2_single |
| `B5 B7 W2 W6B7 W4 B7 W5B7 W3B7 W2` | 9 | 12 | ins2_single |
| `B5 B7 W2 W6B7 W4 W4B7 B6 W3B6 W2` | 9 | 12 | ins2_single |
| `B5 B7 W4 W2B3 B5 W2B5 W3 W3B6 W3` | 9 | 12 | ins2_single |
| `B5 W2 B5 W3 W3B6 B6 W4B7 W4 W6B7` | 9 | 12 | ins2_single |
| `B5 W2 B6 W2 W3B6 B6 W4B7 W4 W6B7` | 9 | 12 | ins2_single |
| `B4 B7 W4 B47 W25 B5 W2B5 W3 W3B6 W2` | 10 | 14 | pair_adj2 |
| `B4 W2 B5 W2 W3B6 B6 W4B7 W4 B47 W25` | 10 | 14 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 B6 W24 B47 W4` | 10 | 14 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 B6 W4 B47 W24` | 10 | 14 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W24 B47 W5` | 10 | 14 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W3 B7 W4` | 10 | 12 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W4 B47 W25` | 10 | 14 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W45B7 B7 W5` | 10 | 14 | pair_same2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2B7 W4` | 10 | 13 | add1 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B7 W45B6` | 10 | 14 | pair_same2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B7 W5B6` | 10 | 13 | add1 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 W5B6 W4B7` | 10 | 14 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 W5B67 W4` | 10 | 14 | pair_same2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 W5B7 W5B7` | 10 | 14 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B57 W5B6 W4` | 10 | 14 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 W3B4 B7 W4` | 10 | 13 | add1 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 W3B45 B7 W4` | 10 | 14 | pair_same2 |
| `B4 W2 B5 W2B5 W3 W3B6 W23B4 B5 B7 W4` | 10 | 14 | pair_same2 |
| `B4 W2 B5 W2B5 W3 W3B6 W3 B5 B47 W24` | 10 | 14 | pair_adj2 |
| `B4 W2 W4 B7 W3B6 B6 W4B7 W4 B47 W25` | 10 | 14 | pair_adj2 |
| `B4 W2 W4 B7 W3B6 B6 W4B7 W4 B7 W25` | 10 | 13 | add1 |
| `B46 W2 B5 W2B5 W3 W3B6 W2 B5 B6 W4` | 10 | 13 | add1 |
| `B47 W25 B5 W2 W4 B6 W3B6 B6 W4B7 W4` | 10 | 14 | pair_adj2 |
| `B47 W25 B5 W2B5 W3 W3B6 W2 B5 B6 W4` | 10 | 14 | pair_adj2 |
| `B47 W2B3 B6 W2 W3 B6 B7 W3 W6B7 W24` | 10 | 14 | pair_adj2 |
| `B5 B6 W4 W5B4 W2B7 B5 W2B5 W3 W3B6 W2` | 10 | 14 | pair_adj2 |
| `B5 B6 W4B7 W5B4 W2 B5 W2B5 W3 W3B6 W2` | 10 | 14 | pair_adj2 |
| `B5 W2 W56B7 W3 B7 B6 W3 W2 B6 W2B3` | 10 | 13 | add1 |
| `B5 W2B3 B6 W2 W3 B6 B7 W3 W46B7 W2B6` | 10 | 14 | pair_adj2 |
| `B6 B7 W3 W6B7 W2B5 W3B5 W2B3 B6 W2 W3` | 10 | 14 | pair_adj2 |
| `B4 B6 W4 B6 B5 W2 W3B6 W3 W2B5 B5 W2` | 11 | 13 | ins1_single |
| `B4 B7 W2B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 11 | 14 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W6B7 W2` | 11 | 14 | ins1_wb |
| `B4 B7 W4 W6B7 B4 W2 B5 W2B5 W3 W3B6 W2` | 11 | 14 | ins1_wb |
| `B4 B7 W5 B7 B5 W2 W3B6 W3 W2B5 B5 W2` | 11 | 13 | ins1_single |
| `B4 W2 B5 W2 W3B6 B6 W4B7 W4 B7 W5 W2B3` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2 W6B7 W3B6 B6 W4B7 W4 B7 W5` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 B6 W4 W2B3 B7 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 B6 W4 W3B4 B7 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W4 W2B3 B7 W5` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W4 W3B4 B7 W5` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B7 W4` | 11 | 13 | ins1_single |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2B3 B7 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W4B5 B7 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B6 W4 W4B7` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B6 W4 W5B6` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B6 W4 W6B7` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B7 W2B7 W5` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B7 W5 W6B7` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 W5B6 B7 W5` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 W6B7 B6 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2B3 B6 W4 B7 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2B3 W3 B5 B7 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W2B7 B6 W4 B7 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W3 B5 B7 W4 W6B7` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W6B7 B6 W4 B7 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W6B7 W2 B5 B6 W4` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W6B7 W2 B5 B7 W5` | 11 | 14 | ins1_wb |
| `B4 W2 B5 W2B5 W3 W3B6 W6B7 W3 B5 B7 W4` | 11 | 14 | ins1_wb |
| `B5 W2 W3B6 W6B7 W3 B7 B6 W3 W2 B6 W2B3` | 11 | 14 | ins1_wb |
| `B5 W2 W4B5 W6B7 W3 B7 B6 W3 W2 B6 W2B3` | 11 | 14 | ins1_wb |
| `B5 W2 W5B6 W6B7 W3 B7 B6 W3 W2 B6 W2B3` | 11 | 14 | ins1_wb |
| `B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2B3 W5B6` | 11 | 14 | ins1_wb |
| `B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2B3 W6B7` | 11 | 14 | ins1_wb |
| `B5 W2B3 B6 W2 W3 B6 B7 W3 W6B7 W2 W2B7` | 11 | 14 | ins1_wb |
| `- B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 12 | 13 | remove1 |
| `B4 B5 W3 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 12 | 14 | ins2_single |
| `B4 B5 W3 W3B6 B6 W4B7 W4 B7 W5 B5 W2 W2` | 12 | 14 | ins2_single |
| `B4 B5 W3 W3B6 W3 W2B5 B5 W2 B4 W4 B7 W2` | 12 | 14 | ins2_single |
| `B4 B5 W3 W4 B7 W3B6 B6 W4B7 W4 B7 W5 W2` | 12 | 14 | ins2_single |
| `B4 B5 W3 W5 B7 W4 W4B7 B6 W3B6 B7 W4 W2` | 12 | 14 | ins2_single |
| `B4 B5 W3 W5 B7 W4 W4B7 B6 W3B6 W2 B5 W2` | 12 | 14 | ins2_single |
| `B4 B6 W4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 12 | 14 | ins2_single |
| `B4 B6 W4 W2 B5 W5 B7 W4 W4B7 B6 W3B6 W2` | 12 | 14 | ins2_single |
| `B4 B7 W2 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 12 | 14 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 B6 W4 W2` | 12 | 14 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 B7 W5 W2` | 12 | 14 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B46 W24` | 12 | 16 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B47 W25` | 12 | 16 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 W3B4 W2` | 12 | 15 | add1 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 W3B4 W2B5` | 12 | 16 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 W3B45 W2` | 12 | 16 | pair_same2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 W5B4 W2B7` | 12 | 16 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2B7 W5B4 W2` | 12 | 16 | pair_adj2 |
| `B4 B7 W4 B47 W25 B5 W2B5 W3 W3B6 W2 B4 W2` | 12 | 16 | pair_adj2 |
| `B4 B7 W4 B7 W5 B4 W2 B5 W2B5 W3 W3B6 W2` | 12 | 14 | ins2_single |
| `B4 B7 W4 W2 B4 W5 B7 W4 W4B7 B6 W3B6 W2` | 12 | 14 | ins2_single |
| `B4 B7 W4 W3 B5 W5 B7 W4 W4B7 B6 W3B6 W2` | 12 | 14 | ins2_single |
| `B4 B7 W5 B4 W2 B5 W2B5 W3 W3B6 B7 W4 W2` | 12 | 14 | ins2_single |
| `B4 W2 B4 W2 B5 W2 W3B6 B6 W4B7 W4 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 W2B7` | 12 | 15 | add1 |
| `B4 W2 B4 W2 W4 B7 W3B6 B6 W4B7 W4 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2 W4 B6 W3B6 B6 W4B7 W4 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2 W6B7 W3 B7 B6 W3 W2 B6 W2B3` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 B6 W4 B4 W2 B7 W4` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 B6 W4 W2 B5 B6 W4` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 B6 W4 W2 B5 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 B6 W4 W3 B5 B7 W4` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W4 B4 W2 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W4 W2 B7 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 B7 W4 W3 B5 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 W3B4 B7 W4` | 12 | 15 | add1 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 W3B45 B7 W4` | 12 | 16 | pair_same2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W24 B46 B7 W4` | 12 | 16 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W25 B47 B7 W4` | 12 | 16 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2B5 W3B4 B7 W4` | 12 | 16 | pair_adj2 |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W4 B6 B7 W4` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B4 W5 B7 B7 W4` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B6 W4 B6 W4` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B6 W4 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B7 W2 B6 W4` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 B7 W2 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 W5 B7 B6 W4` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W2 B5 W5 B7 B7 W5` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W3 B5 B6 W4 B7 W4` | 12 | 14 | ins2_single |
| `B4 W2 B5 W2B5 W3 W3B6 W3 B5 W5 B7 B7 W4` | 12 | 14 | ins2_single |
| `B4 W2 B6 W2 W3 B6 B7 W3 W6B7 W2 B5 W2B3` | 12 | 14 | ins2_single |
| `B4 W2 B6 W2 W3 B6 B7 W3 W6B7 W4 B7 W2B3` | 12 | 14 | ins2_single |
| `B4 W2 B7 W4 W6B7 W3 B7 B6 W3 W2 B6 W2B3` | 12 | 14 | ins2_single |
| `B4 W2 W2 B5 W2B3 B6 W2 W3 B6 B7 W3 W6B7` | 12 | 14 | ins2_single |
| `B4 W2 W4 B7 W2B3 B6 W2 W3 B6 B7 W3 W6B7` | 12 | 14 | ins2_single |
| `B4 W2 W6B7 W3 B7 B6 W3 W2 B6 W2B3 B7 W4` | 12 | 14 | ins2_single |
| `B5 B6 W4 W2B3 B6 W2 W3 B6 B7 W3 W6B7 W2` | 12 | 14 | ins2_single |
| `B5 B7 W4 W6B7 W3 B7 B6 W3 W2 B6 W2B3 W3` | 12 | 14 | ins2_single |
| `B5 W2 B5 W2B3 B6 W2 W3 B6 B7 W3 W6B7 W3` | 12 | 14 | ins2_single |
| `B5 W2 B6 W4 W6B7 W3 B7 B6 W3 W2 B6 W2B3` | 12 | 14 | ins2_single |
| `B5 W2 B7 W2 W6B7 W3 B7 B6 W3 W2 B6 W2B3` | 12 | 14 | ins2_single |
| `B5 W2 W3 B5 W6B7 W3 B7 B6 W3 W2 B6 W2B3` | 12 | 14 | ins2_single |
| `B4 B7 W2B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 13 | 16 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W4B5 W2` | 13 | 16 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W5B6 W2` | 13 | 16 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W6B7 W2` | 13 | 16 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W6B7 W2 B4 W2` | 13 | 16 | ins1_wb |
| `B4 B7 W4 W6B7 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 13 | 16 | ins1_wb |
| `B4 W2 B4 W2 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 13 | 15 | ins1_single |
| `B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 W2B3` | 13 | 16 | ins1_wb |
| `B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 W4B5` | 13 | 16 | ins1_wb |
| `- B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2` | 14 | 15 | remove1 |
| `- B7 W5 B7 W3B6 B6 W4B7 W4 B7 W5 B5 W2 W5 B7` | 14 | 15 | remove1 |
| `B4 B5 W3 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 14 | 16 | ins2_single |
| `B4 B5 W3 W2 B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 14 | 16 | ins2_single |
| `B4 B6 W4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 14 | 16 | ins2_single |
| `B4 B6 W4 W2 B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 14 | 16 | ins2_single |
| `B4 B7 W2 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 14 | 16 | ins2_single |
| `B4 B7 W2 W2 B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 14 | 16 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 B6 W4 W2 B4 W2` | 14 | 16 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 B7 W5 W2 B4 W2` | 14 | 16 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 B7 W5 W2` | 14 | 16 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B46 W24` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B47 W25` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 W3B4 W2` | 14 | 17 | add1 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 W3B4 W2B5` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 W3B45 W2` | 14 | 18 | pair_same2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 W5B4 W2B7` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W24 B46 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W25 B47 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2B5 W3B4 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2B7 W5B4 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W4 B6 W2` | 14 | 16 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W5 B7 W2` | 14 | 16 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B46 W24 B4 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B47 W25 B4 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 W3B4 W2 B4 W2` | 14 | 17 | add1 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 W3B4 W2B5 B4 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 W3B45 W2 B4 W2` | 14 | 18 | pair_same2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 W5B4 W2B7 B4 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2B7 W5B4 W2 B4 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B47 W25 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2` | 14 | 18 | pair_adj2 |
| `B4 B7 W4 B7 W5 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 14 | 16 | ins2_single |
| `B4 W2 B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 W2B7` | 14 | 17 | add1 |
| `B4 W2 B4 W2 W3B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 14 | 17 | add1 |
| `B4 W2 B4 W2 W3B45 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 14 | 18 | pair_same2 |
| `B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 B46 W24` | 14 | 18 | pair_adj2 |
| `B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 B47 W25` | 14 | 18 | pair_adj2 |
| `B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 B6 W4` | 14 | 16 | ins2_single |
| `B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 B7 W5` | 14 | 16 | ins2_single |
| `B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 W3B4 W2B5` | 14 | 18 | pair_adj2 |
| `B4 B7 W2B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2` | 15 | 18 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2 W2` | 15 | 17 | ins1_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W4B5 W2` | 15 | 18 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W5B6 W2` | 15 | 18 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W6B7 W2` | 15 | 18 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W4B5 W2 B4 W2` | 15 | 18 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W5B6 W2 B4 W2` | 15 | 18 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W6B7 W2 B4 W2` | 15 | 18 | ins1_wb |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W6B7 W2 B4 W2 B4 W2` | 15 | 18 | ins1_wb |
| `B4 B7 W4 W6B7 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2` | 15 | 18 | ins1_wb |
| `B4 W2 B4 W2 B4 W2 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 15 | 17 | ins1_single |
| `B4 W2 B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 W2B3` | 15 | 18 | ins1_wb |
| `B4 W2 B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 W4B5` | 15 | 18 | ins1_wb |
| `B4 B5 W3 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B5 W3 W2 B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B5 W3 W2 B4 W2 B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 16 | 18 | ins2_single |
| `B4 B6 W4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B6 W4 W2 B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B6 W4 W2 B4 W2 B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 16 | 18 | ins2_single |
| `B4 B7 W2 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B7 W2 W2 B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B7 W2 W2 B4 W2 B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 B6 W4 W2 B4 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 B7 W5 W2 B4 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 B7 W5 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 B7 W5 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W4 B6 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W5 B7 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W4 B6 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W5 B7 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 B7 W4 B7 W5 B4 W2 B5 W2B5 W3 W3B6 W2 B4 W2 B4 W2` | 16 | 18 | ins2_single |
| `B4 W2 B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 B6 W4` | 16 | 18 | ins2_single |
| `B4 W2 B4 W2 B4 W2 W3B6 W3 W2B5 B5 W2 B4 W4 B7 B7 W5` | 16 | 18 | ins2_single |
