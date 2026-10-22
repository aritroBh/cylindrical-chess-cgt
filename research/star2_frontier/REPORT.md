# T8: *2 frontier search

## Five-line summary

- **CHECKED-2:** The 231,071-root old census is reproduced exactly; e.p.-aware/count gives 6,724 zeros, 4,042 stars, and no *2.
- **COMPUTED-1:** The requested flat scopes (a)–(c) contain 7,957,209 canonical roots.
- **COMPUTED-1:** Exact ring scopes C5–C8 contain 7,458,433 roots; **PROVED:** C9 has no root with at most eight pawns.
- **CHECKED-2:** Three flat 5-file, 8-pawn positions are *2 under headline count/e.p.-aware and pass the brief's file-geometry test.
- **COMPUTED-1:** Across the requested scopes the C solver reports 179 *2s and 7 *3s, no *4, and no 9-setting-robust hit; two checked opponent/e.p.-aware hits disagree with `cylcgt`.

## Method and validation

`nimscan.c` is the unmodified copy of `atlas/flat8/rerun/nimscan.c`. `frontier.c` extends it to widths 1–8 with an 8-square file stride, 64 nimber bits, cylindrical file adjacency, cyclic/reflective cylinder symmetry, and separate en-passant-right masks for disconnected components. A right expires when play occurs in its component. Flat roots use file reflection and require both boundary files occupied; ring roots use rotations and reflections and require every file occupied. The no-passer root filter can omit White rank-7 and Black rank-2 pawns: each would necessarily be passed under the requested root-rank restriction.

The nimber mask scans *0 through *63. **PROVED:** With at most eight root pawns on ranks 2–7, every pawn has at most six ranks of forward travel; every move reduces the total remaining travel by at least one, so the game height and any nimber are at most 48. Thus the 64-bit scan covers every possible *k in scope. The terminal win score remains BIG=256.

**CHECKED-2 baseline:** The copied solver and the expanded solver have identical position keys and all nine setting columns on all 231,071 roots (zero differing rows). The e.p.-aware/count column is 6,724 *0, 4,042 *1, and zero *k≥2. The prior census report also records agreement with `cylcgt` over this old scope.

## Search totals and pilots

All pilot projections are CPU-time projections over all nine settings. They are conservative: the small pilots share fewer memo states than exhaustive runs. No nonempty scope exceeded the three-CPU-hour cutoff. Full cylinder jobs ran separately by width and remained well under 45 minutes.

| Scope | Exact roots | Pilot projection | Full-run CPU recorded |
|---|---:|---:|---:|
| (a) Flat width 5, 2–6 pawns | 267,393 | 22.2 s | 1.5 s in setting logs |
| (b) Flat widths 1–4, exactly 7 or 8 | 5,503,282 | 32.7 min refined estimate (width 4: 28.8 min) | 40.1 s in setting logs |
| (c) Flat width 5, exactly 7 | 2,186,534 | 10.2 min | 16.4 s in setting logs |
| (d) C5 | 3,247,022 | 35.8 min | 65.6 s including 4.4 s root enumeration |
| (d) C6 | 2,908,386 | 49.3 min | 68.5 s including 5.6 s root enumeration |
| (d) C7 | 1,136,885 | 10.9 min | 30.4 s including 3.0 s root enumeration |
| (d) C8 | 166,140 | 2.7 min | 4.4 s including 0.5 s root enumeration |
| (d) C9 | 0 | 0 | 0 |

The random C5–C9 cylinder pilot estimated roots before exact enumeration. Exact DFS pilots then measured the C5–C8 root counts above. C9 is empty because a ring needs at least one pawn on each of nine files.

## Nimber detections

**COMPUTED-1:** The C solver's result is based on its specified test: it finds *k when `G + *k` is a previous-player win. Each line in the appendix is a solver hit with its pawn count and exact setting list. The setting abbreviations are `C`=count, `M`=mover, `O`=opponent; `/T`=e.p. on with textbook passed test, `/off`=e.p. off, and `/aware`=e.p. on with the adopted e.p.-aware test.

| Scope | *2 positions | *3 positions | *4 positions | Robust across all 9 | Geometry fit under the stated file test |
|---|---:|---:|---:|---:|---|
| (a) | 2 | 0 | 0 | 0 | 2/2 |
| (b) | 51 | 2 | 0 | 0 | 53/53 |
| (c) | 2 | 0 | 0 | 0 | 2/2 |
| C5 | 70 | 0 | 0 | 0 | 70/70 |
| C6 | 32 | 0 | 0 | 0 | 0/32 |
| C7 | 16 | 3 | 0 | 0 | 0/19 |
| C8 | 6 | 2 | 0 | 0 | 0/8 |

The fit column checks whether the pawn-file span fits in a–d or a–e with an empty buffer before king files f–h. It is a geometry check. C5 rings fit in a–e, but their cylinder values do not transfer automatically when the seam is removed. C6–C8 spans are too wide.

## Flat 8×8 headline witnesses

Targeting the 70 C5 solver hits on the corresponding flat 5-file board, the C `G + *2` test marked these four positions *2:

| Pawns | Count | C P-test settings | Independent `cylcgt` check |
|---|---:|---|---|
| W: a3 b3 c2 e2 / B: a6 c5 d5 e3 | 8 | C/aware, O/aware | *2 at C/aware; `⇑` at O/aware |
| W: a4 b3 c2 d2 / B: a7 b6 c7 e4 | 8 | C/T, C/aware | *2 at C/aware; C/T is C-only |
| W: a4 b3 c3 e2 / B: a7 c5 d5 d6 | 8 | M/T, M/off, M/aware | *2 at M/T and M/off; M/aware unverified |
| W: a6 b4 c4 e3 / B: a7 c7 d6 e6 | 8 | C/aware, O/aware | *2 at C/aware; `⇓` at O/aware |

**CHECKED-2 headline result:** The first, second, and fourth positions are *2 under count/e.p.-aware in both the C solver and `cylcgt`. All four fit the stated a–e geometry with f empty. The third is not a count/e.p.-aware candidate.

**COMPUTED-1 scope note:** Flat width 5 with exactly eight pawns was not exhaustively enumerated. These are targeted tests of the 70 C5 solver hits, so they establish witnesses but not completeness for that omitted flat scope.

These are model-level witnesses under the frozen-trébuchet assumption and the brief's geometric fit rule. **CONJECTURE:** This is not a real-chess certification; actual king moves, the full freeze arrangement, and legal history were not checked.

## Cross-check discrepancy and limits

**COMPUTED-1 discrepancy:** For two checked positions, `W: a3 b3 c2 e2 / B: a6 c5 d5 e3` and `W: a6 b4 c4 e3 / B: a7 c7 d6 e6`, the C mask scan reports *2 under opponent/e.p.-aware. On the same flat `Board(5,8,False,True)`, `cylcgt` returns `⇑` and `⇓`, respectively, neither a nimber. The count/e.p.-aware values in the table above agree across both implementations. **CONJECTURE:** This may reflect the whole-board versus component-sum evaluation boundary. All new scope-wide detections remain **COMPUTED-1**, not a proof that every P-test hit is an exact canonical-form equality.

## Reproduction

Run from the project root. All files written by these commands are under `research/star2_frontier/`.

```sh
cc -O2 -o research/star2_frontier/nimscan research/star2_frontier/nimscan.c
research/star2_frontier/nimscan --max 6 > research/star2_frontier/baseline.tsv 2> research/star2_frontier/baseline.log
cc -O2 -o research/star2_frontier/frontier research/star2_frontier/frontier.c
research/star2_frontier/frontier --width-min 1 --width-max 4 --min 2 --max 6 > research/star2_frontier/frontier_old_scope.tsv 2> research/star2_frontier/frontier_old_scope.log
research/star2_frontier/frontier --flat --width-min 5 --width-max 5 --min 2 --max 6 --pilot 100 > research/star2_frontier/pilot_a.tsv 2> research/star2_frontier/pilot_a.log
research/star2_frontier/frontier --flat --width-min 1 --width-max 4 --min 7 --max 8 --pilot 100 > research/star2_frontier/pilot_b.tsv 2> research/star2_frontier/pilot_b.log
research/star2_frontier/frontier --flat --width-min 4 --width-max 4 --min 7 --max 8 --pilot 5000 > research/star2_frontier/pilot_b_w4_5000.tsv 2> research/star2_frontier/pilot_b_w4_5000.log
research/star2_frontier/frontier --flat --width-min 5 --width-max 5 --min 7 --max 7 --pilot 100 > research/star2_frontier/pilot_c.tsv 2> research/star2_frontier/pilot_c.log
research/star2_frontier/frontier --cylinder --width-min 5 --width-max 9 --min 5 --max 8 --pilot-raw 20000 > research/star2_frontier/pilot_d.tsv 2> research/star2_frontier/pilot_d.log
research/star2_frontier/frontier --cylinder --width-min 5 --width-max 5 --min 5 --max 8 --pilot 100 > research/star2_frontier/pilot_d_c5_exact.tsv 2> research/star2_frontier/pilot_d_c5_exact.log
research/star2_frontier/frontier --cylinder --width-min 6 --width-max 6 --min 6 --max 8 --pilot 100 > research/star2_frontier/pilot_d_c6_exact.tsv 2> research/star2_frontier/pilot_d_c6_exact.log
research/star2_frontier/frontier --cylinder --width-min 7 --width-max 7 --min 7 --max 8 --pilot 100 > research/star2_frontier/pilot_d_c7_exact.tsv 2> research/star2_frontier/pilot_d_c7_exact.log
research/star2_frontier/frontier --cylinder --width-min 8 --width-max 8 --min 8 --max 8 --pilot 100 > research/star2_frontier/pilot_d_c8_exact.tsv 2> research/star2_frontier/pilot_d_c8_exact.log
```

Full searches (large outputs are compressed):

```sh
research/star2_frontier/frontier --flat --width-min 5 --width-max 5 --min 2 --max 6 > research/star2_frontier/scope_a.tsv 2> research/star2_frontier/scope_a.log
set -o pipefail; research/star2_frontier/frontier --flat --width-min 1 --width-max 4 --min 7 --max 8 2> research/star2_frontier/scope_b.log | gzip -1 > research/star2_frontier/scope_b.tsv.gz
set -o pipefail; research/star2_frontier/frontier --flat --width-min 5 --width-max 5 --min 7 --max 7 2> research/star2_frontier/scope_c.log | gzip -1 > research/star2_frontier/scope_c.tsv.gz
set -o pipefail; research/star2_frontier/frontier --cylinder --width-min 5 --width-max 5 --min 5 --max 8 2> research/star2_frontier/scope_d_c5.log | gzip -1 > research/star2_frontier/scope_d_c5.tsv.gz
set -o pipefail; research/star2_frontier/frontier --cylinder --width-min 6 --width-max 6 --min 6 --max 8 2> research/star2_frontier/scope_d_c6.log | gzip -1 > research/star2_frontier/scope_d_c6.tsv.gz
set -o pipefail; research/star2_frontier/frontier --cylinder --width-min 7 --width-max 7 --min 7 --max 8 2> research/star2_frontier/scope_d_c7.log | gzip -1 > research/star2_frontier/scope_d_c7.tsv.gz
set -o pipefail; research/star2_frontier/frontier --cylinder --width-min 8 --width-max 8 --min 8 --max 8 2> research/star2_frontier/scope_d_c8.log | gzip -1 > research/star2_frontier/scope_d_c8.tsv.gz
```

The baseline census check is reproduced by:

```sh
PYTHONPATH=. .venv/bin/python research/star2_frontier/verify_baseline.py
```

Candidate lists are regenerated by:

```sh
PYTHONPATH=. .venv/bin/python research/star2_frontier/summarize.py research/star2_frontier/scope_a.tsv research/star2_frontier/scope_b.tsv.gz research/star2_frontier/scope_c.tsv.gz research/star2_frontier/scope_d_c5.tsv.gz research/star2_frontier/scope_d_c6.tsv.gz research/star2_frontier/scope_d_c7.tsv.gz research/star2_frontier/scope_d_c8.tsv.gz
PYTHONPATH=. .venv/bin/python research/star2_frontier/prepare_c5_flat_test.py
research/star2_frontier/frontier --test research/star2_frontier/c5_flat_embed.in > research/star2_frontier/c5_flat_embed_test.tsv
PYTHONPATH=. .venv/bin/python research/star2_frontier/summarize_flat_probe.py
research/star2_frontier/frontier --eval research/star2_frontier/flat5p8_candidates.in > research/star2_frontier/flat5p8_candidates.tsv
PYTHONPATH=. .venv/bin/python research/star2_frontier/verify_headline.py 1
PYTHONPATH=. .venv/bin/python research/star2_frontier/verify_headline.py 2
PYTHONPATH=. .venv/bin/python research/star2_frontier/verify_headline.py 3
PYTHONPATH=. .venv/bin/python research/star2_frontier/verify_mover.py
PYTHONPATH=. .venv/bin/python research/star2_frontier/verify_disagreement.py
```

## Complete C-solver hit list

**COMPUTED-1:** This is every *k≥2 hit from the requested scopes, with pawn count, settings, and the file-geometry result. The opponent/e.p.-aware discrepancy above applies to the listed mask hits.

```text
research/star2_frontier/scope_a.tsv: roots=267393, maximum nimber seen=2
*2: 2 positions; robust across all 9 settings=0
  6 pawns; settings=C/off; trébuchet-fit=yes; W: a2 c2 d2 / B: b5 c7 e7
  6 pawns; settings=C/off; trébuchet-fit=yes; W: b4 c2 e2 / B: a7 c7 d7
total *k>=2 position-setting hits=2; *3=0; *4=0
research/star2_frontier/scope_b.tsv.gz: roots=5503282, maximum nimber seen=3
*2: 51 positions; robust across all 9 settings=0
  7 pawns; settings=O/aware; trébuchet-fit=yes; W: a2 b2 d2 / B: a6 b6 b7 c4
  7 pawns; settings=C/T,C/aware,M/T,M/aware; trébuchet-fit=yes; W: a4 b3 d2 d3 / B: a7 b7 c5
  7 pawns; settings=C/T,C/aware,M/T,M/aware; trébuchet-fit=yes; W: b4 c2 d2 / B: a6 a7 c6 d5
  7 pawns; settings=O/aware; trébuchet-fit=yes; W: b5 c2 c3 d3 / B: a7 c7 d7
  8 pawns; settings=M/aware; trébuchet-fit=yes; W: a2 a5 b2 c2 / B: a4 a6 b4 c6
  8 pawns; settings=C/off,M/off,O/off; trébuchet-fit=yes; W: a2 a5 b3 c4 / B: a3 a7 b7 c6
  8 pawns; settings=C/off,M/off,O/off; trébuchet-fit=yes; W: a2 a6 b2 c3 / B: a4 a7 b6 c5
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a2 b2 b3 c2 / B: a6 b4 b6 b7
  8 pawns; settings=M/aware; trébuchet-fit=yes; W: a3 a5 b5 c3 / B: a4 a7 b7 c7
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a3 b2 b3 b5 / B: a7 b6 b7 c7
  8 pawns; settings=M/T,M/off; trébuchet-fit=yes; W: a2 a3 b2 d3 / B: a5 c5 c6 d5
  8 pawns; settings=C/aware; trébuchet-fit=yes; W: a2 a3 b3 d2 / B: a4 a6 b6 c7
  8 pawns; settings=M/aware; trébuchet-fit=yes; W: a2 a3 b3 d3 / B: a5 c5 d5 d6
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a2 a4 b3 d3 / B: a6 b5 c5 c6
  8 pawns; settings=M/T; trébuchet-fit=yes; W: a2 b2 c2 d2 / B: a7 b7 c4 d5
  8 pawns; settings=M/T,O/T,O/aware; trébuchet-fit=yes; W: a2 b2 c2 d2 / B: b4 b7 c5 d6
  8 pawns; settings=C/T,C/aware,M/T,M/aware; trébuchet-fit=yes; W: a2 b3 b4 c2 / B: b5 b7 c6 d6
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a2 b3 c2 c3 / B: a3 a5 c6 d7
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a2 b3 c2 c3 / B: a4 a6 b5 d5
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a2 b3 c3 d2 / B: a6 b5 b7 d3
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a2 b5 c3 d4 / B: a3 b7 c7 d6
  8 pawns; settings=M/aware; trébuchet-fit=yes; W: a3 a4 b4 d4 / B: a6 c6 d6 d7
  8 pawns; settings=C/aware; trébuchet-fit=yes; W: a3 a5 b3 c2 / B: a6 a7 b6 d7
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a3 a5 b4 d4 / B: a7 b6 c6 c7
  8 pawns; settings=O/aware; trébuchet-fit=yes; W: a3 b2 c2 d2 / B: a4 b6 c7 d4
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a3 b2 c3 d2 / B: a5 b7 c5 c7
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a3 b4 c3 c4 / B: a5 a7 b6 d6
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a3 b5 c3 d4 / B: a4 b7 c7 d6
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a4 a6 c3 d2 / B: a7 b6 c6 c7
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a4 b2 c2 c4 / B: a6 b7 c6 d7
  8 pawns; settings=M/T,M/aware; trébuchet-fit=yes; W: a4 b2 c2 d2 / B: a7 b7 c7 d4
  8 pawns; settings=C/off,O/off; trébuchet-fit=yes; W: a4 b2 c2 d3 / B: a5 b6 c7 d7
  8 pawns; settings=O/aware; trébuchet-fit=yes; W: a4 b2 c3 d2 / B: a7 b6 c6 d5
  8 pawns; settings=M/T,M/off; trébuchet-fit=yes; W: a4 b3 b4 d4 / B: a6 c7 d6 d7
  8 pawns; settings=C/off,O/off; trébuchet-fit=yes; W: a4 b3 c2 d2 / B: a5 b7 c7 d6
  8 pawns; settings=O/aware; trébuchet-fit=yes; W: a4 b3 c3 d2 / B: a7 b6 c7 d5
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a4 b4 c3 d2 / B: a7 b6 c5 d5
  8 pawns; settings=M/T; trébuchet-fit=yes; W: a4 b5 c2 d2 / B: a7 b7 c7 d7
  8 pawns; settings=C/T; trébuchet-fit=yes; W: a5 b2 c2 d2 / B: a7 b7 c5 d4
  8 pawns; settings=M/T,M/aware; trébuchet-fit=yes; W: a5 b2 c2 d2 / B: a7 b7 c7 d5
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a5 b2 c2 d3 / B: a6 b4 c6 d5
  8 pawns; settings=C/off,M/off,O/off; trébuchet-fit=yes; W: a5 b2 c2 d3 / B: b4 b7 c6 d5
  8 pawns; settings=O/aware; trébuchet-fit=yes; W: a5 b3 c2 d5 / B: a6 b7 c7 d7
  8 pawns; settings=O/aware; trébuchet-fit=yes; W: a5 b3 c4 d4 / B: a7 b7 c6 c7
  8 pawns; settings=C/T; trébuchet-fit=yes; W: a5 b4 c2 d2 / B: a7 b7 c7 d4
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a6 b2 c2 d3 / B: a7 b4 c6 d5
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a6 c2 c4 d3 / B: a7 b6 c6 d7
  8 pawns; settings=O/aware; trébuchet-fit=yes; W: b2 b3 c2 d2 / B: a5 b5 c6 d4
  8 pawns; settings=C/T,C/aware,M/T,M/aware; trébuchet-fit=yes; W: b2 b4 c3 d3 / B: a7 b5 b6 c7
  8 pawns; settings=C/off,M/off,O/off; trébuchet-fit=yes; W: b2 b5 c3 d4 / B: a4 b7 c7 d6
  8 pawns; settings=M/T,O/T,O/aware; trébuchet-fit=yes; W: b2 b5 c4 d3 / B: a7 b7 c7 d7
*3: 2 positions; robust across all 9 settings=0
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a2 b5 c3 d4 / B: a4 b7 c7 d6
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a5 b2 c2 d3 / B: a7 b4 c6 d5
total *k>=2 position-setting hits=94; *3=2; *4=0
research/star2_frontier/scope_c.tsv.gz: roots=2186534, maximum nimber seen=2
*2: 2 positions; robust across all 9 settings=0
  7 pawns; settings=M/off; trébuchet-fit=yes; W: a2 c2 e2 / B: a3 a4 b7 d7
  7 pawns; settings=M/off; trébuchet-fit=yes; W: a5 a6 b2 d2 / B: a7 c7 e7
total *k>=2 position-setting hits=2; *3=0; *4=0
research/star2_frontier/scope_d_c5.tsv.gz: roots=3247022, maximum nimber seen=2
*2: 70 positions; robust across all 9 settings=0
  6 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a2 b2 c2 / B: b3 d7 e6
  6 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a3 b3 d3 / B: a6 c6 e6
  6 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a3 c3 d2 / B: b5 d5 e5
  6 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a4 b4 d4 / B: a7 c6 e6
  6 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a6 c3 d2 / B: a7 b7 e7
  8 pawns; settings=M/T,M/aware; trébuchet-fit=yes; W: a2 a3 b3 d2 / B: a5 c4 c7 e6
  8 pawns; settings=M/off; trébuchet-fit=yes; W: a2 a3 b3 d2 / B: a6 b5 c6 e7
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a2 a3 b3 d2 / B: a6 c6 e5 e7
  8 pawns; settings=C/aware; trébuchet-fit=yes; W: a2 a3 b3 d3 / B: a7 c5 e5 e6
  8 pawns; settings=C/aware,O/aware; trébuchet-fit=yes; W: a2 a3 c3 d2 / B: a4 b5 d5 e5
  8 pawns; settings=C/aware,M/aware; trébuchet-fit=yes; W: a2 a3 c3 d2 / B: b5 b6 d5 e5
  8 pawns; settings=M/T,M/aware; trébuchet-fit=yes; W: a2 a4 b2 d2 / B: b7 c5 c7 e6
  8 pawns; settings=C/off,O/T,O/off,O/aware; trébuchet-fit=yes; W: a2 a4 b2 d2 / B: b7 c5 c7 e7
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a2 a4 b3 d3 / B: b6 b7 c6 e7
  8 pawns; settings=M/T; trébuchet-fit=yes; W: a2 a4 b4 d4 / B: a6 b7 c7 e6
  8 pawns; settings=M/T,M/aware; trébuchet-fit=yes; W: a2 a4 c3 e2 / B: b7 d5 d7 e7
  8 pawns; settings=C/off; trébuchet-fit=yes; W: a2 a5 b2 d2 / B: a6 c7 d6 e7
  8 pawns; settings=C/T,C/off,O/T,O/off; trébuchet-fit=yes; W: a2 a5 b4 d2 / B: a4 a7 c7 e5
  8 pawns; settings=M/T,M/aware; trébuchet-fit=yes; W: a2 a5 c4 d3 / B: b6 c6 c7 e7
  8 pawns; settings=C/aware; trébuchet-fit=yes; W: a2 b2 c2 d2 / B: b5 b7 d6 e4
  8 pawns; settings=C/aware; trébuchet-fit=yes; W: a2 b2 c2 d2 / B: b6 b7 d5 e4
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a3 a4 b2 c4 / B: a6 d7 e6 e7
  8 pawns; settings=M/T,M/off,M/aware; trébuchet-fit=yes; W: a3 a4 b3 d2 / B: a5 a6 c7 e6
  8 pawns; settings=M/T,M/off,M/aware; trébuchet-fit=yes; W: a3 a4 b4 d2 / B: b6 c6 d5 e7
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a3 a4 c4 d2 / B: a5 b7 d6 e6
  8 pawns; settings=C/aware; trébuchet-fit=yes; W: a3 a4 c4 e2 / B: b6 d6 e6 e7
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a3 a5 c3 d2 / B: b5 b7 d5 e5
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a3 a5 c3 e2 / B: b5 b7 d5 e5
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a3 b2 b3 c2 / B: a5 a6 d5 e7
  8 pawns; settings=C/off; trébuchet-fit=yes; W: a3 b2 c2 e2 / B: a7 b7 c6 d7
  8 pawns; settings=C/off; trébuchet-fit=yes; W: a3 b2 c3 d2 / B: a4 a7 c7 e7
  8 pawns; settings=M/aware; trébuchet-fit=yes; W: a3 b2 c3 d2 / B: a5 b6 c7 e5
  8 pawns; settings=M/T; trébuchet-fit=yes; W: a3 b3 c2 d2 / B: b5 b7 c5 e5
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a3 b3 c2 d2 / B: b5 c6 d7 e7
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a3 b3 c2 d3 / B: a6 c6 d7 e6
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a3 b3 c2 e2 / B: a5 b6 c7 d7
  8 pawns; settings=C/aware,O/aware; trébuchet-fit=yes; W: a3 b3 c2 e2 / B: a6 c5 d5 e3
  8 pawns; settings=M/T,M/aware; trébuchet-fit=yes; W: a3 b3 c3 d2 / B: a5 c7 d5 e5
  8 pawns; settings=M/T,M/off,M/aware; trébuchet-fit=yes; W: a3 b3 c3 d3 / B: a6 b6 d6 e6
  8 pawns; settings=C/T; trébuchet-fit=yes; W: a4 b2 c2 e2 / B: a6 c4 d6 e6
  8 pawns; settings=M/aware; trébuchet-fit=yes; W: a4 b2 c2 e2 / B: a6 c4 d7 e6
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a4 b3 c2 d2 / B: a6 b6 c7 e7
  8 pawns; settings=O/T,O/aware; trébuchet-fit=yes; W: a4 b3 c2 d2 / B: a6 b7 c7 e6
  8 pawns; settings=C/T,C/aware; trébuchet-fit=yes; W: a4 b3 c2 d2 / B: a7 b6 c7 e4
  8 pawns; settings=M/T,M/off,M/aware; trébuchet-fit=yes; W: a4 b3 c2 d3 / B: a7 b6 c5 e6
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a4 b3 c2 e3 / B: a5 a6 c5 d5
  8 pawns; settings=M/off; trébuchet-fit=yes; W: a4 b3 c2 e3 / B: a6 b6 b7 d7
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a4 b3 c2 e3 / B: b7 c6 d5 e6
  8 pawns; settings=M/T,M/off,M/aware; trébuchet-fit=yes; W: a4 b3 c3 d3 / B: a6 b6 c5 e6
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a4 b3 c3 e2 / B: a5 a6 c7 d5
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a4 b3 c3 e2 / B: a6 b6 c5 d7
  8 pawns; settings=M/T,M/off,M/aware; trébuchet-fit=yes; W: a4 b3 c3 e2 / B: a7 c5 d5 d6
  8 pawns; settings=M/aware; trébuchet-fit=yes; W: a4 b4 c3 d2 / B: b6 c7 d6 e7
  8 pawns; settings=M/T,M/aware; trébuchet-fit=yes; W: a4 b4 c4 d2 / B: a6 c7 d6 e6
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a4 b4 d2 d4 / B: a7 c4 c6 e6
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a4 b4 d2 d4 / B: a7 c6 e4 e6
  8 pawns; settings=C/off,O/off; trébuchet-fit=yes; W: a4 b4 d2 d4 / B: a7 c7 d3 e6
  8 pawns; settings=C/aware,M/aware; trébuchet-fit=yes; W: a4 b4 d3 d4 / B: a7 c6 c7 e6
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=yes; W: a4 b4 d3 d4 / B: a7 c6 d5 e6
  8 pawns; settings=M/aware; trébuchet-fit=yes; W: a4 c3 d2 e2 / B: a7 b6 d5 e7
  8 pawns; settings=C/T,C/aware; trébuchet-fit=yes; W: a5 b2 c3 d2 / B: b5 c6 d7 e7
  8 pawns; settings=M/aware; trébuchet-fit=yes; W: a5 b2 c3 d3 / B: a7 c7 d5 e7
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a5 b3 c2 d2 / B: b5 c6 d4 e7
  8 pawns; settings=C/T; trébuchet-fit=yes; W: a5 b3 c3 d3 / B: a7 c7 d5 e7
  8 pawns; settings=O/off; trébuchet-fit=yes; W: a5 b3 c4 e2 / B: a7 b7 c6 d4
  8 pawns; settings=C/aware,O/aware; trébuchet-fit=yes; W: a5 b4 c4 e4 / B: a6 a7 c7 d6
  8 pawns; settings=C/aware; trébuchet-fit=yes; W: a5 b4 d2 d3 / B: b7 c7 d7 e7
  8 pawns; settings=C/aware; trébuchet-fit=yes; W: a5 c2 c4 e3 / B: b7 c7 d7 e7
  8 pawns; settings=C/off,O/off; trébuchet-fit=yes; W: a6 b3 c2 e2 / B: a5 a7 c5 d5
  8 pawns; settings=C/aware,O/aware; trébuchet-fit=yes; W: a6 b4 c4 e3 / B: a7 c7 d6 e6
total *k>=2 position-setting hits=138; *3=0; *4=0
research/star2_frontier/scope_d_c6.tsv.gz: roots=2908386, maximum nimber seen=2
*2: 32 positions; robust across all 9 settings=0
  6 pawns; settings=O/aware; trébuchet-fit=no; W: a3 b2 d2 / B: c6 e7 f6
  6 pawns; settings=O/aware; trébuchet-fit=no; W: a3 b2 d3 / B: c7 e7 f6
  8 pawns; settings=M/off; trébuchet-fit=no; W: a2 a5 c2 e2 / B: b4 b7 d7 f7
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a2 b2 d2 e2 / B: a7 c4 e5 f4
  8 pawns; settings=O/T; trébuchet-fit=no; W: a3 a5 b4 d2 / B: a7 c7 e6 f6
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a3 b2 c2 e2 / B: a6 c5 d4 f7
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a3 b2 c2 e2 / B: b6 c5 d4 f5
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a3 b2 d2 e2 / B: a6 c7 d5 f7
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a3 b2 d2 e2 / B: b5 c7 e5 f7
  8 pawns; settings=C/T,M/T; trébuchet-fit=no; W: a3 b2 d2 f2 / B: a6 c4 c5 e5
  8 pawns; settings=O/T; trébuchet-fit=no; W: a3 b3 c2 e2 / B: c4 c6 d5 f7
  8 pawns; settings=O/T,O/off; trébuchet-fit=no; W: a3 b3 d3 e2 / B: b5 c5 d4 f7
  8 pawns; settings=M/T; trébuchet-fit=no; W: a3 c2 d3 e2 / B: b7 c6 e5 f5
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=no; W: a3 c3 d2 e2 / B: b6 d7 e7 f6
  8 pawns; settings=C/T,M/T; trébuchet-fit=no; W: a4 a5 c4 e3 / B: b7 d7 e6 f7
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=no; W: a4 b2 d2 e2 / B: a5 c7 d5 f7
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a4 b2 d3 e2 / B: a7 c7 d6 f7
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=no; W: a4 b2 d4 e2 / B: a7 c7 d5 f7
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a4 b2 d4 e2 / B: a7 c7 d7 f6
  8 pawns; settings=C/off; trébuchet-fit=no; W: a4 b3 c2 e2 / B: a7 b7 d4 f7
  8 pawns; settings=M/off; trébuchet-fit=no; W: a4 b3 c2 e3 / B: a6 b5 d6 f7
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=no; W: a4 b3 c2 e3 / B: b6 c6 d5 f6
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=no; W: a4 b3 c3 e3 / B: b7 c6 d5 f6
  8 pawns; settings=M/T; trébuchet-fit=no; W: a4 b4 d3 e2 / B: b7 c6 d7 f6
  8 pawns; settings=M/off; trébuchet-fit=no; W: a4 b4 d4 e2 / B: a7 c7 d5 f6
  8 pawns; settings=M/off; trébuchet-fit=no; W: a4 c3 d2 f2 / B: a5 b7 d5 e5
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a5 b4 c3 e4 / B: b7 c7 d6 f7
  8 pawns; settings=O/T,O/off; trébuchet-fit=no; W: a5 b4 c4 e2 / B: a6 c6 d6 f7
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a5 b4 d3 e2 / B: b7 c7 d6 f7
  8 pawns; settings=O/aware; trébuchet-fit=no; W: a5 b4 d5 f2 / B: b7 c7 e7 f7
  8 pawns; settings=C/off; trébuchet-fit=no; W: a5 c2 d2 e2 / B: b7 c6 d5 f7
  8 pawns; settings=C/off,O/off; trébuchet-fit=no; W: a6 b2 d2 f2 / B: a7 b3 c7 e7
total *k>=2 position-setting hits=47; *3=0; *4=0
research/star2_frontier/scope_d_c7.tsv.gz: roots=1136885, maximum nimber seen=3
*2: 16 positions; robust across all 9 settings=0
  8 pawns; settings=C/off; trébuchet-fit=no; W: a2 a4 d2 e2 / B: b7 c7 f5 g7
  8 pawns; settings=C/off; trébuchet-fit=no; W: a3 b2 d2 e2 / B: c7 d7 f7 g6
  8 pawns; settings=O/off; trébuchet-fit=no; W: a3 c2 d2 f2 / B: b7 d5 e6 g5
  8 pawns; settings=O/off; trébuchet-fit=no; W: a3 c2 d2 f2 / B: b7 d7 e5 g5
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=no; W: a3 c3 e3 f2 / B: b5 d5 f5 g5
  8 pawns; settings=C/off; trébuchet-fit=no; W: a4 b2 d2 e2 / B: b7 c7 f4 g7
  8 pawns; settings=C/off; trébuchet-fit=no; W: a4 b2 d2 e2 / B: c5 c7 f7 g7
  8 pawns; settings=C/off; trébuchet-fit=no; W: a4 b2 d2 e2 / B: c5 d7 f7 g6
  8 pawns; settings=O/off; trébuchet-fit=no; W: a4 b3 d4 f2 / B: a7 c7 e6 g7
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=no; W: a4 b4 d3 f3 / B: a7 c6 e5 g6
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=no; W: a4 b4 d4 f4 / B: a7 c6 e6 g6
  8 pawns; settings=O/T,O/off,O/aware; trébuchet-fit=no; W: a4 c3 d2 f3 / B: b6 d5 e5 g6
  8 pawns; settings=O/off; trébuchet-fit=no; W: a4 c4 d2 f2 / B: b7 d7 e7 g6
  8 pawns; settings=C/off; trébuchet-fit=no; W: a4 d3 e2 g2 / B: b7 c5 f7 g7
  8 pawns; settings=C/T,C/off,M/aware; trébuchet-fit=no; W: a5 b2 c2 e2 / B: a4 d7 f7 g7
  8 pawns; settings=C/off; trébuchet-fit=no; W: a5 b2 d2 e2 / B: c5 d7 f7 g7
*3: 3 positions; robust across all 9 settings=0
  8 pawns; settings=C/off; trébuchet-fit=no; W: a2 b2 d2 e2 / B: b7 c7 f7 g7
  8 pawns; settings=C/off; trébuchet-fit=no; W: a4 b2 d2 e2 / B: b7 c7 f5 g7
  8 pawns; settings=C/off; trébuchet-fit=no; W: a4 b2 d2 e2 / B: c5 d7 f7 g7
total *k>=2 position-setting hits=29; *3=3; *4=0
research/star2_frontier/scope_d_c8.tsv.gz: roots=166140, maximum nimber seen=3
*2: 6 positions; robust across all 9 settings=0
  8 pawns; settings=C/T,C/off; trébuchet-fit=no; W: a3 b2 d3 f2 / B: c7 e6 g7 h6
  8 pawns; settings=M/aware; trébuchet-fit=no; W: a3 c3 d2 g2 / B: b7 e7 f6 h6
  8 pawns; settings=C/T,C/off; trébuchet-fit=no; W: a4 c2 d2 f2 / B: b4 e7 g7 h6
  8 pawns; settings=C/T,C/off; trébuchet-fit=no; W: a5 c2 d2 f2 / B: b4 e7 g7 h7
  8 pawns; settings=C/off,O/off; trébuchet-fit=no; W: a5 c2 e2 g2 / B: b7 d7 f7 h4
  8 pawns; settings=C/T,C/off; trébuchet-fit=no; W: a5 c3 d2 f2 / B: b5 e7 g7 h7
*3: 2 positions; robust across all 9 settings=0
  8 pawns; settings=C/T,C/off; trébuchet-fit=no; W: a4 c2 d2 f2 / B: b4 e7 g7 h7
  8 pawns; settings=C/T,C/off; trébuchet-fit=no; W: a5 c2 d2 f2 / B: b5 e7 g7 h7
total *k>=2 position-setting hits=15; *3=2; *4=0
```
