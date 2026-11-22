# Referee Report on the Proof of Square Rule S

## Verdict (5 lines)

**SOUND WITH MINOR FIX** — The proof is correct for the frozen-king pawn game on boards with H ≥ 4 (the tested H=6,8 satisfy this). The claim "holds for any H ≥ 3" is technically incorrect because the double-step formula underestimates distance when H=3 (start-rank double step would go off-board), but soundness is preserved (S simply never certifies). All lemmas are valid, the ply accounting is exact, and the scope (frozen game only, not real chess) is clearly stated. Exhaustive check (COMPUTED-1) corroborates: 0/158,544 unsound.

## 1. Completeness of the argument

**Lemmas 1–3 are complete and correctly argued.**

- **Lemma 1 (Passer safety):** Rank monotonicity is the key. X's runner advances toward promotion; Y's pawns move oppositely, so their rank in X's direction never increases. A pawn not beyond the runner initially cannot become beyond it later. Normal capture requires an enemy pawn on (f±1, r±1) ahead of the runner — impossible by passedness. En passant requires an enemy pawn on the landing rank (beyond the start rank), which would have been beyond the runner before the push, contradicting e.p.-aware passedness. Own pawns cannot block (runner is front) or capture onto the runner's square (no enemy pawn there). Cylinder wrap-around does not affect rank monotonicity. **PROVED.**

- **Lemma 2 (Y's promotion lower bound):** Each pawn's rank progress per move is at most 2 on its first move (double step from start rank, if on-board) and at most 1 on every subsequent move, including captures (captures advance exactly one rank). `sdist_Y(r)` assumes this maximal progress every move. Obstructions, blockages, or detours can only increase the move count. The minimum over *all* Y pawns (blocked or not) gives a valid lower bound `d` for Y's earliest possible promotion. **PROVED.**

- **Lemma 3 (Ply accounting):** X pushes every X-turn; the runner's distance `n` counts X-moves. X's n-th push occurs on ply `2n-1` (X first) or `2n` (Y first). Y's earliest promotion requires `d` Y-moves, occurring on ply `2d` (X first) or `2d-1` (Y first). The inequalities `n ≤ d` (X first) and `n < d` (Y first) guarantee X's promotion ply is strictly earlier. **PROVED.**

No missing steps. The proof does not depend on an empty file, and the cylinder is handled by cyclic file adjacency in the passed test — rank monotonicity is unchanged.

## 2. Dependence on cylinder / board height

- **Cylinder:** The proof explicitly notes cyclic file adjacency is used in the passed test; rank monotonicity is file-topology-agnostic. **No dependence.**
- **Board height:** The formula `sdist = H - r - (1 if r=2 else 0)` (White) assumes the double step from rank 2 lands on-rank 4, which requires H ≥ 4. For H=3 the double step is illegal (target off-board), so the true unobstructed distance is `H - r`, not `H - r - 1`. The claim "holds for any H ≥ 3" is an overstatement; the proof as written requires H ≥ 4. Since all tested boards have H=6 or 8, this does not affect any reported result. **Minor fix:** restrict the scope claim to H ≥ 4, or adjust `sdist` to `max(1, H - r - (1 if r=2 and H≥4 else 0))`.

## 3. What is NOT claimed (real chess)

Both `PROOF_S.md` and `v2_mechanisms/REPORT.md` are explicit: S is **only** proved for the frozen-king pawn game (kings immobile, king move loses instantly, promotion wins instantly). Real chess with active kings is excluded — a king can step in front of or capture a certified runner. The 128 remaining mismatches after CC are identified as king effects. The REPORT is clear about this limitation.

## 4. Counterexample / missing step

No counterexample exists in the frozen game. The exhaustive search (158,544 cases across 2–3 files, 6–8 ranks, both sides to move, all legal e.p. rights) found **S_UNSOUND = 0** and **RP_UNSOUND = 0** (COMPUTED-1). The proof sketch is complete; no missing step.

## Labels for key claims

| Claim | Label |
|-------|-------|
| Lemma 1 (passer safety) | **PROVED** |
| Lemma 2 (Y's promotion lower bound) | **PROVED** |
| Lemma 3 (ply accounting) | **PROVED** |
| Theorem (S soundness in frozen game) | **PROVED** |
| Exhaustive soundness (0/158,544) | **COMPUTED-1** |
| Python FG = kpsolve --frozen (1,792 roots, 2,932 moves) | **CHECKED-2** |
| Python CG = stored cylcgt outcome (1,792 rows) | **CHECKED-2** |
| Scope claim "H ≥ 3" | **CONJECTURE** (false for H=3; true for H≥4) |
| Real-chess mechanism of 8 king-overlay rows | **NOT DETERMINED** (per v2_mechanisms/REPORT.md) |

## Reproduce

```sh
cd /Users/aritro/Downloads/Research/Chessendgames/research/v2_mechanisms
python3 -I cc.py   # exhaustive soundness (S_UNSOUND = 0) and re-score
```

(End of report)