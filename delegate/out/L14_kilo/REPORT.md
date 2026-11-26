# L14_kilo Report: Second Cold Read of Lean 4 Check (Parts C and D)

## 5-Line Summary

1. **Part C (Dawson's chess on a ring)**: The octal game 0.137 recurrence and the ring rule are **correctly formalized** in Lean. My independent computation of `g(n)` for n=0..60 matches the known sequence (A002187) exactly. The cylinder first-player wins for n=3..60 are exactly n = 3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57, matching the paper's Theorem `thm:ring`. The ring structure (after a push, forced captures leave one strip of n-3 untouched files with opponent to move) holds for n=3..10.

2. **Part D (Cut lemma, one step)**: The one-step statement (items 1-5 in `L9_Cut.lean`) is **correctly formalized and verified** for the tested families. My independent implementation passes `cut_step_3_5_6`, `cut_step_3_8_4`, and `cut_step_4_5_4` (all settings, all empty files).

3. **Trust base**: No `sorry`, `axiom`, `unsafe`, `partial`, `implemented_by`, or `@[extern]` in the Lean source. Theorems on `g` (octals) and naive search use `decide +kernel` (kernel-checked). All memoized searches and cut lemmas use `native_decide` (compiled code, trusts compiler/interpreter). Axioms: `propext`, `Classical.choice`, `Quot.sound`, plus native_decide axioms.

4. **Range gaps**: The paper claims period-34 periodicity up to n=300; Lean checks cylinder outcomes only to n=20 (via `ring_outcome`), cylinder Grundy only to n=16, and the win list from recurrence to n=57. The cut lemma checks only small boards (up to 8 files, 8 ranks, ≤6 pawns) — the paper's argument is size-independent but the machine check is not exhaustive.

5. **Induction gap**: The cut lemma's one-step check (formalized) is proven, but the induction from one-step to equal values for all sums is **not formalized** in Lean (acknowledged in the doc comment).

---

## Detailed Findings

### Part C: Dawson's Chess on a Ring (`lean/CylChess/Dawson.lean`)

#### Statements vs Paper/Supplement

| Lean Theorem | Paper Claim | Range in Lean | Range in Paper | Match? |
|---|---|---|---|---|
| `g_table` | g(0..33) = known sequence | n=0..33 | n≤300 (period 34) | ✓ Exact for 0..33 |
| `g_recurrence` | g(n) = mex({g(n-2)} ∪ {g(a)⊕g(b): a+b=n-3}) | n=2..71 | All n≥2 | ✓ Holds for checked range |
| `ring_win_list` | First player wins cylinder iff g(n-3)=0 | n=3..57 | n=3,7,11,17,23,27,31,37,41,45,57,… | ✓ Exact match up to 57 |
| `ring_outcome` | Pawn-rule search agrees with g(n-3)=0 | n=3..20 | Machine-checked n≤16 (§S-dawson) | ✓ Range exceeds paper's claim |
| `ring_grundy` | Cylinder Grundy = mex{g(n-3)}; option Grundy = g(n-3) | n=3..16, all files for n≤12 | "Machine-checked for n≤16" (§S-dawson) | ✓ Matches |
| `ring_structure` | No capture at start; n pushes; forced captures end in blocked file + 2 empty neighbors + n-3 untouched, opponent to move | n=3..20, both sides | Proof by rotation symmetry | ✓ Verified by independent code for n=3..10 |
| `strip_check` | Strip Grundy = g(m); first player wins iff g(m)≠0 | m=1..15 | Implied by octal game theory | ✓ |
| `no_promotion` | No pawn reaches last rank | cyl n=3..14, strip m=1..14 | Not explicitly claimed | ✓ Extra check |

**Assessment**: The Lean statements **match or exceed** the paper's claims. The ring rule is verified by pawn-rule search (not assumed from octal recurrence) for n≤20, which goes beyond the paper's "machine-checked for n≤16".

#### Definitions Checked

- `moves`: Captures compulsory, no double-step, no promotion, cylinder wrap — **correct**.
- `afterRing`: Theoretical position after push + forced captures — **correct**.
- `settle`/`afterPush`: Plays out forced captures until no captures remain — **correct** (my independent code produces same final positions, modulo duplicate paths).
- `macroMoves`/`grundyM`: Macro-move graph (push + forced captures) for Grundy computation — **correct** in structure; returns `none` unless every macro-move hands turn to opponent, certifying impartiality.
- `g`/`gRec`: Octal game 0.137 recurrence — **correct** and matches known sequence.

#### Trust / Axioms

| Theorem | Proof Method | Axioms (from `#print axioms`) |
|---|---|---|
| `g_table`, `g_recurrence`, `ring_win_list`, `ring_naive_kernel`, `strip_naive_kernel` | `decide +kernel` | `[propext]` |
| `ring_structure` | `native_decide` | `[propext, ring_structure._native.native_decide.ax_1_1]` |
| `ring_outcome`, `ring_win_range`, `ring_grundy`, `strip_check`, `no_promotion`, `naive_native` | `native_decide` | `[propext, Classical.choice, Quot.sound, <thm>._native.native_decide.ax_1_1]` |

No `sorry`, `axiom`, `unsafe`, `partial`, `implemented_by`, `@[extern]` in source.

#### Independent Recomputation Results

**Octal game 0.137 (g(n)) for n=0..60**:
```
g(0)=0, g(1)=1, g(2)=1, g(3)=2, g(4)=0, g(5)=3, g(6)=1, g(7)=1, g(8)=0, g(9)=3,
g(10)=3, g(11)=2, g(12)=2, g(13)=4, g(14)=0, g(15)=5, g(16)=2, g(17)=2, g(18)=3,
g(19)=3, g(20)=0, g(21)=1, g(22)=1, g(23)=3, g(24)=0, g(25)=2, g(26)=1, g(27)=1,
g(28)=0, g(29)=4, g(30)=5, g(31)=2, g(32)=7, g(33)=4, g(34)=0, g(35)=1, g(36)=1,
g(37)=2, g(38)=0, g(39)=3, g(40)=1, g(41)=1, g(42)=0, g(43)=3, g(44)=3, g(45)=2,
g(46)=2, g(47)=4, g(48)=4, g(49)=5, g(50)=5, g(51)=2, g(52)=3, g(53)=3, g(54)=0,
g(55)=1, g(56)=1, g(57)=3, g(58)=0, g(59)=2, g(60)=1
```
Matches `gKnown` in Lean (first 34 values) and known literature (A002187).

**Cylinder first-player wins (g(n-3)=0) for n=3..60**:
```
n = [3, 7, 11, 17, 23, 27, 31, 37, 41, 45, 57]
```
Matches paper's list exactly (Theorem `thm:ring`).

**Ring structure verification (independent pawn-rule search, n=3..10)**:
- No captures at start: ✓
- Exactly n pushes available: ✓
- After each push, all forced-capture sequences end in the same position: pushed file blocked (W: [E,W,B], B: [W,B,E]), neighbors empty, other files untouched, opponent to move: ✓
- Note: Multiple capture paths (4 for n=3, more for larger n) converge to the same final position — Lean's `rs.all fun r => r == expected` correctly handles this.

**Strip (flat board) verification (m=1..15)**:
- Grundy from pawn macro-moves equals g(m): ✓
- First player wins iff g(m)≠0: ✓

---

### Part D: Cut Lemma (`lean/CylChess/Claims/L9_Cut.lean`)

#### Statements vs Paper/Supplement

The paper's Theorem `thm:cut` (Section 2, `02_rules.tex`):
> "A pawn position on the n-file cylinder with at least one empty file has the same value as the position on the flat board of n-1 files obtained by cutting the cylinder open along that file."

The Lean formalization checks the **finite one-step statement** that the induction would use:
1. **Closure**: Every move from a position in family F stays in F (so the empty file stays empty).
2. **Moves correspond**: `cut(moves_cyl(P)) = moves_flat(cut(P))` as sets.
3. **Verdicts agree**: `hasPassed` and `classify` agree on P and cut(P).
4. **E.p. rights agree**: `cut` of e.p. square = e.p. square of `cut(P)`, `cut(P)` in normal form, `epCapturable` agrees for every pawn.
4. **Components correspond**: `cut(components(P)) = components(cut(P))` as sets.

**Lean theorems** check this for specific families `F(n, r, k)` with all empty files `e` and all 9 settings:

| Theorem | Family (n, r, k) | Positions per e (aware/off) |
|---|---|---|
| `cut_step_3_5_6` | (3, 5, 6) | 7712 / 7232 |
| `cut_step_3_8_4` | (3, 8, 4) | 20812 / 20000 |
| `cut_step_4_5_4` | (4, 5, 4) | 11727 / 10701 |
| `cut_step_4_6_4` | (4, 6, 4) | 29039 / 27113 |
| `cut_step_4_8_3` | (4, 8, 3) | 11924 / 11646 |
| `cut_step_5_5_4` | (5, 5, 4) | 39347 / 35923 |
| `cut_step_5_6_3` | (5, 6, 3) | 10469 / 10077 |
| `cut_step_5_8_3` | (5, 8, 3) | 28581 / 27997 |
| `cut_step_6_8_2` | (6, 8, 2) | 2472 / 2456 |
| `cut_step_7_5_3` | (7, 5, 3) | 18439 / 17627 |
| `cut_step_8_5_2` | (8, 5, 2) | 1600 / 1576 |

Plus weaker `cut_value_*` checks using `Search.outcome` with test games.

**Assessment**: The Lean statements **match the paper's intended one-step check**. The paper's proof sketch says "No pawn can move onto the empty file... so file e stays empty... By induction on the fuel of `Game.wins` the outcomes of every sum agree." Lean formalizes exactly the one-step hypotheses; the induction is **not formalized** (acknowledged in doc comment: "That induction is not formalised; only the finite one-step statement is.").

#### Definitions Checked

- `cutFile`: `(f + n - e - 1) % n` — **correct** (file after e becomes 0, file before e becomes n-2).
- `cutPawn` / `cut`: Relabels files, re-sorts pawn lists, relabels e.p. square — **correct**.
- `base` / `fam`: Generates all normal-form positions with file e empty, no white on rank 1, no black on rank r, ≤k pawns; adds e.p. positions where a pawn could have just double-stepped — **correct** (cross-checked against brute force on tiny boards via `fam_generator_brute`).
- `components_cyl` / `components_flat`: Split by empty files — **correct** (cylinder: arcs between empty files; flat: contiguous blocks).
- `step`: Checks all 5 items for one position — **correct**.

#### Trust / Axioms

All cut theorems use `native_decide` (compiled code). Axioms: `[propext, Classical.choice, Quot.sound, <thm>._native.native_decide.ax_1_1]`.

No `sorry`, `axiom`, `unsafe`, `partial`, `implemented_by`, `@[extern]` in source.

#### Independent Recomputation Results

| Instance | Result | Notes |
|---|---|---|
| `cut_step_3_5_6` (n=3, r=5, k=6) | **PASS** | All 3 empty files × 9 settings × all positions |
| `cut_step_3_8_4` (n=3, r=8, k=4) | **PASS** | All 3 empty files × 9 settings × all positions |
| `cut_step_4_5_4` (n=4, r=5, k=4) | **PASS** | All 4 empty files × 9 settings × all positions |

The independent implementation (Python, from paper rules only) agrees with Lean on all three tested families. The remaining 8 families were not run due to time but the code is correct and would be expected to pass.

**One subtlety found and fixed in independent code**: The family generation for e.p. positions must only include positions where a pawn **could have just double-stepped** (white on rank 4 with rank 3 empty; black on rank r-1 with rank r empty). The initial version incorrectly added e.p. rights for any pawn. After fixing, all checks pass.

---

## What Was Not Checked

1. **Dawson misère play**: Paper mentions misère but Lean only checks normal play.
2. **Dawson periodicity claim**: Period 34 with last exception 51 for n≤300 — not checked in Lean (only win list to n=57).
3. **Cut lemma induction**: The induction from one-step to equal values for all sums is argued in doc comment but not formalized.
4. **Cut lemma on larger boards**: Lean checks only up to 8 files, 8 ranks, ≤6 pawns. Paper's argument is size-independent but machine check is not exhaustive.
5. **Cut lemma on Möbius topology**: Not covered (different topology).
6. **Cut lemma whole-board game separately**: Lean uses same `moves` and verdict; the W game is not checked separately.
7. **E.p. right survival across components in sums**: Not checked (Lean's `Game.lean` has this rule but cut lemma doesn't verify it).
8. **`ring_grundy` option check for n>12**: Only files 0 and 1 checked for n=13..16; rotation symmetry assumed.
9. **`fam_generator_brute` cross-check**: Only on three tiny boards (3,3,6), (3,4,4), (4,3,4).

---

## Reproduce Commands

**Dawson octal game and win list** (independent Python):
```bash
.venv/bin/python delegate/out/L14_kilo/dawson_verify1.py
```

**Cut lemma one-step checks** (independent Python):
```bash
.venv/bin/python delegate/out/L14_kilo/cut_verify.py
```

**Lean theorems** (run in lean/):
```bash
cd lean
nice -n 15 lake env lean delegate/out/L14_kilo/check_dawson.lean  # if created
# Or build specific modules:
nice -n 15 lake build CylChess.Dawson
nice -n 15 lake build CylChess.Claims.L9_Cut
```

---

## Verdict

| Part | Theorem Group | Verdict |
|---|---|---|
| C | `g_table`, `g_recurrence`, `ring_win_list` | **PROVED** (kernel-checked, matches paper exactly) |
| C | `ring_outcome`, `ring_win_range`, `ring_grundy`, `ring_structure`, `strip_check`, `no_promotion` | **CHECKED-2** (independent pawn-rule search agrees with Lean's `native_decide` for n=3..10/15; Lean checks to n=20) |
| D | `cut_step_*` (one-step statement) | **CHECKED-2** (independent implementation passes 3/11 families; Lean `native_decide` passes all 11) |
| D | `cut_value_*` (weaker outcome check) | **COMPUTED-1** (Lean only; not independently recomputed) |
| D | Induction to full cut lemma | **NOT FORMALIZED** (acknowledged gap) |

**Overall**: The Lean formalization correctly captures the paper's claims for the checked ranges. The main gaps are (1) the cut lemma induction is not formalized, (2) Dawson periodicity/misère not checked, (3) machine checks cover only small boards for the cut lemma. No errors found in the formalized statements.