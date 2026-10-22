# Rules for Chess on the Möbius Strip and the Klein Bottle

This document specifies the exact movement and pawn rules for chess on two non-orientable board topologies.

## 1. Board Geometry

### 1.1 Möbius Strip (8×8)
- **Files:** 8 files labelled a–h. File h is glued to file a with a half-twist: square (h, r) is identified with (a, 9−r) for r = 1..8.
- **Ranks:** 8 ranks labelled 1–8, **not** glued. The board has two boundaries: rank 1 and rank 8.
- **Coordinates:** A square is (f, r) with f ∈ {0..7} (a=0, ..., h=7), r ∈ {1..8}.
- **Neighbour across the seam:**
  - (7, r) → right neighbour is (0, 9−r)
  - (0, r) → left neighbour is (7, 9−r)

### 1.2 Klein Bottle (8×8)
- **Files:** Same Möbius gluing as above: (h, r) ~ (a, 9−r).
- **Ranks:** Ranks 1 and 8 are glued straight (no twist): (f, 8) ~ (f, 1) for all f.
- **Coordinates:** (f, r) with f ∈ {0..7}, r ∈ {0..7} (0-based for modular arithmetic).
- **Neighbour across file seam:** (7, r) ↔ (0, (8−r) mod 8) [with ranks 0..7, the formula is (0, 7−r)].
- **Neighbour across rank seam:** (f, 7) ↑ → (f, 0); (f, 0) ↓ → (f, 7).

## 2. Piece Movement

### 2.1 King
Moves one step in any of the 8 directions, with wraparound following the board topology.
- On the Möbius strip: vertical moves (↑/↓) stop at ranks 1 and 8 (no rank wraparound). Horizontal and diagonal moves wrap across the file seam with the rank flip.
- On the Klein bottle: all 8 directions wrap (files with flip, ranks without flip).

### 2.2 Knight
Standard (2,1) leaps. The target square is computed by applying the file and rank offsets with the board's wraparound rules.
- Möbius: file offset wraps with rank flip; rank offset does not wrap (knight cannot jump off rank 1 or 8).
- Klein bottle: both offsets wrap (file with flip, rank without flip).

### 2.3 Sliders (Rook, Bishop, Queen)
A slider ray proceeds step by step in its direction. At each step the coordinate transformation for that direction is applied.
- The ray **stops** when the next square would be the slider's own starting square (i.e., a full loop returns to origin). This prevents a "null move" where a rook circles the rank/file and returns to its square.
- On the Möbius strip:
  - Horizontal rays (←/→) wrap across the file seam with rank flip, and continue until they would return to the start square.
  - Vertical rays (↑/↓) do not wrap; they stop at the board edge.
  - Diagonal rays wrap across the file seam with rank flip; the rank component does not wrap, so the ray terminates at rank 1 or 8.
- On the Klein bottle:
  - All rays wrap in both dimensions (file with flip, rank without flip).
  - A ray stops when it would return to the starting square.

### 2.4 Pawns
- **Forward direction:** White moves toward rank 8 (+1 rank), Black toward rank 1 (−1 rank).
- **Capture:** Diagonally forward-left and forward-right, with file wraparound per the board topology.
- **Double step:** From starting rank (White rank 2, Black rank 7) if both squares are empty.
- **En passant:** Standard, with the capture square computed using the board's geometry.
- **Promotion:** On reaching the last rank (White rank 8, Black rank 1) — **but see §3 for the seam-crossing convention.**

## 3. Pawn Seam-Crossing Convention (Möbius Strip Only)

On the Möbius strip, a pawn that captures across the twisted seam (from file h to file a or vice versa) arrives on a square whose rank is flipped (r → 9−r). This creates an ambiguity: does the pawn continue moving in its original "forward" direction, or does "forward" reverse because the board is twisted?

**Convention adopted:** A pawn that crosses the twisted seam **reverses its forward direction**.

### Justification
1. **Topological consistency:** On a Möbius strip, a vector transported once around the strip returns reversed. A pawn's "forward" is a tangent vector along the rank direction; crossing the seam once flips it.
2. **No edge pawns:** On the cylinder, all files are equivalent and there are no edge files. On the Möbius strip, the same holds — every file is equivalent — but the twist means that a pawn circling the board returns to its file facing the opposite direction. Allowing the direction to flip preserves file equivalence.
3. **Promotion remains well-defined:** A White pawn that crosses the seam an odd number of times moves "toward rank 1" (the opposite promotion rank). It will eventually promote on rank 1 (Black's home rank), which is now its forward edge. A pawn crossing an even number of times promotes normally on rank 8.
4. **Alternative rejected:** "Pawns may not cross the seam" would break file equivalence and create artificial edge files. "Forward never flips" would mean a pawn circling the board promotes on the same physical edge it started from, which is topologically inconsistent.

### Formal Rule
- Each pawn carries a **direction flag**: +1 (toward rank 8) or −1 (toward rank 1). Initially White = +1, Black = −1.
- When a pawn makes a **capturing move** that crosses the file seam (i.e., its file changes from 7→0 or 0→7 via the Möbius identification), its direction flag is multiplied by −1.
- Non-capturing moves (single/double step) never cross the file seam because they only change rank.
- Promotion occurs when a pawn reaches the rank corresponding to its current direction flag: rank 8 if flag = +1, rank 1 if flag = −1.
- En passant capture across the seam also flips the capturing pawn's direction flag.

### Klein Bottle
The Klein bottle's file seam is the same Möbius twist, so the **same convention applies**: capturing across the file seam flips the pawn's forward direction. The rank seam (1↔8) is a straight gluing, so crossing it does not flip direction.

## 4. Additional Rules
- **No castling.**
- **No 50-move rule** (DTM tablebases).
- **Stalemate is a draw.**
- **Bare kings are a draw.**
- **Rook null-move prohibition:** A rook (or queen/rook component) may not make a full loop around a closed rank/file and return to its starting square as a legal move. The ray stops before the starting square.
- **Legality:** A position is legal (for the side to move) if:
  - All pieces occupy distinct squares.
  - Kings are not adjacent (including across glued edges).
  - The side not to move is not in check.

## 5. Coordinate Implementation (0-based)

For implementation, use 0-based coordinates: f ∈ {0..7}, r ∈ {0..7} (rank 1 = 0, rank 8 = 7).

### Möbius Strip
```c
// step from (f, r) by (df, dr)
int f2 = (f + df) & 7;  // wrap files
int r2 = r + dr;        // no rank wrap
if (r2 < 0 || r2 >= 8) return -1;  // off board
// if file wrapped (df != 0 and (f+df) outside 0..7), flip rank
if (wrapF && (f + df < 0 || f + df >= 8)) {
    r2 = 7 - r2;  // rank flip: 0↔7, 1↔6, ...
    if (r2 < 0 || r2 >= 8) return -1;
}
return r2 * 8 + f2;
```

### Klein Bottle
```c
// step from (f, r) by (df, dr)
int f2 = (f + df) & 7;
int r2 = (r + dr) & 7;
// if file wrapped, flip rank
if (df != 0 && (f + df < 0 || f + df >= 8)) {
    r2 = (7 - r2) & 7;  // flip then wrap rank
}
return r2 * 8 + f2;
```

## 6. Summary of Differences from Cylinder/Torus

| Feature | Plane | Cylinder | Torus | Möbius Strip | Klein Bottle |
|---------|-------|----------|-------|--------------|--------------|
| File wrap | No | Yes (straight) | Yes (straight) | Yes (twisted) | Yes (twisted) |
| Rank wrap | No | No | Yes (straight) | No | Yes (straight) |
| King moves | 8 dir, bounded | 8 dir, file wrap | 8 dir, both wrap | 8 dir, file wrap+flip | 8 dir, both wrap (file flip) |
| Knight moves | bounded | file wrap | both wrap | file wrap+flip | both wrap (file flip) |
| Slider rays | bounded | file wrap, stop at loop | both wrap, stop at loop | file wrap+flip, stop at loop/rank edge | both wrap (file flip), stop at loop |
| Pawn forward | fixed | fixed | fixed | **flips on seam capture** | **flips on file seam capture** |
| Promotion rank | fixed | fixed | fixed | **depends on seam crossings** | **depends on file seam crossings** |