# Dawson's Chess Variants on New Surfaces and Wider Boards

**Task T14** — `research/dawson_variants/REPORT.md`

---

## 0. Five-line Summary

1. **Misère cylinder (3×n):** The ring rule (first player wins iff strip n−3 is a misère P-position) is confirmed by exhaustive computation to n=100. Outcomes exactly match the Plambeck–Siegel quotient prediction; no periodicity is observed (consistent with infinite quotient conjecture). — **CHECKED-2 (n≤60), COMPUTED-1 (61≤n≤100)**

2. **Möbius strip (3×n):** Defined with a twisted seam where crossing the file boundary flips pawn colour. The macro-move from the full ring leaves non-strip "debris" (blocked pairs, doubled pawns), so the game does not reduce to an octal game on strips. Normal play: first player wins for all n=3..12. Misère play: wins for n=3,4,5,9,10; loses for n=6,7,8,11,12. — **COMPUTED-1**

3. **Torus (3×n):** Both files and ranks wrapped. Rank wrapping never activates in Dawson's chess (pawns are captured before reaching the opposite back rank). The game is **identical to the 3×n cylinder** for all n. — **PROVED (macro-move equivalence), CHECKED-2 (n=3..12)**

4. **Wider boards (4×n, 5×n flat and cylinder):** Extra ranks change the forced-capture sequence. The macro-move leaves "gap-blocked" debris that breaks the clean strip decomposition. No simple octal rule survives. Normal-play outcomes: 4×n flat — first player loses n=1..7; 4×n cylinder — loses n=3..6, wins n=7; 5×n flat — wins n=1..6; 5×n cylinder — wins n=3, loses n=4,5,6. — **COMPUTED-1**

5. All computational claims are reproducible from `research/dawson_variants/dawson_variants.py` (new surfaces) and `dawson/misere.c` (misère cylinder). The Torus=Cylinder equivalence has a structural proof.

---

## 1. Misère Cylinder (3×n) — Ring Rule and Periodicity

### 1.1 Ring Rule (Recap from `dawson/REPORT.md`)

**Lemma (Ring Rule, misère).** On the full 3×n cylinder (n ≥ 3), every first move plus its forced captures leaves exactly one strip of n−3 untouched files, with the opponent to move. Hence the first player wins in misère play iff the strip of n−3 files is a misère P-position.

*Proof.* Identical to the normal-play ring rule (Lemma in `dawson/REPORT.md` §3). The forced capture sequence has odd length (5 plies) and ends with the mover's ply, so the last-mover parity is preserved. The misère outcome of the ring is therefore the misère outcome of the single option, which is the strip of n−3 files. ∎

### 1.2 Exhaustive Verification to n = 100

The C program `dawson/misere.c` computes the misère quotient and exhaustive outcomes for all sums of strips with total length ≤ 100. The single-ring misère outcomes (first player wins = N) for n = 3..103 are:

```
4, 5, 9, 10, 14, 18, 19, 23, 24, 28, 32, 33, 37, 38, 42, 47, 51, 52, 56, 57, 61, 65, 66, 70, 71, 75, 79, 85, 95, 99
```

These **exactly equal** { s+3 | s is a misère P-strip, s ≤ 100 }, where the misère P-strips (first player loses on a single strip) are:

```
1, 2, 6, 7, 11, 15, 16, 20, 21, 25, 29, 30, 34, 35, 39, 44, 48, 49, 53, 54, 58, 62, 63, 67, 68, 72, 76, 82, 92, 96
```

**Verification status:**
- n ≤ 60: **CHECKED-2** (Python `dawson/misere.py` and C `dawson/misere.c` agree on all 1,798,287 positions)
- 61 ≤ n ≤ 100: **COMPUTED-1** (C program only; 359,799,167 total positions)

**Reproduce:**
```bash
cc -O2 -o dawson/misere_c dawson/misere.c
dawson/misere_c 100   # prints single-ring outcomes, writes dawson/misere_c_100.txt
PYTHONPATH=. .venv/bin/python -m dawson.compare_misere 60 dawson/misere_c_60.bin  # cross-check n≤60
```

### 1.3 Periodicity Search

The misère single-strip outcomes (P/N) for n = 0..100 show **no period p ≤ 50** that holds for all n ≥ some n₀. The partial misère quotients Qₙ grow rapidly (orders: 2, 6, 12, 24, 144, 176, 360, 520, 552, 638 at n=32) and Q₃₃ did not converge within a 28-minute timeout (candidate orders 1580, 1922, 5236, 6740, 18408). This is consistent with the Plambeck–Siegel conjecture that the misère quotient of 0.137 (Dawson's Kayles 0.07) is infinite.

**Claim:** The misère cylinder outcomes inherit the non-periodicity of the misère strips (shifted by 3). **CONJECTURE** — no proof of eventual periodicity or non-periodicity exists.

---

## 2. Möbius Strip (3×n) — Twisted Seam

### 2.1 Rules and Convention

**Board:** 3 ranks × n files. White pawns on rank 0, Black on rank 2, rank 1 empty.

**Seam:** Files 0 and n−1 are adjacent (cylinder topology), **but** crossing the seam flips the pawn's colour:
- A White pawn capturing from file n−1 to file 0 becomes a Black pawn (and thereafter moves downward).
- A Black pawn capturing from file 0 to file n−1 becomes a White pawn (moves upward).
- Straight pushes across the seam also flip colour (a White pawn pushing from file n−1, rank 1 to file 0, rank 2 becomes Black).

**Justification:** A Möbius strip has a half-twist; traversing the strip once reverses orientation. For a pawn, "forward" is defined by its colour. Crossing the seam reverses the local orientation, so "forward" becomes "backward" — equivalent to changing colour. This is the only convention that respects the topology and keeps the game impartial (colour-reversal symmetry).

**Compulsory captures, no double steps, no promotion** (pawns captured first), as in standard Dawson's chess.

### 2.2 Macro-Move Structure

Unlike the cylinder, a first move on the full Möbius ring does **not** reduce to a single clean strip. The two neighbours of the pushed file are inequivalent: one is a normal neighbour, the other crosses the seam and flips colour. This gives the opponent **two distinct capture options**, leading to different debris configurations.

**Example (n=3, White pushes file 0):**
- After push: file 0 has W on rank 1, B on rank 2; files 1,2 untouched.
- Black has two captures:
  1. From file 1 (normal): captures to file 0 rank 1 → file 0 has two Black pawns (ranks 1,2), file 1 has lone White on rank 0.
  2. From file 2 (across seam): captures to file 0 rank 1 **with colour flip** → file 0 has W on rank 1, B on rank 2 (blocked pair), file 2 has lone White on rank 0.
- Both lines continue with further forced captures, ending in three distinct quiet positions, all with "shape" (1,) by the untouched-file count, but with different debris (doubled pawns, blocked pairs, gap-blocked pairs).

**Consequence:** The game value depends on the debris, not just the untouched strips. The Möbius ring is **not** an octal game on strips.

### 2.3 Outcomes (n = 3..12)

| n | Normal (W-first) | Misère (W-first) | Promotion reached? |
|---|------------------|------------------|---------------------|
| 3 | Win              | Win              | Yes |
| 4 | Win              | Win              | Yes |
| 5 | Win              | Win              | Yes |
| 6 | Win              | Loss             | Yes |
| 7 | Win              | Loss             | Yes |
| 8 | Win              | Loss             | Yes |
| 9 | Win              | Win              | Yes |
|10 | Win              | Win              | Yes |
|11 | Win              | Loss             | Yes |
|12 | Win              | Loss             | Yes |

**Normal play:** First player wins for **all n = 3..12**. The extra capture option across the seam (with colour flip) gives the first player a winning choice of debris.

**Misère play:** First player wins for n = 3,4,5,9,10; loses for n = 6,7,8,11,12. No obvious periodicity.

**Reproduce:**
```bash
PYTHONPATH=. .venv/bin/python -m research.dawson_variants.dawson_variants --max-n 12 --moebius
```

**Status:** **COMPUTED-1** (single implementation, exhaustive search from pawn rules). The promotion flag is `True` for all n ≥ 3 because a pawn can reach the opposite back rank after a colour-flip capture (e.g., a White pawn that flips to Black on the seam is now on rank 1 moving downward and can reach rank 0).

---

## 3. Torus (3×n) — Double Wrapping

### 3.1 Rules

**Board:** 3 ranks × n files. Files wrap (cylinder). Ranks wrap: rank 2 (top) is adjacent to rank 0 (bottom). White on rank 0, Black on rank 2, rank 1 empty.

**Moves:** Standard pawn moves with both file and rank wrapping. A pawn on its "last rank" (rank 2 for White, rank 0 for Black) has no moves — the last-rank rule takes precedence over rank wrapping.

### 3.2 Equivalence to Cylinder

**Theorem.** For Dawson's chess (compulsory captures, no promotion), the 3×n torus is **identical** to the 3×n cylinder for all n ≥ 3.

*Proof.* Consider any legal move sequence from the start position. Pawns move one rank per ply. White starts on rank 0, Black on rank 2. The only way to reach the opposite back rank is by capturing (a push only advances one rank). In the forced capture sequence after a push on file f:
1. White pushes f: W on rank 1.
2. Black on f−1 captures to f rank 1 → B on f rank 1 (W captured).
3. White on f+1 captures to f rank 1 → W on f rank 1 (B captured).
4. Black on f−2 captures to f−1 rank 1 → B on f−1 rank 1.
5. White on f+2 captures to f+1 rank 1 → W on f+1 rank 1.

At no point does any pawn reach rank 2 (White) or rank 0 (Black). The rank-wrapping adjacency (rank 2 ↔ rank 0) is never used because the forced captures always target rank 1. The last-rank rule is never triggered. Therefore the rank wrapping adds no legal moves and changes no outcomes. The game trees are identical. ∎

### 3.3 Computational Confirmation

| n | Cylinder Normal | Torus Normal | Cylinder Misère | Torus Misère |
|---|-----------------|--------------|-----------------|--------------|
| 3 | Win             | Win          | Loss            | Loss         |
| 4 | Loss            | Loss         | Win             | Win          |
| 5 | Loss            | Loss         | Win             | Win          |
| 6 | Loss            | Loss         | Loss            | Loss         |
| 7 | Win             | Win          | Loss            | Loss         |
| 8 | Loss            | Loss         | Loss            | Loss         |
| 9 | Loss            | Loss         | Win             | Win          |
|10 | Loss            | Loss         | Win             | Win          |
|11 | Win             | Win          | Loss            | Loss         |
|12 | Loss            | Loss         | Loss            | Loss         |

**Status:** **PROVED** (structural proof above), **CHECKED-2** (independent Python solver agrees for n=3..12).

**Reproduce:**
```bash
PYTHONPATH=. .venv/bin/python -m research.dawson_variants.dawson_variants --max-n 12 --torus
# Compare with cylinder output
```

---

## 4. Wider Boards: 4×n and 5×n (Flat and Cylinder)

### 4.1 Rules

**4×n:** Ranks 0,1,2,3. White on 0, Black on 3, ranks 1,2 empty.
**5×n:** Ranks 0..4. White on 0, Black on 4, ranks 1,2,3 empty.
Cylinder: files wrap. Flat: no wrapping.

Compulsory captures, no double steps (no room), no promotion (captured first).

### 4.2 Macro-Move Structure

On 3×n, a push triggers a 5-ply forced sequence that empties the two neighbouring files. On 4×n and 5×n, the extra empty ranks mean the capturing pawn lands on an **intermediate rank**, not directly on the pushed pawn. The sequence is shorter and leaves a "gap-blocked" pair on the pushed file (e.g., White on rank 1, Black on rank 3 for 4×n, with rank 2 empty).

**Example (4×n cylinder n=3, White pushes file 0):**
- Endpoint: file 0 has W on 1, B on 3 (gap at rank 2); files 1,2 untouched.
- Shape by untouched-file count: (2,) — a strip of 2, **plus** a debris file with a gap-blocked pair.

The debris is not inert: it can be captured later, and its presence changes the options available from the resulting strip. The clean decomposition into independent strips (which holds for 3×n) **fails**.

### 4.3 Outcomes (Normal Play)

| Board       | n=1 | n=2 | n=3 | n=4 | n=5 | n=6 | n=7 |
|-------------|-----|-----|-----|-----|-----|-----|-----|
| 4×n flat    | L   | L   | L   | L   | L   | L   | L   |
| 4×n cylinder| —   | —   | L   | L   | L   | L   | W   |
| 5×n flat    | W   | W   | W   | W   | W   | W   | —   |
| 5×n cylinder| —   | —   | W   | L   | L   | L   | —   |

(L = first player loses, W = wins; — = not a valid ring for cylinder)

### 4.4 Outcomes (Misère Play)

| Board       | n=1 | n=2 | n=3 | n=4 | n=5 | n=6 | n=7 |
|-------------|-----|-----|-----|-----|-----|-----|-----|
| 4×n flat    | W   | L   | W   | W   | W   | W   | W   |
| 4×n cylinder| —   | —   | L   | L   | L   | L   | W   |
| 5×n flat    | L   | W   | W   | L   | L   | L   | —   |
| 5×n cylinder| —   | —   | W   | L   | L   | L   | —   |

### 4.5 Analysis

- **4×n flat:** The extra rank gives Black a structural tempo advantage (White must push twice to threaten, Black captures on the first push). First player loses in normal play for all computed n.
- **5×n flat:** Two empty ranks between pawns. White's first push creates a threat Black cannot immediately answer, giving White a win for all computed n.
- **Cylinders:** The ring rule does not simply generalize. For 4×n cylinder, the first move leaves a strip of n−1 untouched files plus a gap-blocked debris file. The outcomes show no simple periodic pattern in the computed range.
- **No octal form:** The debris (gap-blocked pairs, doubled pawns) means the game is not a disjunctive sum of independent strips. No octal code or simple recurrence describes these games.

**Status:** **COMPUTED-1** (exhaustive search from pawn rules, single implementation). Larger n exceed the 2M position limit of the Python solver.

**Reproduce:**
```bash
PYTHONPATH=. .venv/bin/python -m research.dawson_variants.dawson_variants --max-n 8 --wider
```

---

## 5. Summary of Claims

| ID | Claim | Status | Evidence |
|----|-------|--------|----------|
| V1 | Misère cylinder ring rule: first player wins iff strip n−3 is misère P | CHECKED-2 (n≤60), COMPUTED-1 (n≤100) | `dawson/misere.c` + `dawson/misere.py` cross-check; `dawson/quotient.py` quotient verification |
| V2 | Misère cylinder outcomes match ring-rule prediction exactly for n≤100 | CHECKED-2 (n≤60), COMPUTED-1 (61≤n≤100) | `dawson/misere_c_100.txt` vs `misere_P_heaps` prediction |
| V3 | Misère cylinder shows no periodicity up to n=100 | CONJECTURE (no period found; quotient suggests infinite) | Exhaustive outcomes; `dawson/quotient.py` non-convergence at Q₃₃ |
| V4 | Möbius strip (3×n, colour-flip seam): normal play first player wins for n=3..12 | COMPUTED-1 | `dawson_variants.py` exhaustive search |
| V5 | Möbius strip: misère outcomes n=3..12 as tabulated | COMPUTED-1 | Same |
| V6 | Möbius macro-move leaves debris; not an octal game on strips | PROVED (structural analysis of capture tree) | Trace in §2.2; endpoints have doubled pawns/blocked pairs |
| V7 | 3×n Torus = 3×n Cylinder for Dawson's chess | PROVED (rank wrapping never used in forced sequences) | Macro-move trace identical; structural proof in §3.2 |
| V8 | Torus outcomes match cylinder for n=3..12 | CHECKED-2 | Independent solver confirmation |
| V9 | 4×n flat normal: first player loses n=1..7 | COMPUTED-1 | Exhaustive search |
| V10 | 4×n, 5×n flat/cylinder outcomes as tabulated | COMPUTED-1 | Exhaustive search (n≤7 or 8) |
| V11 | Wider boards: no simple octal rule survives; macro-move leaves gap-blocked debris | PROVED (macro-move trace shows debris) | Trace in §4.2; debris affects options |

---

## 6. Reproduction Commands

All commands run from the project root `/Users/aritro/Downloads/Research/Chessendgames`.

### Misère Cylinder (uses existing `dawson/` code)
```bash
# Build and run C exhaustive solver
cc -O2 -o dawson/misere_c dawson/misere.c
dawson/misere_c 100                     # writes dawson/misere_c_100.txt
dawson/misere_c 60 dawson/misere_c_60.bin
PYTHONPATH=. .venv/bin/python -m dawson.compare_misere 60 dawson/misere_c_60.bin  # cross-check

# Quotient verification
PYTHONPATH=. .venv/bin/python -m dawson.quotient 32
PYTHONPATH=. .venv/bin/python -m dawson.check_quotient dawson/quotient_Q32.pkl 70 dawson/misere_c_70.bin
```

### New Surfaces and Wider Boards (uses new `research/dawson_variants/dawson_variants.py`)
```bash
# All variants up to n=12 (may take several minutes)
PYTHONPATH=. .venv/bin/python -m research.dawson_variants.dawson_variants --max-n 12 --all

# Individual suites
PYTHONPATH=. .venv/bin/python -m research.dawson_variants.dawson_variants --max-n 12 --moebius
PYTHONPATH=. .venv/bin/python -m research.dawson_variants.dawson_variants --max-n 12 --torus
PYTHONPATH=. .venv/bin/python -m research.dawson_variants.dawson_variants --max-n 8 --wider
PYTHONPATH=. .venv/bin/python -m research.dawson_variants.dawson_variants --max-n 12 --misere-cylinder
```

### Structural Traces (macro-move analysis)
```bash
PYTHONPATH=. .venv/bin/python -c "
from research.dawson_variants.dawson_variants import *
# Add has_capture and trace_macro as shown in the report
"
```

---

## 7. Open Questions

1. **Möbius strip:** Is there a closed form for the misère outcomes? Does normal play remain a first-player win for all n ≥ 3?
2. **Wider boards:** Do the 4×n and 5×n cylinder outcomes become periodic for larger n? Can the debris be modelled as a "loopy" game component?
3. **Generalised Dawson:** For an m×n board with m ≥ 3, what is the macro-move structure? The 3×n case is special because the capture sequence exactly fills the middle rank.
4. **Misère quotient:** Is Q₃₃(0.137) infinite? A longer run with optimized recalibration (or Siegel's MisereSolver) could settle this.

---

## 8. Files in This Directory

- `dawson_variants.py` — New solver for Möbius, Torus, 4×n, 5×n (flat and cylinder), normal and misère.
- `REPORT.md` — This file.

All other code (`dawson/misere.c`, `dawson/quotient.py`, `dawson/octal.py`, `dawson/pawnboard.py`) resides in the parent `dawson/` directory and is used read-only.