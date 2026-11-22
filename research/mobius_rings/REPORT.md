# Pawn rings on the Moebius strip (Elkies model, whole board, 8 ranks)

## Headline

The least number of pawns in a Moebius ring *2 is **6, 8, 6, 8, 8, 8 for n = 3, 4, 5, 6, 7, 8**. The cylinder needs
n+3 = 6, 7, 8, 9 for n = 3..6 and ten for n = 7, 8. So the strip is lower for n = 5, 6, 7, 8, equal at n = 3 and one
pawn higher at n = 4. For n = 8 the value 8 is the fewest a ring can have.

| n | least pawns, Moebius *2 | rings *2 at that count (orbits / colour-distinct) | cylinder | label |
|---|---|---|---|---|
| 3 | 6 | 1 / 1 | 6 | C2 |
| 4 | 8 | 6 / 10 | 7 | C2 |
| 5 | 6 | 1 / 2 | 8 | C2 |
| 6 | 8 | 6 / 11 | 9 | C2 |
| 7 | 8 | 1 / 2 | 10 | C2 |
| 8 | 8 | 1 / 1 | 10 | C2 |

(Cylinder column: the figures given in the task, not recomputed. I did recompute with `rg_copy`: C4 first *2 at 7
pawns, C5 first *2 at 8 pawns, none below.) "Least" means no ring *2 with fewer pawns, from n pawns upward
(exhaustive, see Coverage). I make no claim for a formula in n.

**A *3 does appear:** Moebius n = 5 with 9 pawns has one
*3 orbit (2 colour-distinct), and n = 6 with 9 pawns has one (2). No other (n, pawns) scanned has a *3. On the
cylinder, C4 with 4..10 pawns and C5 with 5..9 pawns have no *3 (rg scan, `results/cylinder_hist.txt`), so on C5 the
strip gets a *3 at a pawn count where the cylinder has none. The cylinder's own least *3 for n = 5, 6 was not
found (not scanned beyond those counts). Nimbers above *3 were not looked for (heaps h <= 3 only).

## Example positions (ring notation: one entry per file, left to right, W/B + ranks)

The seam sits between the LAST entry and the FIRST entry: a capture from the last file to the first file (or back)
lands on the flipped rank 9 - r and reverses the pawn's direction.

- n = 3, 6 pawns: `W3B6 W2B7 W4B5` (self-colour-reverse)
- n = 5, 6 pawns: `B6 W3 B5 W2 W3B7`
- n = 4, 8 pawns (one of six): `B5 W23 W2B67 W4B7`
- n = 6, 8 pawns: `B4 W2 W2 W2B6 B5 W3B7`
- n = 7, 8 pawns: `B6 W2 W3 B6 B7 W3 W6B7`
- n = 8, 8 pawns: `B7 W3 W3 B6 W3 B6 B6 W2`
- *3: n = 5, 9 pawns `B67 W4 W2B6 W2B5 W5B7`; n = 6, 9 pawns `B7 W4 W23 B5 W3B7 W4B7`

All hits: `results/hits_all.txt` (66 rings: 64 *2, 2 *3), one ring per orbit.

## Rules as implemented (convention, 3 lines)

1. n files, 8 ranks. A step across the seam (last file <-> first file) flips the rank r -> 9 - r; only captures
   and e.p. captures cross it.
2. Every pawn has a direction flag d (White starts +1, Black -1); a capture across the seam flips d (RULES.md 3).
   Home rank, double step and promotion edge follow the flag, not the colour: d = +1 double-steps from rank 2 and
   promotes on 8, d = -1 double-steps from rank 7 and promotes on 1 (so a White pawn that crossed once moves down).
3. Passed = no enemy pawn of either direction strictly ahead (in the pawn's own direction) on its file or the two
   neighbouring files, seam neighbours read with flipped ranks; a pawn still capturable e.p. is not passed; the game
   ends at the first passed pawn; if a move leaves both sides passed, race rule "count" (as `rg`). Normal play,
   no move loses, X + *h may move *h -> *h' at any time; the e.p. right survives a heap move (as in `rg`).

Why the flag (not the colour) owns the home rank: the one-file rotation of the strip (pawns crossing the seam get
r -> 9 - r and d -> -d) must be a symmetry, and with this convention it is: `val/symtests.log`, 4,500 random flagged
positions for n = 3, 4, 5 are invariant under rotation, the global flip, the mirror and the colour swap in C1 and C2.
A colour-tied home rank would break that. I did not run the colour-tied variant.

## Rings and symmetry group

Ring = root ring: default directions, pawns on ranks 2..7, a pawn on every file, no passed pawn.
Group used (order 4): identity, mirror (file i -> n+1-i), kappa = colour swap with rank flip r -> 9 - r, and
mirror*kappa. Counts are orbits; "colour-distinct" splits an orbit into its colour-reversal pair when they differ
(the cylinder convention).

- Colour swap is a symmetry of the strip: swapping colours and keeping rank and flag is an exact symmetry of the
  rules (L and R exchange, *k stays *k). Alone it does not map root rings to root rings (Black would be d = +1);
  with the flip r -> 9 - r (the rotation by n files, an isometry) it does. That is kappa.
- File rotation is an isometry of the game but it turns pawns that cross the seam into reversed-flag pawns, so a
  rotated root ring is not a root ring. Root rings differing by a rotation are therefore listed separately.
  Rings with reversed flags were not enumerated.
- Pre-filter White ranks 2..6, Black 3..7 is exact (rank-7 White would need an enemy on rank 8 or, across the seam,
  rank 1). The enumerator's orbit counts equal an independent brute force without the filter for (n, pawns) = (3,3),
  (3,4), (3,5), (3,6), (4,4), (4,5): 55, 786, 5765, 27787, 251, 5642 (`val/ringcount_check.txt`).

## Coverage (exhaustive; orbits of rings, signature h = 0..3)

| n | pawns | rings | *2 orbits | *3 orbits | label |
|---|---|---|---|---|---|
| 3 | 3..10 | 55, 786, 5765, 27787, 95947, 251443, 512666, 827780 | 0,0,0,1,0,1,0,0 | 0 | C2 |
| 4 | 4..9 | 251, 5642, 60566, 408222, 1978925, 7337669 | 0,0,0,0,6,3 | 0 | C2 |
| 5 | 5..9 | 1663, 47019, 617753, 5207816, 31909703 | 0,1,0,14,15 | 0,0,0,0,1 | C2 |
| 6 | 6..9 | 11157, 355262, 5599633, 57178358 | 0,0,6,15 | 0,0,0,1 | C2 |
| 7 | 7..8 | 65613, 2570131 | 0,1 | 0 | C2 |
| 8 | 8 | 427178 | 1 | 0 | C2 |

Full signature histograms per (n, pawns): `results/histograms.tsv`; table `results/summary.tsv`.
Cylinder comparison (rg, `results/cylinder_hist.txt`): C4 7 pawns 2 *2 classes, 8 pawns 3, 9 pawns 0, 10 pawns 19;
C5 8 pawns 14, 9 pawns 4; no *3 anywhere in those runs.

## Checks, with labels

- C1 = `mob1.c`, C2 = `mob2.c` (different encoding and recursion, see below). **C2 label**: C1 and C2 per-ring
  signature files (one byte per ring, compressed in `results/*.sig.zst`) and histograms are byte-identical for every
  chunk of every row above (`results/c1_c2_agreement.txt`, 50 chunks, 0 disagreements).
- The 66 hits: the existing Part B engine (`research/mobius/mob_pawns.py`, exact CGT value) gives exactly *2 (or *3)
  for 51 of them: the 50 hits found before the n = 6, 9-pawn scan (`val/hit_check_py.log`, 0 differences) and the
  n = 6, 9-pawn *3 (value *3). The other 15 n = 6, 9-pawn *2 hits were not re-checked by Part B (C1 = C2 only). All
  66 are legal root rings (independent test) and keep their signature under all 2n rotations, the mirror and the
  colour swap in C1 and C2 (1,640 images, 0 mismatches).
- Task 1a, twist off (kind 1) vs `rg_copy`: C3 6 pawns all 160,515 labelled rings; C4 7 pawns all 285,090; C5 8 pawns
  all 2,869,124 rings; plus a 2,000 sample of C5: C1 = C2 = rg on every ring (`val/validate_all.log`).
- Task 1b, twist on vs the existing Part B code: all 187,360 positions with 1..4 pawns on 3 files (default flags,
  ranks 1..8), C1 = C2 = Part B, including the 55,924 positions it calls RACE.
- Task 5: 500 random non-passed positions on 8 files using only files 3..6 (1-based) and 500 on 7 files touching only
  one end file: Moebius = flat (= cylinder for the first set), C1 = C2 (`val/symtests.log`). The reason it must hold:
  captures stay on the victim's file, so the file set never grows, and the seam matters only if both end files are
  occupied.

## Programs

`mring.h` enumerator (shared). C1 `mob1.c`: per-file per-colour per-direction rank bitmasks in the chart, memo on
(position, h, side). C2 `mob2.c`: geometry on the double cover (2n-file cylinder, twin lift at file+n, rank 9-r,
direction -d), cell-array state, one memo entry per position holding both movers x h = 0..3, moves into positions
where the opponent has an immediate win skipped, e.p. tested for real capturability. Drivers: `run_scans.sh`,
`run_scans_rev.sh`. Checks: `partb_compare.py`, `symtests.py`, `ringcount.py`, `hit_check_py.py`,
`hit_symmetry_check.py`, `hit_ring_legality.py`, `validate_all.sh` (the `val/*.zst` inputs must be `zstd -d`
first), `cyl_scan.sh`. Compile: `cc -O3 -march=native -o mob1 mob1.c` (same for mob2, mring).

## Not done

- n >= 9; n = 6 with 10+ pawns; n = 7 with 9+ pawns (a C1 scan of n = 7, 9 pawns was stopped before any chunk
  finished and its partial files removed); n = 3 with 11+, n = 4 with 10+, n = 5 with 10+ pawns.
- The cylinder's least *3 for n = 3..8 and the Part B re-check of 15 of the n = 6, 9-pawn *2 hits.
- Rings with reversed-flag pawns; the colour-tied home-rank variant; e.p. expiring after a heap move; other race rules.
- Nimbers above *3; any proof or family for the Moebius *2 rings; Part B comparison on widths above 3.
- Pawn counts and the word "least" are for root rings under the enumerator described above only.
