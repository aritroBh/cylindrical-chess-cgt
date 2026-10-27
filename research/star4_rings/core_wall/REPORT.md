# star4_rings/core_wall: core-in-wall enumeration (REPORT)

**Summary (5 lines).**
1. I evaluated 23,235,751 rings "core of w = 3..6 files, p = w..w+4 core pawns, closed by an alternating W2/B4 wall of L = 4 or 5 files, both phases" (n = w+4 or w+5), each with the full rg signature of G+*h, h = 0..7. 20,135,751 of them are EXHAUSTIVE (every core of w=3 with p<=7, w=4 with p<=7, w=5 with p<=7, w=6 with p<=7, plus w=4, p=8 for the L=5 phase-1 wall); the other 3,100,000 are uniform random samples of the larger layers (w=4 p=8, w=5 p=8,9, w=6 p=8,9,10).
2. **No *4 anywhere, and no *3 or higher: the maximum nimber in the whole family is *2.** Counts: *0 = 81,506, *1 = 42,477, *2 = 7, *3 = *4 = *5 = *6 = *7 = 0; 11,713,590 rings are N for all of h=0..7 (no nimber <= *7), the rest (11.4M) are decided non-nimbers (L/R-type).
3. The seven *2 rings all have narrow cores (w = 3 or 4, 6 to 8 core pawns); each pumps as *2 for every second wall length up to n = 18-20 and none ever becomes *3 (176 longer-wall rings, n <= 20). The only near miss is W4B7 W2B6 W2B7 W2 B4 W2 B4 with signature NNNRRRRR (G+*3 is a Right win, so it is not a nimber).
4. Verification: my fast engine (rgq, same win/gen/cls code as rg.c, plus early stop and table flush) agrees with the unmodified rg (MAXN=64, solve 7) on 4,810 positions (full signature) and on all 2,071 distinct reported hit rings; the 23 positions that overflowed the default table were re-run with TBITS=24 (all NNNNNNNN); exhaustive layer sizes equal the independent counts of gen.c.
5. SUPPLEMENTARY (outside the brief): one-pawn local moves around the *2 rings (they leave the wall family) DO reach *3 within 3 moves (41 distinct *3 rings, n = 8 or 9, all re-checked with the unmodified rg), and a second round restricted to the *3 and near-*4 rings (2 complete levels, 2,418 rings) found no *4 (see section 6).

## 1. What was run

- Game and engine: whole-board pawn game on the n-file cylinder, 8 ranks, race rule "count", e.p. on, a pawn that can be taken e.p. is not passed, game ends at the first passed pawn. Engine `rg.c` copied from `research/ring_family_proof/rg.c` (unchanged, built `cc -O2 -DMAXN=64 -o rg rg.c -lpthread`, used for verification only).
- Fast engine `cwq.c` (binary `cwq`): the same `gen`, `cls`, `has_passed`, `pdist`, `win` code as rg.c, with five changes that do not touch the game logic: (1) MAXN=24 (smaller positions, faster hashing; n <= 20 here); (2) the memo table is flushed between positions when 30% full instead of exiting, and a position that still overflows the 2^21-entry table is recorded as TABLEFULL (and re-run later with TBITS=24); (3) h is evaluated in increasing order and the loop stops at the first non-N result: if it is P the signature is NNN..P..NNN (G+*k = P implies G+*h = N for every h > k by moving *h to *k), if it is L or R the position is not a nimber and the rest is not needed; (4) the ring generator and sampler are built in (one process per worker); (5) a job queue (`cwq queue jobs.txt out`). `rgq.c` is the same engine without the generator; `rgq solvef 7` computes all 8 values (no early stop).
- Resources: 2 worker processes, each `nice -n 15`, about 112 MB RSS each, no git, no pkill/killall (the workers were stopped with a STOP file or by PID). The machine load average was about 270 on 14 cores, so each worker received about 20% of a core: 106 jobs took 3.15 worker-hours of wall time (about 1.7 h elapsed, 15:06-16:48) which is roughly 0.6 CPU-hours. The follow-up runs (walls, local search, verification) were one process at a time.

## 2. The enumeration
- Ring order: core files c_0..c_{w-1} followed by wall files x_0..x_{L-1} (cyclic). Wall phase 0: x = W2 B4 W2 B4 (W2 B4 W2 B4 W2 for L=5); phase 1: x = B4 W2 B4 W2 (B4 W2 B4 W2 B4). n = w+L.
- Core: every file non-empty, p core pawns in total (p = w..w+4), white pawns on ranks 2..6, black pawns on ranks 3..7 (a white pawn on rank 7 or a black pawn on rank 2 is always passed, so this loses nothing), no two pawns on one square, and **no passed pawn anywhere in the ring** (textbook test, the wall pawns are never passed because they are blocked inside the wall).
- Symmetry: the game is invariant under reflection (file order reversed; checked: 2,405 sampled rings and their mirror images, 0 differences). For L=4 the mirror image of (core, phase 1) is (reversed core, phase 0), so only phase 0 is run. For L=5 both phases are palindromic, so the exhaustive runs keep one of each mirror pair (core <= reversed core). Colour reversal does not map the family to itself (W2 goes to B7, not B4) so it is not used. The sampled layers draw ordered core tuples uniformly (no mirror reduction).
- Exhaustive layers were sharded (`E` jobs, shard s of S by a counter over the DFS order). Evaluated counts equal the independent counts of `gen.c` for every exhaustive layer (e.g. w=6 p=7: 1,866,335 + 1,197,866 + 725,751 = 3,789,952; w=5 p=7: 6,210,666; w=4 p=8, L=5 phase 1: 3,716,101) and, for the sampler, `samp.c`'s DP total times acceptance matches `gen.c` (w=5 p=9, L=4: 7.51e8 x 0.1967 = 1.48e8 against 149,070,665 counted).
- Size of the full space (valid cores, all three wall variants, L=5 mirror-reduced when exhaustive): w=3: 502 / 7,416 / 53,701 / 252,724 / 859,586 for p=3..7; w=4: 3,032 / 61,770 / 611,653 / 3,930,951 / 18,438,160 for p=4..8; w=5: 19,315 / 496,771 / 6,210,666 / 50,580,151 / 302,060,841 for p=5..9; w=6: 121,611 / 3,789,952 for p=6,7 and about 8.6e7 / 8.6e8 / 6.2e9 (ordered cores, estimated from the sampler) for p=8,9,10. The random samples therefore cover about 4.1% (w=4 p=8), 1.1% (w=5 p=8), 0.15% (w=5 p=9), 0.5% (w=6 p=8), 0.05% (w=6 p=9) and 0.007% (w=6 p=10) of their layers: for those layers "no *3/*4" is a statistical statement, not a proof.

## 3. Distribution of nimbers by (w, p)
Class columns: `*k` = signature with P exactly at h=k (a nimber); `allN` = N for all h=0..7 (no nimber <= *7; includes non-nimbers and any nimber >= *8); `nn_h0` = first non-N result at h=0 is L or R (G itself is a Left or Right win: not a nimber); `nn_h1`, `nn_h2+` = first non-N result at h=1, or at h>=2, is L or R (not a nimber); `unres` = table overflow not resolved (0 after the TBITS=24 re-run of 23 positions, all of which are allN). "exhaustive" rows are complete layers, "random sample" rows are uniform samples. The w=4 p=8 sample row includes 250,000 draws of the L=5 phase-1 variant that is also run exhaustively.


#### Per (w, p), summed over the three wall variants (L=4 ph0, L=5 ph0, L=5 ph1)

| cell | evaluated | *0 | *1 | *2 | *3 | *4 | *5+ | allN | nn_h0 | nn_h1 | nn_h2+ | unres |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w=3 p=3 exhaustive | 502 | 25 | 10 | 0 | 0 | 0 | 0 | 212 | 239 | 16 | 0 | 0 |
| w=3 p=4 exhaustive | 7416 | 245 | 115 | 0 | 0 | 0 | 0 | 2761 | 3948 | 331 | 16 | 0 |
| w=3 p=5 exhaustive | 53701 | 714 | 267 | 0 | 0 | 0 | 0 | 19018 | 31403 | 2261 | 38 | 0 |
| w=3 p=6 exhaustive | 252724 | 2633 | 987 | 2 | 0 | 0 | 0 | 95246 | 145349 | 8194 | 313 | 0 |
| w=3 p=7 exhaustive | 859586 | 4824 | 1601 | 1 | 0 | 0 | 0 | 333778 | 493822 | 24830 | 730 | 0 |
| w=4 p=4 exhaustive | 3032 | 133 | 88 | 0 | 0 | 0 | 0 | 1598 | 1109 | 102 | 2 | 0 |
| w=4 p=5 exhaustive | 61770 | 744 | 368 | 0 | 0 | 0 | 0 | 28166 | 30357 | 2094 | 41 | 0 |
| w=4 p=6 exhaustive | 611653 | 5158 | 2700 | 0 | 0 | 0 | 0 | 274440 | 313720 | 15221 | 414 | 0 |
| w=4 p=7 exhaustive | 3930951 | 16640 | 7397 | 3 | 0 | 0 | 0 | 1733378 | 2091244 | 80412 | 1877 | 0 |
| w=4 p=8 exhaustive (1/3 variants) | 3716101 | 4971 | 1869 | 0 | 0 | 0 | 0 | 1817872 | 1849684 | 41009 | 696 | 0 |
| w=4 p=8 random sample | 750000 | 1966 | 911 | 1 | 0 | 0 | 0 | 341516 | 393771 | 11528 | 307 | 0 |
| w=5 p=5 exhaustive | 19315 | 281 | 188 | 0 | 0 | 0 | 0 | 10900 | 7550 | 391 | 5 | 0 |
| w=5 p=6 exhaustive | 496771 | 4165 | 2679 | 0 | 0 | 0 | 0 | 265898 | 213594 | 10194 | 241 | 0 |
| w=5 p=7 exhaustive | 6210666 | 21494 | 11884 | 0 | 0 | 0 | 0 | 3167731 | 2906876 | 101025 | 1656 | 0 |
| w=5 p=8 random sample | 550000 | 1247 | 689 | 0 | 0 | 0 | 0 | 281364 | 260033 | 6518 | 149 | 0 |
| w=5 p=9 random sample | 450000 | 558 | 257 | 0 | 0 | 0 | 0 | 229910 | 215120 | 4066 | 89 | 0 |
| w=6 p=6 exhaustive | 121611 | 1424 | 1147 | 0 | 0 | 0 | 0 | 77593 | 39157 | 2248 | 42 | 0 |
| w=6 p=7 exhaustive | 3789952 | 12552 | 8326 | 0 | 0 | 0 | 0 | 2258443 | 1455203 | 54694 | 734 | 0 |
| w=6 p=8 random sample | 450000 | 904 | 600 | 0 | 0 | 0 | 0 | 262245 | 182024 | 4143 | 84 | 0 |
| w=6 p=9 random sample | 450000 | 499 | 248 | 0 | 0 | 0 | 0 | 256800 | 189324 | 3059 | 70 | 0 |
| w=6 p=10 random sample | 450000 | 329 | 146 | 0 | 0 | 0 | 0 | 254721 | 192205 | 2529 | 70 | 0 |
| **ALL** | 23235751 | 81506 | 42477 | 7 | 0 | 0 | 0 | 11713590 | 11015732 | 374865 | 7574 | 0 |

#### Per variant (L = wall length, ph = wall phase; E = exhaustive shards, S = sample)

| cell | evaluated | *0 | *1 | *2 | *3 | *4 | *5+ | allN | nn_h0 | nn_h1 | nn_h2+ | unres |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| w=3 p=3 L=4 ph=0 E(1/1 shards) | 236 | 8 | 4 | 0 | 0 | 0 | 0 | 101 | 115 | 8 | 0 | 0 |
| w=3 p=3 L=5 ph=0 E(1/1 shards) | 165 | 10 | 3 | 0 | 0 | 0 | 0 | 61 | 84 | 7 | 0 | 0 |
| w=3 p=3 L=5 ph=1 E(1/1 shards) | 101 | 7 | 3 | 0 | 0 | 0 | 0 | 50 | 40 | 1 | 0 | 0 |
| w=3 p=4 L=4 ph=0 E(1/1 shards) | 3587 | 135 | 64 | 0 | 0 | 0 | 0 | 1397 | 1834 | 146 | 11 | 0 |
| w=3 p=4 L=5 ph=0 E(1/1 shards) | 2365 | 89 | 44 | 0 | 0 | 0 | 0 | 761 | 1331 | 135 | 5 | 0 |
| w=3 p=4 L=5 ph=1 E(1/1 shards) | 1464 | 21 | 7 | 0 | 0 | 0 | 0 | 603 | 783 | 50 | 0 | 0 |
| w=3 p=5 L=4 ph=0 E(1/1 shards) | 26235 | 320 | 110 | 0 | 0 | 0 | 0 | 9032 | 15513 | 1253 | 7 | 0 |
| w=3 p=5 L=5 ph=0 E(1/1 shards) | 16709 | 254 | 95 | 0 | 0 | 0 | 0 | 5454 | 10108 | 779 | 19 | 0 |
| w=3 p=5 L=5 ph=1 E(1/1 shards) | 10757 | 140 | 62 | 0 | 0 | 0 | 0 | 4532 | 5782 | 229 | 12 | 0 |
| w=3 p=6 L=4 ph=0 E(1/1 shards) | 124324 | 1436 | 551 | 1 | 0 | 0 | 0 | 47339 | 70928 | 3892 | 177 | 0 |
| w=3 p=6 L=5 ph=0 E(1/1 shards) | 76759 | 932 | 371 | 1 | 0 | 0 | 0 | 26808 | 45486 | 3039 | 122 | 0 |
| w=3 p=6 L=5 ph=1 E(1/1 shards) | 51641 | 265 | 65 | 0 | 0 | 0 | 0 | 21099 | 28935 | 1263 | 14 | 0 |
| w=3 p=7 L=4 ph=0 E(1/1 shards) | 424594 | 2225 | 716 | 0 | 0 | 0 | 0 | 162074 | 246245 | 13017 | 317 | 0 |
| w=3 p=7 L=5 ph=0 E(1/1 shards) | 255413 | 1861 | 639 | 1 | 0 | 0 | 0 | 94872 | 148919 | 8814 | 307 | 0 |
| w=3 p=7 L=5 ph=1 E(1/1 shards) | 179579 | 738 | 246 | 0 | 0 | 0 | 0 | 76832 | 98658 | 2999 | 106 | 0 |
| w=4 p=4 L=4 ph=0 E(1/1 shards) | 1525 | 75 | 50 | 0 | 0 | 0 | 0 | 795 | 549 | 54 | 2 | 0 |
| w=4 p=4 L=5 ph=0 E(1/1 shards) | 925 | 53 | 36 | 0 | 0 | 0 | 0 | 451 | 343 | 42 | 0 | 0 |
| w=4 p=4 L=5 ph=1 E(1/1 shards) | 582 | 5 | 2 | 0 | 0 | 0 | 0 | 352 | 217 | 6 | 0 | 0 |
| w=4 p=5 L=4 ph=0 E(1/1 shards) | 30836 | 331 | 168 | 0 | 0 | 0 | 0 | 13666 | 15502 | 1156 | 13 | 0 |
| w=4 p=5 L=5 ph=0 E(1/1 shards) | 19094 | 254 | 113 | 0 | 0 | 0 | 0 | 7967 | 9973 | 770 | 17 | 0 |
| w=4 p=5 L=5 ph=1 E(1/1 shards) | 11840 | 159 | 87 | 0 | 0 | 0 | 0 | 6533 | 4882 | 168 | 11 | 0 |
| w=4 p=6 L=4 ph=0 E(1/1 shards) | 303966 | 2896 | 1545 | 0 | 0 | 0 | 0 | 137916 | 154122 | 7238 | 249 | 0 |
| w=4 p=6 L=5 ph=0 E(1/1 shards) | 188599 | 1850 | 1004 | 0 | 0 | 0 | 0 | 77111 | 102680 | 5807 | 147 | 0 |
| w=4 p=6 L=5 ph=1 E(1/1 shards) | 119088 | 412 | 151 | 0 | 0 | 0 | 0 | 59413 | 56918 | 2176 | 18 | 0 |
| w=4 p=7 L=4 ph=0 E(4/4 shards) | 1953151 | 7841 | 3537 | 3 | 0 | 0 | 0 | 852741 | 1045737 | 42473 | 819 | 0 |
| w=4 p=7 L=5 ph=0 E(3/3 shards) | 1199768 | 6083 | 2617 | 0 | 0 | 0 | 0 | 492324 | 668687 | 29309 | 748 | 0 |
| w=4 p=7 L=5 ph=1 E(2/2 shards) | 778032 | 2716 | 1243 | 0 | 0 | 0 | 0 | 388313 | 376820 | 8630 | 310 | 0 |
| w=4 p=8 L=4 ph=0 S | 250000 | 779 | 364 | 0 | 0 | 0 | 0 | 112818 | 131934 | 3974 | 131 | 0 |
| w=4 p=8 L=5 ph=0 S | 250000 | 902 | 423 | 1 | 0 | 0 | 0 | 106251 | 137371 | 4918 | 134 | 0 |
| w=4 p=8 L=5 ph=1 E(6/6 shards) | 3716101 | 4971 | 1869 | 0 | 0 | 0 | 0 | 1817872 | 1849684 | 41009 | 696 | 0 |
| w=4 p=8 L=5 ph=1 S | 250000 | 285 | 124 | 0 | 0 | 0 | 0 | 122447 | 124466 | 2636 | 42 | 0 |
| w=5 p=5 L=4 ph=0 E(1/1 shards) | 9233 | 121 | 83 | 0 | 0 | 0 | 0 | 5313 | 3532 | 183 | 1 | 0 |
| w=5 p=5 L=5 ph=0 E(1/1 shards) | 6342 | 91 | 58 | 0 | 0 | 0 | 0 | 3205 | 2824 | 162 | 2 | 0 |
| w=5 p=5 L=5 ph=1 E(1/1 shards) | 3740 | 69 | 47 | 0 | 0 | 0 | 0 | 2382 | 1194 | 46 | 2 | 0 |
| w=5 p=6 L=4 ph=0 E(1/1 shards) | 242188 | 2347 | 1495 | 0 | 0 | 0 | 0 | 133705 | 99572 | 4910 | 159 | 0 |
| w=5 p=6 L=5 ph=0 E(1/1 shards) | 158557 | 1518 | 1029 | 0 | 0 | 0 | 0 | 75824 | 76160 | 3959 | 67 | 0 |
| w=5 p=6 L=5 ph=1 E(1/1 shards) | 96026 | 300 | 155 | 0 | 0 | 0 | 0 | 56369 | 37862 | 1325 | 15 | 0 |
| w=5 p=7 L=4 ph=0 E(6/6 shards) | 3047010 | 9923 | 5560 | 0 | 0 | 0 | 0 | 1564955 | 1411928 | 53964 | 680 | 0 |
| w=5 p=7 L=5 ph=0 E(4/4 shards) | 1952827 | 7716 | 4074 | 0 | 0 | 0 | 0 | 909445 | 993719 | 37213 | 660 | 0 |
| w=5 p=7 L=5 ph=1 E(3/3 shards) | 1210829 | 3855 | 2250 | 0 | 0 | 0 | 0 | 693331 | 501229 | 9848 | 316 | 0 |
| w=5 p=8 L=4 ph=0 S | 250000 | 653 | 376 | 0 | 0 | 0 | 0 | 128585 | 117264 | 3041 | 81 | 0 |
| w=5 p=8 L=5 ph=0 S | 150000 | 414 | 237 | 0 | 0 | 0 | 0 | 70346 | 76712 | 2237 | 54 | 0 |
| w=5 p=8 L=5 ph=1 S | 150000 | 180 | 76 | 0 | 0 | 0 | 0 | 82433 | 66057 | 1240 | 14 | 0 |
| w=5 p=9 L=4 ph=0 S | 150000 | 189 | 88 | 0 | 0 | 0 | 0 | 76141 | 72052 | 1495 | 35 | 0 |
| w=5 p=9 L=5 ph=0 S | 150000 | 238 | 122 | 0 | 0 | 0 | 0 | 71311 | 76571 | 1722 | 36 | 0 |
| w=5 p=9 L=5 ph=1 S | 150000 | 131 | 47 | 0 | 0 | 0 | 0 | 82458 | 66497 | 849 | 18 | 0 |
| w=6 p=6 L=4 ph=0 E(1/1 shards) | 59695 | 794 | 631 | 0 | 0 | 0 | 0 | 39103 | 17908 | 1235 | 24 | 0 |
| w=6 p=6 L=5 ph=0 E(1/1 shards) | 38705 | 541 | 460 | 0 | 0 | 0 | 0 | 22530 | 14283 | 874 | 17 | 0 |
| w=6 p=6 L=5 ph=1 E(1/1 shards) | 23211 | 89 | 56 | 0 | 0 | 0 | 0 | 15960 | 6966 | 139 | 1 | 0 |
| w=6 p=7 L=4 ph=0 E(4/4 shards) | 1866335 | 5715 | 3913 | 0 | 0 | 0 | 0 | 1117763 | 709717 | 28947 | 280 | 0 |
| w=6 p=7 L=5 ph=0 E(3/3 shards) | 1197866 | 4347 | 2728 | 0 | 0 | 0 | 0 | 661941 | 507882 | 20671 | 297 | 0 |
| w=6 p=7 L=5 ph=1 E(2/2 shards) | 725751 | 2490 | 1685 | 0 | 0 | 0 | 0 | 478739 | 237604 | 5076 | 157 | 0 |
| w=6 p=8 L=4 ph=0 S | 150000 | 377 | 247 | 0 | 0 | 0 | 0 | 87804 | 60083 | 1453 | 36 | 0 |
| w=6 p=8 L=5 ph=0 S | 150000 | 365 | 265 | 0 | 0 | 0 | 0 | 80616 | 66942 | 1772 | 40 | 0 |
| w=6 p=8 L=5 ph=1 S | 150000 | 162 | 88 | 0 | 0 | 0 | 0 | 93825 | 54999 | 918 | 8 | 0 |
| w=6 p=9 L=4 ph=0 S | 150000 | 171 | 89 | 0 | 0 | 0 | 0 | 85262 | 63285 | 1179 | 14 | 0 |
| w=6 p=9 L=5 ph=0 S | 150000 | 222 | 88 | 0 | 0 | 0 | 0 | 79339 | 68999 | 1316 | 36 | 0 |
| w=6 p=9 L=5 ph=1 S | 150000 | 106 | 71 | 0 | 0 | 0 | 0 | 92199 | 57040 | 564 | 20 | 0 |
| w=6 p=10 L=4 ph=0 S | 150000 | 128 | 59 | 0 | 0 | 0 | 0 | 84944 | 63921 | 919 | 29 | 0 |
| w=6 p=10 L=5 ph=0 S | 150000 | 149 | 67 | 0 | 0 | 0 | 0 | 79607 | 69067 | 1079 | 31 | 0 |
| w=6 p=10 L=5 ph=1 S | 150000 | 52 | 20 | 0 | 0 | 0 | 0 | 90170 | 59217 | 531 | 10 | 0 |


## 4. Every *2, *3, *4 hit and every near miss of the enumeration

**No *3, no *4, no nimber above *2 appeared in any of the 23,235,751 rings.** The signature counts for the whole enumeration whose first non-N entry is at h >= 2: NNPNNNNN (*2) 7, NNL..... 2,581, NNR..... 4,992, NNNR.... 1 (the signature NNNRRRRR); no signature starts with NNNN.

The seven *2 rings (all verified with the unmodified rg):

| job | ring (token per file) | signature |
|---|---|---|
| E_3_6_4_0_0of1 | `W4B7 W3B6 W2B7 W2 B4 W2 B4` | NNPNNNNN |
| E_3_6_5_0_0of1 | `B5 W2B5 W35B6 W2 B4 W2 B4 W2` | NNPNNNNN |
| E_3_7_5_0_0of1 | `W2B46 W4B6 W3B7 W2 B4 W2 B4 W2` | NNPNNNNN |
| E_4_7_4_0_0of4 | `W2 B5 W2B5 W35B6 W2 B4 W2 B4` | NNPNNNNN |
| E_4_7_4_0_0of4 | `W2 W35B6 W2B5 B5 W2 B4 W2 B4` | NNPNNNNN |
| E_4_7_4_0_1of4 | `W26B7 W2 W3B7 B5 W2 B4 W2 B4` | NNPNNNNN |
| S_4_8_5_0_n200000_s2 | `B7 W3B6 W34B67 W4 W2 B4 W2 B4 W2` | NNPNNNNN |

The only ring whose first non-N result is at h = 3 (closest to *3, and 1 step from a *4 pattern NNNNPNNN is not applicable):

| job | ring | signature |
|---|---|---|
| E_3_6_4_0_0of1 | `W4B7 W2B6 W2B7 W2 B4 W2 B4` | NNNR.... |

Full signature of that ring from `rgq solvef 7`: NNNRRRRR. Rings with `star4` signature NNNNPNNN: **none**.

Sanity anchors: the known *2 ring P_10 = `W5 B7 W4 W4B7 B6 W3B6 W2 B4 W2 B4` is inside this family (w=6, p=8, L=4, phase 0; no passed pawn) and evaluates to NNPNNNNN (*2) with the unmodified rg (it is not in the sample, p=8 at w=6 is sampled); the known *3 rings Q_8 = `W4 B7 W3B6 W3 W2B5 B5 W2 B4` and the C8 ring `W5 B7 W4 W4B7 B6 W3B6 W2 B5` evaluate to NNNPNNNN with both engines but are not in the family (their wall has a B5 defect).

## 5. Longer walls (n up to 20) for the *2 cores and the near miss

For each of the 8 cores above (cores = first w tokens) I closed the core with alternating W2/B4 walls of length L = 4..16 (n = w+L <= 20), both phases, and evaluated all 208 rings with `rgq solvef 7` (`walls.py`, results in `walls_results.tsv`). Entries: `*2` = NNPNNNNN, `N8` = NNNNNNNN, `L-all`/`R-all` = L or R for every h; other strings are the raw signature.


| core (w files) | origin | phase | L=4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| B5 W2B5 W35B6 | NNPNNNNN (L=5) | 0 | R-all | *2 | R-all | *2 | R-all | *2 | R-all | *2 | R-all | *2 | R-all | *2 | R-all |
| B5 W2B5 W35B6 | NNPNNNNN (L=5) | 1 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 |
| B7 W3B6 W34B67 W4 | NNPNNNNN (L=5) | 0 | NRRRRRRR | *2 | NRRRRRRR | *2 | NRRRRRRR | *2 | NRRRRRRR | *2 | NRRRRRRR | *2 | NRRRRRRR | *2 | NRRRRRRR |
| B7 W3B6 W34B67 W4 | NNPNNNNN (L=5) | 1 | NRRRRRRR | R-all | NNRRRRRR | R-all | NNRRRRRR | R-all | *2 | NRRRRRRR | *2 | NRRRRRRR | *2 | NRRRRRRR | *2 |
| W2 B5 W2B5 W35B6 | NNPNNNNN (L=4) | 0 | *2 | L-all | *2 | L-all | *2 | L-all | *2 | L-all | *2 | L-all | *2 | L-all | *2 |
| W2 B5 W2B5 W35B6 | NNPNNNNN (L=4) | 1 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 | N8 |
| W2 W35B6 W2B5 B5 | NNPNNNNN (L=4) | 0 | *2 | L-all | *2 | L-all | *2 | L-all | *2 | L-all | *2 | L-all | *2 | L-all | *2 |
| W2 W35B6 W2B5 B5 | NNPNNNNN (L=4) | 1 | L-all | R-all | L-all | R-all | L-all | R-all | L-all | R-all | L-all | R-all | L-all | R-all | L-all |
| W26B7 W2 W3B7 B5 | NNPNNNNN (L=4) | 0 | *2 | L-all | *2 | L-all | *2 | L-all | *2 | L-all | *2 | L-all | *2 | L-all | *2 |
| W26B7 W2 W3B7 B5 | NNPNNNNN (L=4) | 1 | N8 | RNRRRRRR | N8 | RNRRRRRR | N8 | RNRRRRRR | N8 | RNRRRRRR | N8 | RNRRRRRR | N8 | RNRRRRRR | N8 |
| W2B46 W4B6 W3B7 | NNPNNNNN (L=5) | 0 | R-all | *2 | R-all | *2 | R-all | *2 | R-all | *2 | R-all | *2 | R-all | *2 | R-all |
| W2B46 W4B6 W3B7 | NNPNNNNN (L=5) | 1 | RNRRRRRR | R-all | RNRRRRRR | R-all | RNRRRRRR | R-all | NNRRRRRR | R-all | NNRRRRRR | R-all | NNRRRRRR | R-all | NNRRRRRR |
| W4B7 W2B6 W2B7 | NNNR.... (L=4) | 0 | NNNRRRRR | LNLLLLLL | LNNNNNNN | LNLLLLLL | LNNNNNNN | LNLLLLLL | LNNNNNNN | LNLLLLLL | LNNNNNNN | LNLLLLLL | LNNNNNNN | LNLLLLLL | LNNNNNNN |
| W4B7 W2B6 W2B7 | NNNR.... (L=4) | 1 | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all |
| W4B7 W3B6 W2B7 | NNPNNNNN (L=4) | 0 | *2 | NLLLLLLL | NNLLLLLL | NLLLLLLL | NNLLLLLL | NLLLLLLL | NNLLLLLL | NLLLLLLL | NNLLLLLL | NLLLLLLL | NNLLLLLL | NLLLLLLL | NNLLLLLL |
| W4B7 W3B6 W2B7 | NNPNNNNN (L=4) | 1 | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all | R-all |


Reading: every *2 core stays *2 for a whole arithmetic progression of wall lengths (period 2 in L, up to n = 18-20), as in the P_n family; the wall length never produces a *3 or a *4 and the signature NNNR of the near miss occurs only for L=4.


## 6. SUPPLEMENTARY local search (not part of the requested enumeration)

Because the wall-closure family contains *2 but no *3, I used the leftover time for a one-pawn local search around the hits: from every ring with first-non-N index >= 2 (the 7 *2 rings and the near miss), apply every single move (shift a pawn one rank, delete a pawn, add a pawn on any file, W ranks 2..6, B ranks 3..7), keep rings with no passed pawn, canonicalise under rotation/reflection, evaluate with `rgq solvef 7`, and continue from every new ring with first-non-N index >= 2 (`nbr.py`, depth 3); then a second round whose frontier is restricted to rings with first-non-N index >= 3, i.e. the *3 and near-*4 rings (`nbr2.py`; it was stopped by PID at the time cap during depth 3, so only depths 1 and 2 are complete and the depth-3 batch is lost). These moves can change the wall, so the rings leave the family.
- Round 1 log: `depth 1: evaluated 472 new rings (total 472), frontier 17 / depth 2: evaluated 1321 new rings (total 1793), frontier 77 / depth 3: evaluated 5742 new rings (total 7535), frontier 197 / signature counts (first non-N >= 1 or P): {'NLLLLLLL': 152, 'NNPNNNNN': 122, 'NRRRRRRR': 103, 'PNNNNNNN': 103, 'NNRRRRRR': 100, 'RNRRRRRR': 91, 'RNNNNNNN': 78, 'LNLLLLLL': 71, 'NPNNNNNN': 59, 'NRNNNNNN': 45, 'NNLLLLLL': 39, 'LNNLLLLL': 39, 'LNNNNNNN': 31, 'NLNNNNNN': 23, 'NLNLLLLL': 10, 'NNNPNNNN': 9, 'NNNLLLLL': 7, 'NNRNNNNN': 7, 'NNLNNNNN': 6, 'RNNRRRRR': 2, 'NRRNRRRR': 1, 'NRNRRRRR': 1, 'NNNRNNNN': 1}`
- Round 2 log: `depth 1: evaluated 1518 new rings (total 1518), frontier 11 / depth 2: evaluated 900 new rings (total 2418), frontier 34 / depth 3 aborted at the time cap (first batch of 3000 rings did not finish in 10 min); depth 1 and 2 are complete`
- Distinct rings with signature NNNPNNNN (*3): **41**. Distinct rings with NNNNPNNN (*4): **0**. Near-*4 non-nimber signatures seen (count of rings): {'NNNLLLLL': 15, 'NNNRNNNN': 1, 'NNNLNNNN': 5}.

The *3 rings found (canonical rotation/reflection, n = number of tokens):

| n | ring | first seen |
|---|---|---|
| 9 | `- - W2B4 W4 W34B67 W3B6 B7 W2 W3B4` | depth2 |
| 9 | `- B5 W2 W4 W34B67 W3B6 B7 W2 W3B4` | depth3 |
| 9 | `- B5 W2 W4 W34B67 W3B6 B7 W2 W3B45` | depth1 |
| 9 | `- B5 W2 W4 W34B67 W3B6 B7 W2 W3B456` | depth2 |
| 9 | `- W2 B4 W2 B7 W3B6 W34B67 W4 W2B4` | depth3 |
| 9 | `- W2 W3B4 W2 B7 W3B6 W34B67 W4 W2B4` | depth1 |
| 9 | `- W2 W3B4 W2B5 B7 W3B6 W34B67 W4 W2B4` | depth2 |
| 9 | `- W2 W3B45 W2 B7 W3B6 W34B67 W4 W2B4` | depth2 |
| 9 | `- W2B3 W3B4 W2 B7 W3B6 W34B67 W4 W2B4` | depth2 |
| 9 | `- W2B4 W4 W34B67 W3B6 B7 W2 W3B4 W2B5` | depth2 |
| 8 | `- W3B4 W2 B5 W2B5 W35B6 W2B3 W3B5` | depth2 |
| 9 | `- W3B4 W2 B7 W3B6 W34B67 W4 - W3B5` | depth2 |
| 9 | `- W3B4 W2 B7 W3B6 W34B67 W4 W2B3 W3B5` | depth2 |
| 8 | `- W3B4 W2 W35B7 W2B5 B5 W2B5 W3B4` | depth2 |
| 9 | `- W3B5 W2 B4 W2 B7 W3B6 W34B67 W4` | depth3 |
| 8 | `- W3B5 W2 B4 W2 W2B46 W4B6 W3B7` | depth3 |
| 9 | `- W3B5 W2 W3B4 W2 B7 W3B6 W34B67 W4` | depth1 |
| 9 | `- W3B5 W2 W3B4 W2B5 B7 W3B6 W34B67 W4` | depth2 |
| 9 | `- W3B5 W2 W3B45 W2 B7 W3B6 W34B67 W4` | depth2 |
| 9 | `- W3B5 W2B3 W3B4 W2 B7 W3B6 W34B67 W4` | depth2 |
| 8 | `B4 W2 B5 W2B5 W35B6 W2B3 W3B5 W2` | depth3 |
| 9 | `B4 W2 B7 W3B6 W34B67 W4 W2B3 W3B5 W2` | depth3 |
| 8 | `B4 W2 W2B46 W4B6 W3B7 W2B3 W3B5 W2` | depth3 |
| 8 | `B4 W2 W35B7 W2B5 B5 W2B5 W3B4 W2` | depth3 |
| 8 | `B4 W2 W35B7 W2B5 B5 W2B5 W3B4 W24B5` | depth2 |
| 8 | `B4 W2 W35B7 W2B5 B5 W2B5 W3B4 W2B5` | depth1 |
| 8 | `B5 W2 W3B4 W2 W3B5 W2B3 W35B6 W2B5` | depth1 |
| 8 | `B5 W2 W3B4 W2B3 W3B5 W2B3 W35B6 W2B5` | depth2 |
| 8 | `B5 W2 W3B45 W2 W3B5 W2B3 W35B6 W2B5` | depth2 |
| 9 | `B5 W2 W4 W34B67 W3B6 B7 W2 W3B4 W2B3` | depth3 |
| 9 | `B5 W2 W4 W34B67 W3B6 B7 W2 W3B45 W2B3` | depth1 |
| 9 | `B5 W2 W4 W34B67 W3B6 B7 W2 W3B456 W2B3` | depth2 |
| 8 | `B5 W2B5 W35B6 W2B3 W3B5 W2 W3B4 W2B5` | depth2 |
| 8 | `B5 W2B5 W35B7 W2 W3B4 W2 W3B4 W2B5` | depth1 |
| 8 | `B5 W2B5 W35B7 W2 W3B4 W2B3 W3B4 W2B5` | depth2 |
| 8 | `B5 W2B5 W35B7 W2 W3B4 W2B5 W3B4 W2B5` | depth2 |
| 8 | `B5 W2B5 W35B7 W2 W3B45 W2 W3B4 W2B5` | depth2 |
| 9 | `B7 W2 W3B4 W2 W3B5 W2B3 W4 W34B67 W3B6` | depth1 |
| 9 | `B7 W2 W3B4 W2B3 W3B5 W2B3 W4 W34B67 W3B6` | depth2 |
| 9 | `B7 W2 W3B45 W2 W3B5 W2B3 W4 W34B67 W3B6` | depth2 |
| 9 | `B7 W2B5 W3B4 W2 W3B5 W2B3 W4 W34B67 W3B6` | depth2 |

Structure (by eye, on the first few rings): the *3 rings look like a *2 core of the enumeration plus a small attached group, e.g. `B4 W2 B5 W2B5 W35B6 W2B3 W3B5 W2` is the *2 ring `B5 W2B5 W35B6 W2 B4 W2 B4 W2` with the W2/B4 wall tail replaced by a W2B3 / W3B5 pair, in line with the flat-board finding (every *3 = *2 core + *1 group, research/star4_hunt/REPORT.md). These rings are NOT in the requested family and are listed only as leads; all 41 were re-evaluated with the unmodified rg (MAXN=64, solve 7): 0 disagreements. The structural reading above was checked by eye on the first few rings only.


## 7. Verification and caveats

- **Engine equivalence.** 2,405 rings (every (w,p,L,phase) cell, 40 draws each, plus the 5 known rings) and their 2,405 mirror images (4,810 positions): unmodified `rg solve 7` (MAXN=64, batches of 40, line counts checked) against `rgq solvef 7` (full signature): 0 differences; against `rgq solveq 7` (early stop, tail rule applied): 0 differences; mirror images: 0 differences (`val/`).
- **Hits.** `verify_hits.py` re-evaluated all 2,071 distinct HIT rings (examples of *0, *1, *2 and every ring with first-non-N index >= 3) with the unmodified rg: 0 disagreements (`verify_hits.out`).
- **Exhaustive histograms** from `cwq` equal those of the separate `gen | rgq` pipeline on three test cells (`qt/`).
- **TABLEFULL.** 23 rings overflowed the 2^21-entry table (w=5 p=9 L=5 ph0: 3, w=6 p=9: 2, w=6 p=10: 18); `retry_in.txt` re-run with `TBITS=24 rgq solvef 7`: all 23 are NNNNNNNN (`retry_out.txt`), already folded into the tables.
- **Not established.** (a) The sampled layers (w=4 p=8 except L=5 ph1, w=5 p=8, 9, w=6 p=8, 9, 10) are samples of 0.007% to 4% of their layers, so *3/*4 rings can exist there; the yield of *2 is about 1 in 3 million even in the exhaustive layers, so samples of this size could not have seen one. (b) "allN" does not separate non-nimbers from nimbers >= *8. (c) Cores of w > 6, walls other than alternating W2/B4 of length 4 or 5, and p > w+4 are not covered. (d) The whole-board model is used throughout (the e.p. flag is cleared by any move), as in rg.c.
- Two process-handling slips, both harmless: while shortening round 2 I rewrote `jobs.txt` under running workers (they kept reading the old inode), so I stopped them with a STOP file and restarted; two sample jobs were then run twice with the same seed (the duplicate output is kept in `dup/` and excluded from all tables), and one more duplicate pair was pre-claimed so it never ran.

## 8. Commands
```
cd research/star4_rings/core_wall
cp ../../ring_family_proof/rg.c rg.c && cc -O2 -DMAXN=64 -o rg rg.c -lpthread        # reference engine (verification)
cc -O2 -o gen gen.c; cc -O2 -o samp samp.c                                         # generator (count/emit) and DP-uniform sampler
cc -O2 -o rgq rgq.c -lpthread; cc -O2 -o cwq cwq.c -lpthread                       # fast engine; engine + generator + queue
./gen W P L PH count                                                               # number of cores of one (w,p,L,phase) cell
python3 - (script in this session) > jobs.txt                                      # 106 job lines: ID E W P L PH SHARD NSHARDS | ID S W P L PH N SEED
for k in 1 2; do JOBMAXSEC=1800 TBITS=21 nohup nice -n 15 ./cwq queue jobs.txt out 7200 & done   # 2 workers; touch out/STOP to end
python3 report_tables.py > tables.md                                               # tables (reads out/*.res, retry_out.txt)
cat out/*.retry | sort -u > retry_in.txt; TBITS=24 nice -n 15 ./rgq solvef 7 < retry_in.txt > retry_out.txt
python3 verify_hits.py > verify_hits.out                                           # unmodified rg on every HIT ring
python3 walls.py 2 16 > walls_results.tsv                                          # longer walls, n <= 20
python3 nbr.py 3 60000 > nbr_results.tsv 2> nbr_err.txt; python3 nbr2.py 3 20000 > nbr2_results.tsv 2> nbr2_err.txt   # supplementary
python3 make_report.py                                                             # this file
```
Single positions: `echo "W4B7 W3B6 W2B7 W2 B4 W2 B4" | ./rg solve 7`.

## 9. Files
`out/*.res` (per-job histograms, HIT lines, #DONE), `jobs.txt`, `tables.md`, `walls_results.tsv`, `walls_table.md`, `nbr_results.tsv`, `nbr2_results.tsv`, `verify_hits.out`, `retry_*.txt`, `val/` (engine validation), `qt/` (queue test), `dup/` (excluded duplicate jobs), sources `cwq.c rgq.c rg.c gen.c samp.c`, scripts `report_tables.py walls.py nbr.py nbr2.py verify_hits.py summarize.py make_report.py`.
