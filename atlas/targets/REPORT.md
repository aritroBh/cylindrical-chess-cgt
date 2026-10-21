# Elkies Targets: Robustness Across 9 Core Settings

**5-Line Summary of Findings**
1. Only 4 of 9 Elkies target values have robust positions (same value in all 9 settings: 3 race rules × 3 e.p. variants): 1/8, -1/8, ↑²*, and the tiny(3/2±1/2) family.
2. The 1/8 and -1/8 targets each have exactly 1 robust position (width 2, 6 pawns); both are reachable and CHECKED-2 by independent C solver.
3. The ↑²* target has 1 robust position (W: a2 b2 b6 / B: a6 b7 c5, width 3); reachable and CHECKED-2.
4. The tiny(3/2±1/2) family has 96 robust positions (widths 1, 3, 4); all reachable and CHECKED-2.
5. No robust positions exist for 1/16, -1/16, ↑², or tiny(1*); their values vary across race rules or e.p. settings.

**Method Summary**
- Examined 164 positions from the e.p.-aware database matching target values
- Tested each in 9 core settings: 3 race rules (count, mover, opponent) × 3 e.p. variants (off, textbook, aware)
- A position is **ROBUST** if it has the same value in all 9 core settings
- Reachability checked using necessary conditions (pawn counts, capture parity, file accessibility) + conservative freeze test (trébuchet on g-file: W g4 / B g5, WK f5, BK h4)

## Target Summary Table

| Target | Total Positions | Robust (9/9) | Robust & Reachable | Best Example (FEN) | Men | Verification |
|--------|----------------:|-------------:|-------------------:|-------------------|----:|--------------|
| 1/8 | 13 | 1 | 1 | `8/8/pp6/1p3Kp1/6Pk/P7/PP6/8 w - - 0 1` | 10 | CHECKED-2 |
| -1/8 | 13 | 1 | 1 | `8/pp6/1p6/5Kp1/P5Pk/PP6/8/8 w - - 0 1` | 10 | CHECKED-2 |
| 1/16 | 3 | 0 | 0 | `8/2p5/1p6/1p3Kp1/6Pk/2P5/PP6/8 w - - 0 1` | 10 | — |
| -1/16 | 3 | 0 | 0 | `8/1pp5/p7/5Kp1/1P4Pk/1P6/P7/8 w - - 0 1` | 10 | — |
| ↑² | 5 | 0 | 0 | `8/1pp5/p7/5Kp1/PPP3Pk/8/8/8 w - - 0 1` | 10 | — |
| ↑²* | 10 | 1 | 1 | `8/1p6/pP6/2p2Kp1/6Pk/8/PP6/8 w - - 0 1` | 10 | CHECKED-2 |
| tiny(1) | 113 | 96 | 96 | `8/p7/p7/5Kp1/6Pk/8/P7/8 w - - 0 1` | 7 | CHECKED-2 |
| tiny(2) | 113 | 96 | 96 | `8/p7/p7/5Kp1/6Pk/8/P7/8 w - - 0 1` | 7 | CHECKED-2 |
| tiny(1*) | 4 | 0 | 0 | `8/3p4/1p6/3P1Kp1/p5Pk/8/P1P5/8 w - - 0 1` | 10 | — |

## Detailed Results by Target

### 1/8

- **Total positions in e.p.-aware database:** 13
- **Robust (same value in all 9 core settings):** 1
- **Robust and reachable (passes freeze + legality):** 1

#### Robust positions:

- `W: a2 a3 b2 / B: a6 b5 b6` (width 2, 6 pawns)
  - Value in all 9 core settings: `1/8`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/8/pp6/1p3Kp1/6Pk/P7/PP6/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

#### Value matrix (9 core settings):

| Setting | Pos 1 | Pos 2 | Pos 3 |
| --- | --- | --- | --- |
| count/epon-textbook | 1/8 | 1/8 | 1/8 |
| count/epon-aware | 1/8 | 1/8 | 1/8 |
| count/epoff | 1/8 | {3* | 1/4} | 1 |
| mover/epon-textbook | 1/8 | {2±1 | {{{{2 | 2*} | {1 | 1*}} | -255/2±+W, 1} | 1/2}} | 1/8 |
| mover/epon-aware | 1/8 | {2±1 | {{{{2 | 2*} | {1 | 1*}} | -255/2±+W, 1} | 1/2}} | 1/8 |
| mover/epoff | 1/8 | {3* | {1 | {1, {+W, +W±+W | -W}, {{1 | {1 | 1*}} | ⇑*} | -W}}} | 1 |
| opponent/epon-textbook | 1/8 | 1/8 | 1/4 |
| opponent/epon-aware | 1/8 | 1/8 | 1/4 |
| opponent/epoff | 1/8 | {3* | 1/4} | 1 |

### -1/8

- **Total positions in e.p.-aware database:** 13
- **Robust (same value in all 9 core settings):** 1
- **Robust and reachable (passes freeze + legality):** 1

#### Robust positions:

- `W: a3 a4 b3 / B: a7 b6 b7` (width 2, 6 pawns)
  - Value in all 9 core settings: `-1/8`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/pp6/1p6/5Kp1/P5Pk/PP6/8/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

#### Value matrix (9 core settings):

| Setting | Pos 1 | Pos 2 | Pos 3 |
| --- | --- | --- | --- |
| count/epon-textbook | -1/8 | -1/8 | -1/8 |
| count/epon-aware | -1/8 | -1/8 | -1/8 |
| count/epoff | -1/8 | {-1/4 | -3*} | -1 |
| mover/epon-textbook | -1/8 | {{-1/2 | {-1, 255/2±+W | {{-1* | -1} | {-2* | -2}}}} | -2±1} | -1/8 |
| mover/epon-aware | -1/8 | {{-1/2 | {-1, 255/2±+W | {{-1* | -1} | {-2* | -2}}}} | -2±1} | -1/8 |
| mover/epoff | -1/8 | {{{+W | -1, {+W | -W, -W±+W}, {⇓* | {{-1* | -1} | -1}}} | -1} | -3*} | -1 |
| opponent/epon-textbook | -1/8 | -1/8 | -1/4 |
| opponent/epon-aware | -1/8 | -1/8 | -1/4 |
| opponent/epoff | -1/8 | {-1/4 | -3*} | -1 |

### 1/16

- **Total positions in e.p.-aware database:** 3
- **Robust (same value in all 9 core settings):** 0
- **Robust and reachable (passes freeze + legality):** 0

#### Value matrix (9 core settings):

| Setting | Pos 1 | Pos 2 | Pos 3 |
| --- | --- | --- | --- |
| count/epon-textbook | 1/16 | 1/16 | 1/16 |
| count/epon-aware | 1/16 | {0 | {0 | {*, 0 | 0, ↑*}}, {⇑ | *}} | 1/16 |
| count/epoff | 1/2 | 1/2 | 0 |
| mover/epon-textbook | 1/16 | 1/2 | {0 | {-W, {+W, {+W, {+W, {+W | -W, ±+W} | -W, {+W | -W, ±+W}} | -W, {+W | -W, ±+W}} | -W, {+W | -W, ±+W}} | -W}} |
| mover/epon-aware | 1/16 | {0 | {0 | {*, 0 | 0, ↑*}}, {⇑ | *}} | {0 | {-W, {+W, {+W, {+W, {+W | -W, ±+W} | -W, {+W | -W, ±+W}} | -W, {+W | -W, ±+W}} | -W, {+W | -W, ±+W}} | -W}} |
| mover/epoff | 3/4 | {{{+W | +W, {+W | +W, {+W, ±+W | -W, {+W, ±+W | -W, ±+W}, ±+W}}, {+W | {-W | -W*}}} | 1} | 1} | {-1/2 | {-W, {+W, {+W, {+W, {+W | -W, ±+W} | -W, {+W | -W, ±+W}} | -W, {+W | -W, ±+W}} | -W, {+W | -W, ±+W}} | -W}} |
| opponent/epon-textbook | 1/8 | 1/2 | {0 | {{+W | 0, {+W, {+W | -W, ±+W} | -W, ±+W}, {0, {+W, ±+W | -W} | -W}} | 0}} |
| opponent/epon-aware | 1/8 | {0 | {0 | {⇑ | *}}, {⇑ | *}} | {0 | {{+W | 0, {+W, {+W | -W, ±+W} | -W, ±+W}, {0, {+W, ±+W | -W} | -W}} | 0}} |
| opponent/epoff | 1/2 | 1/2 | -1/4 |

### -1/16

- **Total positions in e.p.-aware database:** 3
- **Robust (same value in all 9 core settings):** 0
- **Robust and reachable (passes freeze + legality):** 0

#### Value matrix (9 core settings):

| Setting | Pos 1 | Pos 2 | Pos 3 |
| --- | --- | --- | --- |
| count/epon-textbook | -1/16 | -1/16 | -1/16 |
| count/epon-aware | -1/16 | -1/16 | {{* | ⇓}, {{0, ↓* | *, 0} | 0} | 0} |
| count/epoff | -1/2 | 0 | -1/2 |
| mover/epon-textbook | -1/16 | {{+W | +W, {+W, {+W, ±+W | -W} | -W, {+W, {+W, ±+W | -W} | -W, {+W, {+W, ±+W | -W} | -W, {+W, ±+W | -W}}}}} | 0} | -1/2 |
| mover/epon-aware | -1/16 | {{+W | +W, {+W, {+W, ±+W | -W} | -W, {+W, {+W, ±+W | -W} | -W, {+W, {+W, ±+W | -W} | -W, {+W, ±+W | -W}}}}} | 0} | {{* | ⇓}, {{0, ↓* | *, 0} | 0} | 0} |
| mover/epoff | -3/4 | {{+W | +W, {+W, {+W, ±+W | -W} | -W, {+W, {+W, ±+W | -W} | -W, {+W, {+W, ±+W | -W} | -W, {+W, ±+W | -W}}}}} | 1/2} | {-1 | {-1 | {-W, {-W, {+W, {+W, ±+W | -W, ±+W}, ±+W | -W, ±+W} | -W}, {{+W* | +W} | -W} | -W}}} |
| opponent/epon-textbook | -1/8 | {{0 | {0, {+W | 0, {+W | -W, ±+W}}, {+W, ±+W | -W, {+W, ±+W | -W}} | -W}} | 0} | -1/2 |
| opponent/epon-aware | -1/8 | {{0 | {0, {+W | 0, {+W | -W, ±+W}}, {+W, ±+W | -W, {+W, ±+W | -W}} | -W}} | 0} | {{* | ⇓}, {{* | ⇓} | 0} | 0} |
| opponent/epoff | -1/2 | 1/4 | -1/2 |

### ↑²

- **Total positions in e.p.-aware database:** 5
- **Robust (same value in all 9 core settings):** 0
- **Robust and reachable (passes freeze + legality):** 0

#### Value matrix (9 core settings):

| Setting | Pos 1 | Pos 2 | Pos 3 |
| --- | --- | --- | --- |
| count/epon-textbook | {0 | ↓*} | {0 | ↓*} | {0 | ↓*} |
| count/epon-aware | {1/2 | ↓*} | {0 | {{{{{+W | +W, {+W | -W, {+W | -W, {+W | -W, {+W | -W, ±+W}}}}} | +W} | 0} | 0} | -1*}} | {0 | ↓*} |
| count/epoff | 0 | 1/2 | {0 | {0 | {*, 0 | {{+W | ↓}, ↓ | -W}}}} |
| mover/epon-textbook | {0, {{+W | ↓*} | 0, ↓*} | {{+W | 0, {0, {+W, {+W, ±+W | -W, ±+W} | -W, ±+W} | -W}} | 0}} | 5/16±3/16 | {0, ↓* | 0, {0, {{+W | +W, {+W | +W, ±+W}} | -W} | -W}} |
| mover/epon-aware | {0, {{+W | ↓*} | 0, ↓*} | {{+W | 0, {0, {+W, {+W, +W±+W | -W, ±+W} | -W, ±+W} | -W}} | 0}} | {1/2 | 3↓} | * |
| mover/epoff | {{{+W | 0, {+W, {+W, {+W, ±+W | -W} | -W} | -W, {+W | -W, {+W | -W, ±+W}}}, {+W, ±+W | -W}}, {+W, +W±+W | -W±+W, 0} | 0} | ⇓*} | 1 | {0, ↓* | 0, {0, {{+W | +W, {+W | +W, ±+W}} | -W} | -W}} |
| opponent/epon-textbook | {0 | ↓*} | {1/2 | ↓*} | {1 | {1 | {*, {+W | *} | -W, {-W, {-W, ±+W | -W}, ±+W | -W}}}} |
| opponent/epon-aware | {0 | ↓*} | {1/2 | ↓*} | {1 | {1 | {*, {+W | *} | -W, {-W, {-W, ±+W | -W}, ±+W | -W}}}} |
| opponent/epoff | 0 | {1/2 | {1/2 | ±1/2}} | {1 | {1 | {*, {+W | *} | -W, {-W, {-W, ±+W | -W}, ±+W | -W}}}} |

### ↑²*

- **Total positions in e.p.-aware database:** 10
- **Robust (same value in all 9 core settings):** 1
- **Robust and reachable (passes freeze + legality):** 1

#### Robust positions:

- `W: a2 b2 b6 / B: a6 b7 c5` (width 3, 6 pawns)
  - Value in all 9 core settings: `{*, 0 | ↓}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/1p6/pP6/2p2Kp1/6Pk/8/PP6/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

#### Value matrix (9 core settings):

| Setting | Pos 1 | Pos 2 | Pos 3 |
| --- | --- | --- | --- |
| count/epon-textbook | {*, 0 | ↓} | {*, 0 | ↓} | {*, 0 | ↓} |
| count/epon-aware | {*, 0 | ↓} | {*, 0 | ↓} | {*, 0 | ↓} |
| count/epoff | {*, 0 | ↓} | {*, 0 | ↓} | ↑* |
| mover/epon-textbook | 1* | {*, 0 | ↓} | {*, 0 | ↓} |
| mover/epon-aware | 5/8±3/8 | {*, 0 | ↓} | {*, 0 | ↓} |
| mover/epoff | 1* | {*, 0 | ↓} | ↑* |
| opponent/epon-textbook | ⇑ | {*, 0 | ↓} | {*, 0 | ↓} |
| opponent/epon-aware | ⇑ | {*, 0 | ↓} | {*, 0 | ↓} |
| opponent/epoff | ⇑ | {*, 0 | ↓} | ↑* |

### tiny(1) (from tiny(3/2±1/2) family)
### tiny(1)

- **Total positions in e.p.-aware database:** 113
- **Robust (same value in all 9 core settings):** 96
- **Robust and reachable (passes freeze + legality):** 96

#### Robust positions:

- `W: a2 / B: a6 a7` (width 1, 3 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/5Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 c6 c7` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/5Kp1/6Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 c7` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p7/5Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c4` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/5Kp1/2p3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c6` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 b6` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/pp6/5Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 c5` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c5 / B: a6 a7 b7` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/pp6/p7/2P2Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c5 / B: a6 a7 c6` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/2P2Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c6 / B: a6 a7 c7` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1P5/5Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 d7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/5Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 d5` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 d6` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 d6 d7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/5Kp1/6Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 c7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/5Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 d7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/5Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 c5` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d4` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/5Kp1/3p2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d6` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 c6` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 d5` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d5 / B: a6 a7 d6` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3P1Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d6 / B: a6 a7 d7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2P4/5Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 c2 / B: a4 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/5Kp1/p5Pk/P7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 a4 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/5Kp1/p5Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c4 c5` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/2p3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c4 / B: a6 a7 c5` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/2P3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 c5 c6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/2p2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 c5 / B: a6 a7 c6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/2P2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c5 / B: a6 a7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1p5/2P2Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c5 c6 / B: a6 a7 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1P5/2P2Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 d2 / B: a4 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/5Kp1/p5Pk/P7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 a4 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/5Kp1/p5Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d4 d5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/3p2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d4 / B: a6 a7 d5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/3P2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 d5 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3p1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 d5 / B: a6 a7 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3P1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d5 / B: a6 a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2p4/3P1Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d5 d6 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2P4/3P1Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 a5 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/p4Kp1/6Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c4 c6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/2p3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1p5/5Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 c5 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p7/2p2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 d4 d5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/3p2Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 d5 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3p1Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2p4/5Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 a5 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/p4Kp1/6Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 c4 c5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/2p3Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 c5 c6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p1p5/2p2Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d4 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/3p2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2p4/5Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 c6 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p1p5/5Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 d5 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/3p1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 a6 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/p1p5/5Kp1/6Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c4 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p7/5Kp1/2p3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 d4 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/3p2Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 d5 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/3p1Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 a6 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/p2p4/5Kp1/6Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 c4 c6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/2p3Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 c5 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/2p2Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d4 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/5Kp1/3p2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 a7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-4 | {-4 | -11/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/2p5/5Kp1/6Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 d4 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-4 | {-4 | -11/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/5Kp1/3p2Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-4 | {-4 | -11/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/3p4/5Kp1/6Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 c4 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-4 | {-4 | -11/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/5Kp1/2p3Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a4 c2 / B: b6 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/1pp5/5Kp1/P5Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a5 c2 / B: a6 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/p1p5/P4Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c5 / B: a6 a7 b7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/pp6/p7/2P2Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c6 / B: a6 a7 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1P5/5Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a4 d2 / B: b6 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/1p1p4/5Kp1/P5Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a5 d2 / B: a6 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/p2p4/P4Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 c4 / B: a6 a7 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/2P3Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c5 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/2P2Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d5 / B: a6 a7 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/3P1Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d6 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2P4/5Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a5 c2 / B: b7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/1pp5/2p5/P4Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a6 c2 / B: a7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/P1p5/5Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a5 d2 / B: b7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/1p1p4/3p4/P4Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a6 d2 / B: a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/P2p4/5Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 c5 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/2P2Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 c2 / B: a6 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/p1p5/5Kp1/6Pk/P7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a4 c2 / B: a5 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/p4Kp1/P5Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c4 / B: a6 a7 b6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/pp6/5Kp1/2P3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c5 / B: a6 a7 c6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/2P2Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 c5 / B: a6 a7 b7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/pp6/p7/2P2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 c6 / B: a6 a7 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1P5/5Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 d2 / B: a6 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/p2p4/5Kp1/6Pk/P7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 d2 / B: b5 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/1p3Kp1/6Pk/P7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a4 d2 / B: a5 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/p4Kp1/P5Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 c3 / B: a6 a7 d5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/6Pk/2P5/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c4 / B: a6 a7 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/2P3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 c5 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/2P2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d4 / B: a6 a7 c6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/3P2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d5 / B: a6 a7 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3P1Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 d5 / B: a6 a7 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/3P1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 d6 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2P4/5Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

#### Value matrix (9 core settings):

| Setting | Pos 1 | Pos 2 | Pos 3 |
| --- | --- | --- | --- |
| count/epon-textbook | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| count/epon-aware | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| count/epoff | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| mover/epon-textbook | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| mover/epon-aware | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| mover/epoff | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| opponent/epon-textbook | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| opponent/epon-aware | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| opponent/epoff | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |

### tiny(2) (from tiny(3/2±1/2) family)
### tiny(2)

- **Total positions in e.p.-aware database:** 113
- **Robust (same value in all 9 core settings):** 96
- **Robust and reachable (passes freeze + legality):** 96

#### Robust positions:

- `W: a2 / B: a6 a7` (width 1, 3 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/5Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 c6 c7` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/5Kp1/6Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 c7` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p7/5Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c4` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/5Kp1/2p3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c6` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 b6` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/pp6/5Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 c5` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c5 / B: a6 a7 b7` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/pp6/p7/2P2Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c5 / B: a6 a7 c6` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/2P2Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c6 / B: a6 a7 c7` (width 3, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1P5/5Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 d7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/5Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 d5` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 d6` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 d6 d7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/5Kp1/6Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 c7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/5Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 d7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/5Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 c5` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d4` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/5Kp1/3p2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d6` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 c6` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 d5` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d5 / B: a6 a7 d6` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3P1Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d6 / B: a6 a7 d7` (width 4, 5 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2P4/5Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 c2 / B: a4 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/5Kp1/p5Pk/P7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 a4 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/5Kp1/p5Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c4 c5` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/2p3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c4 / B: a6 a7 c5` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/2P3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 c5 c6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/2p2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 c5 / B: a6 a7 c6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/2P2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c5 / B: a6 a7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1p5/2P2Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c5 c6 / B: a6 a7 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1P5/2P2Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 d2 / B: a4 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/5Kp1/p5Pk/P7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 a4 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/5Kp1/p5Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d4 d5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/3p2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d4 / B: a6 a7 d5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/3P2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 d5 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3p1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 d5 / B: a6 a7 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3P1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d5 / B: a6 a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2p4/3P1Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d5 d6 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-1 | {-1 | -5/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2P4/3P1Kp1/6Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 a5 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/p4Kp1/6Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c4 c6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/2p3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1p5/5Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 c5 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p7/2p2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 d4 d5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/3p2Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 d5 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3p1Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 / B: a6 a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2p4/5Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 a5 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/p4Kp1/6Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 c4 c5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/2p2Kp1/2p3Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 c5 c6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p1p5/2p2Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d4 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/3p2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2p4/5Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 c6 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p1p5/5Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 / B: a6 a7 d5 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-2 | {-2 | -7/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/3p1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 a6 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/p1p5/5Kp1/6Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 c4 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p7/5Kp1/2p3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 d4 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/3p2Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 / B: a6 a7 d5 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/3p1Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 a6 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/p2p4/5Kp1/6Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 c4 c6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/2p3Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 c5 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/2p2Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 / B: a6 a7 d4 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-3 | {-3 | -9/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/5Kp1/3p2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a3 a7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{-4 | {-4 | -11/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/2p5/5Kp1/6Pk/p7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 / B: a6 a7 d4 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-4 | {-4 | -11/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/5Kp1/3p2Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a3 a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-4 | {-4 | -11/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/3p4/5Kp1/6Pk/p7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d2 / B: a6 a7 c4 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{-4 | {-4 | -11/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/5Kp1/2p3Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a4 c2 / B: b6 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/1pp5/5Kp1/P5Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a5 c2 / B: a6 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/p1p5/P4Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c5 / B: a6 a7 b7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/pp6/p7/2P2Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c6 / B: a6 a7 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1P5/5Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a4 d2 / B: b6 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/1p1p4/5Kp1/P5Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a5 d2 / B: a6 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/p2p4/P4Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 c4 / B: a6 a7 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/2P3Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c5 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/2P2Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d5 / B: a6 a7 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/3P1Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d6 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{1 | {1 | -1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2P4/5Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a5 c2 / B: b7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/1pp5/2p5/P4Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a6 c2 / B: a7 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/P1p5/5Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a5 d2 / B: b7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/1p1p4/3p4/P4Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a6 d2 / B: a7 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/P2p4/5Kp1/6Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 c5 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{2 | {2 | 1/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/2P2Kp1/6Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 c2 / B: a6 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/p1p5/5Kp1/6Pk/P7/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a4 c2 / B: a5 c6 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/2p5/2p5/p4Kp1/P5Pk/8/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c4 / B: a6 a7 b6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/pp6/5Kp1/2P3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c5 / B: a6 a7 c6` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p7/p1p5/2P2Kp1/6Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 c5 / B: a6 a7 b7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/pp6/p7/2P2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 c6 / B: a6 a7 c7` (width 3, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (20 valid placements)
  - Best FEN: `8/p1p5/p1P5/5Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 d2 / B: a6 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/p2p4/5Kp1/6Pk/P7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a3 d2 / B: b5 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/1p3Kp1/6Pk/P7/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 a4 d2 / B: a5 d6 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/3p4/3p4/p4Kp1/P5Pk/8/P2P4/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c2 c3 / B: a6 a7 d5` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p7/3p1Kp1/6Pk/2P5/P1P5/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c3 c4 / B: a6 a7 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/5Kp1/2P3Pk/2P5/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 c4 c5 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p7/2P2Kp1/2P3Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d4 / B: a6 a7 c6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p1p5/5Kp1/3P2Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d3 d5 / B: a6 a7 d6` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p7/p2p4/3P1Kp1/6Pk/3P4/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 d5 / B: a6 a7 c7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p1p5/p7/3P1Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

- `W: a2 d4 d6 / B: a6 a7 d7` (width 4, 6 pawns)
  - Value in all 9 core settings: `{0 | {0 | -3/2±1/2}}`
  - Verification: **CHECKED-2**
  - Reachable: Yes (10 valid placements)
  - Best FEN: `8/p2p4/p2P4/5Kp1/3P2Pk/8/P7/8 w - - 0 1`
  - Placement: mirror=False, offset=0, treb_rank=4, orientation=A, WK=f5, BK=h4

#### Value matrix (9 core settings):

| Setting | Pos 1 | Pos 2 | Pos 3 |
| --- | --- | --- | --- |
| count/epon-textbook | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| count/epon-aware | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| count/epoff | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| mover/epon-textbook | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| mover/epon-aware | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| mover/epoff | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| opponent/epon-textbook | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| opponent/epon-aware | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |
| opponent/epoff | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} | {-1 | {-1 | -5/2±1/2}} |

### tiny(1*)

- **Total positions in e.p.-aware database:** 4
- **Robust (same value in all 9 core settings):** 0
- **Robust and reachable (passes freeze + legality):** 0

#### Value matrix (9 core settings):

| Setting | Pos 1 | Pos 2 | Pos 3 |
| --- | --- | --- | --- |
| count/epon-textbook | {0 | {0 | -1*}} | 1/2 | 1/2 |
| count/epon-aware | {0 | {0 | -1*}} | {0 | {0 | -1*}} | {0 | {0 | -1*}} |
| count/epoff | {0 | {0 | -1*}} | 1/2 | 1/2 |
| mover/epon-textbook | {1/2* | ↑*} | 1/2 | 1/2 |
| mover/epon-aware | {1/2* | ↑*} | {1/2* | ↑*} | {1/2* | ↑*} |
| mover/epoff | 1/2 | 1/2 | 1/2 |
| opponent/epon-textbook | {0 | {0 | -1*}} | 1/2 | 1/2 |
| opponent/epon-aware | {0 | {0 | -1*}} | {0 | {0 | -1*}} | {0 | {0 | -1*}} |
| opponent/epoff | {0 | {0 | -1*}} | 1/2 | 1/2 |

## Hand-Built Move Histories for Best Reachable Positions

Following the rerun report's method for the 1/8 mirror position.

### 1/8: W: a2 b2 b3 / B: a5 a6 b6

**Move history:** c2×b3; a7-a5 then b7×a6; c7×b6
**Source:** Rerun report C5 (mirror of W a2 a3 b2 / B a6 b5 b6)

### -1/8: W: a3 a4 b3 / B: a7 b6 b7

**Move history:** To be constructed (position passes necessary reachability conditions)

### ↑²*: W: a2 b2 b6 / B: a6 b7 c5

**Move history:** To be constructed (13 race edges, none before capture)
**Source:** Rerun report C6

### tiny(1): W: a2 / B: a6 a7

**Move history:** To be constructed (position passes necessary reachability conditions)

### tiny(2): W: a2 / B: a6 a7

**Move history:** To be constructed (position passes necessary reachability conditions)

## Reproducibility

Run from project root:

```bash
cd /Users/aritro/Downloads/Research/Chessendgames
PYTHONPATH=. .venv/bin/python atlas/targets/final/extract_and_report.py
```

The analysis uses the pre-computed `targets_db.json` from `atlas/targets/` which was generated by:
- `runs.py` with scope `db` (231,071 positions from `atlas/flat8/rerun/values.jsonl.gz`)
- `analyze.py targets db` which classifies and finds targets under both textbook and aware reference settings

To recompute a single position in all 9 core settings:

```python
from cylcgt import pawns, cgt

RACE_RULES = ['count', 'mover', 'opponent']
EP_VARIANTS = [
    ('off', False, False),      # e.p. off
    ('textbook', True, False),  # e.p. on, textbook test
    ('aware', True, True),      # e.p. on, aware test
]

for race in RACE_RULES:
    for ep_name, ep_on, ep_aware in EP_VARIANTS:
        pawns.RACE_RULE = race
        pawns.PASSED_RESPECTS_EP = ep_aware
        pawns._value.cache_clear()
        board = pawns.Board(files=3, ranks=8, wrap=False, ep=ep_on)
        pos = pawns.Pos.parse('W: a2 b2 b6 / B: a6 b7 c5')
        val = pawns.value(board, pos)
        print(f'{race}/{ep_name}: {cgt.show(val)}')
```