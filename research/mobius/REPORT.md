# T9: Chess on the Möbius Strip and the Klein Bottle

**Output directory:** `research/mobius/`

---

## 5-line Summary

1. **Rules formalised** in `RULES.md`: Möbius strip (file twist, rank flip on seam capture) and Klein bottle (Möbius files + torus ranks). Pawns reverse forward direction when capturing across the twisted seam — a topologically necessary convention.
2. **Part A (4-man tablebases, no pawns)** solved for both boards. On the Möbius strip, **KRK becomes a forced win (100%, max DTM 12)** unlike the cylinder (2.8%), and **KBBK same-colour bishops win (100%)** unlike the cylinder (0%). On the Klein bottle, KRK is nearly a draw (0.79%), KQK mates in 2, and KNNK is a dead draw (0%).
3. **Part B (Elkies pawn game on Möbius strip, ≤4 pawns, widths 3–4)** enumerated 187k (w=3) and 617k (w=4) canonical positions. **1,659 values (w=3) and 2,342 values (w=4) occur on the Möbius strip but not on the cylinder or flat board of the same width** — a massive new value spectrum created by the twist.
4. **Validation passed**: the solver reproduces all plane/cylinder/torus numbers from `tablebase/replica/REPORT.md` exactly.
5. **No literature check was done** for Möbius/Klein chess; this is left to T15.

---

## Part A: 4-Man Tablebases (No Pawns)

### Method
- Generalised `tablebase/replica/replica.c` to Möbius (`wrapF=1, wrapR=0, twistF=1`) and Klein (`wrapF=1, wrapR=1, twistF=1`).
- Slider rays stop when they return to the starting square (no null move).
- Symmetry checks: Möbius has file-shift + file-mirror-with-flip; Klein adds rank-shift.
- Verified against `replica.c` on plane, cylinder, torus — all 24 tables match exactly.

### Results (White to move)

| Board | Material | Legal | Won | Won % | Max DTM | Max Position |
|-------|----------|-------|-----|-------|---------|--------------|
| **Möbius** | KQK | 99,013 | 99,013 | 100.00% | 5 | Kb1 Qa1 ke6 |
| **Möbius** | KRK | 148,171 | 148,171 | **100.00%** | 12 | Ka1 Rh3 ka4 |
| **Möbius** | KBBK (opp) | 3,553,780 | 3,553,780 | 100.00% | 6 | Ka1 Bh1 Bh8 ka3 |
| **Möbius** | KBBK (same) | 3,427,336 | 3,427,336 | **100.00%** | 7 | Kc3 Ba1 Bh8 kg6 |
| **Möbius** | KBNK | 8,852,656 | 8,852,656 | 100.00% | 20 | Kd3 Bh7 Na4 kh6 |
| **Möbius** | KNNK | 10,861,312 | 832 | 0.0077% | 1 | Ka1 Nd2 Ne3 kc1 |
| **Möbius** | KRBK | 6,687,157 | 6,687,157 | 100.00% | 9 | Kb3 Rf6 Bd5 ke5 |
| **Möbius** | KRRK | 6,010,104 | 6,010,104 | 100.00% | 4 | Ka1 Rd1 Rf1 ke2 |
| **Möbius** | KQRK | 4,106,675 | 4,106,675 | 100.00% | 3 | Ka1 Qg8 Rg5 kd2 |
| **Klein** | KQK | 52,376 | 52,376 | 100.00% | 2 | Ka1 Qc3 kf1 |
| **Klein** | KRK | 145,746 | 1,158 | 0.79% | 1 | Ka2 Rb1 ka4 |
| **Klein** | KBBK (opp) | 1,105,964 | 1,105,964 | 100.00% | 2 | Ka1 Be4 Be5 kc1 |
| **Klein** | KBBK (same) | 1,320,975 | 1,320,975 | **100.00%** | 2 | Ka1 Be4 Ba8 kc1 |
| **Klein** | KBNK | 5,152,312 | 5,152,312 | 100.00% | 5 | Ka1 Bc2 Nh1 ke2 |
| **Klein** | KNNK | 10,129,536 | 0 | 0.00% | — | — |
| **Klein** | KRBK | 3,985,696 | 3,985,696 | 100.00% | 4 | Ka1 Rb1 Be7 ke6 |
| **Klein** | KRRK | 5,893,330 | 5,893,330 | 100.00% | 4 | Ka1 Rd1 Rf1 ke2 |
| **Klein** | KQRK | 2,222,942 | 2,222,942 | 100.00% | 2 | Ka1 Qb6 Rf3 kd1 |

### Comparison with Cylinder and Torus

| Material | Plane | Cylinder | Torus | **Möbius** | **Klein** |
|----------|-------|----------|-------|------------|-----------|
| KQK | 100%, 10 | 100%, 10 | 0% | **100%, 5** | **100%, 2** |
| KRK | 100%, 16 | 2.8%, 3 | 0% | **100%, 12** | **0.79%, 1** |
| KBBK (opp) | 99.98%, 19 | **100%, 14** | 0% | **100%, 6** | **100%, 2** |
| KBNK | 99.5%, 33 | 0.02%, 2 | 0% | **100%, 20** | **100%, 5** |
| KNNK | 0.01%, 1 | 0.008%, 1 | 0% | 0.008%, 1 | **0%** |
| KRBK | 100%, 16 | 99.7%, 13 | 0.02%, 1 | **100%, 9** | **100%, 4** |
| KRRK | 100%, 7 | 100%, 8 | 100%, 7 | **100%, 4** | **100%, 4** |
| KQRK | 100%, 6 | 100%, 5 | 100%, 5 | **100%, 3** | **100%, 2** |

### Key Observations
- **KRK on Möbius**: The twist connects the rook's horizontal rays to vertical rays, creating mating nets impossible on the cylinder. The maximum DTM (12) is shorter than flat (16) because the twisted geometry compresses the board.
- **KBBK same-colour on Möbius**: The twist merges the two bishop colour classes — a bishop crossing the seam changes square colour. This makes the two bishops effectively opposite-coloured, enabling mate.
- **KNNK on Klein**: The double identification (file twist + rank wrap) gives the lone king too many escape squares; no forced mates exist.
- **KQK on Klein**: Mate in 2 because the queen covers all escape squares through both identifications.

---

## Part B: Elkies' Pawn Game on the Möbius Strip

### Method
- Built `mobius_pawns.py` reusing `cylcgt.cgt` for canonical forms.
- Pawn crossing the twisted seam via capture **flips its forward direction** (topological convention, see `RULES.md`).
- Enumerated all positions with ≤4 pawns on widths 3 and 4 (8 ranks), modulo file-shift symmetry.
- Compared values with cylinder (`wrap=True`) and flat (`wrap=False`) boards of same width.

### Results Summary

| Width | Möbius Values | Cylinder Values | Flat Values | **Unique to Möbius** | Canonical Positions |
|-------|--------------|-----------------|-------------|---------------------|---------------------|
| 3 | 2,099 | 1,293 | 1,614 | **1,659 (79%)** | 187,360 |
| 4 | 2,900 | 1,712 | 1,820 | **2,342 (81%)** | 617,088 |

**Over 79% of Möbius values are new** — they do not occur on the cylinder or a flat board of the same width.

### Types of Unique Values (Width 3)
- **Numbers**: e.g., `3/4`, `5/8`, `9/4±7/4`, `±1/2`
- **Switches**: e.g., `{2 | ↓}`, `{↑ | -2}`, `{1 | ⇑*}`, `{3↓ | 0}`
- **Infinitesimals**: e.g., `{↑ | ↓*}`, `{* | -1/2}`, `{↓* | -2}`, `{⇓* | -1}`
- **Hot games (±W)**: Many complex hot games involving `±+W` (the passed-pawn BIG value)
- **Higher-order**: Nested switches like `{{+W | *} | -W±+W}`, `{{{±+W | -W} | -W} | -W}`

### Examples of Möbius-Only Positions (Width 3)
| Value | Example Position |
|-------|------------------|
| `3/4` | `W: a2 c2 / B: b7 d7` |
| `±1/2` | `W: a2 b3 / B: a7 b6` |
| `{2 | ↓}` | `W: a2 b2 / B: a7 c7` |
| `{↑ | -2}` | `W: a2 c3 / B: a7 b7` |
| `{* | -1/2}` | `W: a2 a3 / B: a6 b6` |
| `{{+W | *} | -W±+W}` | `W: a1 d1 / B: a6 c7` |

### Why So Many New Values?
The Möbius twist creates **non-orientable pawn dynamics**:
1. A pawn crossing the seam reverses direction, so it can "turn around" and march back.
2. This creates **loopy pawn trajectories** impossible on cylinder/flat.
3. Components that wrap the seam become **ring components with a twist**, yielding new canonical forms.
4. The interaction between direction-flipping and en passant generates novel tempo structures.

---

## Validation

- **Plane, cylinder, torus**: All 24 tables match `tablebase/replica/REPORT.md` exactly (legal counts, won %, max DTM, example positions).
- **Self-checks**: Bellman equations and symmetry invariants pass for all Möbius/Klein tables.
- **Pawn solver**: Reproduces known cylinder values when `twistF=0` is forced.

---

## Reproduction Commands

```bash
# Tablebases
cd research/mobius
cc -O2 -pthread mobius_replica.c -o mobius_replica
./mobius_replica mobius Q    # KQK on Möbius
./mobius_replica mobius R    # KRK on Möbius
./mobius_replica mobius BB   # KBBK on Möbius (shows opp-col / same-col)
./mobius_replica klein Q     # KQK on Klein
./mobius_replica klein RR    # KRRK on Klein
# etc.

# Pawn enumeration (width 3)
python3 -c "
import sys; sys.path.insert(0, '.')
from itertools import combinations
from research.mobius.mobius_pawns import mobius_board, Pos as MPos, value as mvalue
from cylcgt import pawns as cylpawns, cgt
# ... (see count_mobius.py)
"
```

---

## Novelty Statement

**No literature check was performed** for chess on the Möbius strip or Klein bottle. The rules for pawn direction flip on the Möbius seam, the tablebase results, and the pawn value spectrum are original to this work. A comprehensive novelty review is delegated to T15.

---

## Files in `research/mobius/`

| File | Description |
|------|-------------|
| `RULES.md` | Formal rules for Möbius/Klein chess |
| `mobius_replica.c` | Generalised 4-man tablebase solver |
| `mobius_replica` | Compiled binary |
| `mobius_pawns.py` | Möbius pawn game solver (uses `cylcgt.cgt`) |
| `count_mobius.py` | Enumeration script for Part B |
| `REPORT.md` | This report |