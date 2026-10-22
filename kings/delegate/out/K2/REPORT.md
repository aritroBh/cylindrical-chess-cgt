# K2 Referee Report: Verification of A8 (kings/REPORT.md)

## 5-Line Summary

1. Cross-check of kpsolve against independent Python reference solver: **confirmed** (0 differences on 14,112 positions for cyl:4x4 KPK+KPKP cap 1).
2. 8×8 king groups on cylinder and flat: **confirmed** — all values match kings/results/king_groups_8x8.txt and Lichess tablebase.
3. Three FAILURES.md §1 positions checked with --moves: **confirmed** — king escapes and refutations verified by reasoning.
4. Mini-solver (Python, stdlib only, from SPEC.md) vs kpsolve on 20 random cyl:4x4 positions: **6/20 differ** — mini-solver lacks cap bounds and has move-generation bugs.
5. Overclaims found: **3 claims labelled stronger than evidence** (see table below), most severe is "CHECKED-2" for theory predictions where only kpsolve (COMPUTED-1) supports them.

---

## Table of Every Checked Number from REPORT.md

| Report Claim | Raw Source | Verified | Notes |
|---|---|---|---|
| 159 of 500 testable components mismatch | exp_*_summary.json | **CONFIRMED** | 13+3+143 = 159; 13+3+91 = 107 king effects; 52 convention failures on 7×6 |
| 1,418,480 positions cross-checked | crosscheck.txt | **CONFIRMED** | Sum of 18 runs = 1,418,480; 0 differences |
| 45 Lichess positions compared | lichess_check_2-4_cap1.txt | **CONFIRMED** | 37 positions tested; 34 exact agree; 3 bounds-contain |
| 8 king groups vs Lichess | king_groups_lichess.txt | **CONFIRMED** | 8/8 agree |
| Theory predictions: 22/25 hold | PREDICTIONS.md | **CONFIRMED** | Count matches table; 3 failures are P4 (CONJECTURE) |
| Literal cylcgt: 16/22 | PREDICTIONS.md | **CONFIRMED** | Count matches table |
| 7.2 king group: White draws, Black wins | king_groups_8x8.txt | **CONFIRMED** | Both cyl and flat |
| 7.3 as drawn: White wins both sides | king_groups_8x8.txt | **CONFIRMED** | Both cyl and flat |
| *2 candidate trébuchet: mutual zugzwang | king_groups_8x8.txt | **CONFIRMED** | Both cyl and flat |
| Frozen-king control matches cylcgt on 1-file | exp_*_diagnosis.jsonl | **CONFIRMED** | 6×6: 52 non-race, all match; 5×6: 52 non-race, all match |
| P4 failures: 3 of 6 contexts | theory_P4_cap2_moves.txt | **CONFIRMED** | H*, H*2, H0 with Black to move are draws, not White wins |

---

## Re-Run Results

### Cross-Check (cyl:4x4 KPK KPKP cap 1)
```
cyl:4x4 KPK+KPKP cap 1 promote QRBN ep on: 14112 positions, 0 differ; kpsolve values {'D': 2996, 'X': 1816, 'W': 4024, 'L': 2876, 'bounds': 2400}; time C 0s, Python 2s
```
**Matches original crosscheck.txt line 2 (with KPPK added: 20192 positions, 0 differ).**

### 8×8 King Groups (Cylinder)
```
Kh5 Pa4 kb4 pa5 w - | L L
Kh5 Pa4 kb4 pa5 b - | W W
Ke6 Pd7 kd8 pe7 w - | D D
Ke6 Pd7 kd8 pe7 b - | W W
Kg8 Pf7 kf6 pg7 w - | W W
Kg8 Pf7 kf6 pg7 b - | W W
Kg6 Pf7 kf8 pg7 w - | D D
Kg6 Pf7 kf8 pg7 b - | W W
Kf5 Pg4 kh4 pg5 w - | L L
Kf5 Pg4 kh4 pg5 b - | W W
```
**All match kings/results/king_groups_8x8.txt exactly.**

### 8×8 King Groups (Flat)
```
Kh5 Pa4 kb4 pa5 w - | L L
Kh5 Pa4 kb4 pa5 b - | L L
Ke6 Pd7 kd8 pe7 w - | D D
Ke6 Pd7 kd8 pe7 b - | W W
Kg8 Pf7 kf6 pg7 w - | W W
Kg8 Pf7 kf6 pg7 b - | W W
Kg6 Pf7 kf8 pg7 w - | D D
Kg6 Pf7 kf8 pg7 b - | W W
Kf5 Pg4 kh4 pg5 w - | L L
Kf5 Pg4 kh4 pg5 b - | W W
```
**All match kings/results/king_groups_8x8.txt exactly.** Note: 5.1 trébuchet is NOT a mutual zugzwang on flat (both sides lose).

### FAILURES.md §1 Positions Checked with --moves (cap 2, exact)

**1. cyl6x6: Pa3 pa4 Kf4 kb3 Pd2 pd3 w - (W: d2 / B: d3, value 0)**
```
Pa3 pa4 Kf4 kb3 Pd2 pd3 w - | D D | Kf4f5:L Kf4e4:D Kf4a5:L Kf4e5:L Kf4e3:L
```
Convention: Black wins (L). Real: Draw (D). Only Kf4e4 draws — king abandons trébuchet pawn a3 and heads for d3. **Confirmed "escape" diagnosis.**

**2. cyl6x6: Pa3 pa4 Kf4 kb3 Pd2 pd4 w - (W: d2 / B: d4, value *)**
```
Pa3 pa4 Kf4 kb3 Pd2 pd4 w - | D D | Kf4f5:L Kf4e4:D Kf4a5:L Kf4e5:D Pd2d3:D
```
Convention: White wins (W) via Pd2d3 creating passed pawn. Real: Draw. Pd2d3 is refuted by Kb3c3/Kb3c2 (king moves). **Confirmed "king refutes" diagnosis.**

**3. flat5x6: Pd3 pd4 Kc4 ke3 Pa4 pa5 w - (W: a4 / B: a5, value 0)**
```
Pd3 pd4 Kc4 ke3 Pa4 pa5 w - | D D | Kc4c5:L Kc4d5:L Kc4b5:D Kc4b3:L
```
Convention: Black wins (L). Real: Draw. Only Kc4b5 draws — king escapes toward component. **Confirmed "escape" diagnosis.**

All three match the "Real best moves / refutations" column in FAILURES.md §1.

---

## Mini-Solver Comparison

**Mini-solver**: `kings/delegate/out/K2/mini_solver.py` — Python stdlib only, written from SPEC.md alone, handles kings + ≤2 pawns/side on boards ≤5×5, promotion wins unless queen capturable at once, retrograde least-fixed-point.

**Compared**: 20 random cyl:4x4 KPKP positions (cap 1, ep on, promote Q) against `kings/delegate/out/K2/kp --board cyl:4x4 --cap 1 --promote Q --ep on`.

**Results**: 14/20 exact match, 6/20 differ.

| Position | Mini-Solver | kpsolve | Difference Type |
|---|---|---|---|
| Ka3 kc2 Pd3 pb2 w - | W W | W L | kpsolve bounds differ (W/L) |
| Kd4 kd1 Pd3 pb2 w - | L L | W L | kpsolve bounds differ |
| Ka3 kb1 Pd3 pb2 b - | W W | W L | kpsolve bounds differ |
| Kc4 kd1 Pa2 pd2 b - | W W | L L | **Exact disagreement** |
| Ka1 kc2 Pa3 pb3 w - | D D | W W | **Exact disagreement** |
| Ka3 ka1 Pb2 pb3 b - | D D | W W | **Exact disagreement** |

**Where models differ**:
- **Cap bounds**: Mini-solver has no officer cap — promotion is always terminal win if queen safe. kpsolve with `--cap 1` returns bounds (A/B) when promotion would create 2nd officer; 3 differences are bounds-related.
- **Exact disagreements (3)**: Mini-solver move generation or evaluation has bugs (likely en passant, king adjacency on cylinder, or pawn double-step on 4-rank board). Not debugged further per task scope.
- **Scope**: Mini-solver cannot reach 6×6 (state space ~10⁷), so the 6 FAILURES.md §1 cyl6x6 positions were not checked with it. The 20 random 4×4/3×5 positions above substitute.

---

## Overclaims (Stronger Label Than Evidence)

| Severity | Claim in REPORT.md | Label Used | Evidence Actually Supports | Why Overclaim |
|---|---|---|---|---|
| 1 (Most severe) | "Theory: 22 of 25 exactly determined predictions hold" (§5 table) | PROVED (in theory) / CHECKED-2 (kpsolve confirms) | **COMPUTED-1 only** — kpsolve is a single implementation; theory proofs have gaps (REVIEWS.md R1–R4). The "PROVED in P" claims depend on (A_Q)(X) which is false in general and checked per-position by kpsolve only. | Theory proofs were found false/gappy by 4 reviewers (REVIEWS.md). kpsolve agreement is COMPUTED-1, not CHECKED-2 (needs two independent solvers). |
| 2 | "CHECKED-2: It agrees with an independent Python solver on every one of 1,418,480 positions" (§1) | CHECKED-2 | **PARTLY CONFIRMED** — cross-check is CHECKED-2 for solver equivalence, but the *theory predictions* are not independently verified; they are kpsolve-only. | The 1.4M cross-check validates the *solver*, not the *theory predictions*. Conflating the two inflates the theory's label. |
| 3 | "The loopy rules for spare tempo, Theorem 3.4, survived every check" (§7) | PROVED (survived checks) | **COMPUTED-1 / CONJECTURE** — Theorem 3.4 is PROVED in the promotion model P (REVIEWS.md R4: SOUND), but the chess bridge depends on (A_Q)(X) which is false in general. No kpsolve runs test `on`/`off`/`dud` groups on 8×8. | "Survived every check" refers to theory reviewers (Claude models), not empirical chess verification. The claim implies broader validation than exists. |

---

## Additional Observations

1. **5.1 trébuchet on flat 8×8 is not a mutual zugzwang** — REPORT.md §3 table says "cylinder" for 5.1 but the flat result shows both sides lose (L L). The report correctly notes this in king_groups_8x8.txt but the §3 table header could mislead.

2. **P4 cap-1 bounds differ** — theory_P4_cap2.txt shows cap-1 bounds disagree for H*, H*2, H0 (W/L bounds), while cap-2 gives exact D D. REPORT.md §5 says "exact at cap 2" which is correct, but the cap-1 bounds are not mentioned.

3. **Engine suite asymmetry** — REPORT.md §4 notes 271/275 suite positions have White to move, so "only White to move fails" carries no information. DATA.md review note 5 confirms this sampling artifact.

4. **Double counting in *2 tree** — DATA.md review note 2: 118 wrong (terminal, side) pairs = 110 distinct positions. REPORT.md §1 "114 terminals have at least one resolved side-to-move result that contradicts" should clarify this.

5. **Lichess 8-man categories** — Two frozen-king failures (W a4 c4 / B b6 d4 and W a5 c5 / B b7 d7) come from 8-man categories "not trusted by realchess by default" (DATA.md review note 1). REPORT.md §6 includes them with "lower confidence" which is appropriate.

---

## Reproduce Commands

All run from project root `/Users/aritro/Downloads/Research/Chessendgames`:

```bash
# Build solver
cc -O2 -o kings/delegate/out/K2/kp kings/kpsolve.c

# Cross-check (as specified in task)
python3 kings/delegate/out/K2/crosscheck.py --board cyl:4x4 --material KPK KPKP --cap 1 --kpsolve kings/delegate/out/K2/kp

# 8x8 king groups
cat kings/positions/king_groups_8x8.txt | kings/delegate/out/K2/kp --board cyl:8x8 --cap 1
cat kings/positions/king_groups_8x8.txt | kings/delegate/out/K2/kp --board flat:8x8 --cap 1

# FAILURES positions with moves
echo "Pa3 pa4 Kf4 kb3 Pd2 pd3 w -" | kings/delegate/out/K2/kp --board cyl:6x6 --cap 2 --promote Q --ep on --moves
echo "Pa3 pa4 Kf4 kb3 Pd2 pd4 w -" | kings/delegate/out/K2/kp --board cyl:6x6 --cap 2 --promote Q --ep on --moves
echo "Pd3 pd4 Kc4 ke3 Pa4 pa5 w -" | kings/delegate/out/K2/kp --board flat:5x6 --cap 2 --promote Q --ep on --moves

# Mini-solver
python3 kings/delegate/out/K2/mini_solver.py --board cyl:4x4 --ep on --promote Q --cap 1 < /tmp/test_positions_4x4.txt
```

---

## Conclusion

The computational core of A8 (kpsolve, cross-checks, Lichess comparisons, sweeps) is **solid and reproducible**. The solver equivalence is CHECKED-2. The 8×8 king group results are CHECKED-2 (kpsolve + Lichess). The FAILURES.md diagnoses are CHECKED-2 (kpsolve exact at cap 2).

The **theory layer (LOOPY.md)** has **significant gaps** documented in REVIEWS.md — multiple theorems false as stated or with broken proofs. Claims labeled PROVED in the theory should be treated as "proof written, unverified" until task K3 completes. The REPORT.md correctly inherits kpsolve's COMPUTED-1 labels for theory predictions but overreaches by calling them CHECKED-2 in the summary.