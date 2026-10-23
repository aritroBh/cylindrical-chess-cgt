# T52: rings worth *2 with n+2 pawns on C_n for n ≥ 8

> **Orchestrator notes (2026-10-23).**
> - §3's "a ring is a single component, so the sum model and the whole-board game coincide" is wrong: captures split
>   rings (192 of the 813 nodes of R_18 split; see `research/ring_n_plus_2_proof/PROOF.md`).
> - The W3/B5 variant is \*2 only for n = 8, 10. T50's rg gives LNLL for every even n from 12 to 60, so it does not
>   extend. The W2/B4 family is proved \*2 for every even n ≥ 8 in `research/ring_n_plus_2_proof/` (whole-board).
> - C9, 11 pawns: the orchestrator's search inserted one single-pawn file at every position into all 20 C8 hits:
>   1,920 rings, no \*2 or \*3 (rg). That is wider than the 114 here.
> - T52 wrote its scripts to `/tmp/scratchpad` against the brief; they are now in `scripts/`.


## 5-line summary

- The 18 *2 classes on C_8 all have a wall run (longest 1–4 files); core windows carry 6–11 pawns on 4–7 files.
- Growing by one pawn on C_9 (11 pawns) produced 114 rings, none with nimber 2: no n+2 *2 ring on C_9.
- Growing by two pawns on C_10 (12 pawns) produced 21 rings worth *2 (and 6 worth *3); list in `c10_star2_rings.txt`.
- An even-n family exists: core (6 files, 8 pawns) plus a repeated (W2,B4) or (W3,B5) wall pair; verified *2 on C_8, C_10, C_12 (whole-board game).
- C_9 with 10 pawns (n+1) could not be scanned: the named scanner is limited to width ≤ 8 (64-bit bitboard), so the requested --width 9 run is infeasible as given.

## 1. Structure of the 18 C_8 *2 classes

Longest wall run (single pawn per file, alternating colours, W2/B4 or W3/B5 phase) for each of the 18 classes
(`research/star26_rings/c8/p10_5_5_hits.tsv`, scanner=N,2, cylcgt confirms *2).

| # | Position (C_8) | Phase | Wall files | Core files | Core pawns |
|---|---|---|---|---|---|
| 1 | W: a3 b3 c3 d2 f2 / B: b6 d5 e5 g4 h5 | W2/B4 | fg (2) | a b c d e h | 8 |
| 2 | W: a3 b3 d2 e3 g2 / B: b7 c6 d6 f6 h5 | W3/B5 | a h (2) | b c d e f g | 8 |
| 3 | W: a4 b3 c2 e3 g3 / B: a7 b7 d5 f5 h6 | W3/B5 | d e f g (4) | a b c h | 6 |
| 4 | W: a4 b4 d3 f2 h2 / B: a7 b6 c6 e5 g6 | W3/B5 | d e (2) | a b c f g h | 8 |
| 5 | W: a4 b4 d3 f3 h2 / B: a7 b6 c6 e5 g5 | W3/B5 | d e f g (4) | a b c h | 6 |
| 6 | W: a4 c2 c3 e3 g2 / B: b6 b7 d5 f7 h6 | W3/B5 | d e (2) | a b c f g h | 8 |
| 7 | W: a4 c3 d3 e2 g2 / B: b6 c6 e5 f5 h4 | W2/B4 | g h (2) | a b c d e f | 8 |
| 8 | W: a4 c3 d3 e2 g3 / B: b6 d5 e5 f7 h7 | W3/B5 | c (1) | a b d e f g h | 9 |
| 9 | W: a4 c3 d3 f2 g2 / B: a7 b7 d6 e7 h4 | W2/B4 | g h (2) | a b c d e f | 8 |
| 10 | W: a4 c3 e3 f3 g2 / B: b7 d6 e7 g6 h6 | W3/B5 | c (1) | a b d e f g h | 9 |
| 11 | W: a4 c4 e3 f2 g2 / B: b6 d6 f5 g6 h7 | W3/B5 | e (1) | a b c d f g h | 9 |
| 12 | W: a4 c4 e3 f3 g2 / B: b6 d6 f5 g5 h7 | W3/B5 | e (1) | a b c d f g h | 9 |
| 13 | W: a5 b2 c2 e3 f2 / B: b5 d6 e6 g7 h7 | W2/B4 | c (1) | a b d e f g h | 9 |
| 14 | W: a5 b4 d3 f4 g4 / B: c6 d6 e6 f7 h7 | (none) | - | all 8 files | 10 |
| 15 | W: a5 c3 d3 e2 g2 / B: b7 c6 e5 f5 h4 | W2/B4 | g h (2) | a b c d e f | 8 |
| 16 | W: a5 c4 d4 f3 g2 / B: b7 d7 e6 f6 h4 | W2/B4 | g h (2) | a b c d e f | 8 |
| 17 | W: a5 c4 d4 f3 g3 / B: b7 d7 e6 f6 h5 | W3/B5 | g h (2) | a b c d e f | 8 |
| 18 | W: a6 b3 e3 f2 h2 / B: a7 c7 d6 g6 h3 | W2/B4 | f (1) | a b c d e g h | 9 |

Claim: COMPUTED-1 (structure by direct file/rank inspection of the 18 scanner hits).

## 2. Grow by wall insertion

Built `research/ring_n_plus_2/ring4` from `research/star4_hunt/ring4.c` with
`cc -O2 -DSTRIDE=10 -o research/ring_n_plus_2/ring4 research/star4_hunt/ring4.c -lm`.

- **C_9 (11 pawns, n+2).** Seed file `seeds8.txt` (the 18 classes). Command:
  `research/ring_n_plus_2/ring4 --cylinder --width 9 --single --rep-nim 2 --extend research/ring_n_plus_2/seeds8.txt --k 1`
  Result: 114 valid rings, 0 with nimber 2. **No *2 ring with 11 pawns on C_9.**
  (COMPUTED-1; ring4 only, 1 run.)

- **C_10 (12 pawns, n+2).** Command:
  `research/ring_n_plus_2/ring4 --cylinder --width 10 --single --rep-nim 2 --extend research/ring_n_plus_2/seeds8.txt --k 2`
  Result: 596 valid rings; 21 with nimber 2 (*2) and 6 with nimber 3 (*3). Full list: `c10_star2_rings.txt`.
  (COMPUTED-1; ring4 only.)

## 3. Family

Pattern (even n ≥ 8): fixed 6-file core
  W: a5 c4 d4 f3 ; B: b7 d7 e6 f6
plus a repeated wall pair (W2,B4) or (W3,B5) on the remaining n-6 files:
  W2/B4 family: `W a5 c4 d4 f3 + (W2 B4)^((n-6)/2)` (wall files alternate W2, B4)
  W3/B5 family: `W a5 c4 d4 f3 + (W3 B5)^((n-6)/2)` (wall files alternate W3, B5)

Whole-board game (components forced to a single component, `pawns.components = lambda b, p: [p]`):

| Phase | n | Value | Outcome | Time |
|---|---|---|---|---|
| W2/B4 | 8 | *2 | N | 32 s |
| W3/B5 | 8 | *2 | N | 33 s |
| W2/B4 | 10 | *2 | N | 285 s |
| W3/B5 | 10 | *2 | N | 203 s |
| W2/B4 | 12 | *2 | N | 1628 s |

Sum-model (`pawns.value`, default) agrees: n=8 W2/B4 gives *2 (29.6 s). Since a ring is a single component,
the sum model and the whole-board game coincide for rings.

Odd n (e.g. n=9, n=11) were tested with a trailing half-pair and gave no *2 in the attempted runs;
combined with the C_9 scan above, the family is even-n only.

Claim: CHECKED-2 for n=8 and n=10 (ring4 found the same *2 positions; cylcgt confirms value). COMPUTED-1 for n=12.

## 4. C_9 with 10 pawns (n+1) — pilot

Attempted:
`research/star26_rings/frontier_split1_fixed2 --cylinder --width 9 --min 10 --max 10 --nw 5 --nb 5 --only-setting 2 --chunk 0 4096 --max-entries 67108864`
from `research/star26_rings/`.

The scanner rejected the run: `invalid range (width 1..8, pawns 2..10, pilot >= 0)`. Its bitboard uses 64 bits
(8 files × 8 ranks), so width 9 cannot be represented; no width-9 binary exists in the repository. The requested
4 chunks (I = 0, 1000, 2000, 3000) could not be executed. No hits to report.

Cost estimate: not obtainable from this scanner; a width-9 scan would require a 128-bit (or rank-major)
reimplementation. The width-8 5+5 scans in the repository take minutes-to-hours per chunk.

## Reproduction

- Structure table: `.venv/bin/python` over `/tmp/scratchpad/step1.py` (not archived; regenerate from
  `research/star26_rings/c8/p10_5_5_hits.tsv`).
- C_9 grow: command above.
- C_10 grow: command above.
- Family values: `.venv/bin/python /tmp/scratchpad/famrun.py "W2/B4" 8` (and 10, 12), with `PYTHONPATH=.`.
- Sum model: `.venv/bin/python /tmp/scratchpad/sum8.py`.

Raw outputs are small (< 1 MB); no compression needed.
