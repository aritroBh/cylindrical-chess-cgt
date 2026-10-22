# T44: KPKP on the cylinder and the ordinary board (Sonnet, after Kilo walled its free tier)

Saved by the orchestrating session on 2026-10-22. The verifier's findings come first and take precedence.

## Verifier verdict: ACCEPT_WITH_FIXES

5-LINE SUMMARY
1. I could not refute T44. My own numpy code, written separately from the agent's analyze_t44.py, re-parsed all 8 .zst chunks and reproduced every headline count exactly (COMPUTED-1): legal sets, W/D/L/bound tables, exact shares, cylinder-vs-flat flips, and the mutual-zugzwang (MZ) counts including the 576 cylinder-only pairs (set-identical to mz_cyl_only.tsv.zst).
2. The old research/kpkp/*.out.zst are confirmed not KPKP: enumerate.c lines 66 and 70 print the Black pawn as 'P', and `zstdcat kpkp_cyl.in.zst | grep -c ' p[a-h][1-8]'` gives 0 (same for flat and kppk_flat).
3. CHECKED-2: kings/ref/solve.py (cap 1, both bounds) agreed with the tables on 64/64 positions per board that I chose myself (128/128). They include all 18 example positions E1-E8, 12 exact cyl-vs-flat flips, 12 positions from 6 cylinder-only MZ pairs the agent had not tested, and 24 random seam-file positions (some only bounded). F1/F2 also agree on both boards (4/4). Separately, all 740 ref lines in the agent's check_{cyl,flat}_G{1,2,3}.out match my tables (740/740).
4. Extra checks beyond the brief. Flat table vs the Lichess tablebase: 40/40 new exact positions agree, plus 6 cached KPkp positions consistent (3 exact matches, 3 inside the bounds); this covers the flat board only. A full kpsolve --cap 0 run of both boards nests inside the cap-1 table with 0 violations over 29.5M positions.
5. Verdict ACCEPT_WITH_FIXES. No number changes. Four wording fixes are needed: state the denominators and the exact-vs-exact scope of the flip percentages, scope the CHECKED-2 label to the sample, do not compare 992 with 452 MZ pairs as totals, and give the unit (pair vs position) of MZ counts (details under problems).

WHAT I RECOMPUTED (own code, not the agent's)
- File integrity (COMPUTED-1). All 8 chunks have exactly 26-byte lines. Zero X results, zero duplicate positions, and A >= B on every line. An independent numpy enumeration of legal KPKP positions gives 7,314,800 per side to move on the cylinder and 7,436,088 on the flat board. The sets are identical to the files (0 mismatches either side). The .err files give 2745 layers, 224,796,672 states, depth 8, 230.5-261.5 s per chunk, as claimed.
- Mirror symmetry (flip ranks, swap colours, swap side to move, (A,B) -> (-B,-A)): 0 missing, 0 differing on both boards, both directions. This is one program checking itself.
- Cylinder-vs-flat pairing (COMPUTED-1). Every cylinder-legal position is flat-legal. 121,288 flat-only positions per side to move (242,576 in total) have no cylinder twin. Per side to move: 5,405,002 same-exact, 621,024 exact-and-different, 12,852 certainly different with an inexact side, 1,275,922 undecided. Flat-to-cylinder flips, White to move: W>D 253,270, L>D 204,130, D>W 84,520, L>W 38,812, D>L 23,096, W>L 17,196. All agree.
- MZ (COMPUTED-1). Certain pairs: cylinder 992 (L,D 456, L,W 80, D,W 456), flat 452 (196/60/196). Both 416, cylinder-only 576 (278 L,D / 20 L,W / 278 D,W), flat-only 36. Possible-but-uncertain pairs: cylinder 223,640, flat 589,864. Cylinder-certain with flat uncertain: 0. Cylinder-only with the pawns on files a and h: 60. All 20 strict cylinder-only pairs are the four locked-pawn patterns Ka3/Ph2/kg2/ph3, Kb3/Pa2/kh2/pa3, Kg3/Ph2/ka2/ph3, Kh3/Pa2/kb2/pa3, each shifted over 5 rank positions. E1-E6 are all in the cylinder-only MZ list. E7 (L/L) and E8 (W/L) are race examples, not MZ, which matches the report's wording.
- Percentages recomputed. Cylinder 40.74/27.97/20.42 and 10.86 inexact; flat 40.17/22.22/21.09 and 16.51 inexact; exact shares 89.14% and 83.49%. The per-column sums close: 6,520,144 + 794,656 = 7,314,800; 6,208,032 + 1,228,056 = 7,436,088.
- Strata. 4,902,552 cylinder and 4,978,268 flat positions (33.51%) lie in the three sampling strata. By stratum: G1 (files a/h) 5.85%, G2 13.83%, G3 13.83%, all as cylinder shares.
- Examples. I regenerated every FEN (E1, E1b, E2-E8, F1, F2) from the position strings: all match. The cyl/flat values in the report's example table match both the big tables and the --moves listings (examples_{cyl,flat}.out, examples2_*.out). The per-example move narratives match the listings.

TABLE FOR A PAPER (White to move; Black to move is the colour-swapped mirror; COMPUTED-1)
Board | legal | White wins | Draws | Black wins | bounds differ
Cylinder 8x8 | 7,314,800 | 2,980,368 (40.74%) | 2,045,768 (27.97%) | 1,494,008 (20.42%) | 794,656 (10.86%)
Flat 8x8 | 7,436,088 | 2,987,432 (40.17%) | 1,652,522 (22.22%) | 1,568,078 (21.09%) | 1,228,056 (16.51%)
Exact: 89.14% (cylinder), 83.49% (flat). Pairs of identical squares, White to move: same-exact 5,405,002; exact-and-different 621,024; undecided 1,275,922.
Certain MZ pairs: cylinder 992, flat 452, cylinder-only 576 (20 strict). These are lower bounds (possible-only pairs: 223,640 and 589,864).

EXAMPLES (FEN, cylinder rules; values White to move / Black to move; labels: CHECKED-2 by kpsolve and ref, re-solved by me with ref for E1-E8, F1, F2)
E1 8/p7/8/7P/8/3k4/8/3K4 w - - 0 1: cyl L/D, flat W/W (MZ, pawn race frozen by the seam)
E1b 8/7p/8/P7/8/4k3/8/4K3 w - - 0 1: cyl L/D, flat W/W
E2 8/8/8/8/8/K6p/6kP/8 w - - 0 1: cyl L/W strict MZ, flat L/L
E3 8/8/8/8/8/pK6/P6k/8 w - - 0 1: cyl L/W strict MZ, flat W/W
E4 7k/p6P/K7/8/8/8/8/8 w - - 0 1: cyl D/W, flat D/D
E5 8/1k6/p6P/K7/8/8/8/8 w - - 0 1: cyl D/W, flat W/W
E6 8/8/8/8/8/7k/p6P/K7 w - - 0 1: cyl L/D, flat D/D
E7 8/8/p7/8/7P/4k3/8/4K3 w - - 0 1: cyl L/L, flat W/D (race frozen by the seam)
E8 4k3/8/8/3K4/8/p7/7P/8 w - - 0 1: cyl W/L, flat L/L (hxa3 across the seam)
F1 8/8/8/8/1p6/8/P7/K1k5 w - - 0 1: cyl D, flat L
F2 8/8/8/8/7p/k3K2P/8/8 w - - 0 1: cyl L, flat D

REPRODUCE (my files are in the scratchpad, not in t44; S = /private/tmp/claude-501/-Users-aritro-Downloads-Research-Chessendgames/57318271-9bbf-42b4-b8cf-b9d442308061/scratchpad)
- Headline recompute: cd $S && nice -n 15 /Users/aritro/Downloads/Research/Chessendgames/.venv-ml/bin/python -I recompute.py (output recompute.out, recompute.json, cyl_only_mine.txt)
- Set equality with the agent's TSV: zstdcat research/kpkp/t44/mz_cyl_only.tsv.zst | tail -n +2 | awk -F'\t' '{print $1" "$2" "$3" "$4}' | sort | diff - <(sort $S/cyl_only_mine.txt)
- Own ref re-solve: $S/t44v/select_inputs.py makes in_cap1.txt and exp_cap1_{cyl,flat}.txt; then PYTHONPATH=. .venv/bin/python -m kings.ref.solve --board cyl:8x8 --ep on --promote QRBN --cap 1 < $S/t44v/in_cap1.txt (also flat). Do not pass -I there, because it drops PYTHONPATH and the module is not found.
- Agent's ref outputs vs my tables, and cached Lichess: $S/t44v/checks2.py
- Lichess probe (40 new requests, ledger t44v/lichess_ledger.jsonl): $S/t44v/lichess40.py
- Cap-0 full run: $S/t44v/run_cap0.sh; nesting check: $S/t44v/nesting.py
- Cap-0 sample: kings/kpsolve --board cyl:8x8 --ep on --promote QRBN --cap 0 < $S/t44v/u0_cyl.in, compared with check_cyl_U0.out
- Old-data bug: zstdcat research/kpkp/kpkp_cyl.in.zst | grep -c ' p[a-h][1-8]'

Resource note: at most 2 processes of mine at a time, nice -n 15, no kill or git commands, nothing written inside research/kpkp/t44 or paper/. The 40 Lichess requests are within the 200 allowance and added cache files under realchess/cache by design.

### Fixes and problems found by the verifier

- Wording, scope of the flip percentages: '621,024 per side to move (8.49%)' has no denominator. It is 8.49% of all 7,314,800 paired positions, but 10.3% of the 6,026,026 pairs that are exact on both boards (82.4% of all pairs). The six flip counts, including the 'most flips make the cylinder drawish' statement (73.7% of exact flips end in a cylinder draw: W>D plus L>D is 457,400 of 621,024), only describe exact-vs-exact pairs. The other 17.6% of pairs (1,275,922 undecided and 12,852 certainly different with an inexact side) could change the direction split. Say 'among exact-vs-exact pairs' in the paper.
- Wording, scope of CHECKED-2: the cap-1 second-program sample is random only inside three pawn-file strata that hold 33.5% of positions (G1 5.85%, G2 13.83%, G3 13.83%), so no positions with the pawns on, for example, c/a, or e/e are cap-1-checked by the agent. The cap-0 sample is uniform, but it is not a check of the cap-1 table values, and only about 11% of cap-0 positions are exact (cylinder 780,728 of 7,314,800 per side), so it mostly compares bound pairs. Label the table counts as COMPUTED-1 supported by a sampled second-program check (n=370 cap-1 stratified, n=340 cap-0 uniform per board), and keep CHECKED-2 for the individually re-solved examples. The report text is already honest about the strata. The risk is only that 'CHECKED-2, 0 disagreements' in the summary is read as covering the tables. My extra 64 per board (G1 only) and the flat Lichess check do not change this scope.
- Wording, MZ totals: 992 (cylinder) vs 452 (flat) are lower bounds, and the flat board has far more undetermined pairs (589,864 against 223,640 on the cylinder). The pair '992 vs 452' therefore does not show that the cylinder has more mutual zugzwangs than the flat board. Only the cylinder-only count (576) is a solid comparison, because for those the flat pair is certainly not an MZ (and 0 cylinder-certain pairs have an uncertain flat status). Also state the unit: counts are pairs, so 2 positions each (1,984 cylinder and 904 flat positions), whereas the brief says 'count positions'.
- Minor: the position set excludes positions with a pending e.p. right (target '-'), so 'all legal KPKP positions' is relative to that. The report says so in Settings, but the paper table should say it too. The reported counts also include retrograde-unreachable placements, as usual for tablebase counts.
- Minor: the report does not mention that the flat table can be checked against the Lichess tablebase, which is the only external ground truth available. I did it (40/40 plus 6 cached); the report should add it as flat-only external support. Nothing external exists for the cylinder.
- Minor/transparency: 'the first launch of the cap-1 chains vanished silently, cause unknown' may be related to the documented 2026-10-22 pkill -f 0 incident in COMMON.md, but I cannot establish that. Results come from the rerun and agree with my recomputation.

## Agent report (verbatim)

**5-line summary**
1. The existing `research/kpkp/kpkp_{cyl,flat}.out.zst` are not KPKP. `enumerate.c` wrote the Black pawn as `P`, so every line is K+2 White pawns v K (COMPUTED-1: `zstdcat kpkp_cyl.in.zst | grep -c ' p[a-h][1-8]'` gives 0). That is why they hold only W/D/X and no Black wins; `XX` means illegal input (White to move while a second White pawn attacks the Black king). The old `kppk_*` inputs have the same bug (K+3P v K). I did not use those files; every number below comes from a fresh solve of the 8×8 boards.
2. I enumerated all legal KPKP positions with the black pawn as `p`. That gives 14,629,600 positions on the cylinder and 14,872,176 on the flat board. I solved both with `kings/kpsolve --ep on --promote QRBN --cap 1`, in 4 streamed chunks of 71–77 MB per board.
3. Exact (A==B) results cover 89.14% of cylinder positions and 83.49% of flat ones. The rest are bounded only (the second promotion is capped). Exact values are true values of the unrestricted game (COMPUTED-1).
4. Cylinder against flat, on identical squares: 1,242,048 exact-versus-exact positions differ. Most flips make the cylinder drawish: flat win to cylinder draw is 253,270 against 84,520 the other way, per side to move. Certain mutual-zugzwang pairs number 992 on the cylinder and 452 on the flat board; 576 are cylinder-only, and 20 of those are strict (whoever moves loses).
5. Second program (`kings/ref/solve.py`), CHECKED-2, 0 disagreements. Cap-1 sample: 370 positions per board, including 40 positions from 20 cylinder-only mutual-zugzwang pairs, and 24 example positions. Cap-0 sample: 340 per board, 300 of them uniform over the whole board. The cap-1 sample is random only inside pawn-file strata that cover about 33.5% of positions.

**1. Settings**
- Command: `kings/kpsolve --board {cyl|flat}:8x8 --ep on --promote QRBN --cap 1`.
- Cap 1 means at most one officer in total, both colours together. A second promotion is a capped promotion: bound A scores it a White win, bound B a Black win.
- Every chunk run reported the same layer count: 2745 layers, 224,796,672 states, depth 8, 230–262 s wall under load, "capped promotions met (two bounds)".
- The old (invalid) runs reported 1373 layers and 112,402,432 states, half as many, as expected without a Black pawn.
- Position set: every legal placement of K, P, k, p with both pawns on ranks 2–7 and the e.p. field `-`. Positions with a live e.p. right pending are not enumerated, though the solver plays e.p. inside the game.
- `kpsolve` accepted every enumerated line, with no `X` in the output.
- Exact positions: cylinder 6,520,144 per side to move (13,040,288 of 14,629,600); flat 6,208,032 per side to move (12,416,064 of 14,872,176).

**2. Statistics** (COMPUTED-1)

| Board | To move | Legal | White wins | Draws | Black wins | Bounds differ (W/L, W/D, D/L) |
|---|---|---|---|---|---|---|
| Cylinder | White | 7,314,800 | 2,980,368 (40.74%) | 2,045,768 (27.97%) | 1,494,008 (20.42%) | 794,656 (10.86%): 534,600 / 173,848 / 86,208 |
| Cylinder | Black | 7,314,800 | 1,494,008 (20.42%) | 2,045,768 (27.97%) | 2,980,368 (40.74%) | 794,656: 534,600 / 86,208 / 173,848 |
| Flat | White | 7,436,088 | 2,987,432 (40.17%) | 1,652,522 (22.22%) | 1,568,078 (21.09%) | 1,228,056 (16.51%): 714,434 / 306,856 / 206,766 |
| Flat | Black | 7,436,088 | 1,568,078 (21.09%) | 1,652,522 (22.22%) | 2,987,432 (40.17%) | 1,228,056: 714,434 / 206,766 / 306,856 |

"W/L" means bound A is W and bound B is L, so the true value is undecided. Each table is exactly mirror-symmetric under flipping ranks, swapping colours and swapping the side to move. I checked this position by position for all 14,629,600 cylinder and 14,872,176 flat positions: 0 missing, 0 differing (`symmetry_check.out`). It is a consistency check of one program.

**Cylinder against flat** (pair = same squares, same side to move; shown for White to move, and Black to move is the colour-swapped mirror):
- All 14,629,600 cylinder-legal positions are also flat-legal. 242,576 flat-legal positions have no cylinder twin, because they involve a king adjacency or pawn attack across the seam.
- Both boards exact and equal: 5,405,002 per side to move.
- Both exact and different: 621,024 per side to move (8.49%), 1,242,048 in total.
- Certainly different, with one board only bounded: 12,852 per side to move. Undecided (an inexact side overlaps): 1,275,922 per side to move.

| Flat to cylinder (White to move) | Positions |
|---|---|
| W to D | 253,270 |
| W to L | 17,196 |
| D to W | 84,520 |
| D to L | 23,096 |
| L to D | 204,130 |
| L to W | 38,812 |

**3. Mutual zugzwangs** (COMPUTED-1 for the counts)
- Definition: for the same squares, the value v_w with White to move is below v_b with Black to move, in White's view with L<D<W. The mover does worse than the other side would, and the condition is the same for both sides.
- "Certain" means the upper bound of v_w is below the lower bound of v_b. These counts are lower bounds. Pairs where an unresolved value could still make one: cylinder 223,640, flat 589,864.
- Each pair is 2 positions.

| Board | Certain pairs | (L,D) | (L,W), strict | (D,W) |
|---|---|---|---|---|
| Cylinder | 992 | 456 | 80 | 456 |
| Flat | 452 | 196 | 60 | 196 |

- Pairs in both: 416. Cylinder-only (cylinder certain, flat certainly not): 576 (278 L/D, 278 D/W, 20 strict). Flat-only: 36.
- 60 of the 576 cylinder-only pairs have the pawns on files a and h, one each.
- All 20 strict cylinder-only pairs are the same four locked-pawn patterns shifted over ranks 2–7, with the kings straddling the seam.
- Full list: `mz_cyl_only.tsv.zst`.

**Examples** (all CHECKED-2). FENs are placement plus side only, and cylinder rules are assumed. Values are (White to move / Black to move) from White's view; "cyl" is the cylinder and "flat" the ordinary board.

| ID | Position | FEN | cyl | flat |
|---|---|---|---|---|
| E1 | Kd1 Ph5 kd3 pa7 | `8/p7/8/7P/8/3k4/8/3K4 w - - 0 1` | L / D | W / W |
| E1b | Ke1 Pa5 ke3 ph7 (mirror of E1) | `8/7p/8/P7/8/4k3/8/4K3 w - - 0 1` | L / D | W / W |
| E2 | Ka3 Ph2 kg2 ph3 | `8/8/8/8/8/K6p/6kP/8 w - - 0 1` | L / W | L / L |
| E3 | Kb3 Pa2 kh2 pa3 | `8/8/8/8/8/pK6/P6k/8 w - - 0 1` | L / W | W / W |
| E4 | Ka6 Ph7 kh8 pa7 | `7k/p6P/K7/8/8/8/8/8 w - - 0 1` | D / W | D / D |
| E5 | Ka5 Ph6 kb7 pa6 | `8/1k6/p6P/K7/8/8/8/8 w - - 0 1` | D / W | W / W |
| E6 | Ka1 Ph2 kh3 pa2 | `8/8/8/8/8/7k/p6P/K7 w - - 0 1` | L / D | D / D |
| E7 | Ke1 Ph4 ke3 pa6 | `8/8/p7/8/7P/4k3/8/4K3 w - - 0 1` | L / L | W / D |
| E8 | Kd5 Ph2 ke8 pa3 | `4k3/8/8/3K4/8/p7/7P/8 w - - 0 1` | W / L | L / L |
| F1 | Ka1 Pa2 kc1 pb4 | `8/8/8/8/1p6/8/P7/K1k5 w - - 0 1` | D / (not listed) | L / (not listed) |
| F2 | Ke3 Ph3 ka3 ph4 | `8/8/8/8/7p/k3K2P/8/8 w - - 0 1` | L / (not listed) | D / (not listed) |

What `--moves` shows for each:
- **E1, E7: pawn race frozen by the seam.** The h-pawn guards a6, the e.p. square included, and the a-pawn guards h6. On the flat board the h-pawn simply wins the race.
  - E1: with White to move all 3 moves lose (Kc1, Ke1, h6). With Black to move the five king moves draw and both pawn moves lose.
  - E7: with White to move Kf1, Kd1 and h5 all lose.
- **E2, E3: strict mutual zugzwang.** The locked pawns sit on the seam file, and a king across the seam protects or attacks them.
  - E2: all 5 moves lose for each side.
  - E3: all 5 moves lose for each side.
  - On the flat board Kxh2 is legal in E2, which is why it is not a mutual zugzwang there.
- **E4:** with Black to move the only move is Kg7, which loses. h8 and a7 are adjacent across the seam. With White to move Kb7 loses and the other three moves draw.
- **E5:** with Black to move all five king moves lose. With White to move all four moves draw.
- **E6:** the Black king on h3 guards a2 across the seam, so White's only move is Kb2, which loses.
- **E8:** hxa3 across the seam wins at once. On the flat board the a-pawn queens first.
- **F1:** the king escapes through the seam (Kh1, Kh2 draw). On the flat board only losing pawn moves exist.
- **F2:** the Black king on a3 attacks the White pawn on h3 across the seam.

**4. Second-program checks** (CHECKED-2; 0 disagreements; both bounds A and B compared)
- **Cap 1** (same settings as the table, expected values from the tables). There are 330 random positions per board, 110 in each stratum (white-pawn file / black-pawn file):
  - G1: a,h / a,h
  - G2: b,d,g / b,e,g
  - G3: c,e,f / c,d,f
- The three strata hold 4,902,552 cylinder positions and 4,978,268 flat positions.
- Why strata: the reference solver is pure Python and needs about 5 s per officer layer. A uniform sample over all files needs about 400 layers per board.
- Result: cylinder 370/370 and flat 370/370, counting the 40 mutual-zugzwang positions (20 cylinder-only pairs). The flat board is checked on the same squares.
- **Cap 0** (promotions terminal; expected values from a fresh `kpsolve --cap 0`): 300 positions uniform over the whole board plus the 40 mutual-zugzwang positions. Cylinder 340/340, flat 340/340.
- **Examples:** E1–E8 give 18/18 on each board, and F1–F2 plus four other flips give 6/6 on each board.
- Job times were 568–920 s each.
- The first launch of the cap-1 chains vanished silently; I did not kill it and the cause is unknown. I relaunched it detached, and the numbers above are from the rerun.

**Reproduce** (from `/Users/aritro/Downloads/Research/Chessendgames`; run the solves and checks at most 2 at a time, under `nice -n 15`)
```
cc -O2 -o research/kpkp/t44/enum_kpkp research/kpkp/t44/enum_kpkp.c
research/kpkp/t44/run_solve.sh cyl      # and: flat   (about 4.5 min per chunk, 4 chunks)
.venv/bin/python -I research/kpkp/t44/analyze_t44.py          # stats.json, mz_cyl_only.tsv.zst, samples
.venv/bin/python -I research/kpkp/t44/symmetry_check.py
.venv/bin/python -I research/kpkp/t44/make_checks.py ; .venv/bin/python -I research/kpkp/t44/make_checks_g3.py
PYTHONPATH=. .venv/bin/python -I research/kpkp/t44/run_checks.py cyl_G1 cyl_G2 cyl_G3 cyl_U0   # and: flat_*
kings/kpsolve --board cyl:8x8 --ep on --promote QRBN --cap 1 --moves < research/kpkp/t44/examples.in
PYTHONPATH=. .venv/bin/python -I research/kpkp/t44/check_examples.py cyl examples   # also: flat, examples2
zstdcat research/kpkp/kpkp_cyl.in.zst | grep -c ' p[a-h][1-8]'   # bug evidence: 0
```

**Notes**
- Do not use `research/kpkp/analyze_kpkp.py` or `analyze_full.py`. They read the invalid data, and `analyze_kpkp.py` also scores inexact positions by bound A.
- Peak RSS was not logged; `ps` showed 0.7–1.6 GB per `kpsolve` while it ran.
- Everything is in `/Users/aritro/Downloads/Research/Chessendgames/research/kpkp/t44/` (33 MB). Compressed chunk tables: `kpkp_{cyl,flat}_{0..3}.out.zst`. Settings and layer counts per chunk: `kpkp_*_*.err`.
