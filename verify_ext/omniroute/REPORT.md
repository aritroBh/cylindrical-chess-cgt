# T1b Independent Verification Report

## 5-line Summary

1. **Claim (a) AGREED**: On 4-file flat 8-rank board, `W a2 c2 / B b7 d7` = *2 under textbook passed test (all three race rules, e.p. on/off), 0 under opponent race rule.
2. **Claim (b) AGREED**: Under e.p.-aware test with e.p. on, same position = {2±1|−2±1} (mean 0, temperature 2) for count and mover race rules.
3. **Claim (c) AGREED**: Exhaustive census of 793,299 positions (flat 8 ranks, widths 1–4, pawns on ranks 2–7, ≥1 pawn/side, ≤6 total, no passed pawn at root) under e.p.-aware count rule with e.p. on found **zero** positions with value *k for k ≥ 2.
4. **Claim (d) AGREED**: `W a2 a3 b2 / B a6 b5 b6` = 1/8 in all 9 settings (3 race rules × 3 e.p./passed-test combinations).
5. **Claim (e) AGREED**: `W a2 b2 b6 / B a6 b7 c5` = {0,*|↓} in all 9 settings.

---

## Verification Table

| Claim | Description | Verdict | Evidence |
|-------|-------------|---------|----------|
| (a) | *2 under textbook (count/mover, e.p. on/off); 0 under opponent | AGREE | 6/6 sub-checks match |
| (b) | {2±1|−2±1} under e.p.-aware (count/mover, e.p. on) | AGREE | 2/2 sub-checks match |
| (c) | No *k (k≥2) in scope (e.p.-aware, count, e.p. on) | AGREE | 0 hits in 793,299 positions |
| (d) | 1/8 in all 9 settings | AGREE | 9/9 sub-checks match |
| (e) | {0,*|↓} in all 9 settings | AGREE | 9/9 sub-checks match |

---

## Methodology

### Independent Implementation
- Written from scratch in Python (stdlib only), **no imports or references** to `cylcgt/`, `sumtest/`, `lemmas/`, `crosscheck/`, or `atlas/`.
- Implements canonical-form CGT: Conway order (`≤`), dominated/reversible option removal, canonical constructors for integers, dyadics, nimbers.
- Pawn move generation: single/double steps, captures, en passant (standard chess rules).
- Two passed-pawn tests:
  - **Textbook**: pawn passed iff no enemy pawn on adjacent file ahead.
  - **E.p.-aware**: pawn that can be captured en passant is NOT passed (per 2026-10-16 convention).
- Three race rules for double-passed positions: "count" (fewest moves to promote, tie → next mover), "mover" (side to move wins), "opponent" (other side wins).
- BIG = 256 for passed-pawn terminal values.

### Canonical Form Reduction
```
canonical(G):
  while changes:
    remove dominated options (Left prefers larger, Right prefers smaller)
    bypass reversible options (if G^L^R ≤ G, replace G^L with G^L^L; symmetrically for Right)
```

### Nimber Census Optimization (Claim c)
- Direct outcome-mask computation for G + *k (k = 0..512) avoids full canonical form.
- Recursive `_outcome_masks(w, b, ep, last)` returns (left_mask, right_mask) where bit k = 1 iff player wins G + *k moving first.
- Terminal shortcuts: ZERO → P-position only at k=0; positive number → Left wins all; negative → Right wins all.
- Memoized with LRU cache (1M entries) for speed.
- Total positions checked: 793,299 (widths 1–4 after no-passed-root filter).
- Runtime: ~5 minutes on a single core.

---

## Reproduction Commands

```bash
# Headline claims (a,b,d,e) — fast
cd /Users/aritro/Downloads/Research/Chessendgames
PYTHONPATH=. .venv/bin/python verify_ext/omniroute/solver.py headlines

# Census claim (c) — ~5 minutes
PYTHONPATH=. .venv/bin/python verify_ext/omniroute/solver.py census
```

---

## Notes

- The position count (793,299) exceeds the 231,071 cited in `RESULTS.md` because the scope definition here includes all widths 1–4 without additional filters (e.g., component separation). The key result — **no *k with k ≥ 2** — is robust across both scopes.
- All 26 headline sub-checks and the full census agree with the `cylcgt`/`sumtest` results.
- No discrepancies found.

---

## Code

The complete solver is in `verify_ext/omniroute/solver.py` (self-contained, ~600 lines).